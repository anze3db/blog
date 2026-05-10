---
title: "Letting Claude Upgrade My Raspberry Pi"
date: 2026-05-10T19:00:00+01:00
series: ["Agentic Adventures"]
---

I have two Raspberry Pis at home. One hosts my various sites including [fedidevs.com](https://fedidevs.com/) and the other supports it by storing backups of all the configs and data. This includes a streaming hot standby of the Postgres database that powers some of my sites. I am not (yet) brave enough to run Claude on my primary Pi, but I decided to let it loose on my secondary.

Doing an in-place dist upgrade on a Raspberry Pi is [generally not recommended](https://www.raspberrypi.com/documentation/computers/os.html#upgrade). The official guidance is to do a clean install instead. Since it felt very likely that I'd be doing a clean install in any case to get from Bookworm (Debian 12) to Trixie (Debian 13), I figured this was the perfect opportunity to see if Claude could pull a miracle.

## The deal

I gave Claude a single instruction: do the dist-upgrade, but keep Postgres pinned on 15. Physical replication needs the same major version on both sides, and my primary is still on Bookworm and Postgres 15.

I had to do exactly two things during the whole upgrade:

- `sudo -v` once, so Claude had a non-prompting sudo session for the duration.
- `sudo reboot` at the end.

Everything else (the `apt full-upgrade`, the recovery passes, the package juggling) happened while I was enjoying my Sunday away from the computer.

## The t64 mess

Trixie ships the [64-bit `time_t` transition](https://wiki.debian.org/ReleaseGoals/64bit-time) so 32-bit architectures keep working past 2038. The visible side effect on a Pi is that *a lot* of libraries get renamed in one cycle: `libfoo` becomes `libfoot64`, sometimes with overlapping file ownership, sometimes with conflicting Replaces/Breaks between the new and old packages. apt's resolver doesn't always find a clean path through this on its own.

For my Raspberry Pi it took ten recovery passes. Claude was force-removing packages, reinstalling the Trixie versions afterwards, and using `dpkg -i --force-overwrite` in places where the package metadata still disagreed about who owned a given file (`lxpanel` over files from `lxplug-batt`, `pi-greeter` over files from `raspberrypi-ui-mods`). The list of things it had to remove during recovery includes `python3-rpi.gpio`, `python3-libgpiod`, `pcmanfm`, `lxhotkey-core`, and a handful of `python3-*` development packages.

I like the occasional Linux admin fiddling, but this went well beyond what I'd have had patience for. Claude, however, didn't get tired or frustrated and plowed through until there were no errors left.

## The reboot

I only skimmed through everything Claude did to get the full-upgrade through, and from what I saw I wasn't confident the OS would reboot cleanly.

To my surprise, the Raspberry Pi came back up on the new kernel. Postgres 15 was still pinned. The replication slot reconnected to the primary, `apt-get check` was clean, and `dpkg --audit` had nothing to say. Everything was running perfectly on Trixie.

One warning did show up, though:

```
WARNING: database "postgres" has a collation version mismatch
DETAIL:  The database was created using collation version 2.36,
         but the operating system provides version 2.41.
```

Trixie bumped glibc from 2.36 to 2.41. Postgres records the collation version per database (which on Linux comes from glibc), and if the sort order changes between glibc versions, existing B-tree indexes on `text`/`varchar` columns can disagree with how the new version orders those values.

Changes between 2.36 and 2.41 are small, so the realistic risk on mostly-ASCII data is low. Besides, I'm only using the replica for disaster recovery, so I decided to leave it as is. The warning will go away once I upgrade the primary Raspberry Pi to Trixie and reindex all the tables.

## Fin

I've done many system upgrades over the years and they are always a pain. On paper, this was probably one of the worst upgrades I've done. In practice, it felt like a breeze because I never had to look up any of the things that went wrong.

Yes, there is a chance the OS is in an inconsistent state and something might blow up at some point later. And yes, Claude could have even set up a backdoor, since I didn't verify all the commands that it ran. 🤷‍♂️

But the Raspberry Pi is working and doing its job on the new version. I'm not ready to unleash Claude on my primary Raspberry Pi with live production databases, but Claude and the rest of the LLM tooling are slowly gaining more and more of my trust.
