---
layout: post
title: "My plans for Raspberry Pi"
tags: raspberrypi
---


A week or so ago, I was able to preorder a little piece of hardware named Raspberry Pi. On the day the thing got released I and quite a few other people, managed to take down websites from Farnell and RS Components. The first 10.000 units sold out in 7 minutes or so. 

What is it
----------

<img class="txt-img" src="/assets/pics/berryLogo.jpg" title="Raspberry logo" width="119" alt="logo" />
Unless you have been living under a rock, you probably already know what a Raspberry Pi is. It's a tiny computer with an ARM processor, hdmi, audio, ethernet and 2 usb ports. It is somewhat comparable by performance to an iPhone, but a Raspberry Pi costs less than a HDMI connector for the said phone. It was made to help children across the world to learn programming, but the first few batches will probably be all bought up by geeks like me.

Why do I want one
-----------------

I already own a similar device - an ARMv5 board with a 196MHz processor and some RAM. I use it to run an annoying IRC bot, that logs our chats and tells us when a link is a repost (some of it's code is on [Github](https://github.com/Smotko/botko), but it's not the prettiest thing I've writen). This little ARM board is great, but I have ran into a few problems with it. I haven't managed to get git working, as all of my crosscompiling attempts have failed and compiling on the actual board takes forever before it throws up a random error. To be fair, I had this problem with everything that isn't in the default buildroot environment, which only contains a handful of applications I would like to use.

Raspberry Pi is, on the other hand, backed up by actual Linux distributions (Arch, Debian and Fedora) and I am very confident, that installing software will not be such a pain. This will of course make the Pi useful for many things. Here are a few that come to mind: 

* Host for private git repositories,
* simple webserver for testing out things like nodejs,
* SSH "entrance" for my home network,
* my IRC chat bot.

The Raspberry Pi is ideal for this as it has a processor that can tackle all of these things and is completely silent, as it doesn't need a fan. To top off, it uses only a small amount of energy.

And much more
-------------

The stuff I mentioned so far is just the geeky stuff that I will be doing as soon as I get my new board. There are many uses for it for less techy users as well. It  can be used as a movie player (it even plays full hd videos), and it can probably transform ones USB hard drive into a network disk. As it can run a desktop environment it could even be used for some simple office work or web browsing.

What about you
-------------

Do you have any ideas? What are you going to do with your Raspberry 3.14?
