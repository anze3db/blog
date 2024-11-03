---
layout: post
title: "Learning Haskell, wrote startsWith a bunch of times"
tags: haskell
---


So I started learning Haskell a day or so ago. I dived right into <http://learnyouahaskell.com> and read through the first few chapters. As soon as I learned how to write an if statement and got familiar with some basic list functions (head, tail and such) I started experimenting with my own code. I don't know why, but I decided to implement a simple startsWith function, here is the first version:

{% highlight haskell %}
    startsWith' l s =
        if null s then
            True
        else 
            if null l then
                False
            else 
                if head l == head s then
                    startsWith' (tail l) (tail s)
                else
                    False
{% endhighlight haskell %} 

Now I know what you are thinking. This looks horrible and I know I shouldn't write code that looks like this. I agree completely, but at the time of writing I only knew really basic Haskell syntax. After reading another chapter I quickly improved my code:

{% highlight haskell %}
    startsWith' _ [] = True
    startsWith' [] _ = False
    startsWith' l s =
        if head l == head s then
            startsWith' (tail l) (tail s)
        else
            False
{% endhighlight haskell %}
              
Writing code like this is familiar to me as I have done some Prolog programming for a class. It seems 'academic' programming languages tend to borrow each others ideas almost as much as other languages do! I was also delighted to see that, similarly to Prolog, Haskell provides a shortcut for retrieving the head and the tail of the list:

{% highlight haskell %}
    startsWith' _ [] = True
    startsWith' [] _ = False
    startsWith' (hl:tl) (hs:ts) =
        if hl == hs then
            startsWith' tl ts
        else
            False
{% endhighlight haskell %}

But unfortunately this is where similarities between these two languages end. If this was Prolog I could get rid of the last if statement like this:

{% highlight haskell %}
    startsWith' _ [] = True
    startsWith' [] _ = False
    startsWith' (h:tl) (h:ts) = startsWith' tl ts
    startsWith' _ _ = False
{% endhighlight haskell %}

Notice that the `h` variable has been 'defined' twice. Prolog magically understands this as the head of the first list needs to be the same as the head of the second list. Awesome, right? Thankfully Haskell didn't leave me hanging. It has something called 'guards' and with their help I got rid of the last if statement:

{% highlight haskell %}
    startsWith' _ [] = True
    startsWith' [] _ = False
    startsWith' (hl:tl) (hs:ts) 
        | hl == hs = startsWith' tl ts
        | otherwise = False
{% endhighlight haskell %}

I would not be embarrassed to introduce this last code snippet to my mother. It's a great improvement over the hideous first version. I have not yet reached the end of the tutorial and there are probably ways of improving it even further. Any ideas? 

I like Haskell so far. The reason I started learning it in the first place was because I wanted to improve my coding in general. Learning a purely functional language seemed like a good idea as it teaches you all about side effects and makes your brain think differently. This something an engineers brain should know how to do...
