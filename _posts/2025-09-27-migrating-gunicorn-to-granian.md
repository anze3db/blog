---
layout: post
title: Migrating Gunicorn to Granian
date: 2025-09-27 23:02 +0100
---

I migrated one of my Django apps from Gunicorn to Granian yesterday. Here is how the migration went and some of my thoughts on Granian and Gunicorn.

# Migration

This is the second time I attempted to try out Granian. The first time I got blocked because Granian didn't support [unix sockets](https://github.com/emmett-framework/granian/issues/97). I run several Django apps on the same host behind Nginx, and I'm using Unix sockets for communication between Nginx and Gunicorn. I could have switched to using ports, but I didn't want to mess with Nginx for this experiment.

Since then, Granian has added support for Unix sockets, so this is no longer a blocker. In fact, all the Gunicorn settings that I was using had their equivalent in Granian, including the ability to set the process name (again, extremely useful when running multiple Django Apps on a single host).

This was my existing `gunicorn.conf.py` file:

```python
proc_name = "fedidevs"
bind = "unix:fedidevs.sock"
workers = 4
threads = 4
```

And this is how I now start Granian:

```sh
granian \
    --interface wsgi fedidevs.wsgi:application \
    --process-name fedidevs \
    --uds fedidevs.sock \
    --workers 4 \
    --blocking-threads 4
```

# Performance

Granian is written in Rust, so it should be faster than Gunicorn, which is in pure Python. [Granian's benchmark](https://github.com/emmett-framework/granian/blob/master/benchmarks/vs.md#wsgi) says that Granian should be about `10ms` faster than Gunicorn Gthread for WSGI.

![Chart of response times before and after the upgrade. No visible difference.](/assets/pics/granian-gunicorn.png)

However, as we can see from the response times on my app above, there appears to be no change in response times. You can't even tell where on the chart I switched from Gunicorn to Granian.

This is probably because Gunicorn (and now Granian) was already running behind Nginx, so all the request scheduling was already done by the efficient Nginx C code before it reached Gunicorn's Python code.

# Docs

Grenian doesn't have a dedicated docs page like Gunicorn, but the Readme is comprehensive. I enjoyed reading the [Workers and threads](https://github.com/emmett-framework/granian?tab=readme-ov-file#workers-and-threads) section, and I feel it provides better guidance than Gunicorn's [How Many Workers?](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) and [How Many Threads?](https://docs.gunicorn.org/en/latest/design.html#how-many-threads) sections, which feel a bit dated.

# Request timeouts

I was hoping that Granian's `--blocking-threads-idle-timeout` would kill requests that have been running for too long. Unfortunately, it seems to work like Gunicorn's `--timeout` parameter and only kills workers that have stopped responding.

Not useful if you end up with a bunch of idle requests because a third-party service stopped responding. The only solution for this is to add timeouts to all I/O operations of your application rigorously.

# Fin

If you enjoy trying out new things, do give Granian a go; it's a wonderful project. Your existing projects can continue using Gunicorn. You probably won't see a big difference after the migration.
