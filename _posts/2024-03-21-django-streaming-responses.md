---
title: "Django Streaming HTTP Responses"
description: "How and when to use Streaming HTTP responses and when not to."
date: 2024-03-21 0:00:00 +0000
image: assets/cards/2024-03-21-django-streaming-responses.png
---

In this blog post, I'll explain how and when to use Django's [StreamingHttpResponse](https://docs.djangoproject.com/en/5.0/ref/request-response/#streaminghttpresponse-objects), what you can accomplish with it, and when it might not be a good idea. Let's start with the how.

# How to create a Streaming HTTP Response in Django

```python
import time

from django.http import StreamingHttpResponse


def streaming(_):
    def generate():
        for i in range(3):
            time.sleep(1)
            yield f"Chunk: {i}\n".encode()

    return StreamingHttpResponse(generate())

urls = [
    path("stream/", streaming),
]
```
If you are using Django 4.2 or later, you can use `async` iterators:

```python
import asyncio

from django.http import StreamingHttpResponse


def astreaming(_):
    async def stream():
        for i in range(3):
            await asyncio.sleep(1)
            yield f"Chunk: {i}\n".encode()

    return StreamingHttpResponse(stream())

urls = [
    path("astreaming/", astreaming),
]
```


That's it! The `stream` function is a generator that yields strings. Each chunk is sent to the client as soon as it's yielded. I've added the `time.sleep` so that we can see it working:

<video style="width:100%; padding: 20px 20px 20px 20px; border-radius: 34px; overflow: hidden;" src="/assets/videos/stream-simple.mp4" muted autoplay loop></video>

Django doesn't render an HTTP response itself. Instead, it follows the [WSGI](https://peps.python.org/pep-3333/) (or [ASGI](https://asgi.readthedocs.io/en/latest/specs/main.html)) spec. It's then up to your WSGI server to create the HTTP response. 

For example, Gunicorn receives Django's streaming HTTP response intent and creates an [HTTP/1.1 Chunked Response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Transfer-Encoding#chunked) from it. Gunicorn's response is then streamed to your browser. See [How Does Django's StreamingHttpResponse Work, Exactly?](https://andrewbrookins.com/django/how-does-djangos-streaminghttpresponse-work-exactly/) by Andrew for more details.

Even though chunked responses are not supported by HTTP/2, Nginx (and other modern proxy servers) have no issues converting the Chunked HTTP Response from Gunicorn to an HTTP/2 (or HTTP/3) equivalent, so even when your website is serving HTTP/2 requests, your response will still be streamed.

# When to use Streaming HTTP Response

A good use case for Streaming HTTP Responses is generating a large `CSV` file. If the file has several GBs of data, you could generate it on the fly, line by line, ensuring your view never exceeds a few KBs of memory.

Streaming HTTP Responses are also used to implement [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events). SSE is a one-way communication channel that can be a good fit for implementing notifications, live updates, etc. Check out [django-eventstream](https://github.com/fanout/django-eventstream) for a Django package that makes it easy to use SSE.

I've been playing around with creating a ChatGPT-like user interface with *zero* lines of JavaScript. While this isn't the best use case for streaming responses (see reasons below), it's a fun example and seems to work pretty well:

<video style="width:100%; padding: 20px 20px 20px 20px; border-radius: 34px; overflow: hidden;" src="/assets/videos/chatgpt-low.mp4" muted autoplay loop></video>

Sadly, I couldn't use Django's Templating system to get this example to work because Django's `Template.render` can't be streamed. There is a [Trac issue](https://code.djangoproject.com/ticket/31507) for this, and there was even [a PR](https://github.com/django/django/pull/4783) opened with the change implemented before work stalled. Since there was no activity in the last five years, is it not actually worth adding?

# Things to know about Streaming HTTP Response

Besides being unable to use Django's templating system, there are a few other things to remember when using Streaming HTTP Responses.

When using Streaming HTTP Responses, be aware that the connection is kept open while the response is generated. This can make your life miserable in several ways:

1. The thread/worker generating the response will be blocked until it's done streaming the response. If the response takes a long time (minutes or even longer), you need to provision many concurrent workers to make sure there are always workers available for new requests. Using async solves this problem, since an async worker can handle hundreds or thousands of concurrent requests.
2. Most systems assume requests resolve fast. Fly will kill your request in 60 seconds, while Heroku will kill it in 30 seconds. Even Gunicorn with a sync worker will kill the request after 30 seconds (or whatever your `--timeout` setting is) while the worker is streaming data! Increasing the timeout and ensuring you use gthread workers might be necessary to avoid this issue, but it might not always be possible. Also, increasing or disabling timeouts globally because of one or two streaming views is not the best idea.
3. Browsers only allow six simultaneous connections to a single domain. If you are trying to stream into multiple windows/tabs simultaneously, you might encounter this problem. This is resolved if you use http/2, which allows multiple streams in a single connection.
4. Some Django middlewares might not work as expected. The `GZipMiddleware`, for example, will buffer the entire response before compressing it.
5. Keeping the connection open for an extended period could be challenging. Your clients might disconnect, or your server might kill the connection because you are doing an upgrade. To solve this, you can look at Server-Sent Events that have a built-in reconnection mechanism. A proxy like [Pushpin](https://pushpin.org/) can also help reduce the complexity of your app.

Because of all of these potential issues, use StreamingHttpResponses only when you really have no other choice. Sticking to the traditional way of generating a response will help you keep out of truble.

# To finish up

I hope this post has helped you understand when and how to use Streaming HTTP Responses in Django. To finish up, I'll leave you with another example video of me creating a loader using a Streaming HTTP Response:

<video style="width:100%; padding: 20px 20px 20px 20px; border-radius: 34px; overflow: hidden;" src="/assets/videos/stream-loader.mp4" muted autoplay loop></video>
