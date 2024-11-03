---
layout: post
title: "Writing a Pytest plugin"
description: "How to write a simple pytest plugin."
date: 2023-10-06 0:00:00 +0000
image: /assets/pics/pytest-plugin-og.png
tags: python pytest
---

I've been working on a `pytest` plugin, and I've learned how some of this black magic works, so I thought I'd share.

## Entrypoint

When you install a `pytest` plugin, it will be automatically loaded when you run `pytest`.

```console
❯ pytest
=================== test session starts ====================
platform darwin -- Python 3.11.4, pytest-7.4.2, pluggy-1.3.0
rootdir: /Users/anze/coding/pytest-plugin-example
plugins: exampleplugin-2023.10.6
collected 3 items
```

We can see that my `exampleplugin-2023.10.6` plugin was loaded when we ran the tests.

`pytest` has [many different ways](https://docs.pytest.org/en/7.1.x/how-to/writing_plugins.html#plugin-discovery-order-at-tool-startup) to load a plugin at startup, but the simplest way for the users of the plugin is to use the `pytest11` entrypoint. This entrypoint is a convention that allows `pytest` to automatically load a plugin for any installed package. You can define the entrypoint in your `pyproject.toml` file:

```toml
[project.entry-points.pytest11]
exampleplugin = "exampleplugin.hook"
```

The `exampleplugin.hook` module contains the plugin's hook implementations. The module's name is unimportant, but it's good to name it after the plugin.

## Hook implementations

A `pytest` plugin is a Python module that implements one or more [hooks](https://docs.pytest.org/en/7.1.x/reference.html#hooks). Hooks are plain functions with specific names that `pytest` calls at particular points during its execution. For example, the `pytest_addoption` hook is called when `pytest` parses the command line arguments. The `pytest_runtest_setup` hook is called before each test is run.

You can find the whole list of hooks in the [pytest documentation](https://docs.pytest.org/en/7.1.x/reference.html#hooks), but some of the most important ones are listed below:

```
main()
 +- PyTestPluginManager()
 +- Config()
 +- import+register default built-in plugins
 |   +- pytest_plugin_registerd()
 +- pytest_namespace()
 +- pytest_addoption()
 +- pytest_cmdline_parse() 1:1
 +- pytest_cmdline_main() 1:1
     +- Session()
     +- pytest_configure()
     +- pytest_session_start()
     +- pytest_collection() 1:1
     |   +- pytest_collectreport() per item
     |   +- pytest_collection_modifyitems()
     |   +- pytest_collection_finish()
     +- pytest_runtestloop()
     |   +- pytest_runtest_protocol() per item
     |       +- pytest_runtest_logstart()
     |       +- pytest_runtest_setup()
     |       +- pytest_runtest_call()
     |       +- pytest_runtest_teardown()
     +- pytest_sessionfinish()
     +- pytest_unconfigure()
```
[Source](https://devork.be/talks/pluggy/pluggy.html)

## Publishing the plugin

The easiest way for users to use your pytest plugin is to publish it on PyPI. There are many ways to publish your plugin, but I like using [Hatch](https://hatch.pypa.io/latest/) because it has excellent defaults and it's [easy to automate with GitHub Actions](/automate-hatch-publish). [Hatch's documentation](https://hatch.pypa.io/latest/intro/) does a good job of explaining how to create a new project and publish it.

## Wrapping it up

That's it! You now know how to write a simple pytest plugin and publish it. If you need examples, try searching for the [pytest classifier](https://pypi.org/search/?c=Framework+%3A%3A+Pytest) on PyPI. There are a lot of fantastic plugins out there that you can learn from!
