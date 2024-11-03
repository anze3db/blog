---
layout: post
title: "The Fastest Way to Build a Read-only JSON API"
description: "A short story on how I managed to not overengineer a read-only JSON API."
date: 2023-01-16 1:00:00 +0000
tags: nginx
# image: assets/pics/django32-query-perf.png
---

This is a short story on how I managed to **not** overengineer a read-only JSON API. TLDR: Sometimes a static `.json` file served by nginx is the easiest and fastest way to create a read-only JSON API endpoint.

# The Problem

Last year I needed to build a simple JSON API endpoint for a mobile app that I was developing. The mobile app was a list view of webcams in my area. The final UI ended up looking like this:

![Screenshot of the Surfcams app showing nested lists of surfcams available in my area](/assets/pics/surfcams.jpeg)

Since I wanted to be able to change the contents and the look and feel of the list without reinstalling the mobile application<sup><a href="/faster-api#footnotes">[1]</a></sup> I needed a JSON API to serve the data to be displayed.

# JSON API

When I think about building a JSON API, I usually reach for Python with a framework like [Django](https://www.djangoproject.com/), [Flask](https://flask.palletsprojects.com/en/2.2.x/), or [FastAPI](https://fastapi.tiangolo.com/). Python then connects to a database ([PostgreSQL](https://www.postgresql.org/) or [SQLite](https://www.sqlite.org/index.html) most commonly) and responds to HTTP requests. But in this case, all of that seemed like overkill.

My API doesn't have to change the response often. When it does need to change, I am the only one changing it. A database isn't needed at all! ❌

I also don't need dynamic routing that the above-mentioned frameworks provide. There is only one endpoint! I don't really a web framework either! ❌

The response also doesn't include any dynamic elements that would need to be computed on every request. I had to begrudgingly accept the fact that I don't even need to use Python to solve this problem! ❌

# A Static JSON file

So the whole endpoint ended up being a static `cams.json` file hosted on [nginx](https://www.nginx.com/). Since I already had nginx running on my Raspberry Pi where the project is hosted, I only needed to add the `location /api/` path to my nginx site.conf:

```nginx
    location /api/ {
        root /home/pi/projects/cams;
    }
```

After that I added the following cams.json file into the `/home/pi/projects/cams` folder:

```json
{
    "categories": [
        {
            "title": "⭐️ Favorites",
            "color": "#ffd60a",
            "cams": [
                {
                    "title": "Carcavelos",
                    "subTitle": "Beachcam",
                    "url": "url1.m3u8",
                    "titleColor": "#ffffff",
                    "subTitleColor": "#999999",
                    "backgroundColor": "#363535"
                },
                {
                    "title": "Guincho",
                    "subTitle": "Beachcam",
                    "url": "url2.m3u8",
                    "titleColor": "#ffffff",
                    "subTitleColor": "#999999",
                    "backgroundColor": "#363535"
                },
                {
                    "title": "Costa de Caparica",
                    "subTitle": "Surfline",
                    "url": "url3.m3u8",
                    "titleColor": "#ffffff",
                    "subTitleColor": "#999999",
                    "backgroundColor": "#363535"
                }
            ]
         }
      ]
}
```

The *real* `cam.json` file is almost 1000 lines long, but you get the gist.

And that was it! Going to the `/api/cams.json` endpoint returns the JSON response so it looks and feels like a proper API endpoint. Nginx even correctly sets the `content-type: application/json` header.

The API endpoint has now been running for months and there were never any issues <sup><a href="/faster-api#footnotes">[2]</a></sup>. Fewer moving parts so fewer things go wrong.

# Fin

As engineers, we often like to overengineer our solutions, especially when working on side projects. Do remember to strive for simplicity. Static files scale really well, even when they are serving JSON!

<hr>

### Footnotes 

1. I used [Flutter](https://flutter.dev/) for the mobile application, source code [here](https://github.com/anze3db/surfcams).
1. I did have a week of downtime [that one time](https://twitter.com/anze3db/status/1548736490326343688) when my ISP changed my IP address while I was on vacation 😅. I was only able to get the new IP address once I returned home. I ended up solving this problem with some [Golang code](https://github.com/anze3db/ipster), but that's a whole separate blog post.
