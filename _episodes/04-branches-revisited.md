---
title: "Branches revisited"
teaching: 30
exercises: 20
questions:
- How do branches work?
objectives:
- "Understand branches"
- "Understand conflicts"
keypoints:
- "Learnt how branches work in the context of trees, commits and blobs"
- "Learnt how to change branches and resolve commits"
---
{% include links.md %}


Let's say we're expecting to work on something by itself before sharing with the world. Branches are a good solution for this. Let's look at the changes we made in a previous section, but this time using branches.

We'll create new branches to contain these changes and merge them at a later date. This is a very common workflow in git that allows us to work on very long-running changes and short, quick-turnaround changes, in parallel without breaking the code. 

We'll move into our example-git-flow repository,
~~~
$ cd ~/example-gitflow
~~~
{: .language-bash}
And reset the respository to the way it was when we downloaded it
~~~
$ git reset --hard origin/master
~~~
{: .language-bash}

Let's create a new branch with:
~~~
$ git branch readme-url
~~~
{: .language-bash}
We can see all our branches with
~~~
$ git branch -v
~~~
{: .language-bash}
Notice, we're still on the master branch. We could switch branches right now, but let's make changes on this branch for the moment to see what happens.

Let's first take a look at our git log.
~~~
$ git log -4 --oneline
~~~
{: .language-bash}
Note that we have two branch names, on the same commit as HEAD.
> ## Decorations
>On some older versions of git, you may not see the decorations (e.g. HEAD and master). In this case you will need to add the argument `--decorate` to the `git log` command.
{: .callout}

> ## Branches are labels
>Based on our understanding of commits and chaining or commits, we can see understand branches now as simply a label for the latest commit in a chain. In this case `master` and `party-script` currently point to the same commit.
{: .callout}

We open README.mdown
~~~
$ nano README.mdown
~~~
{: .language-bash}
Add search for `nvie` and replace with `sa2c`. We'll check that we've made some changes
~~~
$ git diff
~~~
And add the file
~~~
$ git add README.mdown
~~~
{: .language-bash}
And double check with status
~~~
$ git status
~~~
{: .language-bash}
Now, let's move over to the readme-url branch
~~~
$ git checkout readme-url
~~~
{: .language-bash}
Remember, checkout moves us to another commit. We now note that it also switches branch when necessary. And we can see the branches again, with
~~~
$ git branch -v
~~~
{: .language-bash}
Note the asterisk next to the current branch. We can see that our repository is also in the same state as before:
~~~
$ git status
~~~
{: .language-bash}

When we commit, our commits always get added as children of the current commit, which in this case is on another branch. Let's create the commit
~~~
$ git commit -m 'Updated README.mdown URLs'
~~~
{: .language-bash}
We can see the commits with
~~~
$ git log -4 --oneline
~~~
{: .language-bash}
Note how readme-url has move forward by one commit, but the master branch has not. 
Although it isn't best practice, we'll also add our name to the AUTHORS list as well in this branch.
~~~
$ nano AUTHORS
~~~
{: .language-bash}
We'll check the change
~~~
$ git diff
~~~
{: .language-bash}
And if we're happy that the change is what we expect, we can add it as
~~~
$ git commit -a -m 'add to AUTHORS list'
~~~
{: .language-bash}

Let's go back to master and continue from there
~~~
$ git checkout master
~~~
{: .language-bash}
Let's create a second branch starting from master, that further changes README.mdown. We'll use a shortcut to create and checkout the branch in a single command this time
~~~
git checkout -b readme-faq
~~~
{: .language-bash}
We'll check the branch we're on with
~~~
git branch -v
~~~
{: .language-bash}
We should see an asterisk next to readme-faq, indicating we're on that branch.
Let's look at our repository now
~~~
$ git log -4 --oneline
~~~
{: .language-bash}
This only shows us the changes which are in the history of the current branch, we can show multiple branches by naming them
~~~
$ git log -4 --oneline master readme-url readme-faq
~~~
{: .language-bash}
Note the position of HEAD and how we can move HEAD by using checkout.
Now we'll adding the word "Please"" to the FAQ line, as before.
~~~
nano README.mdown
~~~
{: .language-bash}
It should read:
~~~
FAQ
---
See the [FAQ](http://github.com/nvie/gitflow/wiki/FAQ) section of the project
Wiki.
~~~
Let's check the changes
~~~
git diff
~~~
{: .language-bash}
And add if we're happy
~~~
git commit -a -m 'FAQ changes'
~~~
{: .language-bash}

We move back to master
~~~
$ git checkout master
~~~
{: .language-bash}
And check that we've moved
~~~
$ git branch -v
~~~
{: .language-bash}

We'll make some politeness changes directly in the master branch, because they're small and quick.
~~~
$ nano README.mdown
~~~
{: .language-bash}
We change the heading `Contributing` to read `Please contribute`, as we did earlier. We verify the change
~~~
$ git diff
~~~
{: .language-bash}
If we're happy, we'll commit everything with
~~~
$ git commit -a -m 'Politeness in contribution'
~~~
{: .language-bash}
Let's have a look at the branches now
~~~
$ git log -4 --oneline master readme-url readme-faq
~~~
{: .language-bash}
We can see all the commits, but they're in chronological order. It isn't immediately obvious which belong to which branches. We can fix this with
~~~
$ git log -4 --oneline --graph master readme-url readme-faq
~~~
{: .language-bash}

We've got three branches now, if we're happy with them, it's time to merge them. We'll check we're on the master branch
~~~
$ git checkout master
~~~
{: .language-bash}
We'll first merge the readme-faq branch
~~~
$ git merge readme-faq
~~~
{: .language-bash}
And check that it's merged in
~~~
$ git log -4 --oneline --graph --all
~~~
{: .language-bash}
We can see that a merge commit has been automatically created. This performs a merge by looking at how the files at the tips of the branches have changed since the branches forked. It then creates a single set of files which contains all of the changes. This is often called a three-way merge because there are three sets of files involved.

Note that a merge commit is special only in that it has multiple parents.

Let's look at the `readme-url` branch next
~~~
$ git merge readme-url
~~~
{: .language-bash}
Let's look at what went wrong
~~~
$ git status
~~~
{: .language-bash}
This time, we see that git has automatically resolved the changes in AUTHORS for us, but is complaining about the README.mdown file.

If we open this, we see that most lines are also resolved, for example the change of URL in the installation section.

But one particular line was changed in both branches differently, so git doesn't know what to do with this line. We're in a merge conflict, running
~~~
$ git log -5 --oneline --graph --all
~~~
{: .language-bash}
Note how we use `--all` as a shortcut for all references. We see that the branches are still not merged, and no merge commit has been created.

If this was an unexpected merge conflict, one thing we could do would be to back out of it with
~~~
$ git merge --abort
~~~
{: .language-bash}
And we can verify that we're no longer in a merge conflict with
~~~
$ git status
~~~
{: .language-bash}

Let's assume however that we want to resolve this merge conflict. We merge again with
~~~
$ git merge readme-url
~~~
{: .language-bash}
We see that the files in the working directory have been changed to match the changes from the merge, but we have some conflicts that need to be resolved before we can merge. Let's look at them in a text editor
~~~
$ nano README.mdown
~~~
{: .language-bash}
And we'll delete the first entry line. So that we keep the URL change. Then add the file with
~~~
git add README.mdown
~~~
{: .language-bash}
We'll check this out again with
~~~
$ git diff --staged
~~~
{: .language-bash}
Oh dear! We've accidentally deleted the Please line... but we noticed too late.

We can checkout from a merge however with
~~~
$ git checkout --conflict=merge README.mdown
~~~
{: .language-bash}
This checks the conflict file our of the repository. Let's look at the staged file again with
~~~
$ nano README.mdown
~~~
{: .language-bash}
We see the file is back to the way it was before.

Another useful trick with checkout is to show the difference between the original copy of the line and the lines that we see. In this case, we can use a similar command to get this information.
~~~
$ git checkout --conflict=diff3 README.mdown
~~~
{: .language-bash}
The conflicted file now shows three versions, the two current branches
and the original state of the line. This is often very useful to get
some context on what has changed and who changed it. Sometimes we
don't want a merged file, we just want the file as it was in a
specific branch. During a merge we can do this by running
~~~
$ git checkout --ours -- README.mdown
~~~
{: .language-bash}
to pick our file, notice how we have no url changes now, but we do have the FAQ changes.
~~~
$ cat README.mdown
~~~
{: .language-bash}
We could also choose only their changes, discarding all of ours
~~~
$ git checkout --theirs -- README.mdown
~~~
{: .language-bash}
This time, there are only changes of URL, but the changes to the FAQ section have been lost. We can verify this with
~~~
$ cat README.mdown
~~~
{: .language-bash}

>## Conflict resolution
>Create two branches which have some changes which will cause conflicts (i.e. are on the same line) and some changes which will not conflict. Merge the two branches.
>>## Solution
>>* Create a new branch from master, and choose some changes to make to a file.
>>* Checkout the master branch, and make some changes to the same file and different files. Make sure some of these changes are on the same line as the changes in the new branch.
>>* From the master branch, run `git merge new-branch`, where new-branch is the name of the new branch.
>>* Resolve the conflicts by editing the file and using the --conflict options.
>{: .solution}
{: .challenge}

>## Merge commits in depth
>Find the merge commit for two branches using `git cat-file -p`. What is different about this commit compared to other commits?
>>## Solution
>>* A merge commit has two (or more) parent commits, for example:
>>
>> ~~~
>> tree ebdba3aefd695fc21d498b6c1da1d19c0b99448a
>> parent 3130b68da842575ef4cca101f40c0a3ce672ecf2
>> parent 682c5ec88a4f4c5efd65291e4aa0fda21fcea9d8
>> author Mark Dawson <mark.dawson@swansea.ac.uk> 1564012142 +0100
>> committer Mark Dawson <mark.dawson@swansea.ac.uk> 1564012142 +0100
>> 
>> Merge branch 'readme-faq'
>> ~~~
>>{: .output}
>{: .solution}
{: .challenge}


>## Branches as heads
>What does the folder `.git/refs/heads/` contain? Can you use `git cat-file -p` to guess?
>>## Solution
>>Each file in the folder refers to the ID of a commit pointed to by a branch. These files define the branches.
>{: .solution}
{: .challenge}
