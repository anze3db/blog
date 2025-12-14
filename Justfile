PORT := env("PORT", "4000")


@_:
    just --list

manage *args:
    uv run manage.py {{ args }}

@server:
    bundle exec jekyll serve --port {{PORT}} --livereload

@server-draft:
    bundle exec jekyll serve --port {{PORT}} --livereload --drafts


@post title:
    bundle exec jekyll post "{{title}}"
