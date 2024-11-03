---
layout: post
title: "Why don't we have code hot swapping on mobile?"
tags: gamedev
---


Code hot swapping is one of the most useful features a language can offer. It allows the developer to see changes as soon as he saves the source code. No restarting needed, your changes just pop up on the screen and your application state is preserved. Hot swapping magically updates method runtimes and gives you **immediate feedback**. This is invaluable and double so for developing graphical applications such as games. You don't believe me, checkout [this talk](http://vimeo.com/36579366#at=3).

A quick example
---------------

In Java hot swapping is supported out of the box. You fire up eclipse, write a simple application like this:

    public class HotSwap {
        public static void main(String[] args) throws InterruptedException {
            while(true){
                swap();
                Thread.sleep(2000L);
            }
        }
        public static void swap(){
            System.out.println(":(");
        }
    }

and press `F11` or select run/debug from the menu. Your application will start printing out a sad face, but you can easily turn that frown upside down, save the file and output will become a smiley face. Amazing right? Now imagine having this much power while developing a game. You can start playing with colors, sizes of objects or even gravity in a platform game. It also works if you're doing an OpenGL application. You will occasionally run into a `Hot Code Replace Failed` dialog and will have to restart your application, but this doesn't happen very often.

Moving on to mobile
-------------------

So now that you are blown away by the awesomeness that is hot swapping, you'll want to use it in your next project. Lets say you are writing a game for Android. You fire up Eclipse again, create a new Android project, do some setting up and start the application the same way you did in the first example. When you try to do a hot swap a dialog will pop up, telling you that this isn't possible.

<a href="/assets/pics/hotswap.png" style="text-align:center;"><img class="" src="/assets/pics/hotswap.png"  width="700" alt="Hot swap doesn't work" /></a>

The problem is that your application gets compiled, packaged, signed and sent to your mobile device where it gets installed. Most of these steps happen every time you launch the application. This set of steps apparently can't be circumvented and thus making code swapping impossible.

Not just Android?
-----------------

From what I can tell (and please correct me if I am wrong) Android Java isn't the only one with this limitation. It's the same sad story with Objective-C on iOS and Windows phone things. Is this really such a hard nut that none of the best and biggest tech companies can crack? This is not a rhetorical question, I am genuinely interested why no one has done this. From the way I see it, this would save lots of developer time. Time that is currently being wasted by slow application restarts.

Solutions?
----------

My current solution is to develop my game using Java with OpenGL ES 2.0 on my desktop and then port it to Android. Most of the code can be shared but this is far from an ideal solution. I still believe hot swapping is well worth the extra work.
