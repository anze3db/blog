---
layout: post
title: "Useful GNU/Linux tools"
tags: linux
---


GNU/Linux is awesome because it gives you a whole lot of simple but useful tools that you can play with. Utilities like `dd`, `sed`, `grep`, `rm`, `find`, `ssh` and many others all have a small sea of parameters that make them do exactly what you want. 

Unfortunately I am very bad at remembering different parameter names and whether or not they should be written in lowercase or uppercase. Thankfully it is very easy to create aliases or even your very own executables. Following is a brief description of some utilities I have made to make my life a bit easier. I've put them all in a [github repository](https://github.com/Smotko/linux-tools) so feel free to fork and/or send pull requests with suggestions!

grepr
-----

    export GREP_OPTIONS='--color=auto'
    grep -rnC ${2:-3} "$1" *

It's a simple `grep` wrapper that forces the grep utility to become recursive by default. The first parameter to grepr is the phrase you're searching for, while the optional second parameter specifies the number of lines above and below the search term to be shown. 

rmr
---

    find . -name $1 | xargs rm
    
`rmr` is similar to grepr. It makes the rm utility recursive. It's useful when you have a bunch of files that end up with .orig in multiple subfolders. You would just write rmr \*.orig to delete them all.


sedre
-----
   
    sed -i "s/$1/$2/g" $3
   
Sedre replaces all of the occurances of the first paramtere with the second parameter in the file specified by the third parameter.


seddl
----

    sed -i "$1d" $2
    
Seddl removes a line from a file. You would write `sed 4 myfile` to remove the fourth line from myfile.

screenshots
----------

    while true; do scrot "%Y-%m-%d_%H-%M_$2.png" & sleep $1; done

Screenshots is a utility I intend to use when I'll be doing my next game jam. It's basically an endless loop that makes screenshots. The first parameter is the number of seconds between screenshots, while the second parameter is a name for the generated pics.


