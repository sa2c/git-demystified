---
title: "Changing History"
teaching: 30
exercises: 20
questions:
- I've just made a mistake, how can I undo it?
objectives:
- "Be able to manipulate the content of the worktree, staging area and commit"
- "Be able to change the last in a branch"
- "Understand HEAD and the latest commit"
- "Be able to move to historical states of the repository"
keypoints:
- "Learnt to change the state of the index, working tree using git reset"
- "Learnt to change the commit which this branch points to with git reset"
- "Learnt to selectively pick up historical versions of files with git checkout"
- "Understand HEAD, master and the latest commit"
---
{% include links.md %}

In the last lesson we learnt about commits and how they chain together to form a sequence. In this lesson we'll start to learn how to manipulate that sequence of commits, in the context of the three trees. We'll explore this with a simple repository.

## Exploring the repository
~~~
$ cd ~/git-demystified/example-blacksheep
~~~
{: .language-bash}
Let's take a look at the files
~~~
$ cat blacksheep.txt
~~~
{: .language-bash}
This contains a few lines from the well-known nursery rhyme.

What about the others?
~~~
$ cat README.txt
~~~
{: .language-bash}
This contains some simple README text. It is usually a good idea to have one of these in your repository. And the final file:
~~~
$ cat commit-number.txt
~~~
{: .language-bash}
This contain a number, this is an incrementing number for each commit. Let's look at the commit history:
~~~
$ git log --oneline
~~~
{: .language-bash}
Seems like we've added parts of the famous nursery rhyme "Baa, baa,
black sheep" incrementally. Since this is a very small repostitory, let's take a
look at the contents of every commit, we can do this with by asking
`git log` for patches
~~~
$ git log -p
~~~
{: .language-bash}
This command would likely be too much information for all but a simple repository, but in this case it's exactly what we need.

# Reset
The reset command is used to manipulate the state of the three trees (working directory, staging area and current commit).

## Reset soft
Let's say that we decide after creating the commits we saw previously are too granular. We created the last three commits independently when we were writing the file, but actually, since they're on the same line, it now makes sense to us to group them logically into a single commit. Let's do this with the reset command
~~~
$ git reset --soft HEAD~3
~~~
{: .language-bash}
The `git reset` command, with `--soft` specified, is the simplest variation of the reset command. It simply moves or sets the tip of the current branch to point to a specified commit. In this case, it points it back by three commits, effectively discarding the later commits. Let's take a look
~~~
$ git status
~~~
{: .language-bash}
Since the staging area and working directory are not touched by git reset `--soft`, we still have the same changes ready to commit.
Let's see what they are:
~~~
$ git diff --staged
~~~
{: .language-bash}
We see that the change to commit, i.e. the difference between the files in the staging area and the files in the last commit of the current branch, is indeed all of the changes made in the last three commits. Let's not commit these as one change to get the change history we wanted:
~~~
$ git commit -m 'Added: Yes, sir, yes, sir, three bags full!'
~~~
{: .language-bash}
Let's take a look at our log to check what has happened
~~~
$ git log -p
~~~
{: .language-bash}
There are now only two commits, and each one adds a complete line to the file. Note that we created a whole new commit.

## Undoing the change
The old commits are still there if we want them, we can change the repository back to the way it was before by resetting the current branch to the commit which we first downloaded. Let's do that now, to get the excercise back to the point it was when we started.
~~~
$ git reset --soft origin/master
~~~
{: .language-bash}
The reference `origin/master` is created by `git clone`, and is a reference to the `master` branch on the remote repository. We'll explain this in more detail later.

Let's look at the repository history again, with
~~~
$ git log -p
~~~
{: .language-bash}

## Reset HEAD and the staging area
In this case, we had all of our content in the staging area reading to commit again. This can be useful when making changes to the commit, but usually we might want to be able to add it again. This is useful if we want to rewind some changes, and re-commit them as a different set of commits.

When we leave out the `--soft` option the default in that case is to perform a "mixed" reset. We could use `--mixed` to indicate this, but since it's the default we'll leave this out. This works by moving `HEAD`, and then copying the current contents of `HEAD` into the staging area. Effectively, this un-adds files.

Let's see how it works.
~~~
$ git reset HEAD~2
~~~
{: .language-bash}
What has this done?
~~~
$ git status
~~~
{: .language-bash}
This time the difference appear are in the working directory, like in the --soft option, but the staging area is the same as current `HEAD`.

We can confirm that HEAD has moved back by two commits with:
~~~
$ git log --oneline
~~~
{: .language-bash}
And see the differences with:
~~~
$ git diff
~~~
{: .language-bash}
The changes from the last two commits all waiting to be staged. This is because the contents of the commit that HEAD has been moved to has _also_ been copied into the staging area.

We can reset our repository to the way it was before with
~~~
$ git reset origin/master
~~~
{: .language-bash}
And check this with
~~~
$ git status
~~~
{: .language-bash}
and
~~~
$ git log
~~~

## Reset everything: treat with care
The final type of reset we can do is called a "hard" reset. Hard is the "next level up" from mixed.

Let's open the file blacksheep.txt and add the line:
~~~
One for the faster and one of same.
~~~
We check what is ready to commit:
~~~
$ git diff
~~~
{: .language-bash}
Let's add this file to commit, maybe we hadn't spotted the typos yet. And, let's create a commit
~~~
$ git commit -m 'Added another line'
~~~
{: .language-bash}
And check that it behaved as we expected
~~~
$ git log -p
~~~
{: .language-bash}
Ahhh....but now we spot our mistake!

We could use a mixed reset to step back by one commit, and then change the files - but maybe we would rather just go back to before we made the changes in the first place and reset the files as well. This is where a hard reset comes in. It does everything a mixed reset does, but also drops all the changes in the working directory. Let's try it
~~~
$ git reset --hard HEAD~
~~~
{: .language-bash}
We expect no changes in the working directory, let's check that
~~~
$ git status
~~~
{: .language-bash}
We also expect the file to be back as it was before we made the changes
~~~
$ cat blacksheep.txt
~~~
{: .language-bash}
And finally, we expect the final commit to have disappeared, let us check the log
~~~
$ git log
~~~
{: .language-bash}

Be VERY, VERY careful with a hard reset. If there are changes in your working directory that haven't been committed yet, you can very easily lose them. It is one of the very few commands in git that will allow you to delete some of your work. If you use this command, it is very likely that you are *trying* to lose changed - make sure this is what you want.

>## What about the commits?
> Before attempting this challenge, reset your repository with `git reset --hard origin/master`
>
> Use git reset to throw away the last commit, but keep the changes in the index:
> ~~~
> $ git reset HEAD~
> ~~~
> {: .language-bash}
> Check that this has work successfully with using a git log command. Recreate the commit with the same commit message:
> ~~~
> $ git commit -m ', three bags full'
> ~~~
> {: .language-bash}
> What do you notice that is different about the commit.
>
> You can use
> ~~~
> $ git cat-file -p <some-commit-id>
> ~~~
> to take a closer look.
> {: .language-bash}
> where `<some-commit-id>` is the ID of a commit, to show all the information that git knows about that commit (and many other objects). Can you guess by running this command why the commit id might be different? Can you guess what might happen if you had already shared this commit with someone else and they had work based on it?
>> ## Solution
>> Recreating a commit changes the commit ID. You should not do this if this is a commit that you have already shared with others, as git will see these as two independent commits. If you push this to a repository, other people may not be able to integrate it with their work.
>{: .solution}
>
{: .challenge}

>## Back in time 
> Before attempting this challenge, reset your repository with `git reset --hard origin/master`
>
> Copying the contents of a file from the current commit is often the opposite action to adding some changes. You can restrict the action of reset to a file with:
>~~~
>git reset -- filename
>~~~
>{: .language-bash}
> Make some changes to a file, add that file to the staging area, and use git reset to undo the action of git add.
>
>>## Solution
>>Add changes to a file with
>> ~~~
>> $ git add <file>
>> ~~~
>> {: .language-bash}
>> then reset the files with
>> ~~~
>> $ git reset -- <file>
>> ~~~
>> {: .language-bash}
>> or
>> ~~~
>> $ git reset HEAD -- <file>
>> ~~~
>> {: .language-bash}
>> or
>> ~~~
>> git reset HEAD -- <file>
>> ~~~
>> {: .language-bash}
>> Note how if we leave out HEAD, then git will assume we want to pull
>> from the HEAD reference by default.
>{: .solution}
>
{: .challenge}

>## Gone with the wind
> Before attempting this challenge, reset your repository with `git reset --hard origin/master`
>
> `git reset --hard` is most useful to throw away all the changes in the current working directory (and the staging area) and start again from the files in the last commit (HEAD). Make some changes in your repository, without adding them to the staging area, check them with git status, then blow away the changes by doing a hard reset to HEAD.
> Use `git status` to check that the changes have gone.
>
>Do the same thing again, but this time try add changes to the staging area before doing a hard reset.
>>## Solution
>>Make some changes to any files in the current directory. Verify that changes have been made with
>> ~~~
>> $ git status
>> ~~~
>> {: .language-bash}
>>then reset the files with
>> ~~~
>> $ git reset --hard HEAD
>> ~~~
>> {: .language-bash}
>>you will lose your changes in this way. Check that the changes have gone with
>> ~~~
>> $ git status
>> ~~~
>> {: .language-bash}
>>The files in both the working directory and the index will be reset.
>{: .solution}
>
{: .challenge}


>## Without a HEAD
>
> What happens if we do a hard reset, but leave out the place to copy files from, like this
> ~~~
> $ git reset --hard
> ~~~
> {: .language-bash}
>
>Can you work out where the files come from
>Hint: it may help to make some changes to the files in the current directory first.
>>## Solution
>>If the origin of the files is not specified, it is assumed to be HEAD by default.
>{: .solution}
>
{: .challenge}

# Checkout on files
The checkout command from earlier has an important variant when passed files as arguments. In this case they behaves very differently. Let's reset our repository to the way it is on the remote server to begin with.
~~~
$ git reset --hard origin/master
~~~
{: .language-bash}
Let us take a look at the content of the `commit-number.txt`
~~~
$ cat commit-number.txt
~~~
{: .language-bash}
Now, let's perform a checkout, this time specifying the `commit-number.txt` file.
~~~
$ git checkout HEAD~3 -- commit-number.txt
~~~
{: .language-bash}

What happened? Previously checkout would have moved `HEAD`.
~~~
$ git log --oneline origin/master
~~~
{: .language-bash}
In fact, we're still on the same commit, HEAD hasn't moved at all this time. It doesn't make sense to move HEAD for some files and keep it in the same place for others, that would get confusing very quickly. Only the file copy operations have been performed. Let's see what effect this has had.
~~~
$ git status
~~~
{: .language-bash}
The file `commit-number.txt` has been copied from the previous commit HEAD~3 into both our working directory as well and into the staging area. We can verify the changes with
~~~
$ git diff --staged
~~~
{: .language-bash}
The file `commit-number.txt` has changed and nothing else has. In this case git checkout with a file behaves very much like we would expect `git reset --hard` to behave with files. It overrides the file in the staging area and working directory and resets any changes. For this reason
~~~
$ git reset --hard HEAD~3 -- commit-number.txt
~~~
{: .language-bash}
This is not a valid command, since it would perform the same operation as the `git checkout` command.

# Reset with files
Using `git reset` with files allow us to copy specific files to and from the index, leaving the working directory unchanged.
Let's reset our repository to the way it was at the beginning of this lesson
~~~
$ git reset --hard origin/master
~~~
{: .language-bash}
Let's make some changes to `README.txt`
~~~
A sample repository containing the nursery rhyme "Baa, baa, black sheep".
This repository is used to demonstrate reset and checkout for git.
~~~
and copy them to the staging area.
~~~
$ git add README.txt
$ git status
~~~
{: .language-bash}
We can use git reset to copy the version in the repository back, effectively undoing the add.

We can unstage the file with
~~~
$ git reset HEAD -- README.txt
~~~
{: .language-bash}

> ## Shorthand Reset
> If we leave out the specification of the commit, HEAD in this case, git will default to HEAD. Let's add the file again. We could have achieved this with `git reset README.txt`
{: .callout}

> ## Just one reset
> Note, only the mixed (default) version of reset makes sense with files. Changing only the position of the branch label (i.e. `--soft`) doesn't make sense with files. The `--hard` variant would make sense, but is equivalent to checkout with files, so doesn't exist.
{: .callout}

>## a-HEAD or not on a-HEAD
> What happens when we use reset to move when we're in a detached HEAD state? How does it differ from when we use reset when a branch is checked out? Run the following two sets of commands - what do they do differently? What is different in output of the final log command? Why?
> ~~~
> $ git checkout master
> $ git checkout HEAD~1
> $ git reset --hard <commit-id>
> $ git log --oneline origin/master
> ~~~
> {: .language-bash}
>
> ~~~
> $ git checkout master
> $ git reset  --hard <commit-id>
> $ git log --oneline origin/master
> ~~~
> {: .language-bash}
>>## Solution
>>When reset is run and we are not on any branch (e.g. in a detached HEAD state), then the reset command cannot change the current branch. It is an operation that doesn't make sense when we have no current branch. In this case, reset will simply move the pointer HEAD, leaving the branch where it is.
>{: .solution}
>
{: .challenge}

>## The disappearing command
> What happens if you run `reset --soft HEAD -- <filename>` or `reset --hard HEAD -- <filename>` with a file in the working directory? Can you guess why this is the behaviour?
>>## Solution
>>Neither of these two commands exist. `reset --soft` with files makes no sense, since `--soft` operates on the current commit only.
>> `reset --hard` with files could make sense, but would be exactly the same as `checkout` with files, therefore only one of the two is implemented.
>{: .solution}
{: .challenge}

>## The dangers of checkout
>
> What happens if you make some modification to README.mdown, add these changes to the staging area with
> ~~~
> $ git add README.mdown
> ~~~
> {: .language-bash}
> and then try to checkout the file with
> ~~~
> $ git checkout HEAD -- README.mdown
> ~~~
> {: .language-bash}
> Can you guess what will happen? Is this potentially dangerous to do?
>
>>## Solution
>>The command
>> ~~~
>> $ git checkout HEAD -- <filename>
>> ~~~
>> {: .language-bash}
>>will overwrite the file filename, even if there are changes. Be careful as you can
>>lose your changes in this way. This command is a useful way to undo any changes you may have made to the files in your working directory.
>{: .solution}
>
{: .challenge}

>## The way things were
>
> Can you use the checkout command to create a commit which contains the file README.mdown as it was 4 commits ago?
> Hint you can refer to four commits ago with HEAD~4
>>## Solution
>>The file can be brought into the current directory with
>> ~~~
>> $ git checkout HEAD~4 -- README.mdown
>> ~~~
>> {: .language-bash}
>> All that remains is to create a new commit, with a command such as
>> ~~~
>> $ git commit -m 'README.mdown as it was in HEAD~4'
>> ~~~
>> {: .language-bash}
>{: .solution}
>
{: .challenge}

>## Without a HEAD
>
> Can you work out what the following command does
>> ~~~
>> $ git checkout -- README.mdown
>> ~~~
>> {: .language-bash}
> Hint: try making some changes to README.mdown and running the command.
>>## Solution
>>This command will revert the file README.mdown to the state it is in the current commit. This is equivalent to running
>> ~~~
>> $ git checkout HEAD -- README.mdown
>> ~~~
>> {: .language-bash}
>>If the commit is not specified, git defaults to using HEAD.
>{: .solution}
>
{: .challenge}
## The Reference Log
Let's change directory back to the gitflow repository from earlier
~~~
$ cd ~/example-gitflow
~~~
{: .language-bash}
Let's check we're on the master branch, with
~~~
$ git checkout master
~~~
{: .language-bash}
And we'll create a file in our repository
~~~
$ touch this-file-will-be-lost.txt
~~~
{: .language-bash}
And add it
~~~
$ git add this-file-will-be-lost.txt
~~~
{: .language-bash}
Bit we won't commit it, let's check the state of the repository
~~~
$ git status
~~~
{: .language-bash}
And let's take a look at the history
~~~
$ git log --oneline --graph -10
~~~
{: .language-bash}
OK, I don't like this, I'm going to delete it all and go back to the way it was before we started this morning.
~~~
$ git reset --hard origin/master
~~~
{: .language-bash}
Bam! We appear to have lost all the hard work we put in this morning. Is there a way to get it back? The branch master has changed, so it's no good looking at that. Remember, a commit doesn't know its children, so it's no good starting from the current commit to look for later commits. Let's use the following command
~~~
$ git log -g
~~~
{: .language-bash}
This looks just like the output of git log, but in fact shows all the actions which have changed the reference HEAD (i.e. the current commit). If we wanted all the actions which have changed the branch master, we could run
~~~
$ git log -g master
~~~
{: .language-bash}
Once we identify the commit we want, we can refer to it either with the commit ID or with its position in the appropriate reflog. Let's take a look at the commit before we move to it
~~~
$ git show HEAD@{5}
~~~
{: .language-bash}
That looks like the commit we want, let's reset the current branch to that point
~~~
$ git reset --hard HEAD@{1}
~~~
{: .language-bash}
This means "go back to the state HEAD was in one moves ago". We could also have used a reference such as `master@{1}` here, if we wanted the master branch.
We can verify that the current branch has changed in the way we wanted with
~~~
$ git log --oneline --graph --all
~~~
{: .language-bash}

We can also use references anywhere we would normally use a commit, for example
~~~
$ git log master@{yesterday}
~~~
{: .language-bash}
or
~~~
$ git show master@{2.hours.ago}
~~~
{: .language-bash}

## Referring to Commits
We've seen a bunch of different type of arguments passed to commands such as git checkout. For example, references to HEAD
~~~
$ git log -1 HEAD
~~~
{: .language-bash}
or to a local branch
~~~
$ git log -1 master
~~~
{: .language-bash}
or a remote branch
~~~
$ git log -1 origin/master
~~~
{: .language-bash}
or a tagged commit
~~~
$ git log -1 0.4.1
~~~
{: .language-bash}
or a reference log entry
~~~
$ git log -1 HEAD@{5}
~~~
{: .language-bash}
or a reference as it was some time ago
~~~
$ git log -1 master@{1.hour.10.minutes.ago}
~~~
{: .language-bash}
or an abbreviated commit ID
~~~
$ git log -1 1ffb
~~~
{: .language-bash}
or a stash references
~~~
$ git log stash@{1}
~~~
{: .language-bash}
or an ancestry reference
~~~
$ git log HEAD~3
~~~
{: .language-bash}

Git is clever about allow you to use any way is most convenient, and will ultimately (in most cases) translate them all to a commit reference behind the scenes.
