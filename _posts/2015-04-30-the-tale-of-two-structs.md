---
layout: post
title: "The Tale of Two Structs"
category:
tags: [coding, go]
---


I've been using golang for the past few days and I really like it. It's fast,
it's typesafe, it's easy to learn and it has concurrency built right into the language.

I have, however, stumbled into a bit of a pickle. file and store the parsed data into a database. It feels like this could simply
be accomplished in a single struct with multiple annotations - some for sql
some for xml, but I can't seem to get it to work.

The XML file is quite simple:

```xml
<?xml version="1.0" encoding="utf-8"?>
<weatherdata>
  <meta>
    <lastupdate>2015-04-18T09:18:16</lastupdate>
    <nextupdate>2015-04-19T22:00:00</nextupdate>
  </meta>
  <sun rise="2015-04-18T06:15:37" set="2015-04-18T19:52:34" />
</weatherdata>
```

And this is my struct that is used by GORM:

```go
type Update struct {
	gorm.Model
	LastUpdate time.Time
	NextUpdate time.Time
	Rise       time.Time
	Set        time.Time
}
```

## First problem

Parsing the dates fails, because the date strings in XML
are missing the timezone:

```bash
Parsing time "2015-04-30T09:05:19" as "2006-01-02T15:04:05Z07:00": cannot parse "" as "Z07:00"
```

I actually managed to solve that by writing my own `UnmarshalXML` and `UnmarshalXMLAttr`
functions ([see here](https://github.com/Smotko/wave-watcher/commit/af24a2e2fc0121e958008fcac36b74c6257d7d81#diff-9598cdbea8bfe979f70803194f8dec94R54)), but then I couldn't get GORM to save my custom Time struct.

My current solution is to use `string` for date fields and then parse them manually (see below).

## Second problem

I can't seem to get the rise attr of the sun element without a sun struct in between:

```go
type UpdateXml struct {
	LastUpdate string `xml:"meta>lastupdate"`
	NextUpdate string `xml:"meta>nextupdate"`
	Sun        struct {
		Rise string `xml:"rise,attr"`
		Set  string `xml:"set,attr"`
	} `xml:"sun"`
}
```

## My solution

So my current solution is to use two structs and a convert function to convert
between the two:

```go
// Helper function for converting UpdateXml -> Update
func (u *UpdateXml) ToUpdate() Update {
	return Update{
		LastUpdate: parse(u.LastUpdate),
		NextUpdate: parse(u.NextUpdate),
		Rise:       parse(u.Sun.Rise),
		Set:        parse(u.Sun.Set),
	}
}
```
