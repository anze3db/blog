---
layout: post
title: Disable runserver warning in Django 5.2
date: 2025-06-24 08:31 +0100
tags: django
---

[Django 5.2 added a new warning](https://docs.djangoproject.com/en/5.2/releases/5.2/#management-commands) that shows up when you start your development server with `python manage.py runserver`:

```
WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/
```

Here is how it looks like in the terminal:

![Warning in the terminal](/assets/pics/django-5-2-warning.png)

The warning is helpful for newcomers because Django's development server is neither secure nor performant enough to be exposed to the internet.

However, if you've already configured your production environment with a proper WSGI/ASGI server, seeing the warning every time your development server reloads becomes tedious.

## The Fix

Luckily, there is a way to disable it with the [DJANGO_RUNSERVER_HIDE_WARNING](https://docs.djangoproject.com/en/5.2/ref/django-admin/#envvar-DJANGO_RUNSERVER_HIDE_WARNING) environment variable:

```
DJANGO_RUNSERVER_HIDE_WARNING=true python manage.py runserver
```

Clean terminal:

![Warning in the terminal fixed](/assets/pics/django-5-2-warning-fixed.png)

If you are using [django-environ](https://django-environ.readthedocs.io/en/latest/) or any other tool that loads environment variables from a `.env` file, you can put the `DJANGO_RUNSERVER_HIDE_WARNING=true` line to it, and the warning will no longer show up. 🎉


