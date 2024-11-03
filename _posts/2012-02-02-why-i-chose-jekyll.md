---
layout: post
title: "Why I chose Jekyll"
---


Choosing a blogging platform that  you like may seem trivial to some, but not to me. All the blogging platforms out there seem either too simple or too complicated for me. This is why I have always resorted to writing my own simple CMS, but the problem was that my own CMS was even worse than all the others. At first it seemed like it suits my needs but I ended up hating it nonetheless.

I tried really hard to get used to Wordpress, I really did! But in the end it just wasn't working, here are a few resons why:

1. Templating is a nightmare. I felt like I needed to invest a lot of time to get my site to behave the way I wanted too.
2. The WYSIWYG editor is crap, but I wouldn't blame WP for this one. I believe that all WYSIWYG editors (Word is another great example) are flawed. Sooner or later the editor will misunderstand what you want it to do and shoot you in the leg.
3. The CMS seems bloated and I get lost in all those settings and sub-settings, plugins, themes and whatnot.

Jekyll to the rescue!
---------------------

Jekyll is a simple static site generator. Basically you feed it a template directory with a page layout and some Markdown content and it spits out a static website which you can upload to your webserver. 

It is really easy to install as well. If you have Ruby installed it is just a matter of getting the Jekyll gem. This is usually done with a single command:

    sudo gem install jekyll

I actually ran into a little problem, the error message was:

    ERROR: Failed to build gem native extension

It turned out that I needed the ruby dev package, the below command fixed my issue:

    sudo apt-get install ruby1.9.1-dev

After that I was all ready to start building my new and shiny blog page.

It gets even better
-----------------------

Github provides something called Github:pages (GP). GP is basically a free static page hosting for your projects and/or personal page. It also has Jekyll built in which means that you simply put your jekyll source into a git repository, push it to a specified github branch and github will generate your blog page automagically. 

Not only does this force you to keep your blogs in a git repository (which is a good idea by itself), it also makes for the most intuitive way of posting a blog post (well at least for a programmer like me).

Some more sugars
----------------
Have you ever wanted beautiful syntax highlighting on your blog? Well Jekyll does Pygments which means I can have beautiful syntax highlighting like this:
```python
def prob42():
    f = open('words.txt')
    
    tri = 0 
    triangle = []
    for n in xrange(1, 1000):
        triangle.append(n * (n + 1) / 2)
    
    for i in f.readlines():
        for j in i.split(',"'):
            w = j.replace('"', '') 
            x = 0 
            for k in w:
                x += ord(k) - 64
            if x in triangle:
                tri += 1
    print tri 
```

I even heard there is LaTeX to PNG support, although I haven't had the time to check that out yet.

There is still a possibility that I will start hating Jekyll after a few months of blogging. But that may just mean that I actually hate blogging. Hopefully this will not happen!

