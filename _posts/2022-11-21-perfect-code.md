---
layout: post
title: "Your Code Doesn't Have to be Perfect"
description: "An example of smelly code that served customers for over 6 years without issues before breaking."
date: 2022-11-21 7:00:00 +0000
tags: python django
# image: assets/pics/django32-query-perf.png
---

Let me tell you a little story about the following code snippet:

```python
template_id = request.GET["template_id"]
load_hub = False
try:
    templates = Template.objects.filter(
        company__hubs__tree_id=tree_id,
        is_public=1,
        deleted=0,
    ).exclude(company_id=company_id)
    for template in templates:
        if int(template_id) == template.id:
            load_hub = True
except:
    pass
```

This code was committed six years ago and was used until very recently by my client's largest customers.

# Code Smells

The first code smell is the bare except. Pylint has a [bare except warning](https://pylint.pycqa.org/en/latest/user_guide/messages/warning/bare-except.html) that warns you against these. They are dangerous because they might catch things the developer doesn't expect. If we had a typo, the bare except would swallow the error. This wasn't the case for us, but the bare except did make it much harder to detect the problem with this code.

The Django ORM query fetches the whole `Template` row data, even though we only accesses the ids. Even worse, the Python code is doing the filtering by id instead of letting the database do that. Super wasteful!

# The problem

Last week this code finally broke. A customer had too many `Template` objects and the query started to time out. Because of the bare try-except, we haven't received a Sentry error and we haven't noticed that the code was broken until the customer reached out 😢

When the query timed out the for loop didn't execute. The bare except block caught the time out exception, but didn't do anything with it. The code continued with `load_hub = False` even though it should have been `True` based on the data in the database. Later on a permission check failed and the users got an unexpected 404.

Luckily, it didn't take us long to debug and fix the issue. We rewrote the code into the following:

```python
template_id = request.GET["template_id"]
load_hub = (
    Template.objects.filter(
        id=template_id,
        company__hubs__tree_id=tree_id,
        is_public=True,
        deleted=False,
    )
    .exclude(company_id=company_id)
    .exists()
)
```

The new code removes the bare except. If the query times out again, we will be notified immediately. It is also much less likely to time out now because we filter the results by the id and only send back a single row.

# The lesson

Don't worry about code perfection. Bugs and poorly performing code are unavoidable and you can do much more damage with [premature optimization](https://wiki.c2.com/?PrematureOptimization).

The example code was far from ideal, but it didn't cause any problems for years. It was good enough and allowed the team to focus on adding value to the customers in other areas of the codebase.

Over the years the company grew to more than 100 employees. That would probably not be possible if the engineers were spending all their time fixing issues like this before they became actual problems.

Do make sure that you can deploy your fixes fast. If the customers have to wait six months for the fix, they will not be happy. 

Also make sure to apply this advice only on code that won't cause harm if it breaks. 🙏
