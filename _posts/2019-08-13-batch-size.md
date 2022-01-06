---
layout: post
title: "The Code Review Batch Size"
date: 2019-08-13 8:00:00 +0000
---

In the [last article](https://blog.codereview.chat/2019/07/15/the-code-review-bottleneck.html) we learned how important it is to reduce the friction in code reviews, by making code reviews your top priority. Based on the [theory of constraints](https://en.wikipedia.org/wiki/Theory_of_constraints), not working on the bottleneck is counterproductive. If your code review queue is backed up, writing more code will not make you deploy features any faster!

The theory of constraints doesn't only help us figure out what to focus on, but it also has a solution for increasing throughput: Decrease your batch size as much as possible. For us developers, the batch size is the number of code changes that go into each release.

If you are reviewing, testing, and deploying multiple thousands of line changes to save time and increase feature velocity the result you'll get might be the exact opposite. By batching so many changes and features together you increase the lead time for each change. Lead time is one of the four key software delivery metrics according to [Accelerate 2018](https://www.goodreads.com/en/book/show/35747076-accelerate) (other 3 are deployment frequency, time to restore service and change failure rate) and is closely correlated with company performance according to the studies conducted in [Accelerate 2018](https://www.goodreads.com/en/book/show/35747076-accelerate).

Putting it plainly, your big releases prevent small fixes and changes from going out sooner. Bigger releases require more testing, more preparation for deployment and it makes the process even slower. This is how you end up on a release schedule that can take months, is always late, and causes havoc when deployed to production in the form of blocker bugs.

Let's focus on the code review side of things and take a look at why big pull requests are never desired. 

# Problem with big pull requests

Developers have this joke that a 5 line pull request will have at least 5 comments or change requests while a 1000 line pull request will be accepted immediately with the words "looks good to me".

This is because to properly review those 1000 lines, the reviewer needs to invest a lot of their own time to fully understand the scope of the changes. Those 1000 lines could even be too much for any reviewer to fully comprehend since the number of things that a human brain can keep track of is limited to [about 7 items](https://phys.org/news/2009-11-brain-magic.html). Often the sheer size of the changes will, at the very least, demotivate the reviewer from doing a good job.

It's often the case that those 1000 lines or more don't change just one aspect of the system. They are usually a group of changes combined to form a whole. Grouping them might be an efficient way for the developer to implement these changes, but usually isn't an efficient way to review, test or deploy them.

Let's take a look at how big pull requests can be broken down into smaller ones that are easier to review, test, and deploy.

# Avoid batching features in a single pull request

We are often tempted to fix or complete multiple tasks while working on a particular part of the codebase and then combine all those changes in a single pull request. 

An example of this could be a pull request that fixes a production issue *and* improves logging around that issue.

When reviewing this pull request a potential problem with the code that adds the logging could delay the merge of the code that fixes a production issue. Your users will be stuck with the bug while you are fixing a logging issue that your users don't even know exists. 

When you write *and* in your PR title consider opening two pull requests instead. This will help the reviewer focus on one problem at the time, making it less likely for mistakes to go through.

This point is even more severe if the issue pops up only when the code is deployed. If there is an issue with the logging code, you might have to revert the bugfix as well to resolve the problem. Not a good place to be in.

# Small code batches

If you had been burnt by the issue above and then decided to vigilantly deploy only one feature at a time, you still occasionally run into issues. Features that are useful to your customers tend not to be just a change to a few lines of code. Instead, they require days or even weeks of work before they become useful.

Checking in code after weeks of work tends to be painful. You'll be working on a feature branch and will need to deal with merges and conflicts. And in the end, you'll have a big merge into your master branch, followed by the big deployment of what was probably months of work put into a feature branch.

The only solution to this is to decouple features from code changes.

# Decouple Features From Code Changes

The only way to address these issues is to avoid having long-running feature branches in the first place. Instead, all the changes should be reviewed and merged into your develop branch as soon as possible. This means deploying code that's not yet ready to be run on production and is therefore hidden from the word in a form of a feature flag.

LaunchDarkly raised $44 million this year helping programmers achieve exactly that, but in most cases, a simple `ENV` variable or a setting flag should be all you need to make sure the feature is not enabled until the last piece is merged and deployed.

The technique described above is called [Trunk Based Development](https://trunkbaseddevelopment.com/) and it tries to address some issues of the [GitFlow](https://datasift.github.io/gitflow/IntroducingGitFlow.html) development model. Most importantly it helps us reduce the batch size for code reviews and helping us speed up feature lead times.

It isn't perfect, of course. Now that you are merging things into master immediately after review, you might end up with dead code in your codebase when the priorities of the project shift. Even if this code is guarded by feature flags it can still pop up in unexpected ways and cause a production issue if there is a problem with your configuration, so you will need to spend some time every few sprints to clean it up.

Do you have a better way of dealing with big pull requests? Let's continue the discussion on Twitter!

<div style="margin-left: auto; margin-right: auto; width:500px;">
<blockquote class="twitter-tweet" data-conversation="none" data-dnt="true"><p lang="en" dir="ltr">Do you have a better way of dealing with big pull requests? Let me know!</p>&mdash; Anže Pečar (@Smotko) <a href="https://twitter.com/Smotko/status/1161220082707705857?ref_src=twsrc%5Etfw">August 13, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
</div>
