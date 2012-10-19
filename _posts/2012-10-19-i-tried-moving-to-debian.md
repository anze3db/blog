---
layout: post
title: "I tried moving to Debian"
category: 
tags: [linux, fail, ubuntu]
---
{% include JB/setup %}

Yesterday I decided it was time to say goodbye to Ubuntu 12.04 and move to Debian Wheezy. This wasn't due to the controversial changes Ubuntu made this release cycle, I don't mind uninstalling a lens I find annoying. I couldn't upgrade to 12.10 because the legacy fglrx drivers no longer work with kernel 3.5. I still wanted to try out something new though, hence Wheezy.

The installation went without a problem, but when I rebooted I got this:

<a href="/assets/pics/linux-fail1.jpg" style="text-align:center;"><img class="" src="/assets/pics/linux-fail1.jpg"  width="700" alt="Linux problems 1" /></a>

I couldn't even get to the root shell. Booting in recovery mode didn't help as well. I even tried reinstalling the system without a graphical user interface, but the end result was the same. Seems like something was seriously wrong with the drivers, but because I couldn't reach the shell I didn't know what to do.

Back to Ubuntu
--------------

After a few hours I gave in and decided to reinstall Ubuntu 12.04. Everything went well until I installed all the updates and restarted the system. Instead of Ubuntu booting back up I got this lovely little message:

<a href="/assets/pics/linux-fail2.jpg" style="text-align:center;"><img class="" src="/assets/pics/linux-fail2.jpg"  width="700" alt="Linux problems 2" /></a>

This was not a good day for Linux. Luckily the solution for this problem was easy - reinstall grub from a live CD. Now I seem to have a working system. 
