---
title: "Django bulk_update Memory Issue"
date: 2025-10-12
slug: "django-bulk-update-memory-issue"
---

Recently, I had to write a Django migration to update hundreds of thousands of database objects.

## Loading the data

With some paper-napkin math I calculated that I can fit all the necessary data in memory, making the migration much simpler than it would have been otherwise. 

First I had to make sure to load only the necessary columns. Django's [`only` queryset method](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#only) came in very handy:

```python
objs_to_update = TheObject.objects.only("id", "field1", "field2", "field3").all()
```

Because I generally don't trust my paper-napkin math, I also made sure to log how much memory each of the steps were using:


```python
process = psutil.Process()
print(process.memory_info().rss // (1024 * 1024))
```

All the loaded objects were below 2GB, so everything seemed good since the machine had 4GB available.

## Updating the objects

With all the objects loaded in memory, it was now time to calculate the new values:

```python
for obj in obj_to_update:
    obj.field3 = compute_new_field3_value(obj)
```

I was also worried about memory during the update, but according to `process.memory_info()`, the memory hasn't increased past 2GB, so it looked like I was on the home stretch.

## Saving the results

Calling `obj.save(update_only="field3")` would have been one option, but it would have taken too long. Luckily, Django has a [bulk_update method](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#bulk-update):

```python
TheObject.objects.bulk_update(objs=objs_to_update, fields=["field3"])
```

Running this statement as is would have generated a HUGE update statement that my database would not have enjoyed seeing. But luckily, `bulk_update` has a `batch_size` parameter that chunks the huge update into multiple smaller ones:

```python
TheObject.objects.bulk_update(objs=objs_to_update, fields=["field3"], batch_size=250)
```

Unfortunately for me, the way `bulk_update` works wasn't what I expected, and it killed my migration with a `SIGTERM` when I ran it in production. ☠️

## Investigating `bulk_update`

Django first prepares a [list of all update clauses](https://github.com/django/django/blob/main/django/db/models/query.py#L937-L956), then creates the transaction, and finally executes the updates one by one in a loop.

I measured memory consumption from within `bulk_update`. After the for loop the memory increased to 4.8GB. The `updates` list ended up taking an extra 2.8GB. That's more than all the data I loaded from the database. 800MB more than I had available on the machine, which explained the `SIGTERM`.

## The solution

The solution for this was to implement my own batching and not using Django's `batch_size`:

```python
with transaction.atomic():
    for batch in batched(things, 250):
        TheObject.objects.bulk_update(objs=objs_to_update, fields=["field3"])
```
This makes sure that we only ever have a maximum 250 update statements in memory at a time. I did some measurements again, and only 62MB of additional memory was used during all of this. With this change, my migration finished successfully! 🎉

## Reporting the issue to Django

I reported this issue on the Django issue tracker: [#36526 bulk_update uses more memory than expected](https://code.djangoproject.com/ticket/36526). The ticket received a patch with a solution [in a few hours](https://github.com/django/django/pull/19677/files), but unfortunately, the solution got rejected. 

There was concern that preparing the update statements within the transaction would prolong it in typical cases and cause all sorts of unintended problems associated with long-running transactions. There is a separate ticket about the performance of [building the update statement](https://code.djangoproject.com/ticket/31202).

A safer solution was to document the memory usage, which was what ended up being the solution that closed my ticket. `batch_update` now has the following warning:

> When updating a large number of objects, be aware that bulk_update() prepares all of the WHEN clauses for every object across all batches before executing any queries. This can require more memory than expected.

## Fin

To me personally the memory leak caused more pain than longer-running transactions ever would, but I understand there are Django projects where the fix would cause issues. There might even be someone out there who relies on extra memory usage to generate more heat for their [workflow](https://xkcd.com/1172/).
