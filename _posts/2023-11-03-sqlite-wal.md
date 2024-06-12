---
layout: post
title: "SQLite Write-Ahead Logging"
description: "Speed up your SQLite writes and reads with this crazy trick. 🤪"
date: 2023-11-03 0:00:00 +0000
# image: /assets/pics/pytest-plugin-og.png
---

I've been working with SQLite lately. It has become my go-to database for all projects!

## Blocking writes

One problem I encountered was that, by default, it uses [rollback journal](https://www.sqlite.org/lockingv3.html#rollback), where any write to the database will also block all reads. Because of this, my [fedidevs.com](https://fedidevs.com) site became unresponsive for about an hour every night while the nightly job inserted fresh data.

The solution was to enable [Write-Ahead Logging](https://www.sqlite.org/wal.html). WAL allows multiple readers to access the database, even if the table is being written to simultaneously. The link above has a few disadvantages listed, but for most web-server use cases, WAL is the better option.

## Enabling WAL

Enable WAL by setting the `journal_mode` to `WAL`:

```bash
sqlite3 db.sqlite3 'PRAGMA journal_mode=WAL;'
```

The `PRAGMA` command only has to be run once per database. The setting is persistent.

## .wal files

When WAL is enabled, SQLite will create `.wal` and `.shm` files. The `.wal` file records transactions committed but not yet applied to the main database. The `.shm` file is used for shared memory and caching.

Do remember to keep an eye on your .wal file sizes. Certain operations (like `VACUUM`) can make them grow as large or even larger than the database itself. If that happens to you as it did to me, you can regain the disk space by running the `wal_checkpoint` command:

```bash
sqlite3 db.sqlite3 'PRAGMA wal_checkpoint(TRUNCATE);'
```

The article [SQLite: Vacuuming the WALs](https://www.theunterminatedstring.com/sqlite-vacuuming/) is worth a read if you need to run VACUUM often.

## Conclusion

With WAL enabled and the VACUUM command removed, [fedidevs.com](https:/fedidevs.com) (and other sites) are running smoothly - bound only by the fact that my Raspberry Pi runs on a [very slow SD card](https://fosstodon.org/@anze3db/111347671377721635) 😅 

I'll write a post about my Raspberry Pi setup in the future.

