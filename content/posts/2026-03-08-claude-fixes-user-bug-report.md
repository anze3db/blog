---
title: "Claude Fixes User Bug"
date: 2026-03-08
series: ["Agentic Adventures"]
---

I received this bug report in a toot from a Fedidevs user:

> Dear @fedidevs 
> 
> I think there is a bug with the starterpacks: When in "Add accounts" I search for an account that is already in the Pack, the tick-box can show empty. When I click it, it will switch to ticked, but the account is actually _removed_ from the pack. This is also confirmed by the number of accounts in the pack going down.

Yes, that definitely sounds like a bug. Let's see if Claude can figure out the root cause.

I used the user's toot as the prompt and after a few minutes of _clauding..._:

``````markdown
## Context

When searching for an account by username (e.g. `@user@instance.org`) in the "Add accounts" view, if that account is already in the starter pack, the checkbox incorrectly appears unchecked. Clicking it toggles to checked but actually **removes** the account from the pack (since the server-side toggle sees it already exists and deletes it).

## Root Cause

In [views.py:176-178](starter_packs/views.py#L176-L178), when a username search finds an account via `crawlone()`, the code creates a **new** queryset without the `in_starter_pack` annotation:

```python
accounts = Account.objects.filter(
    username_at_instance=account.username_at_instance,
)
```

This replaces the annotated queryset (lines 128-142) that has `in_starter_pack` and `is_followed`. Without the annotation, `account.in_starter_pack` is always falsy, so the checkbox renders unchecked.

The full-text search path (line 181) correctly uses `accounts.filter(...)` which preserves annotations. The username search path needs the same treatment.

## Fix

Change line 176-178 from:

```python
accounts = Account.objects.filter(
    username_at_instance=account.username_at_instance,
)
```

To:

```python
accounts = accounts.filter(
    username_at_instance=account.username_at_instance,
)
```

This single-word change (`Account.objects` → `accounts`) keeps the existing annotated queryset and just adds the filter, preserving `in_starter_pack` and `is_followed` annotations.
``````

It nailed it. If I were looking at this problem myself, I'd probably come to the exact same conclusion. I'm not sure I'd be faster though, so if this was a competition, Claude would have won.

Cool, but a bug isn't fixed until there's a test for it.

## Adding a test

> Please also add a test case for this bug

I instructed Claude to add a test for this exact case, and off it went again. _Executing..._

It wrote the test, ran it, and confirmed it passed. Everything looked good, so it happily reported that the job was done.

The test looked plausible, but I decided to verify it. I reverted the bug fix and ran the tests again. The newly added test should have failed, but it still passed.

Claude's test didn't exercise the code it had fixed!

> I have reverted the fix but the test is still passing

_Thinking..._

After thinking for a bit, it figured out it had forgotten to add a mock. A few moments later:

```
Right — crawlone makes a network call and returns None in tests, so the if account: branch on line 175 is never entered. The test needs to mock crawlone to return the account.
```

After a few more tokens, the test was fixed and working properly.

## Validation is going to be key

Claude writes code faster than we do. It uses tools, runs your tests, parses outputs, and fixes failures. But it's still a system that generates the next most probable token.

It can't actually know whether what it did is correct or expected. To it, [dropping your production database](https://alexeyondata.substack.com/p/how-i-dropped-our-production-database) or fixing a user-reported bug are the same. It's up to us to learn how to guide these tools so they don't generate garbage.

In this oneline bug fix, verifying was trivial. But when Claude writes thousands of lines of code and tests, it becomes a real challenge to review everything.

This is going to be the biggest challenge of vibe coding or agentic engineering, however you want to call it.
