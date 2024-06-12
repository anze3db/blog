---
title: "Django SQLite Production Config"
description: "Configure your Django app to use SQLite in production."
date: 2024-06-12 0:00:00 +0000
image: assets/cards/2024-06-12-sqlite-django-config.png
---

The default SQLite configuration in Django is not ideal for running your application in production, but this can easily be resolved by tweaking a few settings!

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

## Django 5.1 or newer

<mark>Django 5.1 is currently in <strong>development</strong> and is expected to be released in August 2024</mark>

In Django 5.1 you can make all the recommended changes in your `settings.py`:

```python
# yourproject/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
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


## Django 5.0, 4.2, or older

To apply the settings above in older versions of Django we will need to create our own sqlite3 engine.

1. Create `yourproject/sqlite3/base.py` file with a `DatabaseWrapper` class:

    ```python
    # yourproject/sqlite3/base.py
    from django.db.backends.sqlite3 import base


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
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.execute("PRAGMA mmap_size = 134217728; -- 128 megabytes")
            conn.execute("PRAGMA journal_size_limit = 27103364; -- 64 megabytes")
            conn.execute("PRAGMA cache_size = 2000")
            return conn
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

# What are these settings?

## WAL

`WAL` allows multiple readers to access the database, even if the table is being written to simultaneously. For more see [my previous post on WAL](/sqlite-wal). 

## IMMEDIATE transactions

If you use [transactions](https://docs.djangoproject.com/en/5.0/topics/db/transactions/#controlling-transactions-explicitly), make them [`IMMEDIATE`](https://sqlite.org/draft/lang_transaction.html#deferred_immediate_and_exclusive_transactions) to avoid unexpected [database is locked errors](/django-sqlite-dblock#cause-2-writes-after-reads-in-transactions).

## Finetuning SQLite

The other settings fintune your applicaiton for web applications. These are also the settings that Rails uses by default since 7.1:

```
synchronous = NORMAL 
mmap_size = 134217728; -- 128 megabytes
journal_size_limit = 27103364; -- 64 megabytes
cache_size = 2000
```

# Not sure if SQLite is a good fit in production?

I have recently gave a talk about my experience in using SQLite in production and I have written blog posts about the issues that I've had. I've also written a blog post benchmarking SQLite performance and comparing it to MySQL and PostgreSQL.

If your application only requires a single application server then SQLite can be a good fit. It's going to perform faster than MySQL and PostgreSQL for reads. If your application is write heavy then SQLite can still work, but keep in mind that SQLite can only have a single write at a time.

