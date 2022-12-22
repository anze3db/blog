---
layout: post
title: "Python 3.11 Enum Breaking Change"
description: "A story on how Enum classes were broken before Python 3.11."
date: 2022-12-21 1:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

Python 3.11 was released almost two months ago and brought [some great improvements to the Enum class](https://docs.python.org/3/whatsnew/3.11.html#enum). Unfortunately, there is also a breaking change and you might be impacted if you are using Enum classes with a `str`/`int` mixin:

```python
from enum import Enum


class Foo(str, Enum):
    BAR = "bar"
```

`Foo.BAR` in Python 3.11 will no longer return the member value `"bar"` when using `format()` or f-strings the way that prior Python versions used to. Instead, it will return the `Foo.BAR` member class. If you are using `Foo.BAR == "bar"` or `f"{Foo.BAR}"` your code will very likely break when you migrate to 3.11. The easiest way to fix it is to replace the `str` mixin with the newly added `StrEnum` class:

```python
from enum import StrEnum

class Foo(StrEnum):
    BAR = "bar"
```

Let's take one step back and take a look at Enum classes and why my project ended up having more than 50 of them with the `str` mixin.

# Enum

Enum classes were introduced in Python 3.4 with [PEP-435](https://peps.python.org/pep-0435/) to help developers define symbolic names for constant values. This is useful because having `Foo.BAR` is much more readable than having the `"bar"` constant spread across the codebase.

Enum classes do have some surprising behaviors. Let's look at the example:

```python
class Foo(Enum):
    BAR = "bar"
```

If you try to use the BAR value in the code like this:

```python
assert Foo.BAR == "bar"
```

You will receive an assertion error! This is because `Foo.BAR` is not a `str` instance as it might seem from the class definition. To get to the `str` value you'd need to write:

```python
assert Foo.BAR.value == "bar"
```

But knowing when to use `.value` is inconvenient. Engineers will try to find a workaround. On the project that I work on the workaround was to add a `str` mixin:

```python
class Foo(str, Enum):
    BAR = "bar"
```

This makes it seem like the problem is solved since `assert Foo.BAR == "bar"` no longer raises an error (in Python 3.10 or older versions), but... 

# There be dragons!

This only works for f-strings and format functions. The old `%` based str formatting syntax will still be broken. The `str` function will also not return `"bar"`. More examples in Python 3.10:


```python
print(Foo.BAR)                 # > Foo.BAR
print(str(Foo.BAR))            # > Foo.BAR
print("%s" % Foo.BAR)          # > Foo.BAR
print(f"{Foo.BAR}")            # > bar
print("{}".format(Foo.BAR))    # > bar
```

This inconsistency was what was fixed in Python 3.11 and the output is now the same everywhere:

```python
print(Foo.BAR)                 # > Foo.BAR
print(str(Foo.BAR))            # > Foo.BAR
print("%s" % Foo.BAR)          # > Foo.BAR
print(f"{Foo.BAR}")            # > Foo.BAR
print("{}".format(Foo.BAR))    # > Foo.BAR
```

Consistency is always good! But this fix was what broke our code.

We were expecting `"bar"` but were now getting `Foo.BAR`! So now we are back on square one. In the cases above `Foo(str, Enum)` behaves the same as `Foo(Enum)` So how can we avoid writing `.value` everywhere?

# StrEnum to the rescue

Luckily, there is a solution for this in Python 3.11. The newly added [StrEnum](https://docs.python.org/3/library/enum.html#enum.StrEnum) class! Now we can write:

```python
from enum import StrEnum

class Foo(StrEnum):
    BAR = "bar"
```

And the results are going to be exactly what we originally wanted with the `str` mixin, except that it's going to work consistenlty for all cases that I could come up with:

```python
print(Foo.BAR)                 # > bar
print(str(Foo.BAR))            # > bar
print("%s" % Foo.BAR)          # > bar
print(f"{Foo.BAR}")            # > bar
print("{}".format(Foo.BAR))    # > bar
```

# Python 3.10 or older

If you want to stop using the `str` mixin and aren't quite ready to upgrade to Python 3.11 yet, I suggest you check out the [`StrEnum` PyPi package](https://pypi.org/project/StrEnum/). For the examples above, it behaves the same as Python 3.11, you just need to import `StrEnum` from `strenum` instead of `enum`.

```python
from strenum import StrEnum

class Foo(StrEnum):
    BAR = "bar"
```

You can keep using the StrEnum package even after you upgrade to Python 3.11, it even has some extra features that the standard library `StrEnum` version doesn't have.

# Python 3.11 what's new page

The [Python 3.11 what's new page](https://docs.python.org/3/whatsnew/3.11.html#enum) seems to have a small mistake in the changelog that describes this change:

> Changed Enum.__format__() (the default for format(), str.format() and f-strings) of enums with mixed-in types (e.g. int, str) to also include the class name in the output, not just the member’s key. This matches the existing behavior of enum.Enum.__str__(), returning e.g. 'AnEnum.MEMBER' for an enum AnEnum(str, Enum) instead of just 'MEMBER'.

Unless I'm misunderstanding something, the documentation should state that the format function and f-strings were returning the MEMBER **value** and not just the MEMBER without the class. I've opened a [PR in the CPython project](https://github.com/python/cpython/pull/100387) to see if we can clear this up a little bit.

# Fin

I was avoiding the use of `Enum`s because of the gotchas outlined in this post, but I do like how the new `StrEnum` (and `IntEnum`) classes work and I think I'll be using them a lot more going forward 🎉
