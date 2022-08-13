---
layout: post
title: "Pyupgrade"
description: "..."
date: 2022-08-11 7:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

`pyupgrade` is an awesome tool. It upgrades your Python code to use the latest and gratest language features and makes your codebase more consistent.

We have recently run it over the whole repository at the day job and the results were great.

Hint to run it on all files:

```python
pyupgrade --py310-plus  `find . -name "*.py" -not -path "./.tox/*"`
```
