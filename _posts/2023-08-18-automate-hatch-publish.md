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

    environment: release
    permissions:
      id-token: write # IMPORTANT: this permission is mandatory for trusted publishing

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
    - name: Publish package distributions to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1

{% endraw %}
```
You can also see it live [on GitHub](https://github.com/anze3db/words-tui/blob/main/.github/workflows/publish.yml).

## How it works

The workflow is triggered when I publish a new release through the GitHub UI (this step is still manual, but I am already considering automating it).

It sets up Python, installs the dependencies, builds the package using [hatch](https://hatch.pypa.io/latest/), runs the tests, and finally uses the [pypi publish](https://github.com/pypa/gh-action-pypi-publish) action to publish it to PyPI.

## Authentication

Authentication is using [Trusted Publishers](https://docs.pypi.org/trusted-publishers/) which is PyPI's implementation of
[OpenID Connect (OIDC)](https://openid.net/connect/). Instead of using a long-lived PyPI token, trusted publishers use short-lived tokens generated on the fly.

Because of this, I didn't have to store a PyPI token on GitHub. Instead, I had to add a new publisher to the project. The PyPI guide on how to do this is [here](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).

When setting up Trusted Publishers make sure you add the following lines to your yaml file. Otherwise, the PyPI action will not work:

```yaml
    permissions:
      id-token: write # IMPORTANT: this permission is mandatory for trusted publishing
```

The PyPI Action publishes all the build artifacts in the `dist/` folder. This folder is populated by the previous step's `hatch build` command. Running both `build` and `publish` in the same job is not recommended because a malicious script inside the build step could elevate privileges, but for this toy project, I think the seperation isn't necessary. 

## Token-Based Authentication

> ⚠️ WARNING ⚠️
>
> This approach is no longer recommended, but the original version of this blog post used token-based authentication. Thank you [Hynek, for showing me the light](https://mastodon.social/@hynek/110911113047685926). I am leaving this section here for posterity.

Initially, I used the `hatch publish` command instead of the PyPI GitHub Action. For authentication, I generated a PyPI token on the [manage account page](https://pypi.org/manage/account/#api-tokens) and then stored it as a repository secret on the GitHub project subpage (`/settings/secrets/actions`) as `HATCH_INDEX_AUTH`. 

I also added a secret for the PyPI username as `HATCH_INDEX_USER`, although the value isn't all that secret (it's `__token__` when using [a PyPI token](https://pypi.org/help/#apitoken)).

The two secrets are then passed to the `environment` of the runner so that `hatch` can access them.

```yaml
{% raw %}
env:
    HATCH_INDEX_AUTH: ${{ secrets.HATCH_INDEX_AUTH }}
    HATCH_INDEX_USER: ${{ secrets.HATCH_INDEX_USER }}
{% endraw %}
```

This approach might still be helpful if you publish to a private PyPI server, but for the public one, use the trusted publisher approach instead. It's more secure, and it's also easier to set up.

## Conclusion

The best thing about this automation is that I don't have to have access to PyPI on the machine I am using. It makes it less likely that I'll accidentally publish my PyPI token, which may or may not have happened in the past 🙈.
