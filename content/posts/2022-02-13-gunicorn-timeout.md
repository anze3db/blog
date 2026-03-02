---
title: "Gunicorn Timeouts"
date: 2022-02-01
slug: "gunicorn-timeout"
draft: true
---

Gunicorn has a --timeout option that only works for sync workers.

> Workers silent for more than this many seconds are killed and restarted.

The problem is that this can happen while the workers are starting which means that the worker can be killed before it even boots up.



