---
layout: post
title: "Integer Overflow Error in a Python Application"
description: "How we found and fixed an integer overflow error in our Django app."
date: 2022-07-02 7:00:00 +0000
image: /assets/pics/boring-sentry-error.png
---

A Sentry error popped up that looked very suspicious.

![Exception stack trace with KeyError -24212](/assets/pics/boring-sentry-error.png)

It piqued my interest for two reasons:

1. Customers were getting upset about it.
2. The value `-24212` was supposed to be a primary key and those tend to be greater than 0.

Something very fishy was going on, so I immediately went and checked if MySQL was to blame:

```sql
SELECT * FROM boring_table WHERE id < 0
```

No results. Can't blame MySQL for this one.

A wildly incorrect integer value can sometimes result from of an [Integer Overflow](https://en.wikipedia.org/wiki/Integer_overflow). Integer Overflow happens when the integer field does not have enough bits to store the value. Part of the bits gets clipped, producing a result that is very much unlike the value we were trying to store.

In Python, Integer Overflows aren't common. In fact, since [PEP-0237](https://peps.python.org/pep-0237/) landed in Python 2.2 they became impossible. Python's integers will continue increasing (or decreasing) without issues until they run out of system memory.

So the Sentry error made no sense, but thanks to my untrusting nature, I decided to walk through the codebase and see what we were doing with `boring_group_id`. A couple of functions up the stack, I found this code:

```python
return (
    pd.concat(
        [
            query_result["BORING_GROUP_ID"],
            query_result["PARENT_BORING_GROUP_ID"],
        ]
    )
    .dropna()
    .astype("int16")
    .unique()
)
```

Looks like those ids were going through a [pandas](https://pandas.pydata.org) dataframe where invalid values and duplicates were dropped. For some reason, we were also casting the values to 16-bit integers. Because of this, the function was returning incorrect values for any id greater than `32_767`. 

Changing the line to `.astype("int64")` resolved the issue and the problem will only pop up again when ids become greater than `9_223_372_036_854_775_807` at which point I *should* be long gone.

We pushed the fix to production and made the customers happy, or at least a little less upset. 🎉
