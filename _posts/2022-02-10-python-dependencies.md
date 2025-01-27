---
layout: post
title: "Python Dependency Management"
description: "Overview of common methods for managing Python dependencies"
date: 2022-02-10 7:00:00 +0000
tags: python
# image: assets/pics/django32-query-perf.png
---

Python has multiple ways for delaing with dependecies and the options can seem intimidating. This blogpost explains the most common dependency management tools and some of the most common commands that one would run.

## requirements.txt

If you worked in Python you probably stumbled onto a file named `requirements.txt`. It's a file containing a list of items to be installed using pip install. An example file could have the following content:

<!-- prettier-ignore-start -->
```python
django
```
<!-- prettier-ignore-end -->

And you can install it with

<!-- prettier-ignore-start -->
```python
pip install -r requirements.txt
```
<!-- prettier-ignore-end -->

The result of the command would look somewhat like:

<!-- prettier-ignore-start -->
```python
pip install -r requirements.txt
Collecting django
  Downloading Django-4.0.2-py3-none-any.whl (8.0 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.0/8.0 MB 1.7 MB/s eta 0:00:00
Collecting sqlparse>=0.2.2
  Using cached sqlparse-0.4.2-py3-none-any.whl (42 kB)
Collecting asgiref<4,>=3.4.1
  Using cached asgiref-3.5.0-py3-none-any.whl (22 kB)
Installing collected packages: sqlparse, asgiref, django
Successfully installed asgiref-3.5.0 django-4.0.2 sqlparse-0.4.2
```
<!-- prettier-ignore-end -->

And we can see that our requirements.txt file installed 3 packages. `asgiref-3.5.0 django-4.0.2 sqlparse-0.4.2`.

The issue with this is that you might install a newer version of Django, sqlparse, or asgiref anytime you run `pip install -r requirements.txt`. This might break your application code and is considered a bad practice.

To solve this problem you can lock all of the pacakges with `pip freeze > requirements.txt` that will save all the versions:

<!-- prettier-ignore-start -->
```python
django==4.0.2
asgiref==3.5.2
sqlparse==0.4.2
```
<!-- prettier-ignore-end -->

But now we have a different problem. We no longer know which dependencies are direct dependencies for our application (django) and which came from our dependencies' dependencies. This makes upgrading dependencies tricky.

Only use this approach for small side projects.

## pip-tools

pip-tools is a suite of tools that automate pinning and installing dependencies. You give it a list of dependencies that your project depends on (in our case that would be `django`) and it generates a requirements.txt file for us automatically. This way we can clearly separate the dependencies that we need from the dependencies or dependencies need, thus solving the main problem from the previous section.

We can create a file called `requirements.in` (although `setup.py` and `pyproject.toml` are also supported) with the following content:

<!-- prettier-ignore-start -->
```python
django
```
<!-- prettier-ignore-end -->

And then we can run `pip-compile requirements.in` which will generate the following requirements.txt file:

<!-- prettier-ignore-start -->
```python
#
# This file is autogenerated by pip-compile with python 3.10
# To update, run:
#
#    pip-compile requirements.in
#
asgiref==3.5.0
    # via django
django==4.0.2
    # via -r requirements.in
sqlparse==0.4.2
    # via django
```
<!-- prettier-ignore-end -->

Now that we have the generatd requirement.txt filem, we can install all the dependencies with `pip install -r requirements.txt` or with `pip-sync requirements.txt`. The advantage of using pip-sync is that it will also uninstall all the packages not in requirements.txt making sure your environment matches the specification.

### Upgrading dependencies

Upgrading dependencies is done with `pip-compile --upgrade`. The command will respect the version pins in your `requirements.in` file. This means that if your `requirements.in` file contains `django<4.1` it will never upgrade django to Django 4.1.

### Dev dependencies

pip-tools doesn't have a way a built in way to separate your production dependencies with your development dependencies like some of the other tools do. Instead, we define a new requirements file and name it something like requirements-dev.in:

```python
-c requirements.txt
black
```

We can generate a compiled requirements-dev.txt file that will include our dev dependencies.

## Pipenv

Pipenv is not just a dependency management tool like pip-tools, but also a Python virtual enviornment manager. To start using pipenv we need to tell it which python version the project will be using: `pipenv --python 3.10`:

<!-- prettier-ignore-start -->
```python
pipenv --python 3.10
Creating a virtualenv for this project...
Pipfile: /Users/anze/coding/python-package-managers/Pipfile
Using /usr/local/bin/python3 (3.10.2) to create virtualenv...
⠼ Creating virtual environment...created virtual environment CPython3.10.2.final.0-64 in 240ms
  creator CPython3Posix(dest=/Users/anze/.local/share/virtualenvs/python-package-managers-KVHa45pe, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/Users/anze/Library/Application Support/virtualenv)
    added seed packages: pip==21.3.1, setuptools==60.3.1, wheel==0.37.1
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

✔ Successfully created virtual environment!
Virtualenv location: /Users/anze/.local/share/virtualenvs/python-package-managers-KVHa45pe
```
<!-- prettier-ignore-end -->

This command will do two things:
1. Generate a new development virtual environment using Python 3.10
2. Create a Pipfile with the following content:

<!-- prettier-ignore-start -->
```python
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]

[dev-packages]

[requires]
python_version = "3.10"
```
<!-- prettier-ignore-end -->

Now if we wanted to add django we would run `pipenv install django`

after running this our pipfile will look like this:

<!-- prettier-ignore-start -->
```python
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
django = "*"

[dev-packages]

[requires]
python_version = "3.10"
```
<!-- prettier-ignore-end -->

And we will also have a Pipenv.lock file with the following content:

<!-- prettier-ignore-start -->
```python
{
    "_meta": {
        "hash": {
            "sha256": "7e6dca07b964c2888324e576ba6c1bc240d74a27b75619fc88bca2ee3979baf8"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.10"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {
        "asgiref": {
            "hashes": [
                "sha256:2f8abc20f7248433085eda803936d98992f1343ddb022065779f37c5da0181d0",
                "sha256:88d59c13d634dcffe0510be048210188edd79aeccb6a6c9028cdad6f31d730a9"
            ],
            "markers": "python_version >= '3.7'",
            "version": "==3.5.0"
        },
        "django": {
            "hashes": [
                "sha256:110fb58fb12eca59e072ad59fc42d771cd642dd7a2f2416582aa9da7a8ef954a",
                "sha256:996495c58bff749232426c88726d8cd38d24c94d7c1d80835aafffa9bc52985a"
            ],
            "index": "pypi",
            "version": "==4.0.2"
        },
        "sqlparse": {
            "hashes": [
                "sha256:0c00730c74263a94e5a9919ade150dfc3b19c574389985446148402998287dae",
                "sha256:48719e356bb8b42991bdbb1e8b83223757b93789c00910a616a071910ca4a64d"
            ],
            "markers": "python_version >= '3.5'",
            "version": "==0.4.2"
        }
    },
    "develop": {}
}
```
<!-- prettier-ignore-end -->

We can see that like pip-tools from the section above, Pipfile.lock also includes the same version pins.

### Upgrading dependencies

To upgrade the dependencies we can run `pipenv update` and it will update all the versions in Pipfile.lock, respecting the constraint in the Pipfile.

### Dev dependencies

To add development dependencies we have to run `pipenv install --dev black` and this will place black into the development section of Pipenv.

## Poetry

We can start a new Poetry project with 

<!-- prettier-ignore-start -->
```python
poetry init
```
<!-- prettier-ignore-end -->

This will generate a new folder structrue for you that looks somewhat like this

<!-- prettier-ignore-start -->
```python
poetry init

This command will guide you through creating your pyproject.toml config.

Package name [python-package-managers]:  django-demo
Version [0.1.0]:
Description []:
Author [Anže Pečar <anze@pecar.me>, n to skip]:
License []:
Compatible Python versions [^3.10]:

Would you like to define your main dependencies interactively? (yes/no) [yes]
You can specify a package in the following forms:
  - A single name (requests)
  - A name and a constraint (requests@^2.23.0)
  - A git url (git+https://github.com/python-poetry/poetry.git)
  - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
  - A file path (../my-package/my-package.whl)
  - A directory (../my-package/)
  - A url (https://example.com/packages/my-package-0.1.0.tar.gz)

Search for package to add (or leave blank to continue): django
Found 20 packages matching django

Enter package # to add, or the complete package name if it is not listed:
 [0] Django
 [1] django-503
 [2] django-scribbler-django2.0
 [3] django-filebrowser-django13
 [4] django-jchart-django3-uvm
 [5] django-tracking-analyzer-django2
 [6] django-totalsum-admin-django3
 [7] django-debug-toolbar-django13
 [8] django-django_csv_exports
 [9] django-suit-redactor-django2
 > 0
Enter the version constraint to require (or leave blank to use the latest version):
Using version ^4.0.2 for Django

Add a package:

Would you like to define your development dependencies interactively? (yes/no) [yes] no
Generated file

[tool.poetry]
name = "django-demo"
version = "0.1.0"
description = ""
authors = ["Anže Pečar <anze@pecar.me>"]

[tool.poetry.dependencies]
python = "^3.10"
Django = "^4.0.2"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes]
```
<!-- prettier-ignore-end -->

This created a pyproject.toml file so now the only thing left to do is to generate a lock file:

<!-- prettier-ignore-start -->
```python
poetry lock
Creating virtualenv django-demo-4WB6S-3I-py3.10 in /Users/anze/Library/Caches/pypoetry/virtualenvs
Updating dependencies
Resolving dependencies... (2.7s)

Writing lock file
```
<!-- prettier-ignore-end -->

The `poetry.lock` file looks like this:

<!-- prettier-ignore-start -->
```python
[[package]]
name = "asgiref"
version = "3.5.0"
description = "ASGI specs, helper code, and adapters"
category = "main"
optional = false
python-versions = ">=3.7"

[package.extras]
tests = ["pytest", "pytest-asyncio", "mypy (>=0.800)"]

[[package]]
name = "django"
version = "4.0.2"
description = "A high-level Python web framework that encourages rapid development and clean, pragmatic design."
category = "main"
optional = false
python-versions = ">=3.8"

[package.dependencies]
asgiref = ">=3.4.1,<4"
sqlparse = ">=0.2.2"
tzdata = {version = "*", markers = "sys_platform == \"win32\""}

[package.extras]
argon2 = ["argon2-cffi (>=19.1.0)"]
bcrypt = ["bcrypt"]

[[package]]
name = "sqlparse"
version = "0.4.2"
description = "A non-validating SQL parser."
category = "main"
optional = false
python-versions = ">=3.5"

[[package]]
name = "tzdata"
version = "2021.5"
description = "Provider of IANA time zone data"
category = "main"
optional = false
python-versions = ">=2"

[metadata]
lock-version = "1.1"
python-versions = "^3.10"
content-hash = "3fb42be116725996c36b953689fc39db958af54df415de893c3608be15d5b925"

[metadata.files]
asgiref = [
    {file = "asgiref-3.5.0-py3-none-any.whl", hash = "sha256:88d59c13d634dcffe0510be048210188edd79aeccb6a6c9028cdad6f31d730a9"},
    {file = "asgiref-3.5.0.tar.gz", hash = "sha256:2f8abc20f7248433085eda803936d98992f1343ddb022065779f37c5da0181d0"},
]
django = [
    {file = "Django-4.0.2-py3-none-any.whl", hash = "sha256:996495c58bff749232426c88726d8cd38d24c94d7c1d80835aafffa9bc52985a"},
    {file = "Django-4.0.2.tar.gz", hash = "sha256:110fb58fb12eca59e072ad59fc42d771cd642dd7a2f2416582aa9da7a8ef954a"},
]
sqlparse = [
    {file = "sqlparse-0.4.2-py3-none-any.whl", hash = "sha256:48719e356bb8b42991bdbb1e8b83223757b93789c00910a616a071910ca4a64d"},
    {file = "sqlparse-0.4.2.tar.gz", hash = "sha256:0c00730c74263a94e5a9919ade150dfc3b19c574389985446148402998287dae"},
]
tzdata = [
    {file = "tzdata-2021.5-py2.py3-none-any.whl", hash = "sha256:3eee491e22ebfe1e5cfcc97a4137cd70f092ce59144d81f8924a844de05ba8f5"},
    {file = "tzdata-2021.5.tar.gz", hash = "sha256:68dbe41afd01b867894bbdfd54fa03f468cfa4f0086bfb4adcd8de8f24f3ee21"},
]

```
<!-- prettier-ignore-end -->

### Upgrading dependencies

To upgrade the dependencies we can run `poetry update` and it will update all the versions in poetry.lock, respecting the constraint in the `pyproject.toml`.

### Dev dependencies

To add development dependencies we have to run `poetry add --dev black` and this will place black into the development section of `pyproject.toml`.
