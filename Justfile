PORT := env("PORT", "4000")

@_:
    just --list

manage *args:
    uv run manage.py {{ args }}

@server:
    hugo server -p {{PORT}}

@server-draft:
    hugo server -p {{PORT}} --buildDrafts

@build:
    hugo --minify

@post title:
    hugo new content "posts/$(date +%Y-%m-%d)-$(echo '{{title}}' | tr '[:upper:] ' '[:lower:]-').md"
