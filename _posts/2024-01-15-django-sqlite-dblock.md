---
title: "Django, SQLite, and the Database is Locked Error"
description: "Explains `database is locked` errors in Django when using SQLite, and how to solve them."
date: 2024-01-16 0:00:00 +0000
image: /assets/cards/2024-01-16-django-sqlite-dblock.png
---

SQLite is gainig traction as a viable option for web applications in production environments. Django developers wanting to use SQLite in production need to be aware of the `database is locked` error, because it might cause confusion in certain cases.

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

There are two possible causes for this error.

## Cause 1: SQLite timed out waiting for the lock

The first reason is well documented in [Django's documentation](https://docs.djangoproject.com/en/5.0/ref/databases/#database-is-locked-errors):

> OperationalError: database is locked errors indicate that your application is experiencing more concurrency than sqlite can handle in default configuration. This error means that one thread or process has an exclusive lock on the database connection and another thread timed out waiting for the lock the be released.

Django also gives three ways to solve the problem:

> Switching to another database backend.

This is correct, although you could do this much later than the docs might have you believe.

> Rewriting your code to reduce concurrency and ensure that database transactions are short-lived.

Also correct. You can accomplish this by optimizing your tables (reducing the number of data written, removing unnecessary indexes, etc.), reducing the amount of work in a single transaction, or upgrading to a faster hard drive option if available.

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

Correct again, but I have to point out that even with 5 seconds of waiting, you can get several hundred of write requests per second. 

The Django docs, however, don't mention that there is another reason for the `database is locked` errors that have nothing to do with how you've set your `timeout.`

## Cause 2: Retrying in the middle of a transaction could break the serializable isolation guarantee

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

The bolded part explains why the request failed even though we weren't near the timeout.

Let's look at the view in my example and see what's going on step by step:

```python
@transaction.atomic()  # Start a deferred transaction; no db lock yet
def read_write_transaction(_):
    read_from_db()  # Read from the db here; no lock yet
    write_to_db()  # Try to acquire a lock in the middle of the transaction, but if the db is already locked, SQLite cannot retry because that might break the serializable isolation guarantees.
    return HttpResponse("OK")
```

# Possible solutins and workarounds

(I am still searching for the best way to solve this issue and I will update the blog post when new solutions pop up)

One obvious workaround (but not very practical!) is always to make sure you do a write request at the start of every transaction:

```python
@transaction.atomic()  # Start a deferred transaction, no lock yet
def write_read_transaction(_):
    write_to_db()  # Try to acquire a lock; if the db is already locked, SQLite will retry. There were no read queries in this transaction, so there is no way to break serializable isolation guarantees.
    read_from_db()  # Read from the db here; the db is already locked
    return HttpResponse("OK")
```

This is very awkward and even impossible in most views where the first thing to do is to fetch the user of the current request.

Luckily, SQLite can acquire a lock immediately when starting a transaction with [`BEGIN IMMEDIATE`](https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions). We can use this in our view like this:

```python
def read_write_transaction_immediate(_):
    connection.cursor().execute("BEGIN IMMEDIATE")  # Acquire the db lock, retry when db is already locked, can still raise, but only if we wait for more than `timeout`.
    read_from_db()  # Read from the db, db is already locked, no problems
    write_to_db()  # Write to the db, db is already locked, no problems
    connection.cursor().execute("COMMIT")
    return HttpResponse("OK")
```

This would work but it isn't production-ready code because we don't handle errors, transaction nesting, and probably ten other things that `transaction.atomic` takes care of for us.

Another option would be to monkey patch `transaction.atomic` like it was done [here](https://code.djangoproject.com/ticket/29280#comment:5). Although, the code no longer works on Django 5.0.

The [most promising solution right now comes from charettes](https://forum.djangoproject.com/t/sqlite-and-database-is-locked-error/26994/2) and proposes to add a `begin_immediate` key to `OPTIONS`:

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

*Any other potential solutions or workarounds that I haven't listed? Please joind the discussion on the [Django forum](https://forum.djangoproject.com/t/sqlite-and-database-is-locked-error/26994). I'll update the post as new ideas come through!*

I think ideally, Django should ensure that `@transaction.atomic()` acquires a write lock immediately (using `BEGIN IMMEDIATE` instead of `BEGIN`). But since there might be a lot of existing code out there relying on deferred transactions, Django can't easily switch the default. This is why [ticket #29280](https://code.djangoproject.com/ticket/29280) was closed 5 years ago, but since it feels like SQLite is gaining traction for the web application use cases it might be worth figuring out how to improve the experience using it in Django.
