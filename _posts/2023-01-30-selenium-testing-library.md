---
layout: post
title: "Selenium Testing Library"
description: "Using the Testing Library with Selenium."
date: 2023-01-30 1:00:00 +0000
# image: assets/pics/django32-query-perf.png
---

[Testing Library](https://testing-library.com/) has become one of the most popular testing tools for writing tests and it currently supports numerous front-end frameworks (React, Reason, Native, Vue, Marko, Angular, Preact, Svelte, Cypress, and more). The Testing Library query API has even been adopted by Playwright in [their recent release](https://github.com/microsoft/playwright/releases/tag/v1.27.0).

The popularity of the Testing Library probably boils down to the following two reasons:

1. Well designed query API
2. Focus on accessibility

# Query API

On first look the Testing Library Query API looks complex. There are 3 types of queries:

1. `getBy...` Returns the matching node and throw an error if nothing matched.
2. `queryBy...` Same as `getBy...` but returns `null` instead of an error if nothing matched. 
3. `findBy...` Returns a promise that is rejected if the element was not found in `1s` (or based on the `timeout` parameter).

You mainly use the `get` queries since they are the fastest. You primarially use `query` when you need to assert that something shouldn't be in the DOM. You use `find` to find elements that might not be in the DOM just yet.


# Accessibility

The main [guiding priciple](https://testing-library.com/docs/guiding-principles) of the Testing Library is that tests should be written to closely resemble how the web pages are going to be used.

This shows itself the most in the [priority](https://testing-library.com/docs/queries/about#priority) for using different locators. `...ByRole` that is used to query every element exposed in the [accessibility tree](https://developer.mozilla.org/en-US/docs/Glossary/Accessibility_tree) should be your top preference for everything. While on the other hand `getByTestId` should be used as the last resort because end users have no way of seeing or hearing it.

# Selenium with Python

With [Selenium with Python](https://selenium-python.readthedocs.io/index.html) we, unfortunately, don't get a good Query API or the accessibility features out of the box.

## Query API

The Query API consists of [two functions to query elements](https://selenium-python.readthedocs.io/locating-elements.html). `find_element` and `find_elements`. This seems simpler, but unfortunately it makes test code much more verbose. First example:

```python
# Assert that only one element is found in the DOM
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
assert len(driver.find_elements(By.Name, "my-element")) == 1
```

Note, that we can't use `find_elment` for this because if there is more than one element with the name `my-element` on the page the function will return the first one and ignore the others. Second example:

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
Waiting for element to appear on the page (a very common operation when writing tests!) is even more verbose and it requires 4 different import statements.


## Accessibility

There are some recently added Selenium features that focused on accessibility ([Relative Locators](https://www.selenium.dev/documentation/webdriver/elements/locators/#relative-locators) added in 4.0), but in general the preffered locators for finding elements in Selenium continue to be CSS or XPath expressions. Users generally don't see your css classes or xpath expressions and even worse, developers like to change those from time to time making your end-to-end tests brittle.

Even though Selenium has a `By.Role` locator it only finds element with an explicit `role` attribute so you can't use it for finding implicit role names in the DOM the same way that you can with the Testing Library's `getByRole`.


# The Solution

The good news is that it's fairly easy to use the Testing Library from Selenium. Since the [dom-testing-library](https://github.com/testing-library/dom-testing-library) is written in JavaScript you can add it to your webpage and then use it's API from within your tests. Unfortunately, this looks a little gross from within Python. First example rewritten using this approach:

```python
# Assert that only one element is found on the page
from selenium import webdriver

driver = webdriver.Firefox()
driver.execute_script("getByLabelText(document, 'My Element") # getBy query raises an execption if more than one element is found
```
Second example:
```python
# Wait until the element is visible on the page
from selenium import webdriver

driver = webdriver.Firefox()
driver.execute_script("findByLabelText(document, 'My Element") # findBy query will wait for 1s before throwing an error
```

I'd argue that using `execute_script` is already an improvement over Selenium's API. We can even locate the input element using its label text, something that is again not easily done with Selenium. 

However, injecting the Testing Library into the DOM and then writing JavaScript is not how we should write our tests. This is why I created a [PyPI package](https://github.com/anze3db/selenium-testing-library) that does all of this for you and exposes a nice 100% type annotated API. First example rewritten using the package:

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

The [`Screen` class](https://github.com/anze3db/selenium-testing-library#testing-library-selectors) exposes all the `get...`, `query...` and `find...` methods as well as all the Testing Library locators (Role, Label Test, TestId, and others) as well as the Selenium ones (XPath, CSS, and others) if you really need them.

# Fin

I think the Testing Library has come up with a really great way for writing front-end tests and I hope to see Selenium adopt some of these ideas in the future so that 3rd party packages like [Selenium Testing Library](https://github.com/anze3db/selenium-testing-library) will no longer be necessary.


