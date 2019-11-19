---
title: "Working with branches"
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
$ cd ~/example-gitflow-branches
~~~
{: .language-bash}

We can list all the commits with
~~~
$ git log -4 --oneline master readme-url readme-faq
~~~
{: .language-bash}

OK, lot's of changes here, but there is some information we're not seeing here
~~~
$ git log -4 --oneline --graph master readme-url readme-faq
~~~
{: .language-bash}

It can be tedious to type every reference, we can use:
~~~
$ git log -4 --oneline --graph --all
~~~
{: .language-bash}

Let's create a new branch
~~~
$ git branch my-branch
~~~
{: .language-bash}

And check what are branches are
~~~
$ git branch -v
~~~
{: .language-bash}

We're still on the master branch, let's switch to our new branch
~~~
$ git checkout my-branch
~~~
{: .language-bash}

Let's make a change
~~~
$ touch some-change
~~~
{: .language-bash}

And check the status
~~~
$ git status
~~~
{: .language-bash}

And commit the change
~~~
$ git commit -a -m 'A commit'
~~~
{: .language-bash}

Our log now shows we've got multiple versions
~~~
$ git log -4 --oneline --graph --all
~~~
{: .language-bash}
Let's create another branch, in one command
~~~
$ git checkout -b another-branch
~~~
{: .language-bash}

How does our tree look now?
~~~
$ git log -4 --oneline --graph --all
~~~
{: .language-bash}
Let's no go back to master:
~~~
$ git checkout master
~~~
{: .language-bash}

~~~
$ git log -4 --oneline --graph --all
~~~
{: .language-bash}
Let's try to delete our branch
~~~
$ git branch --delete --force my-branch another-branch
~~~
{: .language-bash}
Git won't let us delete something isn't merged, that's helpful:
~~~
$ git branch --delete --force my-branch another-branch
~~~
{: .language-bash}

Now let's take a look at the branches that existed before. We'll first merge the readme-faq branch
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
