---
layout: post
title: "How working remotely helped me better understand the codebase"
category: 
tags: [programming, work, freelancing]
---


Last Friday a coworker asked me how was I able to grasp the complexity of our project so quickly, while he's been struggling with it for months. I never gave it much thought, but it was true. I went from novice to pro faster than any other dev that joined the team. This even went so far that the CEO started calling me 'star developer'. At first I fought they were all mocking me, but later I came to realize they were honestly impressed by the progress I've made.

A bit of a background
------------

I don't consider myself to be super smart or a genius or not even a fast learner. I struggled getting both through high school and college, and my grades were never any good. The only thing I got going for me is that I am stubborn. Failing once, twice or even more times will not discourage me from trying to find the correct solution.

My prior experience was of no help to me when I started the job either. In previous jobs I mainly worked on the backend (in Python, PHP, and even Perl), but my role here was on the frontend - in a javascript framework I've never even heard of before (canjs). I did some javascript work before - a couple simple webgl games and a one page app in Angular, but my skills were limited. I didn't even know what a Deferred was when I started.

How did I do it?
------------

So how did I manage to overcome my shortcomings and become the top contributor in such a short time? I think at least a part of the reason was the fact that I live far away from my team. Let me explain why I think this really helped.

The team is located in the heart of San Francisco, but I live 9 time zones away. Because of the 9 hour time difference most of my colleagues across the Atlantic were not available to answer my questions during my workday. This might sound like a huge disadvantage, but it actually wasn't the case. Not having anyone to answer questions forced me to figure it out on my own. This is where my stubbornness come in really handy. I bashed my head against the wall until the code I was trying to fix started working. I probably wasted a lot of time doing this, but it forced me to dig deep into the bowels of the project, but every time I came out with a better understanding of how the application worked.

When you need help, make sure you know exactly what you need
----------------------------------------
<a href="http://xkcd.com/763/" style="text-align:center;"><img class="txt-img" src="/assets/pics/workaround.png" alt="xkcd 763" title="Remember your solution will not always be optimal... (xkcd 764)" width="300px"></a>

Now, of course, I was not always able to figure out everything on my own. In these cases I opened a pull request with my nonworking code and said: "I managed to get this far, but I'm still stuck with X," or something like: "This is working, but I'm not sure if this is the optimal way of doing Y". My coworkers were happy to answers questions of this type. They would just point to a line in the code and tell me where my error was, or told me use function foo instead of function bar and everything started working.

If I were asking questions such as "How do I do Z", my coworkers would get annoyed rather quickly. It would require a lot of effort on their part to explain Z to me, especially if I didn't put in the initial work and wouldn't be able to follow/understand their explanation. Feature Z might ship faster, but my understanding of the system would increase by only a small amount. When I'd have to work on the next thing, I'd just be stuck again.

Final thought
-----------

The point I am trying to make is that living far away forced me to try and solve the problem by myself. Even if it seemed really hard at first. Even if it meant bashing my head against the wall for a couple of hours. Before asking for help, I always tried to get to the bottom of the issue. By failing multiple times I was able understand the issue better, and it allowed me to ask questions that didn't waste my coworkers time. I also ended up understanding the core of the complex system as a byproduct.
