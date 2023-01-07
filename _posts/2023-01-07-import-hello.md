---
layout: post
title: "import __hello__"
description: "The `import __hello__` easter egg in Python."
date: 2023-01-07 1:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

In the [latest episode of the Real Python Podcast](https://realpython.com/podcasts/rpp/139/) the topic of [Python Easter Eggs](https://github.com/OrkoHunter/python-easter-eggs) came up. One of the mentioned easter eggs was `import __hello__`:

```python
>>> import __hello__
Hello World!
>>> import __phello__
Hello world!
```

There is even a spam version of it:

```python
>>> import __phello__.spam
Hello world!
Hello world!
```

# Batteries included

It makes sense that Python - the language with batteries included - also includes a hello world program, one import away right?

These top-level modules weren't added just for fun, according to the comment in the [CPython source code](https://github.com/python/cpython/blob/a109454e828ce2d9bde15dea78405f8ffee653ec/Python/frozen.c#L34-L36) they were added for testing frozen modules:

```c
/* In order to test the support for frozen modules, by default we
   define some simple frozen modules: __hello__, __phello__ (a package),
   and __phello__.spam.  Loading any will print some famous words... */
```

# Python 3.11

In Python 3.11 the `__hello__` and `__phello__` modules no longer print the text when they are imported. You now have to call the module's main method to get the same effect:

```python
>>> import __hello__
>>> __hello__.main()
Hello World!
>>> import __phello__
>>> __phello__.main()
Hello World!
```

This isn't the first time the `__hello__` imports *broke* in a newer Python version. The same thing also happened in the initial versions of Python 3 (3.1, 3.2, 3.3, 3.4) according to [this issue from 2011](https://bugs.python.org/issue11614).

Even though the easter egg was [fixed back in 2011](https://hg.python.org/cpython/rev/44fd95cead7b), it looks like [the change in Python 3.11](https://github.com/python/cpython/issues/100136#issuecomment-1344428244) was intentional and won't be reverted.
