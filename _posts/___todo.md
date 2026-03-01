get_attrib

Often in codebases you'll have to get some JSON data from a third party. You might not even know if the data have to access properties in that json without knowing if they are there or not. In Python you'll probably end up writing code that looks like something like this:

```python
json_dict = fetch_json_from_somewhere()
my_prop = json_dict.get("first_property", {}).get("second_nested_property", {}).get("just_one_more_level", None)
```

The idea is that you want my_prop to be set if all the nested values were present but to be None if we either couldn't get to it or if the value was not set.

The first problem that you'll have is that your code will fail if one of the nested properties isn't missing but is set to an unexpected value:

```python
json_dict = {"first_property": None}
```

In this case first_property isn't a dict so our code will fail!

```python
Traceback (most recent call last):
  File "<python-input-5>", line 1, in <module>
    json_dict.get("first_property", {}).get("other", None)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get
```

So maybe what we should actually do is

```python
my_prop = ((json_dict.get("first_property") or {}).get("second_property") or {}).get("just_one_more_level", None)
```

And this will fix this particular problem but it still won't be fool proof because you never know, the json_api could return first property as a truthy string:

```python
json_dict = {"first_property": "sneaky string"}
```

And now your code will fail:


```python
Traceback (most recent call last):
  File "<python-input-8>", line 1, in <module>
    my_prop = ((json_dict.get("first_property") or {}).get("second_property") or {}).get("just_one_more_level", None)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'get'
```

So at this point we are probably getting desperate and so we might consider writing a function helper:

```python
def get_nested_property(obj: dict, property_path: str) -> Any
    ...
```

And now we can finally safely get our nested property like so:

```python
my_prop = get_nested_property(json_dict, "first_property.second_property.just_one_more_level")
```

This looks like a decent compromise but I've lived with a codebase that used this function extensively and it has left me like this


PTSD DOG IMAGE

The main issue was that you could never exactly knew the shape of your data and when you had to figure out where a particular `None` came from you never knew if it was from the `first_property`, `second_property` or somewhere else. This made debugging production issues very difficult.

Random typos were also a problem. if you accidentally typed `frist_property` the code wouldn't happily return `None` all the time and you might not even notice until it causes problems in production.

Lastly, the `get_nested_property` also grew to support indexing into lists and tuples and of course object properties. This made everything a lot worse because looking at the code you didn't even know if you are dealing with dicts or objects!


## Proper solution?

So how do you deal with the verbose syntax of `json_dict.get("first_property") or {}`? First of all, is it really that verbose? Compared to similar code in other languages I'd say it isn't that bad. Take Go as an example:

```go
if first_property, ok := json_dict["first_property"].(map[string]interface{}); ok {
    if second_property, ok := first_property["second_property"].(map[string]interface{}) {
        if just_one_more_level, ok := second_property["just_one_more_level"] {

        }
    }
}
```

There is PEP-505 that proposed unaware operators so that we could write python code like

```python
first_property?.second_property?.just_one_more_level
```

But it has been deferred for several years now and it might not even happen. And even if it did land in a future version of Python you'll have a very similar problem as with the `get_nested_property` function because you won't know the shape of your data.

Also you don't have to write `get_nested_property` yourself. There are existing pacakges about it on PyPI. But I think the best way to handle this is to take control of your data. Write out the structure of your data and then parse the thing.

```python
@dataclass
class JustOneMoreLevel:
    my_prop: str = ""
@dataclass
class FirstProperty:
    second_property: SecondProperty = field(default=lambda: SecondProperty())
@dataclass
class MyJson:
    first_property: FirstProperty = field(default=lambda: FirstProperty())
```

If you make things not nullable hopefully your libarary of choice will give you a nice error when they are None and you can handle that case seperately.

```python
try:
    parse(json_string, MyJson)
except:
    # You should know what went wrong here
```

And then you use a library of your choice (lots of opinions here as well but that's for another blog post) to coerce your JSON into your types (erroring out when e.g. first_property is an unexpected type).

And then you can finally do:

```python
my_json_parsed.first_property.second_property.just_one_more_level
```

And everybody that sees the code will know exactly what the shape of the data that you are workin with actually looks like.

