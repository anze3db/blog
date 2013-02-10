---
layout: post
title: "The Chrome Javascript editor can do hot swapping"
category: 
tags: [gamedev, web, javascript]
---
{% include JB/setup %}

Hot swapping is the process of replacing code while the application is *running*. It allows a developer to see changes immediately - no recompiling, no waiting on page reloads, and no clicking to get to the application state where the code was changed. Just save the file and you'll see the changes.

I would say hot swapping is a must for making applications with an always active update loop (games) and [this guy](http://vimeo.com/36579366#) would probably agree.

The Chrome editor
-----------------

<img src="/assets/pics/chrome-editor.png" title="Chrome editor" style="padding: 10px;margin:10px auto; display:block;"  />

As you can see from the picture above, the Chrome editor has everything you need.

There is a built in tree list view of all scripts used by the application. The editor supports tabs which are remembered when you close the browser window. You have access to the debugger and all the tools that come with it and the all powerful console is right where you need it.

You can even have the editor side by side with the web page:

<img src="/assets/pics/chrome-editor2.png" title="Chrome editor" style="padding: 10px;margin:10px auto; display:block;"  />

Most importantly it supports **hot swapping out of the box**. When you press `control+s` Chrome will start using the updated file immediately. The need for refreshing the page will greatly decrease.

Saving files locally
-----------------------

By default changes made will be lost when you refresh the page. But with right clicking the source file you can choose the `Save As...` option. Now just point the dialogue box to your local version of the site and now all the changes you make will get written to you hard drive. Awesome! 

The only problem is that you will need to go through the `Save As...` step for every file in your application. It would be nice to just specify your localhost directory and then let Chrome figure out what goes where. Maybe in the next update?

Not just Javascript
-------------------

All of the awesome things I mentioned work for editing css files as well. Designers rejoice!

Now we just need a better interface for saving files locally, an easy way of running unit tests, a vim mode and we will have the perfect editor!



