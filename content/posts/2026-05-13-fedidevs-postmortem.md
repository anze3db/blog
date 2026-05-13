---
title: "Postmortem: a 9-hour Pi outage"
date: 2026-05-13T09:54:55+01:00
---

Today I had almost 9 hours of downtime on [fedidevs.com](https://fedidevs.com) and some of my other sites that I run on a Raspberry Pi at home. The alert came in just as I was heading to bed and I didn't see it until I woke up this morning 🫣

![Fedidevs postmortem](/assets/pics/fedidevs-postmortem.png)

Since [Jake on Mastodon](https://fosstodon.org/@jake@theorangeone.net/116566388806900818) asked for a Cloudflare-style postmortem, here it is:

## Incident report: ~9h loss of upstream connectivity on the `raspberrypi` host

**Date:** 2026-05-12 / 2026-05-13

**Duration:** 8h 53m

**Impact window:** 2026-05-12 23:00 UTC → 2026-05-13 07:53 UTC

**Severity:** SEV-3 (single-host, no public traffic served during the window because outbound DNS was the failure mode)

We'd like to acknowledge the disruption this caused — for everyone who depends on a Raspberry Pi in a flat in Lisbon, this was an unacceptable outage. We are sorry, and we are taking steps to make sure this does not recur in the same form.

### What happened

At **23:00:09 UTC** on 2026-05-12 (00:00 local time), the `raspberrypi` host lost the ability to send packets beyond its default gateway (`192.168.86.1`). DNS queries against the gateway began timing out immediately. The WiFi radio remained associated to the access point throughout the entire incident — `cfg80211` reported no deauthentication, reassociation, or carrier-loss events. From the kernel's perspective, the link was healthy. From every userspace service's perspective, the internet had ceased to exist.

The host stayed in this state for **8 hours and 53 minutes**, until a human operator (a single human, who was asleep) walked over and pulled power at **07:53 UTC**.

### Background

The `raspberrypi` host is a Raspberry Pi 5 (Debian Bookworm, kernel 6.12.34) connected over WiFi to a home router. It runs a small fleet of services, including:

- A `gunicorn`-served applications (`fedidevs` and others), with a Celery worker.
- PostgreSQL 15, Redis, nginx.
- A New Relic infrastructure agent for observability.

The previous boot had been running for **349 days** continuously. We mention this because it is relevant to the size of the gap between "we have monitoring" and "we have monitoring that would have noticed."

### Timeline (UTC)

| Time | Event |
|---|---|
| `2026-05-12 23:00:09` | First DNS timeout observed: `ipster` fails to resolve `api.cloudflare.com` against `192.168.86.1:53` (i/o timeout). |
| `2026-05-12 23:00:09 → 07:53:00` | Continuous, identical failure mode across every service that initiates outbound traffic. New Relic accumulates a 530,000+ event backlog. Gunicorn's OTLP exporter queues ~129 retries. WiFi stays associated. |
| `2026-05-13 07:53:00` | Operator initiates hard reboot. |
| `2026-05-13 07:53:50` | Host comes back up. Connectivity restored on first attempt. |
| `2026-05-13 08:42:00` | Operator opens a session and asks the on-call AI what to do about it. |
| `2026-05-13 08:48:43` | Recovery automation (`net-watchdog.timer`) deployed and enabled. |

### Root cause

We cannot prove the upstream trigger from the host's logs alone — the journal volume from the affected window contains no kernel WiFi events — but the signature is consistent and well-known. At exactly **00:00 local time**, the gateway almost certainly performed a scheduled action (reboot, firmware update, or DHCP lease housekeeping). When it returned to service, the Pi's WiFi stack remained associated to the BSSID at the radio layer but did not re-establish a working data path. `NetworkManager` did not observe a carrier event and therefore had no signal to act on. The connection's `connectivity` check ran in the background and may well have flipped to `limited`, but no action is taken on that signal by default.

In short: the link was up, the route was installed, the radio was happy, and no packets came back.

### Detection

There was none. The incident was detected by a human noticing the next morning that pages did not load. There was no alert, no automated check, and no log-based watchdog that would have escalated.

### Remediation

We have shipped a connectivity watchdog (`net-watchdog`, on a 2-minute systemd timer) that performs an active reachability check against three upstream anycast addresses (`1.1.1.1`, `8.8.8.8`, `9.9.9.9`) bound to `wlan0`. On consecutive failures it executes an escalation ladder:

1. Observe (one failure can be a packet drop).
2. `nmcli device reapply wlan0`.
3. `nmcli device disconnect && connect wlan0`.
4. Restart NetworkManager.
5. Bounce the `wlan0` interface at the link layer.
6. Reboot, as a last resort, after ~24 minutes of confirmed unreachability.

All actions log to the journal under the `net-watchdog` tag.

Worst-case time-to-recover under this design is **~24 minutes**, down from "however long until a human notices." We consider this acceptable for the operating environment (a home server, one human, no SLA), but it is not zero, and we will continue to look for ways to reduce it.

### What we're still not doing

- We are not yet alerting off-host when the watchdog escalates. If the recovery itself fails (e.g., the WiFi driver is wedged at the kernel level and an `ip link` bounce doesn't help), the only signal will be that the host stops responding entirely — which is, again, "human notices the next morning."
- We have not addressed the upstream cause. The router presumably will do whatever it did again. The Pi must remain resilient to it.
- We have no second physical link (no ethernet). The watchdog cannot route around a failed radio.

We do not, at this time, plan a global incident review.

— The Raspberry Pi reliability team (n=1, including the AI)
