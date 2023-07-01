---
layout: post
title: "RDS Blue/Green Deployments"
description: "Upgrading your database with Blue/Green deployments"
date: 2023-07-01 1:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

I've recently had to upgrade a fairly large MySQL database from 5.7 to 8.0 and I was looking for ways to minimize the downtime of the upgrade. Since the database was hosted on RDS I decided to look into the [Blue/Green Deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments-overview.html) feature. This post is a summary of my experience with the feature.

# How does it work?

When you [create a new Blue/Green deployment](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments-creating.html) RDS creates the new instances based on your existing topology. If you have a primary and a replica it will create a new green deployment with a primary and a replica. 

All the data from your blue instances will be replicated into the green instances the same way as data is replicated between primaries and replicas. 

Once the green instances are synced up, you can perform operations on the green instances, e.g. upgrade the database version, increase the instance size, run long-running/blocking schema changes, or change settings in the parameter group that requires a reboot. Since your application traffic is still going to the blue instances, you can perform these operations without any downtime.

When the green instance is ready you can switch application traffic from blue to green. When you do this RDS will run the [Switchover actions](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments-switching.html#blue-green-deployments-switching-actions). This will stop new write operations, drop connections, wait for the green instances to catch up, and then perform the renaming of the instances and endpoints. After the renaming is complete, writes to the green instance are enabled. The blue instance is put into read-only mode and the new data coming into the green instance is NOT replicated back into the blue instance.

From your application's perspective, nothing has changed. The database endpoint URL is still the same as it was before the switch.

# How does it perform?

Prior to running the upgrade on the production environment I tested the Blue/Green deployment and compared it with the normal upgrade process using the RDS modify command. I used [Locust](https://locust.io) to generate a constant load of requests to the database.

The normal upgrade method resulted in 4 minutes and 30 seconds of downtime for both read and write operations:

![image tooltip here](/assets/pics/rds-blue-green-bad.png)

The Blue/Green deployment resulted in ~1 minute of downtime for writes and ~30 seconds of downtime for reads:

![image tooltip here](/assets/pics/rds-blue-green-good.png)

To put these times into perspective, 4.38 minutes of full downtime is 99.99% or four nines of [high availability](https://en.wikipedia.org/wiki/High_availability) per month, while 26.30 seconds of full downtime is 99.999% or five nines!

# Gotchas

There are some gotchas when doing Blue/Green deployments.

Since Blue/Green deployments create new instances the new instances will have new binlogs. This means that if you are using the binlog to replicate to another database or your data lake you'll have to reconfigure the replication once you switch from blue to green. This is not a problem that you would face with an in-place upgrade, since the binlog file names would stay the same.

Some configuration from the blue instances does not transfer over to the green instances. For example, green instances are all created with the same parameter group. If you have a different parameter group for your read replica you'll have to make sure to update the green replica after it's created. This also goes for any other setting, e.g. the binlog retention period setting that you set with `CALL mysql.rds_set_configuration('binlog retention hours', 168);`, this setting will also not transfer over to the green instances so you'll need to set it again once the green instances are created.

# Fin

Blue/Green deployments can be a great tool to minimize downtime when upgrading your database. Especially useful if you find yourself needing to upgrade MySQL to 8.0 later this year when MySQL 5.7 reaches end of life [October 31, 2023](https://endoflife.date/mysql). RDS end of standard support date is [December 2023](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Concepts.VersionMgmt.html).

