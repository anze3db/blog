---
layout: post
title: "Creating Tinder like animations with CSS"
category: 
tags: [sideprojects, freelancing, work, fun, webdev, css]
---

<img src="http://i.imgur.com/NkVwpKT.gif" alt="gif showing how the animation looks like" style="float: right;
margin: 0 0 0 15px;
border-radius: 10px;
border: 1px solid #666;" />
Recently, I've helped in the making of a cool little side project <a href="http://windowshopper.me">WindowShopper</a>. 

My task (among other things) was to make sure the experience on mobile devices is as fun as possible. We drew upon heavily from
the awesome <a href="http://www.gotinder.com/">Tinder app</a>, which is a joy to use, mostly due to the slick swipe gestures and animations. 


Even though, we were making a web application, we wanted a similar experience for our app as well. On the right you can see the end result which using a pinch 
of JavaScript and the awesome CSS3 animations. 

The gif was captured on a 3 year old Android phone while running recording software in the background. In real life it's
even smoother, try it out yourself!

CSS3 animations are amazing
---------------------------

We managed to get the smooth animations by relaying entirely on CSS3. These are styles which make the magic 
happen:

{% highlight css %}

/*I've left out browser specific prefixes (-webkit-transition, -moz-transition, -o-transition, ...) for clarity */

.animate-like.ng-leave,.animate-dislike.ng-leave,.animate-partial{
  transition:all linear 0.3s;
}
.animate-like.ng-leave {
  transform: translateX(0px) rotate(0deg);
}
.animate-partial.animate-like-partial {
  transform: translateX(10%) rotate(5deg);
}
.animate-like.ng-leave.ng-leave-active {
  transform: translateX(100%) rotate(60deg);
}
.animate-dislike.ng-leave {
  transform: translateX(0px) rotate(0deg);
}
.animate-partial.animate-dislike-partial {
  transform: translateX(-10%) rotate(-5deg);
}
.animate-dislike.ng-leave.ng-leave-active {
  transform: translateX(100%) rotate(60deg);
}

{% endhighlight %}

When you drag your finger across the screen, a class will be set based on the direction you're dragging (`.animate-like-partial`
or `.animate-dislike-partial`). This will cause the item to move and rotate slightly. If you change your mind and move 
your finger in the opposite direction the class will be removed. When you release the screen the `.ng-leave-active` class
is set, which removes the item completely. It's so simple it feels like *cheating*.

And it actually is *cheating*. Unlike the native Tinder app, this solution doesn't actually follow your finger - it just 
transitions between possible states. If you'd want to get the item to actually follow your finger, you'd need to move it using
JavaScript. 

Unfortunately, moving DOM elements with JavaScript will not work well on mobile, but you could still make
this work by ditching DOM and using `canvas`.

What do you think? Any ideas on how to make this even better?
