---
layout: post
title: "Automate Hatch Publish with GitHub Actions"
description: "Scribbling down how I automated publishing to PyPI with GitHub Actions."
date: 2023-08-18 0:00:00 +0000
image: assets/pics/words-tui.png
---

I have automated publishing my [words-tui project](https://pypi.org/project/words-tui/) to PyPI with GitHub Actions. This is the workflow file, saved at `.github/workflows/publish.yml`:

```yaml
{% raw %}
name: Publish to PyPI

on:
  release:
    types: [published]

permissions:
  contents: read

jobs:
  deploy:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        cache: 'pip'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip 
        pip install hatch
    - name: Build package
      run: hatch build
    - name: Test package
      run: hatch run test
    - name: Publish package
      env: 
        HATCH_INDEX_AUTH: ${{ secrets.HATCH_INDEX_AUTH }}
        HATCH_INDEX_USER: ${{ secrets.HATCH_INDEX_USER }} 
      run: hatch publish
{% endraw %}
```
You can also see it live [on GitHub](https://github.com/anze3db/words-tui/blob/main/.github/workflows/publish.yml).

## How it works

The workflow is triggered when I publish a new release through the GitHub UI (this step is still manual, but I am already considering automating it).

It sets up Python, installs the dependencies, builds the package using [hatch](https://hatch.pypa.io/latest/), runs the tests, and finally runs the `hatch publish` command to publish it to PyPI.

## Authentication

For authentication, I generated a PyPI token on the [manage account page](https://pypi.org/manage/account/#api-tokens) and then stored it as a repository secret on the GitHub project subpage (`/settings/secrets/actions`) as `HATCH_INDEX_AUTH`. 

I also added a secret for the PyPI username as `HATCH_INDEX_USER`, although the value isn't all that secret (it's `__token__` when using [a PyPI token](https://pypi.org/help/#apitoken)).

The two secrets are then passed to the `environment` of the runner so that `hatch` can access them.

```yaml
{% raw %}
env:
    HATCH_INDEX_AUTH: ${{ secrets.HATCH_INDEX_AUTH }}
    HATCH_INDEX_USER: ${{ secrets.HATCH_INDEX_USER }}
{% endraw %}
```

## Conclusion

The best thing about this automation is that I don't have to have access to PyPI on the machine I am using. It makes it less likely that I'll accidentally publish my PyPI token, which may or may not have happened in the past 🙈.
