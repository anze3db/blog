---
layout: post
title: "Cross-platform Games"
category: 
tags: [gamedev, web, webgl]
---
{% include JB/setup %}

So you want to create a cross-platform game? Here are your options:

2D Canvas
---------

2D Canvas has broad support both for desktop and mobile. It has it's limitations though, the biggest one being that you are bound to the CPU as most implementations can't harness the power of the GPU. You might also need to use a library (or two) to get the input and sound working cross-platform. If you are trying to create a very simple game this might be a good option for you.

WebGL
-----

WebGL solves the biggest issue with 2D Canvas - it gives you direct access to the graphics card (via the OpenGL ES 2.0 API), but it does so with a cost. It looses the cross-platform compatibility of 2D Canvas. Not even all the browsers on the desktop support the API (I am mostly looking at you IE). Android does have some support for WebGL (in Chrome beta via a special flag and in the webkit browser as well), while iOS seems to have support but is currently disabled. There is even an enabler app that you can buy, but I have no idea if it actually works. Hopefully support will improve in time and WebGL will become a viable option for developing cross platform games.


LycheeJS
--------

[LeechyJS](http://martens.ms/lycheeJS/) is a library written in Javascript. It also provides a cool tool called [Lychee-ADK](https://github.com/martensms/lycheeJS-adk), which allows cross-compiling apps to different platforms. It's using the V8 JIT runtime with OpenGL, GLU and GLUT integration. It's still under heavy development, but it promises to have support for Windows, Windows Metro, Linux, Android 2.3, Android 4.x, iOS 5.0+ and even Mac OSX once finished. In the meantime feel free to contribute to the project on [github](https://github.com/martensms/lycheeJS)!

libgdx
------

[LibGDX](http://libgdx.badlogicgames.com/) is a game framework written in Java. It allows you to write your game from the comfort of your desktop and it even has code [hot swapping](http://smotko.si/hotswapping/) support. It uses Google Web Toolkit for porting to the web and Xamarin.iOS for iOS, but the latter requires a license.

MonoGame
--------

[Monogame](http://monogame.codeplex.com/) is an opensource implementation of the XNA Framework. It's goal is to allow developers to port their games to all the major operating systems including Linux, iOS and Android. Only 2D games are supported on iOS and Android at the moment though.

Unity
-----

[Unity](http://unity3d.com/) is a development environment, which currently works on Windows and Mac OSX, but it allows you to export your games to Linux as well. It also supports iOS and Andoroid, but it comes with a cost ($400 or $1500 for the pro license). It also has a web viewer but it doesn't work on Linux yet.

C++
---

From what I can tell all the main mobile OSes support C++ in some way or another. Android has it's NDK, ObjectiveC on iOS can also import C++ files and Microsoft added C++ support in Windows Phone 8. The only problem is that I failed to find a framework/library that would make it easier to write cross-platform games in C++.

Fin
---

Have I missed anything? Let me know in the comments!
