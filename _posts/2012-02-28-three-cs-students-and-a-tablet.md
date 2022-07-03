---
layout: post
title: "Three CS students and a tablet"
category: 
tags: [android, programming, fun]
---


A few weeks ago ComTrade - a local tech company decided to sponsor a challenge event in association with our faculty. The idea was that three teams, each with three students, would work on a fun little project - building an android application that visualizes data received from a remote controlled car. Because the application was meant to run on a Samsung Galaxy Tab 10.1 me and a few of my friends got excited and we signed up for the challenge immediately. 

The rules of the game
---------------------

Each team received a tablet to develop their solution. We were told that the winning team would get to keep all three tablets so we were really motivated to create the best possible application. We did not have a lot of time to do this though. The time constraint was about three weeks and we were in the middle of the exam period when the challenge started.

The application would be receiving data via bluetooth. The remote controlled car was sending data from its G-force sensor, its wheel turn value and its revs count. It was up to us to come up with cool and interesting ways to visualize this data.

Our solution
------------

![Tablet screenshot](/assets/pics/three-student-one-tablet-2.png)

We quickly decided that drawing graphs is all well and good but it would not be enough. So we came up with an idea to draw the actual car in 3D space. The car would move on a virtual road that it plotted as it went. Our final solution actually worked rather well although we would have to do some more calibration with the actual car, if we wanted the path in our simulation to match the path that the car actually made. One can't believe what a difference turning radius can have on the path.

We ended up doing a lot of different graphs as well as many dials and counters, for the more techy people out there. We were drawing all of these in canvas which turned out to be a bad decision as it created quite a few performance issues. We managed to find workarounds but decided that our next app would be OpenGl only. OpenGl ES2.0 if we get a say in it!

The most difficult part of the whole thing was creating a design that looked good. Up until a few hours to the deadline our application looked horrible, but then thankfully [@zidarsk8](https://twitter.com/#!/zidarsk8) opened up gimp and made the application look awesome.

There were a lot of things that we could still improve, but the final application somehow managed to impress the judges and we ended up winning the challenge!

The development process
-------------------

![Tablet screenshot](/assets/pics/three-student-one-tablet-1.png)

We had one tablet but there were three of us. This of course meant that at any given time, two team mates would be forced to use the emulator. Now the thing with the android emulator is that it doesn't really work if you are trying to do something a bit more complex. We all had android phones though so we decided to split the main application into multiple parts. We created a library project that did most of the hard work, and two applications one for the tablet and on really basic for the phone. This allowed me to work on the OpenGl part of the application even if somebody else got the tablet for the night.

We have also learned fast that it is way more difficult to work efficiently in a team, than it is to work alone. It is really hard to focus on the task at hand, when you have two other people sitting beside you, disturbing you with the problems that they are facing while developing their own part of the application. But thankfully we soon got used to it and got more productive. We still feel that there is a lot of room for improvements, we just need more projects like this tune our group programming skills.

How git saved our lives
-------------------

I cannot stress this enough. Without git we would be doomed. The project was rather small which meant that we were editing the same files at the same time quite often. Luckily for us, git handles conflicts automagically 99% of the time, even if the same file was edited by 3 different people. And even when we got merge conflicts they were all trivial to resolve. I used a merge tool called meld, which is awesome and made it really easy to see what code goes where. I ended up looking forward to merge conflicts because they were actually fun to resolve. It is weird how great tooling can create a scary process into a fun activity.

The good and the bad
--------------------

We had fun and we learned a lot. We even got used to working in a group! But there were some downsides too. There were quite a few sleepless nights as we tried to balance exams, the project and our social lives ([@majcnM](https://twitter.com/#!/majcnm) actually had two hours of social life). And even though the whole thing is over, we didn't receive the tablets yet. This is because ComTrade took "our" tablets to the Embedded World to show off the applications at their booth. This, of course, means that we will have to wait two weeks or more to actually get them. And by then the new and shinny tablets will be touched by a million people, which is not a pleasant thought as well.

To conclude
----------

We had a lot of fun developing the android application and we already have ideas how we could use the OpenGl part and turn it into a driving game. We look forward to more android projects in the feature. By the way, if you have an android application that needs to get developed, send us an [email](mailto:smotko@smotko.si). We love challenges!

PS: To see the code and more screenshots check out our repository: <https://github.com/zidarsk8/galaxyCar>
