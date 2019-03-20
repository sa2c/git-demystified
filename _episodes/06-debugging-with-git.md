---
title: "Identifying breaking commits"
teaching: 30
exercises: 0
questions:
- How can I use git to track down problems in code?
objectives:
- "Learn to identify when and in what commit problems were introduced"
keypoints:
- "Learnt to use git blame to identify when a problem line was introduced"
- "Learnt to use binary searches to identify lines which first introduce a problem"
---
{% include links.md %}

## Episode setup
First we need to pull down some code from a remote repository, let's change to our Desktop
~~~
$ cd ~/Desktop
~~~
{: .language-bash}
and clone the code
~~~
$ git clone git@github.com:sa2c/example-hello-world.git
~~~
{: .language-bash}
and change into the fresh repository
~~~
$ cd example-hello-world
~~~
{: .language-bash}
Let's take a look at the contents of this repository
~~~
$ ls
~~~
{: .language-bash}
We see a small number of files; let's have a look inside `hello.sh`.
~~~
$ nano hello.sh
~~~
{: .language-bash}
Since this is an example, most of the file does nothing. Only one line does any work, and it contains an error. Let's try to run the code
~~~
$ ./hello.sh
~~~
{: .language-bash}
This clearly has a problem, as expect. Let's look at the log history to see if we can spot it.
~~~
$ git log --oneline
~~~
{: .language-bash}
If we looked at this for a while, can could probably spot the commit that might be causing the issue, the commit labelled "Changed echo to echom". In reality however, finding the problem wouldn't be this simple. In general, we might not know what file the problem is in, or where in that file. We may have hundreds of files with hundreds of lines each, and no idea where to start looking. Let's start by looking at the inital commit
~~~
$ git checkout 1153
~~~
{: .language-bash}
And see if the `hello.sh` script runs here.
~~~
$ ./hello.sh
~~~
{: .language-bash}
That's good news. The file runs with no problems in the initial commit, somewhere between the two commits something went wrong. In this section, we will explore ways in which we can investigate the sources of errors.
Let's move back to the tip of the master branch.
~~~
$ git checkout master
~~~
{: .language-bash}

## `git blame`

If we know where the problem is in the file, we might ask ourselves what introduced this problem. What commit introduced this line. Let's try this with
~~~
$ git blame hello.sh
~~~
{: .language-bash}
We see that most lines were created in the same commit, but some were modified in other commits. There are a lot of lines here, let's focus on the range 30 to 50
~~~
$ git blame -L 30,50 hello.sh
~~~
{: .language-bash}
That's better. Let's take a closer look at the commit on line 45.
~~~
$ git show da86
~~~
{: .language-bash}
That's interesting. We can see that the problematic line was in fact
copied from another file at this commit. This can make `git blame` a
little less useful, we would like to know the commit in which this set
of lines originally appeared in any file. Fortunately, we can ask `git
blame` to attempt to track movement between files
~~~
$ git blame -C -L 30,50 hello.sh
~~~
{: .language-bash}
`git blame` is a very useful tool if you know the line that causes the
issues in the first place, but you want to look at the commit message
of that generated the line to check where it came from. Now we can see
the lines were actually introduced in another commit, let's take a
look at that commit now
~~~
$ git show 8f67
~~~
{: .language-bash}


## Binary searching with git
We could checkout each commit one at a time, and check each one, but this is very time consuming. We'd have to check out each commit one at a time, like this
~~~
$ git checkout HEAD~7
$ git checkout HEAD~6
$ git checkout HEAD~5
...
$ git checkout HEAD~3
$ git checkout HEAD~2
$ git checkout HEAD~1
~~~
{: .language-bash}
We can do better than this if we choose a half way point between the
bad and good commit, check if that is good or bad, and keep choosing a
half way point until we find the commit that causes the code to go
from good to bad. Git can actually help us do this with the `git
bisect` command. Let's try it
~~~
$ git bisect start
~~~
{: .language-bash}
We mark the current commit as bad
~~~
$ git bisect bad HEAD
~~~
{: .language-bash}
Then we can mark the initial commit as good
~~~
$ git bisect good 1153
~~~
{: .language-bash}
Git will now drop us at a commit half way between the good and the bad commits, we can verify this with
~~~
$ git log --oneline master
~~~
{: .language-bash}
We see some commits marked as bad and good, and git has placed us in the middle commit. Now we can test this commit
~~~
$ ./hello.sh
~~~
{: .language-bash}
It works! The code wasn't broken at this point. Let's mark this commit as good
~~~
$ git bisect good
~~~
{: .language-bash}
Great, git has moved us again. Let's check where we are this time
~~~
$ git log --oneline master
~~~
{: .language-bash}
The markers for good and bad have moved, because we've given bisect more information, and `HEAD` has been placed between them. We know this is the first bad commit, but git doesn't know that yet. Let's test it
~~~
$ ./hello.sh
~~~
{: .language-bash}
This failed, as expected. Let's mark this as a bad commit
~~~
$ git bisect bad
~~~
{: .language-bash}
That's odd. We found the bad commit, but git kept looking. Let's take a look
~~~
$ git log --oneline master
~~~
{: .language-bash}
Git has marked the good and bad commits, but it doesn't know yet if the previous commit might have been the first bad one. It needs us to check that. Let's go ahead and do that
~~~
$ ./hello.sh
~~~
{: .language-bash}
This is a good commit, let's mark it
~~~
$ git bisect good
~~~
{: .language-bash}
Finally, git has found the commit we were looking for and told us where it is. Let's see where we are
~~~
$ git log --oneline master
~~~
{: .language-bash}
Git has marked the relevant commits as bad, but it hasn't moved us to the first bad commit. It left us in this pending state. Let's take a look at the content of the breaking commit
~~~
$ git show da86
~~~
{: .language-bash}
Git is telling us that the problem was introduced by a change that
happened on line 39 of `hello.sh` where `echo` was changed to
`echom`. For us, this was probably a problem that is easy enough to
resolve without using bisect, but for a large complex code base when
we don't know where to start, bisect can instantly point us to the
change which first caused the problem. Let's exit the bisect state and
go back to master with
~~~
$ git bisect reset
~~~
{: .language-bash}
This worked great, and we can go through large numbers of commits with
this technique, but there was a lot of typing. Can git do a better
job? It turns out that it can. Let's look at the return value of the
`hello.sh` script
~~~
$ ./hello.sh
$ echo $?
~~~
{: .language-bash}
The variable `$?` is a special variable containing the return value of
the function. In this case it is non-zero, indicating an error. Let's
look at the historic commit
~~~
$ git log --oneline
$ git checkout 1153
~~~
{: .language-bash}
And test the code
~~~
$ ./hello.sh
$ echo $?
~~~
{: .language-bash}
In this case the script returns 0, indicating success. This is a
common convention in Unix scripts, and you can write your own scripts
that follow this convention. Git can use this convention to decide if
a commit is good or bad. Let's try it
~~~
$ git bisect start HEAD 1153
~~~
{: .language-bash}
Once again, git drops us in the middle of a commit. This time, instead
of running `hello.sh`, we tell git to run it for us
~~~
$ git bisect run './hello.sh'
~~~
{: .language-bash}
Git does all the boring work for us. Every time it runs the command we gave and gets a zero return value, it marks the commit as good, every time it sees a non-zero value, it marks the commit as bad. It then tells us the first commit if finds which changes the state of the repository from "good" to "bad". Now that we're done, we exit again with
~~~
$ git bisect reset
~~~
{: .language-bash}

>## One caveat
> This is a very powerful debugging tool, but it relies on all your
> code being in a runnable state, such that git can automatically
> identify when this state changes. It works best when used with a
> branching and merging strategy, to ensure there are no breaking
> commits on the master branch.
{: .callout}
