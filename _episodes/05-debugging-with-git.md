---
title: "Debugging with git"
teaching: 0
exercises: 0
questions:
- Open questions
objectives:
- ""
keypoints:
- ""
---
{% include links.md %}

# Downloading some code
First we need to grab a same repository, let's change to our home directory
~~~
git clone git@github.com:sa2c/example-hello-world.git ~/example-hello-world
~~~
and change into that repository
~~~
cd ~/example-hello-world
~~~
Let's take a look at the contents of this repository
~~~
ls
~~~
We see a single file, let's have a look inside it.
~~~
nano hello.sh
~~~
Since this is an example, most of the file does nothing. Only one line does any work, and it contains an error. Let's try to run the code
~~~
./hello.sh
~~~
This clearly has a problem, as expect. Let's look at the log history to see if we can spot it.
~~~

git log --oneline
~~~
We can see instantly a commit that might be causing the issue, the commit labelled "Changed echo to echom". In reality however, finding the problem wouldn't be this simple. In general, we might not know what file the problem is in, or where in that file. We may have hundreds of files with hundreds of lines each, and no idea where to start looking. Let's start by looking at the inital commit
~~~
git checkout 8750
~~~
And see if the hello.sh script runs here.
~~~
./hello.sh
~~~
That's good news. The file runs with no problems in the initial commit, somewhere between the two commits something went wrong. In this section, we will explore ways in which we can investiagte the sources of errors.

# Git blame

The first thing we might want to do is to look at the commit where a line was last modified. Let's try this with
~~~
git blame hello.sh
~~~
We see that most lines were created in the same commit, but some were modified later. Let's look more closely at one of those commits, the one where the line containing echom was changed.
~~~
git show b83
~~~
This commit did indeed add this line to the file. Another useful thing to do is to restrict the output of git blame to a specific sequence of lines. Let's say we're interested in lines 30 to 44, can run
~~~
git blame -L 30,44 hello.sh
~~~
Often we copy content between files in git, and something that might have started life in another commit, may only have been copied in the specified commit but might have been initially written in another commit and another file. We can get the original source of each line with the -C option, like this
~~~
git blame -C -L 30,44 hello.sh
~~~
Git blame is a very useful tool if you know the line that causes the issues in the first place, but you want to look at the commit message of that generated the line to check where it came from.

# Binary searching with git
We could checkout each commit one at a time, and check each one, but this is very time consuming. We'd have to check out each commit one at a time, like this
~~~
git checkout HEAD~7
git checkout HEAD~6
git checkout HEAD~5
...
git checkout HEAD~3
git checkout HEAD~2
git checkout HEAD~1
~~~
We can do better than this if we choose a half way point between the bad and good commit, check if that is good or bad, and keep choosing a half way point until we find the commit that causes the code to go from good to bad. Git can actually help us do this with the bisect command. Let's try it
~~~
git bisect start
~~~
We mark the current commit as bad
~~~
git bisect bad HEAD
~~~
Then we can mark the initial commit as good
~~~
git bisect good 8750
~~~
Git will now drop us at a commit half way between the good and the bad commits, we can verify this with
~~~
git log --oneline master
~~~
We see some commits marked as bad and good, and git has placed us in the middle commit. Now we can test this commit
~~~
./hello.sh
~~~
It works! The code wasn't broken at this point. Let's mark this commit as good
~~~
git bisect good
~~~
Great, git has moved us again. Let's check where we are this time
~~~
git log --oneline master
~~~
The markers for good and bad have moved, because we've given bisect more information, and HEAD has been placed between them. We know this is the first bad commit, but git doesn't know that yet. Let's test it
~~~
./hello.sh
~~~
This failed, as expected. Let's mark this as a bad commit
~~~
git bisect bad
~~~
That's odd. We found the bad commit, but git kept looking. Let's take a look
~~~
git log --oneline master
~~~
Git has marked the good and bad commits, but it doesn't know yet if the previous commit might have been the first bad one. It needs us to check that. Let's go ahead and do that
~~~
./hello.sh
~~~
This is a good commit, let's mark it
~~~
git bisect good
~~~
Finally, git has found the commit we were looking for and told us where it is. Let's see where we are
~~~
git log --oneline master
~~~
Git has marked the relevant commits as bad, but it hasn't moved us to the first bad commit. It left us in this pending state. Let's take a look at the content of the breaking commit
~~~
git show 05c0
~~~
Git is telling us that the problem was introduced by a change that happened on line 39 of hello.sh where echo was changed to echom. For us, this was probably a problem that is easy enough to resolve without using bisect, but for a large complex code base when we don't know where to start, bisect can instantly point us to the change which first caused the problem. Let's exit the bisect state and go back to master with
~~~
git bisect reset
~~~
This worked great, and we can go through large numbers of commits with this technique, but there was a lot of typing. Can git do a better job? It turns out that it can. Let's look at the return value of the hello.sh script
~~~
./hello.sh
echo $?
~~~
The variable $? is a special variable containing the return value of the function. In this case it is non-zero, indicating an error. Let's look at the historic commit
~~~
git log --oneline
git checkout 1153
~~~
And test the code
~~~
./hello.sh
echo $?
~~~
In this case the script returns 0, indicating success. This is a common convention in linux scripts, and you can write your own scripts that follow this convention. Git can use this convention to decide if a commit is good or bad. Let's try it
~~~
git bisect start HEAD 1153
~~~
Once again, git drops us in the middle of a commit. This time, instead of running the hello script, we tell git to run it for us
~~~
git bisect run './hello.sh'
~~~
Git does all the boring work for us. Every time it runs the command we gave and gets a zero return value, it marks the commit as good, every time it sees a non-zero value, it marks the commit as bad. It then tells us the first commit if finds which changes the state of the repository from "good" to "bad". Now that we're done, we exit again with
~~~
git bisect reset
~~~
This is a very powerful debugging tool, but it relies on all your code being in a runnable state, such that I can automatically identify. It works best when used with a branching and merging strategy, to ensure there are no breaking commits on the master branch.
