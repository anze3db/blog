---
layout: post
title: "Notes on Flutter"
description: "..."
date: 2022-07-09 7:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

In the last few months I've been working on a small personal project with Flutter. Here are some random thoughts on it.


# What I've made

I am a surfer and I look at surf cams a lot to figure out where to go surfing. I check multiple cams from multiple sources. Switching between the multiple apps has always frustrated me a bit as well as the UI quirks of the apps. Because of this I decided to create an app where I could see all the cams in a Netflix like UI (Netflix spent a lot of time figuring this out so why not).

To implement this I decided to use Flutter.

# How it works

Flutter uses an interesting way to accomplish cross-platformness. Everything that you see in flutter is rendered in a canvas element:

![Everything that you see is rendered in a canvas element](/assets/pics/flutter-canvas.png)

So no nothing is truely "native" in Flutter. Unlike React Native which uses native widgets, Flutter fakes all it's nativeness. This is why you can have a Cupertino styled app running on Android or a Material styled app on an iOS. You can even have a button that toggles between the two styles.

Even though Flutter isn't truley native, it really native. There are some clear tells that it actualy isn't (the two finger scrolling bug for instance), but most people won't tell the difference.

The implementation is also super fast. I tried to see if the app would break a sweat when it had to render a very tall list, but no, buttery smooth even with that.

<video src="/assets/pics/flutter-perf.mp4" autoplay controls></video>

# Quirks

1. Video player very inconsistent between platforms
2. Cupertino/Material UI
3. Stateful Components
4. Web handles touch events poorly

# Ideas
