---
title: "No Downtime Deployments with Gunicorn"
description: "This article shows how to achieve zero-downtime deploys of your Django, Flaks, or FastAPI app using only Gunicorn. It explains how to reload the Gunicorn process with the -HUP signal using systemd or the kill command directly making sure no requests are dropped during the upgrade."
date: 2024-01-02 0:00:00 +0000
image: assets/cards/2024-01-02-gunicorn-restart.png
tags: python django
---

Suppose you're hosting your Django, Flask, or FastAPI application on your server instead of using a platform like Heroku or Fly. You want to continue serving requests while your Gunicorn process restarts to load your application code updates, and you want to avoid setting up a complicated code deployment process. Gunicorn supports this workflow out of the box with the [HUP signal](https://docs.gunicorn.org/en/stable/signals.html#reload-the-configuration).

## The HUP Signal

When the Gunicorn process receives the HUP signal, it will start new worker processes, stop routing requests to the old workers and shut them down once their request queues clear. This way, no request is lost during the upgrade process.

You can use the [`kill` command](https://man7.org/linux/man-pages/man1/kill.1.html) to send the hup signal to your Gunicorn process:

```bash
kill -HUP $(cat gunicorn.pid)
```

Gunicorn doesn't create the `gunicorn.pid` file by default, so you'll have to add the `pidfile` parameter to your `gunicorn.conf.py` config file:

```python
pidfile = "gunicorn.pid"
```

Here is a sample output of the Gunicorn process after sending the HUP signal:

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


## SystemD

If you are using `systemd` to manage your Gunicorn process, you can use the `systemctl reload` command to send the HUP signal to your Gunicorn process:

```bash
systemctl reload gunicorn.service
```

For this to work, you'll need to ensure that the `ExecReload` parameter in your `unicorn.service` file is set to `ExecReload=/bin/kill -s HUP $MAINPID.` See [the example service file in the Gunicorn docs](https://docs.gunicorn.org/en/stable/deploy.html#systemd).

This way, `systemd` will send the HUP signal to the correct process, so you don't have to worry about the process id (PID). The only downside is that `systemd` doesn't recommend using async commands like `kill -HUP` in the `ExecReload` parameter, because it might trigger reloads of depending services before the main service has finished reloading. It's not a huge issue, though, since having other services depend on Gunicorn is rare.

Example output output of `systemctl reload gunicorn.service`. Note that the systemd Reloaded event is logged before the Gunicorn process has finished reloading:

```
Jan 03 13:01:00 raspberrypi systemd[1]: Reloading Gunicorn.
Jan 03 13:01:00 raspberrypi gunicorn[201219]: [2024-01-03 13:01:00 +0000] [201219] [INFO] Handling signal: hup
Jan 03 13:01:00 raspberrypi gunicorn[201219]: [2024-01-03 13:01:00 +0000] [201219] [INFO] Hang up: Master
Jan 03 13:01:00 raspberrypi systemd[1]: Reloaded Gunicorn.
Jan 03 13:01:00 raspberrypi gunicorn[201241]: [2024-01-03 13:01:00 +0000] [201241] [INFO] Booting worker with pid: 201241
Jan 03 13:01:01 raspberrypi gunicorn[201242]: [2024-01-03 13:01:00 +0000] [201242] [INFO] Booting worker with pid: 201242
Jan 03 13:01:01 raspberrypi gunicorn[201244]: [2024-01-03 13:01:01 +0000] [201244] [INFO] Booting worker with pid: 201244
Jan 03 13:01:01 raspberrypi gunicorn[201243]: [2024-01-03 13:01:01 +0000] [201243] [INFO] Booting worker with pid: 201243
Jan 03 13:01:01 raspberrypi gunicorn[201245]: [2024-01-03 13:01:01 +0000] [201245] [INFO] Booting worker with pid: 201245
Jan 03 13:01:01 raspberrypi gunicorn[201223]: [2024-01-03 13:01:01 +0000] [201223] [INFO] Worker exiting (pid: 201223)
Jan 03 13:01:01 raspberrypi gunicorn[201224]: [2024-01-03 13:01:01 +0000] [201224] [INFO] Worker exiting (pid: 201224)
Jan 03 13:01:01 raspberrypi gunicorn[201220]: [2024-01-03 13:01:01 +0000] [201220] [INFO] Worker exiting (pid: 201220)
Jan 03 13:01:01 raspberrypi gunicorn[201221]: [2024-01-03 13:01:01 +0000] [201221] [INFO] Worker exiting (pid: 201221)
Jan 03 13:01:01 raspberrypi gunicorn[201222]: [2024-01-03 13:01:01 +0000] [201222] [INFO] Worker exiting (pid: 201222)
```


## Upgrading Gunicorn itself

The `kill -HUP` method upgrades your application and its dependencies (unless you [preload your app](https://docs.gunicorn.org/en/stable/settings.html#preload-app)!), but it never closes the main Gunicorn process, so Gunicorn itself doesn't get upgraded. This isn't a big deal since Gunicorn updates are rare (there were almost two years between 20.0.4 and 21.0.0 releases), and it's probably not a big deal to restart your app once in a while even if it means losing a few requests, but if you want to avoid downtime there is a way to do it.

First, start a new Gunicorn process alongside the old one:

```bash
kill -USR2 $(cat gunicorn.pid) 
```

Once you see the new Gunicorn process is running, tell the old process to stop serving requests:

```bash
kill -WINCH $(cat gunicorn.pid)
```

Finally, when you confirm that the old process has stopped serving requests, tell it to terminate:

```bash
kill -TERM $(cat gunicorn.pid)
```

More info about this is available in the [official Gunicorn docs](https://docs.gunicorn.org/en/stable/signals.html#upgrading-to-a-new-binary-on-the-fly), along with instructions on how to revert the process if you encounter problems.

## Uvicorn

Uvicorn only runs a single process and isn't recommended for production alone, so the [official Uvicorn docs](https://www.uvicorn.org/deployment/#gunicorn) recommend using a process manager like Gunicorn to overcome this limitation. This is great because we have just learned how to restart Gunicorn without downtime!

To get Gunicorn to run your Uvicorn processes, you only need to define the `worker_class` variable in the config file:

```python
worker_class = "uvicorn.workers.UvicornWorker"
```

## Conclusion

I hope this showed that managing your Gunicorn process is not as complicated as it seems and that you don't have to reach for Kubernetes to achieve no-downtime deployments.
