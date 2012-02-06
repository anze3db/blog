---
layout: post
title: "The AMD Linux Drivers"
category: 
tags: [linux, drivers, catalyst, wtf]
---
{% include JB/setup %}

A couple of days ago AMD released Catalyst 12.1 drivers for Linux. I have been looking forward to this release as I had a lot of issues with previous drivers, namely with gnome-shell support.

Why did I put myself through this?
----------------------------------

Installing AMD drivers on Linux is never a pleasant experience and the open source drivers work out of the box, so why did I put myself through this? Well the open source drivers have a few shortcomings:

1. Battery life: My laptop battery lasts roughly an hour longer on official drivers.
2. GPU temperature: The core temperature is down to a pleasant 42 degrees (was 60+ on open source drivers).
3. I can now run more graphically intensive applications (yay games!). 

Full of hope that this new release will fix all the issues I had with previous versions, I embarked on an epic quest to get it working on my laptop.

Installing proprietary drivers
------------------------------

To install the drivers I followed the steps on the [Unofficial Wiki] [1] page for the AMD Linux driver. The steps themselves are pretty straight forward and I will not go into them here. Instead I will focus on everything that went wrong after I had the drivers installed.

After the reboot I got thrown into fallback mode and something was clearly wrong. Running `fglrxinfo` in the terminal gave me the following error:
     
     X Error of failed request:  BadRequest (invalid request code or no such operation)
       Major opcode of failed request:  139 (ATIFGLEXTENSION)
       Minor opcode of failed request:  66 ()
       Serial number of failed request:  13
       Current serial number in output stream:  13
     

A lot of *googling* later I found out that `modprobe` decided to blacklist the fglrx driver. This was probably due to a failed installation of a previous version. The bottom line was that the kernel module was not being loaded at boot which, of course, caused the drivers to fail. Thankfully the solution was pretty straight forward, I only had to open the modprobe blacklist file, located at `/etc/modprobe.d/blacklist.conf` and delete the following line:

    blacklist fglrx

After another reboot the drivers loaded successfuly working and both gnome-shell and Unity desktop seemed to be working!

There were still some issues though
-----------------------------------

To my surprise both Unity and gnome-shell worked well on the 12.1 Catalyst drivers. Random crashes and visual artifacts were gone and shell animations (when pressing the `<super>` key) were fast and responsive. There was an issue with moving windows across the screen though. The animation was jerky and flickery and it annoyed me to the point that I started *googling* for a solution.

The solution for the Unity desktop is hidden away in `CompizConfig Settings Manager`, under `OpenGl`. I had to disable the option called `Sync To VBlank`. After that dragging windows across the screen worked as it should.

There is a similar solution for the gnome-shell desktop. I had to add the line:

    export CLUTTER_VBLANK=none

To the end of the `~/.profile` file and then everything seemed to be working. That was a fact until I tried to plug in my second monitor.

Multidisplay support
--------------------

Cloned display worked out of the box, but I wanted a big desktop, spanning over both of my monitors. I opened up Catalyst Control Center (Administrative) (`sudo amdcccle`), went to the Display Manager page, selected Multi-display desktop with display(s) 1 and clicked apply. That caused the Catalyst Control Center to die silently without an error. I tried to enable multidisplay in the `Displays` application, where I got this message:

    required virtual size does not fit available size: 
       requested=(3360, 1050), minimum=(320, 200), maximum=(1680, 1680)

Finally something I can *google*! A solution for this is to put the line `Virtual 3360 1050` into the Display SubSection of `/etc/X11/xorg.conf`. My "Screen" section now looks like this:

	Section "Screen"
	    Identifier "aticonfig-Screen[0]-0"
	    Device     "aticonfig-Device[0]-0"
	    Monitor    "aticonfig-Monitor[0]-0"
	    DefaultDepth     24
	    SubSection "Display"
		    Viewport   0 0
		    Virtual 3360 1050
		    Depth     24
	    EndSubSection
	EndSection

But this isn't an optimal solution as it has a few issues:

* It only works if both monitors use the same resolution. In my case both monitors use 1680x1050 and it worked as expected, but a friend of mine was unable to hook up his 1920x1080 monitor beside his smaller laptop screen.
* When I unplug the second monitor, this forces the first monitor to the resolution of 1400x1050 (4:3) and I am unable to set the correct resolution neither in amdcccle nor the Displays application. This is why I have to comment out the `Virtual 3360 1050` line every time I want to unplug the second monitor.

There is probably a way to solve both of these issues, but my *google* skills have failed me, any ideas?

[1]: http://wiki.cchtml.com/index.php/Ubuntu_Oneiric_Installation_Guide#Installing_Proprietary_Drivers_a.k.a._Catalyst.2Ffglrx


