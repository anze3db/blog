---
title: "DjangoCon Europe 2026"
date: 2026-04-28T00:00:00+01:00
---

## Before the conference

My partner and I arrived in Athens a few days before the conference. It was a convenient excuse to visit a European capital we hadn't been to yet, and of course to eat as much delicious food as possible.

{{< gallery base="/assets/pics" >}}
athens-1.jpg
athens-2.jpg
athens-3.jpg
athens-4.jpg
athens-5.png
athens-6.png
athens-7.png
athens-8.png
{{< /gallery >}}

## Django Social

One day before the conference I went to the [django.social](https://www.linkedin.com/company/djangosocial/posts/?feedView=all) event organized by [Jon Gould](https://www.linkedin.com/in/jongould/) and [Andrew Miller](https://www.linkedin.com/in/akmiller89/).

The bar they initially picked got too crowded, so the group moved to the backup place. I came late to the first bar, found no one there, and was a bit lost until I made it to the right spot. Once I did, I felt immediately at home. I met old friends, made some new ones, and had a very fun evening. So fun, in fact, that I forgot to take any photos, so I have no social proof that I was there 😅


## Talks

The next day the conference started. Time to listen to some great talks and mingle with everyone during the breaks. I enjoyed pretty much all the talks and have pages of handwritten notes. A few of the most memorable ones:

* Static Islands, Dynamic Sea by Carlton
* AI-Assisted Contributions and Maintainer Load by Paolo
* Digitising Historical Caving Data with Python and Django by Andrew
* Body of knowledge by Daniele
* Auto-prefetching with model field fetch modes in Django 6.1 by Jacob
* Where did it all `BEGIN;`? by Charlie and Sam

{{< gallery base="/assets/pics" >}}
athens-9.jpeg
athens-10.jpeg
athens-11.jpeg
athens-12.jpeg
{{< /gallery >}}

## Lightning talks

Lightning talks are my favorite part of any conference and they didn't disappoint at DjangoCon.

{{< gallery base="/assets/pics" >}}
athens-13.jpeg
athens-14.jpeg
athens-15.png
{{< /gallery >}}


I also gave a lightning talk of my own on the last day. It was a shorter version of my talk from the Python Lisbon Meetup earlier this month on [how we sped up Django startup times with lazy imports](https://talks.pecar.me/2026-04-17-lazy-imports-djangoconeu.html).

## Sprints

For the sprints I decided to see if our work project ([Fencer](https://fencer.dev/)) works on the main branch of Django. There are many features I'm looking forward to, and I wanted to make sure we'll be in good shape when the final release lands.

### Regressions

Our test suite unearthed two regressions:

1. [#37047](https://code.djangoproject.com/ticket/37047) Crash in Query.orderby_issubset_groupby for descending and random order_by strings
2. [#37048](https://code.djangoproject.com/ticket/37048) Backwards incompatible change to InclusionAdminNode

The first one was fixed by changing the code to handle the edge cases of descending and random sorting. [My PR with the fix](https://github.com/django/django/pull/21121) was merged during the sprints thanks to Jacob!

The second ticket was initially resolved as wontfix since the regression was in an undocumented API. We did end up merging [a note about it to the changelog](https://github.com/django/django/pull/21135). I also got my [fix merged into django-unfold](https://github.com/unfoldadmin/django-unfold/pull/1983), which was what led me to the issue in the first place.

### Fetch modes

With the above issues fixed, our codebase ran smoothly on Django 6.1 and I was able to play around with the new [model field fetch modes](https://docs.djangoproject.com/en/dev/releases/6.1/#model-field-fetch-modes). From what I can tell, they work perfectly. I'll write a longer blog post about this closer to the release date, but it's great to see the number one reason for N+1 queries going away soon!

## Fin

As I am writing this I am feeling exhausted. As an introvert, all the conferencing drained my batteries. Time to retreat home and recharge until the next one (PyCon Portugal in September). Which reminds me: I need to submit my talk proposals. The deadline is April 30th AoE! [Here's the CFP](https://2026.pycon.pt/talks/cfp/).


![Image](/assets/pics/athens-16.jpg)

I'm terrible at taking selfies so I stole this one from [Paolo](https://www.paulox.net), I hope he doesn't mind! PS: he also wrote [his own writeup on DjangoCon 2026](https://www.paulox.net/2026/04/27/my-djangocon-europe-2026/). Be sure to check it out!
