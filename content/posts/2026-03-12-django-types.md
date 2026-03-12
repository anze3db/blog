---
title: "Typing your Django project"
date: 2026-03-12T0:00:00Z
---

The first version of Django was released about 10 years before [Python standardized its type hints syntax](https://peps.python.org/pep-0484/). Because of this it's not surprising that getting type hints to work in your Django project is not going to be trivial.

## django-stubs with mypy

If you want your Django codebase to be type checked then [django-stubs](https://github.com/typeddjango/django-stubs) is the go to package to use. It ships both [type-stubs](https://peps.python.org/pep-0561/) for most of Django's public APIs as well as a mypy plugin that fills in the typing information for all the dynamic black magic that we love Django for. You'll also want to include the monkeypatch from [django-stubs-ext](https://pypi.org/project/django-stubs-ext/) for best results.

This works but it's kinda slow. `mypy` on its own isn't that fast but paired with `django-stubs` that loads your app to fill in the dynamic bits makes the experience even more sluggish - especially if you have a somewhat larger Django application. Yes, there is [mypy daemon](https://mypy.readthedocs.io/en/stable/mypy_daemon.html) that offsets some of this slowness when using `mypy` but in my experience it's not fast enough to comfortably use in your code editor.

I usually put `mypy` with `django-stubs` in the CI to run in parallel with tests.

## pyright, ty, pyrefly

If you prefer speed over completeness then using any of the newer type-checkers is the way to go. Unfortunately, none of them support django-stubs' mypy plugin so you will always get false positive errors.

Most commonly you'll see:


```python
error[unresolved-attribute]: Object of type `User` has no attribute `id`
   --> config/model.py:359:43
    |
359 |             changes={"ignored_by": [None, current_user.id]},
    |                                           ^^^^^^^^^^^^^^^
360 |             actor=current_user,
361 |             timestamp=now,
```

You'll get errors in everywher dynamic Django properties like the `id` field or related relationship names are used. This will likely be all over your codebase.

Some of these tools (looking at you `ty`) currently don't work with `django-stubs` at all. [django-types](https://pypi.org/project/django-types/) can help in these cases. It's a fork of `django-stubs` without the mypy plugin.

The django-types solution for the `id` and related names errors is to explicitly define them on the model. As an example:

```python
class User(models.Model):
    id = models.AutoField(primary_key=True)
    # OR
    id: int
```

Alternatively, using `current_user.pk` usually doesn't show up as a type error so I default to using that.

I run `pyright` in my code editor and have learned to ignore some of the false positives it underlines. I don't use these faster tools in CI, because it's almost impossible to get the errors down to zero. I hope that at some point we'll be able to switch because wheres mypy checks your code base in minutes, ty and friends finish in seconds!

One caveat of using django-stubs and django-types is that they lag behind Django versions. At the time of writing this post Django 6.0 has been out for almost 3 months but neither has released support for the new version. Not a huge issue because in the worst case you can just sprinkle some type ignore comments and still upgrade but still.

## Aside with Django-Mantle

One way to avoid issues with dynamic Django types is to not use dynamic types at all. With [Django-Mantle](https://noumenal.es/mantle/) you define [attrs](https://www.attrs.org/en/stable/) classes and then use helper functions to populate them. From the docs:

```python
from django.db import models

from attrs import define
from mantle import Query


class Bookmark(models.Model):
    url = models.URLField(max_length=500)
    comment = models.TextField()
    favourite = models.BooleanField(default=False)


@define
class BookmarkAttrs:
    url: str
    comment: str
    favourite: bool

rows = Query(Bookmark.objects.all(), BookmarkAttrs).all()
# reveal_type(rows)  # list[BookmarkAttrs]

row = Query(Bookmark.objects.filter(favourite=True), BookmarkAttrs).get()
# reveal_type(row)   # BookmarkAttrs
```

Now as long as your business logic always deals with your `BookmarkAttrs` instead of the underyling Django Model you should have no issues with types!


## Types in Django?

6 years ago, Django made the decision [to not allow types](https://groups.google.com/g/django-developers/c/C_Phs05kL1Q/discussion) in the codebase. Now that typing in Python feels more mature, ([3.14 solved the long running debacle around deferred evaluation of annotations](https://docs.python.org/3.14/whatsnew/3.14.html#whatsnew314-deferred-annotations)), and because new Python web frameworks have become very popular partially becasue they embraced types, the Django community is [trying to figure out how to add types](https://github.com/django/new-features/issues/23#issuecomment-2931554777) so hopefully we will soon see types in Django itself 🤞

The future looks bright, especially if [PEP-0827](https://peps.python.org/pep-0827/) gets accepted. PEP-0827 could pave the way for Django to have some of the more dynamic parts of Django typed without the need for a mypy plugin!

If we can learn anything from the success of FastAPI is that a web frameworks can use runtime type information to provide a good user experience. I'm not saying Django has to change how we define urls (we have [django-ninja](https://django-ninja.dev/) if you want FastAPI like experinece in Django!) but improving the current typing situation would be a big step forward!
