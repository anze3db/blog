---
layout: post
title: "Django-TUI: A Text User Interface for Django Commands"
description: "How I've built django-tui"
date: 2023-08-25 0:00:00 +0000
image: assets/pics/django-tui.png
tags: django
---

![django-tui screenshot](/assets/pics/django-tui.png)

I’ve just launched [django-tui](https://github.com/anze3db/django-tui), a command line tool for listing and running Django commands. It is my second [Textual](https://github.com/textualize/textual) application this month ([link to first - words-tui](./words-tui/)), so I think it's safe to say that I'm embracing the application in the terminal idea.

## How does it work?

`django-tui` uses [Trogon](https://github.com/textualize/trogon) to render all of the UI. Trogon is a project for turning [Cklick CLI](https://click.palletsprojects.com/en/8.1.x/)s into TUI apps.

Most of the code in `django-tui` deals with translating Django commands that usually use [argparse](https://docs.python.org/3/library/argparse.html) to a representation that Trogon understands. I believe I covered most of the different options, but there are probably still some edge cases that I've missed. I'll ship regular updates to address these and add new features in the coming weeks.

If you have any ideas on how to improve django-tui please [let me know](https://github.com/anze3db/django-tui/issues/new) ❤️ 

## DEMO

<video style="width:100%; padding: 0 20px 20px 20px;" src="/assets/videos/django-tui.mp4" poster="assets/pics/words-tui.png" muted autoplay loop></video>

## Fin

I’ve made the tool primarily because I can never remember the commands or their arguments’ names, especially on larger Django projects with many custom commands.

It's great to see that other people find this useful as well. The `django-tui` repository already has 22 stars 🤩


