---
title: "Agentic Adventures"
date: 2026-03-02T22:02:24Z
---

In my [last post](/advent-of-code-2025/#ai-) I mentioned that software engineering is going to be more and more AI driven and since then I've begrudgingly accepted this new reality. The era of handcrafted code is mostly coming to an end.

I say mostly because I still believe there will always be places in our future codebases that require manual intervention. Little surgical removals and additions around the parts where the LLMs get confused and start spinning their wheels without results.

But the vast majority of our code will now be AI generated, so we need to get very familiar with these tools asap, otherwise we'll get left in the dirt.

## First Adventure

That's why I'm starting my agentic adventures. I'm trying to use tools like Claude Code, Codex CLI, and others to get familiar with their capabilities, limits, and strengths.

My first adventure started when I wanted to write this blog post. I went to my Jekyll blog codebase and tried to start the development server only to get a `bundler` error saying that `jekyll` cannot be found. I don't use Ruby much, so trying to figure out how to fix this would easily take 15 minutes or more.

But since we now live in the world of agentic tools, I had another solution. I could ask Mr. Claude to migrate the whole blog to something that isn't Jekyll and doesn't require `bundler`.

After some back and forth on which static site builder to choose, where I briefly considered [Pelican](https://getpelican.com/), I decided on [Hugo](https://gohugo.io/). The decision essentially boiled down to OG image generation.

Claude made it seem like generating those images with Pelican would be painful, and since I'm familiar with Python's image stack I sort of agreed. On the other hand, Hugo had a built-in way to generate these without needing to install extra dependencies. Claude promised that it would be a breeze.

## Hugo It Is

Python is my go-to language (sorry for the Go pun), but even I had to admit that only having to worry about a single binary was alluring. Instead of dealing with `bundler` or `uv` and installing dependencies, I would now only need the single `hugo` binary. Bliss!

And so the agent went and did it. In about 10 minutes it essentially one-shotted the whole migration. Well, except for one thing...

## OG Images

It took me [13 years](/autogenerating-og-image-with-jekyll/) to get static image generation working with Jekyll, so I was very worried how Claude would handle them with Hugo.

To Claude's credit the og images were getting generated, they just looked like crap:

![OG image before improvements](/assets/pics/og-image-before.png)

Then I fell into a rabbit hole of trying to improve them. For the next 30 minutes I was trying to describe to the machine how the OG image should look.

Nothing really worked. Trying to write a detailed description was useless, showing OG images from the old site as well. In the end I had to get my hands dirty and write some of the code myself. I finally settled on:

![OG image after improvements](/assets/pics/og-image-after.png)

Emojis still don't work, but I don't put emojis in titles very often so that's fine.

## Fin

So this has been my general experience. Coding agents are amazing at getting you 90% there, but you'll still need to do some things manually from time to time or be very explicit with the prompt. At least until the next model versions are released 😅

I'm planning on sharing more experiences with this new era of AI-assisted programming. If you want to follow along, feel free to subscribe to the RSS feed or the newsletter below!

I wonder if I can get Claude to figure out how to send an email to the newsletter list after I publish a new post 🤔

