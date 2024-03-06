---
title: "Thoughts on Code Reviews"
description: "My thoughts on code reviews."
date: 2024-03-06 0:00:00 +0000
image: assets/cards/2024-03-06-code-reviews.png
---

I recently got asked about my opinion on code reviews. This was my answer.

> Code reviews are an essential part of the software development life cycle and are even required by regulations and standards like SOX, PCI DSS, etc. They are a great tool for the engineering team to improve the quality of the codebase, share knowledge, and confidently ship new features.

> But code reviews must be implemented with some care because they can lead to bickering around unimportant things, frustration, and poor velocity.

> The main ways to prevent these issues are to make sure your team prioritizes pull request reviews over other work (to shorten the feedback loop as much as possible), keep the PRs as small as possible, making them more manageable to review (feature flags help with this!), and automate as much of the review process as possible including checks and even autocorrections for formatting, lint, etc so that humans focus on more important things.

I've written longer posts on the topic ([here](/code-reviews-and-your-company-goal), [here](/the-code-review-bottleneck), and [here](/batch-size)).

The question reminded me of the time when I was trying to build a tool for helping make code reviews efficient. The tool never took off and I abandoned it after a year or so, but I still think that there is value in the idea. I might revisit it in the future.
