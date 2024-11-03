---
layout: post
title: "Using a game engine to draw a 3D graph crossplatform"
tags: gamedev 
---


It was just a matter of time until my game development hobby started creeping into my *serious* work. I have made 
an application prototype, that draws a 3D graph, using what is essentially a game engine. The application can be run
on Android, iOS, Blackberry and desktop (Windows, Mac OSX, GNU/Linux). 

Here we have the prototype running on my Nexus 7 (the old one):

<img src="/assets/pics/cpp.png" title="The 3D graph" class="middlepic" alt="3D graph" />

The graph is displaying activity on our IRC channel for every hour of every day of the week. It's a rough prototype. The camera 
is fixed, labels don't really show what the graph is about, and it's ugly.

But it shows potential 
----------------------

The app is written in C++ and uses OpenGL ES for rendering. It could handle beautiful animations of realtime data changes without
breaking a sweat. And the same code could be used for most smart phones and tablets<sup><a href="#win">1</a></sup>! 

The game engine I've used is called [Gameplay](http://www.gameplay3d.org/) and it's the easiest way of creating crossplatform
mobile applications I've managed to found. (I have also tried with OGRE and SDL).

Now lets see if I can make this prototype into something actually useful.

PS
--

You can check out the source code on [Github](https://github.com/Smotko/graph), but there is not much there yet.

---------------------------------------

<p><sup id="win">1</sup> Not on tablets and phones running Windows though. It seems to be the only mobile platform not using OpenGL ES.</p>
