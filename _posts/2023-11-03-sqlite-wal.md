---
layout: post
title: "SQLite Write-Ahead Logging"
description: "Speed up your SQLite writes and reads with this crazy trick. 🤪"
date: 2023-11-03 0:00:00 +0000
# image: /assets/pics/pytest-plugin-og.png
---

I've been working with SQLite lately. My [fedidevs.com](fedidevs.com) project uses it as the primary storage.

## Blocking writes

One problem I encountered was that, by default, writes block reads. Because of this, the site became unresponsive for about an hour every night while the nightly job fetched and inserted fresh data from across the fediverse.

The solution was to enable [Write-Ahead Logging](https://www.sqlite.org/wal.html). WAL allows multiple readers to access the database simultaneously, even if the table is being written to.

## Enabling WAL

Enable WAL by setting the `journal_mode` to `WAL`:

```bash
sqlite3 db.sqlite3 'PRAGMA journal_mode=WAL;'
```

The `PRAGMA` command only has to be run once per database. The setting is persistent.

## .wal files

When WAL is enabled, SQLite will create `.wal` and `.shm` files. The `.wal` file records transactions committed but not yet applied to the main database. The `.shm` file is used for shared memory and caching.

Do remember to keep an eye on your .wal file sizes. Certain operations (like `VACUUM`) can make them grow as large or even larger than the database itself. To regain the disk space, run the `wal_checkpoint` command:

```bash
sqlite3 db.sqlite3 'PRAGMA wal_checkpoint(TRUNCATE);'
```

The article [SQLite: Vacuuming the WALs](https://www.theunterminatedstring.com/sqlite-vacuuming/) is worth a read if you need to run VACUUM as it shows a few ways to make sure your storage doesn't spiral out of control.

## Conclusion

With WAL enabled and the VACUUM command removed, [fedidevs.com](https:/fedidevs.com) is chugging along nicely. It only gets a little traffic and is almost free to run since it's hosted on my Raspberry Pi. I'll write a post about this setup in the future.

