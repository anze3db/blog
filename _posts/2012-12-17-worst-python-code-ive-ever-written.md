---
layout: post
title: "Worst python code I've ever written"
tags: python
---


I was doing my homework for the bioinformatics class when I started experimenting with scope in Python. The first thing I noticed 
was that Python list comprehensions don't create a closure. This means that variables defined in the list comprehension 
bleed out into the current scope:

```python
>>> [i for i in range(10)]
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> i
9
>>> 
```


I've combined this with the fact that functions have access to variables from the same scope, and come up with this 
example:


```python
def dpt(s,t):
    def cost():
        gap = -5
        M[i,j] = max(
            M[i-1,j]+gap,
            M[i,j-1]+gap,
            M[i-1,j-1] + blosum(si, tj)
        )
        
    M = defaultdict(int)
    [cost() for i,si in enumerate(s) for j,tj in enumerate(t)]
    return M[len(s)-1, len(t)-1]
```

        
At first glance it doesn't seem like there is something horrbly wrong. But when you try to figure out what the `dpt` 
function actually does, you immediatly find something peculiar. There is function call in the list comprehension that 
takes no arguments. So why am I defining all those variables (`i`, `si`, `j` and `tj`) which aren't being used? 
I don't even need the enumerate calls, right? Wrong! All those variables are being put to good use *inside* the `cost()` 
function! Yes, the cost function has access to all those variables and hence doesn't *need* any paramters at all. 

When I showed this peace of code to my friends they all thought I was insane. We ended up agreing that code should not
be written like this as it makes your program very difficult to understand.

Just for kicks I included these two lines in the homework report as well:

```python
# Two horrible lines that turn the above string into a dict. I am sorry.
arr = [j.split(' ') for j in [i.strip().replace('  ', ' ') for i in b50]]
return reduce(lambda a,b: dict(a.items() + b.items()), [{(arr[0][j],arr[i][0]): int(arr[i][j]) for j in xrange(1, len(arr[i]))} for i in xrange(1,len(arr))])
```

I am a horrible person.
    
By the way, the homework assignment was to compare COX3 mitochondrial gene between multiple species and build an evolutionary tree.
Here is the resulting dendrogram with avrage linkage:

<a href="/assets/pics/dendro1.png" style="text-align:center;"><img class="" src="/assets/pics/dendro1.png"  width="700" alt="Dendrogram" /></a>

I'll probably post the full source code once all the assignments get graded.
