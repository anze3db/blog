---
layout: post
title: "Textual App Auto Reload"
description: "How to automatically reload your Textual app when code changes occur"
date: 2023-08-01 0:00:00 +0000
---

# CSS Live Editing

By running the `textual run` command with the `--dev` switch you enable [live editing of CSS files](https://textual.textualize.io/guide/devtools/#live-editing):

```bash
pip install textual textual-dev # Install Textual and the textual-dev tools
textual run --dev app.py
```

Example:

<video style="width:100%; padding: 0 20px 20px 20px;" src="/assets/videos/textual-live-css.mp4" muted autoplay loop></video>

This is fantastic for making style changes in your TUI app. It allows you to easily fine-tune your app's layout and appearance down to pixel (or character) precision and see the results in real-time.

However, this only works for changes in CSS files. If you make changes to your Python code, you'll have to restart your app to see the changes.

# Python Reloading

Fortunately, there are existing tools to help you restart your application when code changes occur. There is probably a better way, but I like [`pytest-watch`](https://pypi.org/project/pytest-watch/), a plugin for [`pytest`](https://pypi.org/project/pytest/) that re-runs your test suite when you modify your Python files.

`pytest-watch` isn't limited to running tests. You can use the `--runner` flag to run arbitrary commands when file changes are detected. In our case, we want to use pytest-watch to run the textual run command:

```bash
pip install pytest-watch
ptw --runner "textual run --dev app.py"
```

This isn't live editing as the CSS example above. It kills your application with each change and then starts it again, losing internal state in the process. But it's still pretty convenient!

Example:

<video style="width:100%; padding: 0 20px 20px 20px;" src="/assets/videos/textual-reload-python.mp4" muted autoplay loop></video>

# Conclusion

I've been enjoying using Textual. TUI apps are a refreshing break from web apps for me. The tooling around TUI apps is not as advanced as the tooling around web apps, but it is getting better every day.

PS: The app in the video examples is [textual-words](https://github.com/anze3db/textual-words). I'm building it to help me with my daily writing.
