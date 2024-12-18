---
title: "Django SQLite Production Config"
description: "Optimize your Django SQLite configuration for production."
date: 2024-06-14 0:00:00 +0000
image: assets/cards/2024-06-12-sqlite-django-config.png
tags: sqlite django
---

The default SQLite configuration in Django is not ideal for running your application in production. SQLite is optimized for embedded low-concurrency systems out of the box, which is the exact opposite of what your Django application is supposed to do.

Luckily, you can improve concurrency by tweaking a few settings. See how to do it based on the version of Django that you are currently running:

<!-- 

# Use `django-sqlite-engine`

`django-sqlite-engine` comes preconfigured with defaults that should work for most web apps.

1. Install through PyPI:

    ```bash
    pip install django-sqlite-engine
    ```

2. Configure in your `DATABASES`:

    ```python
    # yourproject/settings.py
    DATABASES = {
        "default": {
            "ENGINE": "django_sqlite_engine", # <-- Use custom engine with predefined defaults
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    ```
-->
### ⚠️ WARNING ⚠️

`PRAGMA journal_mode=WAL;` setting can **corrupt your database** if used on a network file system (NFS) commonly used by hosting providers like [PythonAnywhere](https://www.pythonanywhere.com/). Do not enable it if you are unsure about the type of file storage used.

Make sure to go through [SQLite gotchas](/sqlite-prod) before using SQLite in production.

## In Django 5.1 or newer

In Django 5.1, you can tweak all the necessary changes in your `settings.py`:

```python
# yourproject/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 5,  # seconds
            "init_command": """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=NORMAL;
                PRAGMA mmap_size = 134217728;
                PRAGMA journal_size_limit = 27103364;
                PRAGMA cache_size=2000;
            """,
        },
    }
}
```


Note that you don't have to specify `PRAGMA foreign_keys = ON` because it is set by default by Django itself. You also don't need to use `PRAGMA busy_timeout` because you can achieve the same thing by setting the `timeout` database option.


## In Django 5.0, 4.2, or older

### 1. Enable WAL journal mode

The most impactful change you can make is to enable `WAL` `journal_mode`. Without `WAL`, every write request blocks reads and vice versa, which can kill your throughput.

Enabling `WAL` mode has no real downsides and can be achieved by running the following command on your database:

```bash
sqlite3 db.sqlite3 'PRAGMA journal_mode=WAL;'
```

You only have to run this command **once** per database, and the setting will persist.

### 2. Use IMMEDIATE transactions

Using immediate transactions isn't a performance improvement. It will decrease your performance when running transactions, but it will avoid unexpected [database is locked errors](/django-sqlite-dblock#cause-2-writes-after-reads-in-transactions), so it's worth enabling.

To enable IMMEDIATE transactions, you are going to have to create your database engine:

1. Create a `yourproject/sqlite3/base.py` file with a `DatabaseWrapper` class:

    ```python
    # yourproject/sqlite3/base.py
    from django.db.backends.sqlite3 import base


    class DatabaseWrapper(base.DatabaseWrapper):
        def _start_transaction_under_autocommit(self):
            # Acquire a write lock immediately for transactions
            self.cursor().execute("BEGIN IMMEDIATE")
    ```

2. Use the created `DatabaseWrapper` as your SQLite3 engine in your `settings.py`:

    ```python

    # yourproject/settings.py
    DATABASES = {
        "default": {
            "ENGINE": "yourproject.sqlite3", # <-- Use our custom engine
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    ```

# 3. Fine-tune your SQLite settings

A few SQLite settings can improve your application's performance by a few additional percentage points. The magic values below are now also the default in Rails 7.1 and should give you a good starting point, but feel free to tweak `mmap_size`, `journal_size_limit`, and `cache_size` to best suit your application:

```python
# yourproject/sqlite3/base.py
from sqlite3 import dbapi2 as Database

from django.db.backends.sqlite3 import base
from django.db.backends.sqlite3._functions import register as register_functions
from django.utils.asyncio import async_unsafe


class DatabaseWrapper(base.DatabaseWrapper):
    def _start_transaction_under_autocommit(self):
        # Acquire a write lock immediately for transactions
        self.cursor().execute("BEGIN IMMEDIATE")

    @async_unsafe
    def get_new_connection(self, conn_params):
        conn = Database.connect(**conn_params)
        register_functions(conn)

        conn.execute("PRAGMA foreign_keys = ON")
        # The macOS bundled SQLite defaults legacy_alter_table ON, which
        # prevents atomic table renames.
        conn.execute("PRAGMA legacy_alter_table = OFF")

        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute("PRAGMA mmap_size = 134217728")
        conn.execute("PRAGMA journal_size_limit = 27103364")
        conn.execute("PRAGMA cache_size = 2000")

        return conn

```


# Fin

That's it; with these settings, your SQLite database is going to handle the load that most small to medium-sized websites typically get, as long as your use case isn't write-heavy!
