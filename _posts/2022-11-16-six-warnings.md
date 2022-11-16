---
layout: post
title: "Fixing <code>_SixMetaPathImporter.find_spec() not found</code> warnings in Python 3.10"
description: "..."
date: 2022-08-11 7:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

I am helping a client upgrade their Django application to Python 3.10 and we encountered this mysterious warning when running the app on Python 3.10:

```python
<frozen importlib._bootstrap>:914: ImportWarning: _SixMetaPathImporter.find_spec() not found; falling back to find_module()
```

To make matters worse, this warning doesn't only show up once, but more than 200 times when we run `python manage.py runserver`. It completely floods the console output 😱 



A fair amount of googling revealed that the warnings are comming from the [`six` library](https://pypi.org/project/six/). Luckily they already patched the issue in [version 1.16.0](https://github.com/benjaminp/six/blob/master/CHANGES)! We just have to make sure we are running the latest version!

But something isn't right, running `pip show six` shows:

```
Name: six
Version: 1.16.0
Summary: Python 2 and 3 compatibility utilities
Home-page: https://github.com/benjaminp/six
Author: Benjamin Peterson
...
```

We seem to be all up to date! But then why are we still getting the warning spam? 🤔

# Vendored Six

It turns out that it is very common for other packages to *vendor* six. This means that even though we have six `1.16.0` installed, the package has it's own version of six that isn't up to date.

To find the packages with the old version I came up with the following `grep` command:

```bash
grep -r '__author__ = "Benjamin Peterson' -A 1 venv 
```

The command searches through your virtualenv folder for any lines containing the line `__author__ = "Benjamin Peterson`, which is [a line](https://github.com/benjaminp/six/blob/master/six.py#L31) from the `six` library. Tere might be some false positives if you have some other Benjamin's packages installed, but there were no such packages in our case. The `-A 1` argument makes grep print the line after the matched line, which in this case happens to be the version. The problematic packages are the ones where the version string is lower than `1.16.0`:

```bash
venv/lib/python3.10/site-packages/boto/vendored/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/boto/vendored/six.py-__version__ = "1.9.0"
--
venv/lib/python3.10/site-packages/snowflake/connector/vendored/urllib3/packages/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/snowflake/connector/vendored/urllib3/packages/six.py-__version__ = "1.16.0"
--
venv/lib/python3.10/site-packages/botocore/vendored/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/botocore/vendored/six.py-__version__ = "1.10.0"
--
venv/lib/python3.10/site-packages/pip/_vendor/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/pip/_vendor/six.py-__version__ = "1.16.0"
--
venv/lib/python3.10/site-packages/pip/_vendor/urllib3/packages/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/pip/_vendor/urllib3/packages/six.py-__version__ = "1.16.0"
--
venv/lib/python3.10/site-packages/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/six.py-__version__ = "1.16.0"
--
venv/lib/python3.10/site-packages/newrelic/packages/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/newrelic/packages/six.py-__version__ = "1.3.0"
--
venv/lib/python3.10/site-packages/newrelic/packages/urllib3/packages/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/newrelic/packages/urllib3/packages/six.py-__version__ = "1.16.0"
--
venv/lib/python3.10/site-packages/urllib3/packages/six.py:__author__ = "Benjamin Peterson <benjamin AT python DOT org>"
venv/lib/python3.10/site-packages/urllib3/packages/six.py-__version__ = "1.16.0"
```

In this particular case we had to remove the `boto` (it hasn't been maintained in years), and upgrade `botocore` to the latest version. `newrelic` also has an out of date version vendored, but it doesn't seem to be emitting any warnings so we left it be for now.
