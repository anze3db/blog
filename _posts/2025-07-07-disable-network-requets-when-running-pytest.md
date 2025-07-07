---
layout: post
title: Disable network requests when running Pytest
date: 2025-07-07 00:35 +0100
tags: python
---
Even though my team has been diligent with mocking external requests, a few web requests still managed to slip through after a few months of cranking out new features. We only noticed them when our [tests started to fail](https://fosstodon.org/@anze3db/114783230227028153). 🫣

## The mocking problem

Usually, when you write a test for code that makes network requests, you mock your HTTP library of choice, either by using the built-in [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) module or using something like [pytest_httpx](https://colin-b.github.io/pytest_httpx/). 

But the problem with this approach is that it's easy to forget to add the mock. Especially if the network request is an insignificant side effect of the endpoint being tested, or if the HTTP request was added after the test had already been written.

That's precisely what happened to us!

## The socket-level solution

Because of this, I've added a simple Pytest fixture that raises an exception whenever a non-localhost socket connection is established:

```python
import socket

@pytest.fixture(autouse=True)
def block_external_requests(monkeypatch):
 original_getaddrinfo = socket.getaddrinfo

    def raise_on_external_request(*args, **kwargs):
        ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}
        if args[0] not in ALLOWED_HOSTS:
            raise Exception(f"External request detected: {args[0]}")
        return original_getaddrinfo(*args, **kwargs)

 monkeypatch.setattr(socket, "getaddrinfo", raise_on_external_request)
```

There are a hundred different ways to do this (let me know your preferred method!), but with this pytest fixture, I was able to track down all the unintended requests in our test suite, and it will hopefully prevent such requests in the future as well. 🤞

## Fin

May your tests run fast within your localhost! Happy testing.
