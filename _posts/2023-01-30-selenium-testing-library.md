---
layout: post
title: "Selenium Testing Library"
description: "Using the Testing Library with Selenium in Python."
date: 2023-01-30 1:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

[Testing Library](https://testing-library.com/) has become one of the most popular testing tools for writing tests and it currently supports numerous front-end frameworks (React, Reason, Native, Vue, Marko, Angular, Preact, Svelte, Cypress, and more). The Testing Library query API has even been adopted by Playwright in [their recent release](https://github.com/microsoft/playwright/releases/tag/v1.27.0).

The popularity of the Testing Library probably boils down to the following two reasons:

1. Well-designed query API
2. Focus on accessibility

# Query API

On first look, the Testing Library Query API looks complex. There are 3 types of queries:

1. `getBy...` Returns the matching node and throws an error if nothing is matched.
2. `queryBy...` Same as `getBy...` but returns `null` instead of an error if nothing matched. 
3. `findBy...` Returns a promise that is rejected if the element was not found in `1s` (or based on the `timeout` parameter).

You mainly use the `get` queries since they are the fastest. You use `query` when you need to assert that something shouldn't be in the DOM. You use `find` to find elements that might not be in the DOM just yet.


# Accessibility

The main [guiding principle](https://testing-library.com/docs/guiding-principles) of the Testing Library is that tests should be written to closely resemble how the web pages are going to be used.

This shows itself the most in the [priority](https://testing-library.com/docs/queries/about#priority) for using different locators. `...ByRole` that is used to query every element exposed in the [accessibility tree](https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree) should be your top preference for everything. While on the other hand `getByTestId` should be used as the last resort because end users have no way of seeing or hearing it.

# Selenium with Python

In [Selenium with Python](https://selenium-python.readthedocs.io/index.html) we, unfortunately, don't get a good Query API or accessibility features out of the box.

## Query API

The Query API consists of [two functions to query elements](https://selenium-python.readthedocs.io/locating-elements.html). `find_element` and `find_elements`. This seems simpler, but unfortunately, it makes test code much more verbose. First example:

```python
# Assert that only one element is found in the DOM
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
assert len(driver.find_elements(By.Name, "my-element")) == 1
```

Note, that we can't use `find_elment` for this because it doesn't catch the case when there is more than one element with the name `my-element` on the page. In that case, the function returns the first element found and ignores all the other instances. Second example:

```python
# Wait until the element is visible on the page
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
element = WebDriverWait(driver, 1).until(
    EC.presence_of_element_located((By.Name, "my-element"))
)
```
Waiting for the element to appear on the page is even more verbose and it requires 4 different import statements. I see teams create their own wait abstractions to get around this which isn't ideal. You could use [implicit waits](https://www.selenium.dev/documentation/webdriver/waits/#implicit-wait) instead, but they usually aren't recommended.


## Accessibility

Some recently added Selenium features have focused on accessibility ([relative Locators](https://www.selenium.dev/documentation/webdriver/elements/locators/#relative-locators) added in 4.0), but in general, the preferred locators for finding elements in Selenium continue to be CSS or XPath expressions. Users generally don't see your CSS classes or XPath expressions so they should not be your default choice. Even worse, developers like to change those, and that makes your end-to-end tests brittle.

Selenium also doesn't offer the primary locator recommended by the Testing Library - By Role. This is very unfortunate since it's extremely difficult to write your own. I've tried, but implementing [this table of HTML elements and their roles](https://www.w3.org/TR/html-aria/#docconformance) goes beyond a weekend project 😓 

# The Solution

The good news is that it's fairly easy to use the Testing Library from Selenium. Since the [dom-testing-library](https://github.com/testing-library/dom-testing-library) is written in JavaScript you can add it to your webpage and then use its API within your tests. Unfortunately, this looks a little gross in Python. First example rewritten using this approach:

```python
# Assert that only one element is found on the page
from selenium import webdriver

driver = webdriver.Firefox()
driver.execute_script("getByLabelText(document, 'My Element") # getBy query raises an exception if more than one element is found
```
Second example:
```python
# Wait until the element is visible on the page
from selenium import webdriver

driver = webdriver.Firefox()
driver.execute_script("findByLabelText(document, 'My Element") # findBy query will wait for 1s before throwing an error
```

I'd argue that using `execute_script` is already an improvement over Selenium's API. We can even locate the input element using its label text, something that is not easily done with Selenium. 

# Selenium Testing Library

However, injecting the Testing Library into the DOM manually and then writing JavaScript is not the best user experience for writing tests. This is why I created a PyPI package [Selenium Testing Library](https://github.com/anze3db/selenium-testing-library) that takes care of this plumbing and exposes a nice 100% type annotated API. First example rewritten using the Selenium Testing Library:

```python
# Assert that only one element is found on the page
from selenium import webdriver
from selenium_testing_library import Screen

screen = Screen(webdriver.Firefox())
screen.get_by_label_text("My Element")
```
Second example:
```python
# Wait until the element is visible on the page
from selenium import webdriver
from selenium_testing_library import Screen

screen = Screen(webdriver.Firefox())
screen.find_by_label_text("My Element")
```

The [`Screen` class](https://github.com/anze3db/selenium-testing-library#testing-library-selectors) exposes all the `get_by...`, `query_by...` and `find_by...` methods as well as all the Testing Library locators (Role, Label Test, TestId, and others). I even added the Selenium locators including XPath, CSS, and others so that it's easier to transition.

The Selenium Testing Library has been used by my company for more than 1 year now and it powers more than 600 end-to-end tests. The API has been stable and I am not planning on making any backward incompatible changes. Hopefully, DOM Testing Library doesn't make them either 🤞

# Fin

I think the Testing Library has come up with a really great way for writing front-end tests and I hope to see Selenium adopt some of these ideas in the future so that 3rd party packages like [Selenium Testing Library](https://github.com/anze3db/selenium-testing-library) will no longer be necessary.
