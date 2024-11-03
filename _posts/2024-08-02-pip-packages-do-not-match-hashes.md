---
title: "Packages do not match the hashes pip error"
description: "pip sometimes returns a checksum error when the urllib3 library is unable to parse a received TLS packet due to a network error. This pip issue will be resolved in 2025 when Python 3.9 is EOL, but you can get around it today by using wget or curl."
date: 2024-08-02 00:00:00 +0000
image: assets/cards/2024-08-02-pip-packages-do-not-match-hashes.png 
tags: python
---

Yesterday, I received a hashes mismatch error when trying to install the latest Django release candidate on my Raspberry Pi:

```
(.venv) home@raspberrypi:~/fedidevs $ pip install 'django==5.1rc1'
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting django==5.1rc1
  Downloading https://www.piwheels.org/simple/django/Django-5.1rc1-py3-none-any.whl (8.2 MB)
     ━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.5/8.2 MB 66.4 kB/s eta 0:01:26
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.
    django==5.1rc1 from https://www.piwheels.org/simple/django/Django-5.1rc1-py3-none-any.whl#sha256=c4757c4077938e63f9f54d781f77f5673f37469ee312b266d69dc79508ccfd3a:
        Expected sha256 c4757c4077938e63f9f54d781f77f5673f37469ee312b266d69dc79508ccfd3a
             Got        c20395a7e061523712f413ae17beafb5f2213faa172f960a9b1b158517b41eac
```

At first, I thought the problem was with [piwheels](https://www.piwheels.org/) because installing through PyPI didn't raise the same error, but this turned out to be a red herring. The real issue was a network error. I solved it by restarting the wifi on my Raspberry Pi. 🤷

The fact that `pip` was raising a checksum error felt weird, and I wanted to understand why so I dig into the problem.

## Vendored urllib3

It turns out that pip raising the wrong error is [a known issue](https://github.com/pypa/pip/issues/11153). The problem is that the vendored urllib3 version doesn't check if the downloaded content length matches the one specified in the `Content-Length` header. So if a network issue causes the stream to end prematurely, it won't raise an error, and pip will assume that the download completed successfully. The incompletely downloaded file will then fail the checksum test, so we see the checksum error as the result when this happens.

## Why not ugrade urllib3? 

Upgrading the bundled urllib3 would fix the issue. Version 2.0.0 of urllib3 checks the [content length by default](https://github.com/urllib3/urllib3/pull/2514). Unfortunately, the 2.x branch of urllib3 [requires OpenSSL 1.1.1+](https://github.com/urllib3/urllib3/issues/2168), which only became mandatory in Python 3.10 ([PEP 644](https://peps.python.org/pep-0644/)). `pip` has to support Python 3.9 until 2025 so the fix for this particular problem is blocked until then.

## Restarting the download on errors?

While getting a better error message would be an improvement, the proper solution is to retry the download. There is already [a pull request](https://github.com/pypa/pip/pull/11180) that adds this functionality, but it looks like the work on it stalled.

## A solution before 2025?

If you are trying to download a package over a poor connection, you can manually download the wheel file with a tool that automatically restart the download on failues (wget or curl) and then install it with pip:

```
wget https://www.piwheels.org/simple/django/Django-5.1rc1-py3-none-any.whl
pip install Django-5.1rc1-py3-none-any.whl 
```

Here is an example of me downloading the Django package with wget before I restarted the wifi. The download had to be retried three times!

```
Saving to: ‘Django-5.1rc1-py3-none-any.whl’

Django-5.1rc1-py3-none-any.whl         24%[=================>                                                        ]   1.94M  61.4KB/s    in 38s

2024-08-01 22:56:47 (52.9 KB/s) - Read error at byte 2031891/8201361 (Error decoding the received TLS packet.). Retrying.

--2024-08-01 22:56:48--  (try: 2)  https://www.piwheels.org/simple/django/Django-5.1rc1-py3-none-any.whl
Connecting to www.piwheels.org (www.piwheels.org)|46.235.225.189|:443... connected.
HTTP request sent, awaiting response... 206 Partial Content
Length: 8201361 (7.8M), 6169470 (5.9M) remaining
Saving to: ‘Django-5.1rc1-py3-none-any.whl’

Django-5.1rc1-py3-none-any.whl         61%[++++++++++++++++++==========================>                             ]   4.78M  74.5KB/s    in 45s

2024-08-01 22:57:34 (64.1 KB/s) - Read error at byte 5007723/8201361 (Error decoding the received TLS packet.). Retrying.

--2024-08-01 22:57:36--  (try: 3)  https://www.piwheels.org/simple/django/Django-5.1rc1-py3-none-any.whl
Connecting to www.piwheels.org (www.piwheels.org)|46.235.225.189|:443... connected.
HTTP request sent, awaiting response... 206 Partial Content
Length: 8201361 (7.8M), 3193638 (3.0M) remaining
Saving to: ‘Django-5.1rc1-py3-none-any.whl’

Django-5.1rc1-py3-none-any.whl         92%[+++++++++++++++++++++++++++++++++++++++++++++======================>      ]   7.22M  79.0KB/s    in 35s

2024-08-01 22:58:11 (72.3 KB/s) - Read error at byte 7567555/8201361 (Error decoding the received TLS packet.). Retrying.

--2024-08-01 22:58:14--  (try: 4)  https://www.piwheels.org/simple/django/Django-5.1rc1-py3-none-any.whl
Connecting to www.piwheels.org (www.piwheels.org)|46.235.225.189|:443... connected.
HTTP request sent, awaiting response... 206 Partial Content
Length: 8201361 (7.8M), 633806 (619K) remaining
Saving to: ‘Django-5.1rc1-py3-none-any.whl’

Django-5.1rc1-py3-none-any.whl        100%[++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=====>]   7.82M  35.9KB/s    in 13s

2024-08-01 22:58:27 (46.9 KB/s) - ‘Django-5.1rc1-py3-none-any.whl’ saved [8201361/8201361]
```
