---
layout: post
title: "Fly.io Certificate Renewal"
description: "Ensure your SSL certificate doesn't expire to avoid downtime"
date: 2023-06-19 0:00:00 +0000
image: assets/pics/fly-certificate.png
---

One of [my side projects](https://fedidevs.com/) experienced downtime due to an expired SSL certificate. Here's what happened and how I resolved it.

![chart showing 1h and 41 minutes of downtime](/assets/pics/fly-downtime.png)

I host my project on [fly.io](https://fly.io/) and followed the [official docs](https://fly.io/docs/app-guides/custom-domains-with-fly/#accepting-traffic-immediately-for-the-custom-domain) to set up the certificates 3 months ago. The other day I started receiving `SSL Handshake Failed` errors.

To fix the issue, I ran the following commands:

```shell
flyctl certs delete fedidevs.com
flyctl certs create fedidevs.com
```

Surprisingly, I had to delete the existing certificate before creating a new one, or else I encountered the following error:

```
Error: Hostname already exists on app
```

I have found a [forum thread](https://community.fly.io/t/ssl-certificate-did-not-renew-automatically/4924) with others experiencing this same issue. According to a fly.io [employee post](https://community.fly.io/t/ssl-certificate-did-not-renew-automatically/4924/6) the certificates should auto-renew 30 days before expiration, but they did have [a bug](https://community.fly.io/t/ssl-certificate-did-not-renew-automatically/4924/13) that prevented certificates from renewing. Did this bug regress?

Despite having the `A`/`AAAA` records correctly set, my site didn't auto-renew. I've now added the `CNAME` record to my DNS settings hoping that this will fix the problem, but I'll have to wait until September to know for sure. 🤞

![image showing the certificates are valid until September 14, 2023](/assets/pics/fly-certificate.png)
