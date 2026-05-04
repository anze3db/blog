---
title: "Agents Day Lisbon"
date: 2026-05-04T19:38:17+01:00
---

Last week I attended the [Agents Day](https://www.agentsday.org/) Hackathon in Lisbon. It was a full day of talks, socializing, and building agents.

{{< gallery base="/assets/pics" >}}
agents-day1.jpg
agents-day2.jpg
agents-day5.jpg
agents-day7.jpg
{{< /gallery >}}

## Talks

There were a few talks and a round table discussion during the hackathon. The most memorable one for me was about the challenges behind Cloudflare's 16 MCP servers. 

All 2500+ Cloudflare endpoints couldn't fit into a single MCP server, since listing them all used up too many tokens. After a bit of back and forth they ended up with an architecture where the MCP only exposes two endpoints (search and execute), and the agents can figure out the rest.

## My Project

Since this was a hackathon I of course hacked on a project of my own - [Life Ops](https://github.com/anze3db/agents-day-life-ops), an agent that applies the lessons of Site Reliability Engineering to real life situations. Missing a birthday or an anniversary becomes a P1 incident, with alerts, postmortems, etc. It integrated perfectly with PagerDuty, who happened to be one of the sponsors.

## Demos

The project itself was a joke, but the demo I prepared resonated with the people I showed it to, including the mentors who ultimately decided who got to demo on stage. I think this was mostly because the demo wasn't just me showing how it works, but a little skit in which I figure out that I missed my partner's birthday and then have to handle the fallout.

Here's a recording I made as a backup plan in case the demo gods were not on my side:

<video style="width:100%; padding: 0 20px 20px 20px;" src="/assets/videos/agents-day-demo.mp4" muted autoplay loop controls playsinline></video>

As mentioned, only five teams were picked by the five mentors, and I was lucky enough to be one of them.

{{< gallery base="/assets/pics" >}}
agents-day10.jpg
agents-day4.jpg
{{< /gallery >}}

The other demos were:

1. Using agents to organize your second brain.
2. Agents for classifying and valuing wines.
3. Using agents to respond to and fulfill requests in a marketplace.
4. Using agents for voice calls.

All of them a lot more serious than mine 😅

## Fin

I had a fun time and I'll be keeping an eye out for more events like this. Lisbon seems to be the place for this sort of thing right now (there's even a [Cursor Cafe in Lisbon](https://x.com/edwinarbus/status/2044746961509650860)), and it's good to see a community forming around these new tools so that we can figure out how best to use (or not use) them together.
