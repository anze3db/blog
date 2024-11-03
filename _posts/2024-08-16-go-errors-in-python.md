---
title: "Go-like Error Handling Makes no Sense in JavaScript or Python"
description: "Adding special syntax to Javascript or Python to allow Go-like error handling feels like a good idea at first glance, but I think it doesn't improve the issues with error handling in these two languages."
date: 2024-08-16 00:00:00 +0000
image: assets/cards/2024-08-16-go-errors-in-python.png
tags: python go javascript
---

Yesterday, I saw [this proposal](https://github.com/arthurfiorette/proposal-safe-assignment-operator) to add Golike error handling to Javascript, which got me thinking about whether or not this would make sense in my go-to language, Python.

**TLDR:** Even though I am a fan of Go's error handling, I don't think the safe assignment operator adds any value to Python or Javascript. For the real solution, we'd probably have to look at Java instead 😅

## Some background

I've spent the last few months writing Go code, and even though I found error handling in Go very odd at first, I've grown to like it more than I expected. I am now at a point where I kind of miss it when writing Python.

Go doesn't have a `try`/`catch` concept that we know in most other languages. Instead, any function that can `raise` returns an error as one of the return values. Error handling is then done with an if statement like this:

```go
resp, err := http.Get("http://example.com/")
if err != nil {
  // Handle error
}
```

You'll see `if` clauses like this all over the codebase at almost every function call. It seems lengthy at first, but after a while, you *get* it and start appreciating it.

The big win with this approach is that it forces every function to **document its errors**. You can't write a function that can raise an error without having the error in the function signature.

Go's error handling is great not because you use an if statement, but because you are <u>forced to write one</u> every time you might have an unexpected error.

[`Unwrap`](https://doc.rust-lang.org/rust-by-example/error/option_unwrap.html)'s popularity in Rust shows that handing errors with `if`/`match` statements will often be avoided if there is a better option (pun intended).

## Error handling in Python

In Python, a similar HTTP request is usually written as:

```python
response = requests.get("http://example.com/")
```

Nothing in this line of code tells you that something can go wrong with the `get` function call. The function signature doesn't tell you that `get` can raise a `ConnectionError`, and neither does the [documentation](https://requests.readthedocs.io/en/latest/api/#requests.get)! The only way to know that exceptions can be raised is to read the source code for `get` or remember it from past experience!

This is what bothers me about error handling in Python. **We sweep errors under the rug and assume that everything will be okay.** The machine will always have network access, right?

That's not always the case, and when it's not, you'll be woken up in the middle of the night with your production server on fire.

Even if you know that `requests.get` can raise a `ConnectionError,`, you will often forget to write the code to handle it because it's not in your face the same way as Go's error is.

## The Safe Assignment Operator

The idea behind the safe assignment operator is to be able to transform this code:

```python
try:
  response = requests.get("http://example.com/")
except Exception err:
  # Handle error
```

Into:

```python
response, error ?= requests.get("http://example.com/")
if error:
  # Handle error
```

It's syntactic sugar that removes one line of code and one indent. The real problem - knowing that the function can raise an exception - is not addressed.

If you don't know that `requests.get` can raise, you won't use the safe assignment operator the same way as you won't use a `try`/`except`.

## The real solution

If we really want to reduce the risk of overlooking error handling, the language we have to look at is not Go; it's *(unfortunately)* Java!

Java has a way to express raised exceptions in the function signature, by listing the possible raised exceptions with the `throws` keyword:

```java
class ThrowsExecp {
    static void fun() throws IllegalAccessException
    {
        System.out.println("Inside fun(). ");
        throw new IllegalAccessException("demo");
    }
}
```

So, not only does Java force you to catch and handle exceptions that each function can raise, but it also explicitly lists all the exception types that can be raised from within the function. This is one step above what Go does!

But, do we really need/want this in Python/Javascript? In some places, yes, but not everywhere! The beauty of Python is that you can write a one-off script in two minutes and never have to care about any types/errors or anything else! But then you can also write a Django monolith with millions of lines of code that has to work correctly **all the time**!

Therefore, the real solution should be to add some form of [optional exception checking](https://github.com/python/mypy/issues/1773) to tools like mypy and TypeScript.

## BONUS: Does every error even need to be handled?

Even in Go, you often can't deal with a particular error at the place where the function is called. Because of this, most exception handling in Go wraps the original error and then passes it up the stack:

```go
resp, err := http.Get("http://example.com/")
if err != nil {
  return nil, errors.Wrap(err, "error getting example.com")
}
```

This is the same thing that we do in Python/Javascript when we don't handle the exception at all:

```python
response = requests.get("http://example.com/)
```

Yes, we didn't add the custom message `error getting example.com` to the exception as in the Go version, but that's not really handling the error. We often don't need a custom message like this in Python/Javascript because the stack traces are richer and usually even include globals and locals. You don't need any additional information to successfully debug the problem.

So maybe we don't even need rigorous error checking when stack traces are the default [Go, you can also improve the DX around this!](https://github.com/golang/go/issues/63358).

## Verdict

It *pains* me to say this, but the Java solution would be a better fit for Python/TypeScript, than the proposal of the type safe assignment operator. Either that or we rewrite all existing code to use the equivalent of Rust's [Result](https://doc.rust-lang.org/std/result/).
