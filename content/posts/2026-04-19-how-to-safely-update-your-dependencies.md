---
title: "How to Safely Update Your Dependencies"
date: 2026-04-19T00:00:00+01:00
---

With all the supply chain attacks happening lately ([litellm](https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-teampcp-supply-chain-campaign/) being the most recent example) keeping dependencies up to date without risk has been on my mind.

Below is everything I do to keep my personal projects secure, what we do at [Fencer](http://fencer.dev/) to keep our own codebase secure, and what we recommend to the startups we work with.

## Be hesitant about what you add

The best way to reduce the risk of installing a compromised dependency is to avoid relying on it in the first place. Before adding a new dependency, I first make sure that implementing it ourselves would be too much work (or tokens!).

Besides that, I try to ensure the dependency is reliable and well maintained. There is no good way to determine this, but looking at the git history, issues, etc., can usually give you a rough idea.

## Pin to hashes, not just versions

Having a lock file that pins your dependencies to a specific version is good, but not sufficient. Version numbers are not always immutable! A compromised maintainer account can republish a tag or a package version that points to different bytes. Pinning to a hash is what actually protects you.

pip itself ships a `pip hash` command that prints a hash in the format `requirements.txt` expects. For a single file:

```bash
$ pip hash Django-5.1.4-py3-none-any.whl
Django-5.1.4-py3-none-any.whl:
--hash=sha256:236e023f021f5ce7dee5779de7b286565fdea5f4ab86bae5338e3f7b69896cf0
```

To generate hashes for a whole requirements file, download everything first with `pip download` and then hash each file:

```bash
pip download -d ./wheels -r requirements.txt
for f in ./wheels/*; do pip hash "$f"; done
```

Stitch the hashes into `requirements.txt` so each pin looks like:

```
django==5.1.4 \
 --hash=sha256:de3f88c... \
 --hash=sha256:a5a5f9e...
```

And install with hash checking enforced:

```bash
pip install --require-hashes -r requirements.txt
```

The manual stitching is why most people reach for [pip-tools](https://github.com/jazzband/pip-tools) (`pip-compile --generate-hashes`) or `uv`, but it's good to know that plain pip has the primitives.

[`uv`](https://docs.astral.sh/uv/) writes a hashed lockfile by default.

On the JS side, npm's `package-lock.json` already stores integrity hashes for every resolved package. The thing to do is use `npm ci` rather than `npm install` in CI and production builds. `npm ci` fails loudly if the lockfile and `package.json` disagree and verifies the integrity hashes instead of silently re-resolving.

```bash
npm ci
```

### Pin GitHub Actions too

This one gets overlooked a lot: pin your GitHub Actions to a full commit SHA, not a tag. Tags are mutable. A compromised maintainer (or a compromised Action they depend on, [like tj-actions/changed-files earlier this year](https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised)) can repoint `v4` at malicious code, and any workflow using `@v4` picks it up on the next run.

So instead of:

```yaml
- uses: actions/checkout@v4
```

Do:

```yaml
- uses: actions/checkout@<full-sha-of-v4.2.2> # v4.2.2
```

Leaving the human-readable version as a trailing comment lets Dependabot bump the pin while keeping the SHA as the source of truth. If you have a lot of workflows to convert, [pinact](https://github.com/suzuki-shunsuke/pinact) can rewrite all your tag references to SHAs in one pass.

## Update periodically

If all your dependencies are locked and never change, you risk running insecure software. Even if none of your dependencies have open CVEs today, being several versions behind means that when a CVE does drop, you'll have a mountain of accumulated upgrades to work through before you can patch.

The best solution is to automate your dependency upgrades. Dependabot is the canonical tool, but I find it hard to configure without it being too noisy. Dependabot is great for notifying you about and fixing CVEs. Still, for general updates, I prefer a single PR that bumps all your versions at once, and I usually create this workflow with a custom GitHub Action.

90% of the time, this dependency upgrade PR won't require much work, but occasionally you'll have to address a breaking change or a bug in an upstream repository. It's easier to handle these small changes as they pop up than to deal with a whole pile of them after pinning a dependency on the same version for years.

If an individual package upgrade turns out to be a lot of work, you can always pin that specific package to the older version and handle it separately.

## Update with cooldowns

When you update dependencies periodically, you are always at risk that the latest version you're upgrading to has been compromised. These attacks are usually detected and yanked within a few, but you can still get unlucky and pull the bad version during that window.

Dependency cooldowns help here. They instruct your tool to install a new version if it was published more than a specified period ago. The longer the cooldown, the lower the risk of installing a compromised package, but the longer you wait for legitimate security patches too.

I use a 5-day cooldown for most packages and a 1-day cooldown for packages I trust more and want to pull security fixes from quickly. The only such package at the moment is `django`.

`uv` supports this via `exclude-newer` and `exclude-newer-package` in `pyproject.toml`:

```toml
[tool.uv]
exclude-newer = "5 days"
exclude-newer-package = { django = "1 day" }
```

pip 26.0 (released in January 2026) added `--uploaded-prior-to` for the same purpose:

```bash
pip install --uploaded-prior-to 2026-04-12T00:00:00Z -r requirements.txt
```

For now, it only accepts absolute timestamps, so if you want a relative cooldown like "5 days ago," you have to compute the timestamp yourself. The good news is [pip#13837](https://github.com/pypa/pip/pull/13837) has been merged and will ship in pip 26.1, adding ISO 8601 duration support so you'll be able to write:

```bash
pip install --uploaded-prior-to P5D -r requirements.txt
```

`P3D` is ISO 8601 duration syntax: `P` is the period designator and `5D` is 5 days. `P1W` would be a week, `PT1H` an hour (the `T` separates date from time parts).

On the JS side, [all major Node package managers](https://socket.dev/blog/npm-introduces-minimumreleaseage-and-bulk-oidc-configuration) now offer some form of cooldown: pnpm added `minimumReleaseAge` in v10.16, Yarn shipped `npmMinimalAgeGate` in 4.10.0, Bun added `minimumReleaseAge` in v1.3, and npm itself followed with `min-release-age` in CLI 11.x.

## A note on skills

Skills and skill marketplaces for your AI agents are another vector to worry about. Be very careful where and how you install skills, because they execute with the same permissions as your agent and can exfiltrate anything the agent can see. Treat an untrusted skill the same way you'd treat an untrusted npm package running a postinstall script.

## Fin

None of this is bulletproof, but hashes, cooldowns, and a sensible upgrade cadence gets you most of the way there. At [Fencer](http://fencer.dev/), we've helped various companies put these practices in place, so if you'd like a hand rolling them out, feel free to reach out.
