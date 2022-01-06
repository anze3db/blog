---
layout: post
title: "The Code Review Bottleneck"
date: 2019-07-15 8:00:00 +0000
---

Code reviews are [insanely useful](https://blog.codereview.chat/2019/06/27/code-reviews-and-your-company-goal.html). The only problem is that they have the nasty habit of making your cool new feature stuck in the queue waiting for reviewers. Let's take a look at how to make sure code reviews are done as efficiently as possible. Let's see how we can do quality code reviews without impeding feature velocity.

# The Bottleneck

Code reviews are by their nature a bottleneck. They slow down the flow of features on their way to production. In this sense, they work against your goal to ship quality features to your customers as fast as possible. But because code reviews help your team ship fewer bugs and higher quality features they are worth the downside.

The faster you can ship new features the better your company can adjust to new market trends and resolve user issues. Teams that can deliver in weeks outperform teams that deliver in months or even years.

If your pull requests are pilling up and staying open for weeks it might be a sign that your process could use some improvement.

# The Wait Time

The biggest issue with code reviews is the wait time.

When the author of the code opens a pull request and marks it ready for review, they need to **wait** until another person comes along and reviews it. This could be 1 hour after the pull request has been opened (if you are lucky) or it might take a few days or even weeks (if you are not lucky).

After the first review is posted there is almost always a bit of wait time again, before the author sees the review, and then even more if the author needs to adjust the code based on the feedback.

This process can go on for multiple cycles and every handoff adds another bit of wait time. This is how a simple feature that was ready 2 weeks ago still hasn't shipped yet.

The wait time is especially painful for us programmers because, after each wait time, the context is lost and needs to be rebuilt again. The longer the wait time the more difficult it is to remember how all the code changes fit together into the shippable feature.

# The Solution

There is only one way to resolve the wait time issue. It is to try to minimize it as much as possible. The best way to accomplish this is to make code reviews **the top priority** for your team.

When a pull request is ready for review, the reviewers should drop everything and focus on getting it reviewed and merged ASAP. The wait time between handoffs should be measured in minutes and not hours or days.

When a pull request is reviewed and needs updates, the author should drop everything and focus on responding to comments. Again trying to limit the wait time to minutes and not hours if possible. If the review requires a substantial amount of code changes you should discuss it with reviewers to make sure changes will bring business value to customers.

The "drop everything because of code reviews" rule is counter-intuitive for us developers. We like to be in the flow and don't want to break out of it for whatever reason. This is how we feel productive. Code reviews don't make us feel productive because we will not be credited when the feature ships. Usually, it's the author that will take all the credit.

If you follow the rule of code reviews being the top priority your personal productivity will take a hit.

# But the productivity of your team will soar

Your personal productivity is not even remotely as important as the productivity of your team. Your team is most productive when it's shipping features to users. When a feature is ready for code review the developer is saying it's ready to be deployed to production. Your team's most important goal at this point needs to be to make sure the code is shippable.

Anything other than doing the code review is counterproductive for your team. If you spend the rest of the day working on your feature instead of reviewing a pull request, you're blocking a feature from being deployed. Even worse, you are creating a new bottleneck and creating more work in progress which will cause even more context switching down the line.

This is how pull requests pile up and feature velocity plummets.

It's absolutely crucial to make the code reviews the top priority. When a code review comes in you need to stop all other nonproductive activity. This is pretty much anything except maybe firefighting a production issue affecting your customers.

You will be my hero if you say that the current meeting needs to end earlier because you need to go review a newly opened pull request. 🤙

In the next blog post, we'll take a look at some techniques you can use to make it possible to review and merge pull requests as quickly as possible. Spoiler: it's all about reducing the batch size!

Discuss this post on [hacker news](https://news.ycombinator.com/item?id=20438954).
