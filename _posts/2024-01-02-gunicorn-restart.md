---
layout: post
title: "No downtime restarts with Gunicorn"
description: "Restart your Gunicorn process without downtime."
date: 2024-01-02 0:00:00 +0000
# image: /assets/pics/pytest-plugin-og.png
---

## The HUP Signal

Gunicorn uses the [HUP signal](https://docs.gunicorn.org/en/stable/signals.html#reload-the-configuration) that will reload your application without downtime, so, in most cases, you can use the following line for 0-downtime restarts:

```bash
kill -HUP $(cat gunicorn.pid)
```

Gunicorn doesn't create the `gunicorn.pid` file by default, so you'll have to add the `pidfile` parameter to your `gunicorn.conf.py` config file:

```python
pidfile = "gunicorn.pid"
```

Your Gunicorn workers will restart without dropping any requests:

```log
[2024-01-02 17:29:43 +0000] [22791] [INFO] Handling signal: hup
[2024-01-02 17:29:43 +0000] [22791] [INFO] Hang up: Master
[2024-01-02 17:29:43 +0000] [22800] [INFO] Booting worker with pid: 22800
[2024-01-02 17:29:43 +0000] [22801] [INFO] Booting worker with pid: 22801
[2024-01-02 17:29:43 +0000] [22802] [INFO] Booting worker with pid: 22802
[2024-01-02 17:29:43 +0000] [22804] [INFO] Booting worker with pid: 22804
[2024-01-02 17:29:43 +0000] [22806] [INFO] Booting worker with pid: 22806
[2024-01-02 17:29:43 +0000] [22792] [INFO] Worker exiting (pid: 22792)
[2024-01-02 17:29:43 +0000] [22795] [INFO] Worker exiting (pid: 22795)
[2024-01-02 17:29:43 +0000] [22794] [INFO] Worker exiting (pid: 22794)
[2024-01-02 17:29:43 +0000] [22793] [INFO] Worker exiting (pid: 22793)
[2024-01-02 17:29:43 +0000] [22796] [INFO] Worker exiting (pid: 22796)
```

## Upgrading Gunicorn itself

The above method upgrades your application and its dependencies (unless you are [preload your app](https://docs.gunicorn.org/en/stable/settings.html#preload-app)!), but never closes the master Gunicorn process, so it will never get upgraded. This isn't a big deal since Gunicorn updates are rare (there were almost two years between 20.0.4 and 21.0.0 releases). But if you need to upgrade Gunicorn itself and still don't want to risk downtime, you have to do the following:

```bash
kill -USR2 $(cat gunicorn.pid) # Start the new master process alongside the old one
kill -WINCH $(cat gunicorn.pid) # Tell the old master process to stop serving requests
kill -TERM $(cat gunicorn.pid) # Tell the old master process to terminate
# Note that the new process has its pid inside the `unicorn.pid.2 file` now
```
More info about this is available in the [official Gunicorn docs](https://docs.gunicorn.org/en/stable/signals.html#upgrading-to-a-new-binary-on-the-fly).

## Uvicorn

Uvicorn only runs a single process and isn't recommended for production alone! The [official Uvicorn docs](https://www.uvicorn.org/deployment/#gunicorn) recommend using a process manager like Gunicorn to overcome this limitation. This is great, because we already know how to restart Gunicorn without downtime!

To get Gunicorn to run your Uvicorn processes, you only need to define the `worker_class` variable in the config file, and you should be all set:

```python
worker_class = "uvicorn.workers.UvicornWorker"
pidfile = "gunicorn.pid"
```

## Why?

Most PaaS providers (like Heroku or Fly) have their way of restarting your application without downtime, so you don't have to worry about it. But if you're trying to keep things simple and run your app directly on a VPS or a VM, you'll need to figure this out yourself. As we see above, it's pretty easy, so there's no need to reach for something heavy like Kubernetes to get this done!
