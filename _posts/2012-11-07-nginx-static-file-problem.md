---
layout: post
title: "Nginx and VirtualBox shared folders"
category: 
tags: [wtf, web, nginx]
---
{% include JB/setup %}

I found something really peculiar. If you are trying to serve static files with Nginx from a Virtualbox Shared folder, you are going to have a bad time. I agree, you shouldn't be doing this in the first place, but this issue is so weird I really had to write a blog post about it. 

Let me explain
--------------

I have a folder with static files on my local machine (Ubuntu) and I have a Debian virtual machine running nginx. I have added a shared folder that allows the Debian server to access files on my local machine. Here is the `/etc/fstab` file that mounts the shared folder on the server:

    shared /home/smotko/shared vboxsf fmode=770,dmode=770,uid=smotko,gid=www-data 0 0

And this is in my Nginx config:

    location /static/ {
        alias /home/smotko/shared/static/;
    }

Now if I try to load the site.css file from http://site/static/site.css. Everything works as expected, but if I make a small change to the file from my local machine, I get this:

<a href="/assets/pics/nginxwtf.png" style="text-align:center;"><img class="" src="/assets/pics/nginxwtf.png"  width="700" alt="WTF" /></a>

It's a bit of the **old** file and some weird characters. Restarting nginx doesn't help, setting flags such as `expires` `sendfile` and `autoindex` doesn't do anything. If I `mv` site.css to site2.css it displays the changes, but if I then `mv` it back to site.css I get the old file and the weird characters again. `touch`ing the file doesn't help, but if I open it up in `vim` and just do a `:wq` nginx starts serving the updated version of the file.

Why is this happening?
----------------------

I don't really care about the solution, I will never be serving static files from a shared folder. But I would like to know **why** this is happening. From what I can tell, the file edited on my local machine is identical in every way to the file edited on the server and yet Nginx does not agree. Is this a bug in nginx? Is this a bug in vboxfs? Am I doing something wrong? What is going on here?

