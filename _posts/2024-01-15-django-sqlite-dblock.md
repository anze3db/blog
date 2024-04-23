---
title: "Django, SQLite, and the Database is Locked Error"
description: "Explains `database is locked` errors in Django when using SQLite, and how to solve them."
date: 2024-01-16 0:00:00 +0000
image: /assets/cards/2024-01-16-django-sqlite-dblock.png
---

SQLite is gaining traction as a viable option for web applications in production environments. Unfortunately, Django developers wanting to use SQLite in production need to be aware of the `database is locked` error. This blog post explains the two causes for this error and shows how to solve them.

# The Database is Locked Error

When running SQLite in production with at least two workers (threads or processes), you are bound to run into `django.db.utils.OperationalError: database is locked` exception.

<details>
<summary>Click here to a full stack trace example</summary>
<pre><code>
Internal Server Error: /read_write_transaction/
Traceback (most recent call last):
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py", line 328, in execute
    return super().execute(query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: database is locked

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/core/handlers/exception.py", line 55, in inner
    response = get_response(request)
               ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/core/handlers/base.py", line 197, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/.pyenv/versions/3.12.0/lib/python3.12/contextlib.py", line 81, in inner
    return func(*args, **kwds)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/djangosqlite/urls.py", line 64, in read_write_transaction
    write_to_db()
  File "/Users/anze/Coding/djangosqlite/djangosqlite/urls.py", line 25, in write_to_db
    A.objects.create()
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/query.py", line 677, in create
    obj.save(force_insert=True, using=self.db)
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/base.py", line 822, in save
    self.save_base(
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/base.py", line 909, in save_base
    updated = self._save_table(
              ^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/base.py", line 1067, in _save_table
    results = self._do_insert(
              ^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/base.py", line 1108, in _do_insert
    return manager._insert(
           ^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/query.py", line 1845, in _insert
    return query.get_compiler(using=using).execute_sql(returning_fields)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/models/sql/compiler.py", line 1823, in execute_sql
    cursor.execute(sql, params)
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/utils.py", line 122, in execute
    return super().execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/utils.py", line 79, in execute
    return self._execute_with_wrappers(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/utils.py", line 92, in _execute_with_wrappers
    return executor(sql, params, many, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/utils.py", line 100, in _execute
    with self.db.wrap_database_errors:
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/utils.py", line 105, in _execute
    return self.cursor.execute(sql, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/anze/Coding/djangosqlite/.venv/lib/python3.12/site-packages/django/db/backends/sqlite3/base.py", line 328, in execute
    return super().execute(query, params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.OperationalError: database is locked
</code></pre>
</details>

## Cause 0: Writes blocking reads

The default SQLite settings are optimized for embedded systems and not for server workloads where you usually have multiple threads doing reads and writes. By default, any write operation will block all reads. You can fix this by enabling Write-Ahead Logging (WAL):

```
sqlite3 db.sqlite3 'PRAGMA journal_mode=WAL;'
```

With WAL enabled, writes will no longer block reads, and you should see an increase in throughput if your application is read-heavy. I have a whole blog post dedicated [to this topic](/sqlite-wal) if you'd like to know more.

## Cause 1: SQLite timed out waiting for the lock

This error is raised because only one process or thread can write to a SQLite database at a time. When a thread or process needs to write to the database, it has to acquire a database lock. If another thread or process already holds the lock, SQLite will wait for the lock to be released, retrying with exponential backoff for as long as your `timeout` value (5 seconds by default). It raises the `database is locked` error if it cannot require the lock in time.

This is well documented in [Django's documentation](https://docs.djangoproject.com/en/5.0/ref/databases/#database-is-locked-errors).

### Solutions

Django also gives three ways to solve the problem:

> Switching to another database backend.

😢

> Rewriting your code to reduce concurrency and ensure that database transactions are short-lived.

You can accomplish this by optimizing your tables (reducing the number of data written, removing unnecessary indexes, etc.), reducing the amount of work in a single transaction, or upgrading to a faster hard drive option if available.

> Increase the default timeout value by setting the timeout database option:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 20,  # 5 seconds is the default, but we can increase it to, e.g., 20s
        },
    }
}
```
> This will make SQLite wait a bit longer before throwing “database is locked” errors; it won’t really do anything to solve them.

A 5-second wait should give you at least several hundred write requests per second (depending on the structure of the data and underlying hardware), but you can always increase the timeout if you need to.

## Cause 2: Writes after reads in transactions

Sometimes, however, you will see the `database is locked` exception on requests that finished in less than 5 seconds (or whatever your `timeout` was set to).

To show how this can happen, I've created a [GitHub repository](https://github.com/anze3db/django-sqlite-dblock) with steps to reproduce. I used [locust](https://locust.io) to simulate simultaneous requests to reproduce the problem reliably. Results:

```
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /read_write_transaction/                                                         704  199(28.27%) |     18       2     123      5 |   73.00       20.64
```

We can see that the maximum request time during this test was 123 ms, way below the 5-second limit, but we still had a 28.27% failure rate! All those exceptions were `database is locked` errors.

I was baffled by this problem when I first saw it and couldn't figure out the cause until Stephen linked his [blog post](https://fractaledmind.github.io/2023/12/11/sqlite-on-rails-improving-concurrency/) about how he solved it in Rails. Here is the relevant part:

> The issue is that when SQLite attempts to acquire a lock in the middle of a transaction and there is another connection with a lock, SQLite cannot retry the transaction. Retrying in the middle of a transaction could break the serializable isolation that SQLite guarantees. Thus, when SQLite hits a busy exception when trying to upgrade a transaction, it **doesn’t fallback to the busy_handler, it immediately throws the error and halts that transaction**.

Let's look at the view in my example and see what's going on step by step:

```python
@transaction.atomic()  # Start a deferred transaction; no db lock yet
def read_write_transaction(_):
    read_from_db()  # Read from the db here; no lock yet
    write_to_db()  # Try to acquire a lock in the middle of the transaction, but if the db is already locked, SQLite cannot retry because that might break the serializable isolation guarantees.
    return HttpResponse("OK")
```

### Solutions

To solve this problem we need to make SQLite acquire a lock before making any reads. Switching the order of the read and write queries is one option, although not a very practical one:

```python
@transaction.atomic()  # Start a deferred transaction, no lock yet
def write_read_transaction(_):
    write_to_db()  # Try to acquire a lock; if the db is already locked, SQLite will retry. There were no read queries in this transaction, so there is no way to break serializable isolation guarantees.
    read_from_db()  # Read from the db here; the db is already locked
    return HttpResponse("OK")
```

Instead of using the default deferred transaction mode, we can use the [IMMEDIATE transaction mode](https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions).

In Django 5.1 and newer we will be able to set the `IMMEDIATE` transaction mode in the database options:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",  # <-- Set the transaction mode to IMMEDIATE
        },
    }
}
```

Django versions before 5.1 do not support setting the transaction mode out of the box, but we can accomplish this manually like this:

```python
# <-- Note that we are no longer using the @transaction.atomic() decorator
def read_write_transaction_immediate(_):
    connection.cursor().execute("BEGIN IMMEDIATE")  # Acquire the db lock, retry when db is already locked, can still raise, but only if we wait for more than `timeout`.
    read_from_db()  # Read from the db, db is already locked, no problems
    write_to_db()  # Write to the db, db is already locked, no problems
    connection.cursor().execute("COMMIT")
    return HttpResponse("OK")
```

The downside of this approach is that we no longer use the `@transaction.atomic()` decorator, which means we have to handle errors and transaction nesting ourselves.

[Alex on Mastodon](https://fosstodon.org/@alextomkins/111766958328599348) pointed out that we can make Django use `BEGIN IMMEDIATE` as the default by extending the DATABASE_ENGINE the way he did it for the [Wagtail SQLite Benchmark](https://github.com/tomkins/wagtail-sqlite-benchmark/pull/6/files#diff-6ab573a361f60f74d7459fd851a96efbd9a47d18b6401fc991f3a3404cccfa5fR47):

```python
# yourproject/sqlite3/base.py
from django.db.backends.sqlite3 import base


class DatabaseWrapper(base.DatabaseWrapper):
   def _start_transaction_under_autocommit(self):
      # Acquire a write lock immediately for transactions
      self.cursor().execute("BEGIN IMMEDIATE")
```

```python
# yourproject/settings.py
DATABASES = {
    "default": {
        "ENGINE": "yourproject.sqlite3", # <-- Use our custom engine
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

This is the cleanest solution I've seen so far, but do note that it doesn't play nicely with `ATOMIC_REQUESTS=True`. With atomic requests, every request will require a lock before doing any work, making your web server process all requests sequentially.

### Solutions in Django itself

<b>Update 30 Jan 2024:</b> The change was accepted and merged into Django 5.1. See [ticket #29280](https://code.djangoproject.com/ticket/29280) for more details. 🎉

I have started a discussion on the [Django forum](https://forum.djangoproject.com/t/sqlite-and-database-is-locked-error/) to see if we can improve the experience of using SQLite in Django itself.

[Charettes proposed](https://forum.djangoproject.com/t/sqlite-and-database-is-locked-error/26994/2) to add a `begin_immediate` key to `OPTIONS`:

```diff
diff --git a/django/db/backends/sqlite3/base.py b/django/db/backends/sqlite3/base.py
index 08de0bad5a..ce9eab8d9d 100644
--- a/django/db/backends/sqlite3/base.py
+++ b/django/db/backends/sqlite3/base.py
@@ -297,7 +297,12 @@ def _start_transaction_under_autocommit(self):
         Staying in autocommit mode works around a bug of sqlite3 that breaks
         savepoints when autocommit is disabled.
         """
-        self.cursor().execute("BEGIN")
+        sql = (
+            "BEGIN IMMEDIATE"
+            if self.settings_dict["OPTIONS"].get("begin_immediate")
+            else "BEGIN"
+        )
+        self.cursor().execute(sql)

     def is_in_memory_db(self):
         return self.creation.is_in_memory_db(self.settings_dict["NAME"])
```
This is essentially the same as Alex's solution above, but doesn't require you to create a custom engine.

[Carlton Gibson mentioned](https://fosstodon.org/@carlton/111765763646205620) GRDB, a Swift library that uses SQLite as a backend, and this library allows you to [change the transaction mode](https://swiftpackageindex.com/groue/grdb.swift/v6.24.1/documentation/grdb/transactions#Transaction-Kinds). Maybe we can do something similar in Django in the future?

I think ideally, Django should ensure that `@transaction.atomic()` acquires a write lock immediately (using `BEGIN IMMEDIATE` instead of `BEGIN`). But since there is a lot of existing code out there relying on deferred transactions not to mention code with `ATOMIC_REQUESTS=True`, Django can't easily switch the default. This is why [ticket #29280](https://code.djangoproject.com/ticket/29280) was closed 5 years ago, but since it feels like SQLite is gaining traction for the web application use cases it might be worth figuring out how to improve the experience using it in Django.

## Cause 3: Using a Network File System

This issue is not specific to Django but is worth mentioning since it's a common problem with Django (and other SQLite apps) deployments on Azure.

SQLite doesn't support some network file systems, including NFS, SMB, CIFS, and others. If you use SQLite on one of those, you will likely run into `database is locked` or other types of `disk I/O` errors.

This is because these file systems don't implement locking correctly, as described in SQLite's [How to Corrupt Your Database File doc](https://www.sqlite.org/howtocorrupt.html#_filesystems_with_broken_or_missing_lock_implementations).

Martin sent me an email about how frustrating it was when he encountered the problem with his app running on Azure App Services ([azure-docs/issues/47130](https://github.com/MicrosoftDocs/azure-docs/issues/47130)). Be careful since the issue might only surface with concurrent users, who are most likely only in production!

### Solutions

A [kubernetes issue](https://github.com/kubernetes/kubernetes/issues/61767) points at the `nobrl` mount option flag as the solution, and the Azure Storage docs also mention `nobrl` as a way to solve the DB is locked errors [here](https://learn.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/mountoptions-settings-azure-files#other-useful-settings), but I haven't tested it myself so I'm not sure if it's foolproof.

Because of this, my suggestion is to avoid using SQLite over network file systems unless they are implemented with SQLite in mind (like [litefs](https://fly.io/docs/litefs/)).

