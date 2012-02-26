---
layout: post
title: "How we won 3 tablets"
category: 
tags: [android, programming, fun]
---
{% include JB/setup %}

A few weeks ago a ComTrade - local tech company decided to sponsor a challenge event in association with our faculty. The idea was that three teams, each with three students, would work on a fun little project - an application that visualizes data received from a remote controlled car. Because the application was meant to run on a Samsung Galaxy tablet me and two of my friends got excited and we signed up for the challenge immediately. 

The rules of the game
---------------------

As mentioned before there were three teams and each team received a Samsung Galaxy tablet to develop their solution. We were told that the winning team would get to keep all three of the tablets so we were really motivated to create the best possible application. We did not have a lot of time to do this though. The time constraint was about three weeks and we were in the middle of the exam period when the challenge started.

The application would be receiving data via bluetooth. The remote controlled car was sending data from its G-force sensor, its wheel turn value and its revs count. It was up to us to come up with cool and interesting ways to visualize this data.

The development process
-------------------

Even though we had a Galaxy tab to develop on we only had one tab to develop on. This of course meant that at any given time, two team mates would be forced to use the emulator. Now the thing with the android emulator is that it doesn't really work if you try to do some OpenGl. This is why we were forced to split the main application into a library project. We then created a separate project that used the library and displayed all the stuff in the tablet, but we also created a simpler phone application that could be run from our phones. This allowed us to work on OpenGl stuff even if somebody else got the tablet for the night. This was a great decision and it made the development of the OpenGl part of the application much easier, but it did force one of my team mates to use eclipse instead of vim.

We also learned really fast that it is way more difficult to work in a team than it is to work alone. It is really hard to focus on the stuff that you are doing, when you have two other people sitting beside you, disturbing you with the problems that they are facing while developing their own part of the application. We had quite a lot of problems with focusing on the tasks at hand the first few times we tried programming in a group, but we soon got used to it and got more productive. But we really need more projects like this as we all feel that our development process still has a lot of room for improvements.

How git saved our lives
-------------------

I cannot stress this enough. Without git we would be doomed. The project was rather small which meant that we would be editing the same files at the same time quite often. Luckily for us, git handles conflicts automagically in 99% of the time, even if the same file was edited by 3 different people. And even when there were merge conflicts they were trivial to solve. I used a merge tool called meld, which is pure awesome. I was actually looking forward to merge conflicts because they were really fun to resolve. It is weird how great tooling can create a scary process like resolving merge conflicts into a fun activity.

Our solution
------------

We quickly decided that drawing graphs is all well and good but it would not be enough. We came up with an idea that we could draw the actual car in 3D space and try to plot out road that it traveled. And we actually ended up doing just that.

We ended up winning the challenge probably because we were the only team that tried to do something more complex than draw graphs and because we really did put quite a lot of time into the project. We did however had the advantage of being the oldest team in the competition and I belive we were also the only team that had actual OpenGl experience from before.

We had a lot of fun developing the android application and we already have ideas how we could use the OpenGl part of the app and turn it into a driving game. We did not however receive the tablets yet as there is quite a bit of ugly bureaucracy that needs to get sorted out first. We look forward to more android projects in the feature.

By the way, if you have an android application that needs to get developed, send us an email. We love challenges!


