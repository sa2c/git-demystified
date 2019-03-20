---
title: "Reset and checkout"
teaching: 30
exercises: 20
questions:
- What are the differences between reset and checkout and when should I use them?
objectives:
- "Be able to manipulate the content of the worktree, staging area and commit"
- "Be able to change the last in a branch"
- "Be able to move to historical states of the repository"
keypoints:
- "Learnt to change the state of the index, working tree using git reset"
- "Learnt to change the commit which this branch points to with git reset"
- "Learnt to selectively pick up historical versions of files with git checkout"
---
{% include links.md %}

We've already seen some examples of the git checkout. In this section we'll explore the checkout command further, and see how they work in practice.
# Reset
 ~~~
 git clone git@github.com:sa2c/example-blacksheep.git ~/example-blacksheep
 ~~~
 This is a very simple repository, let's see what it does. We change into this directory
 ~~~
 cd ~/example-blacksheep
 ~~~
 Let's take a look at the files
 ~~~
 cat blacksheep.txt
 ~~~
 This contains a few lines from the well-known nursery rhyme.

 What about the others?
 ~~~
 cat README.txt
 ~~~
 This contains some simple README text. It is usually a good idea to have one of these in your repository. And the final file:
 ~~~
 cat commit-number.txt
 ~~~
 This contain a number, this is an incrementing number for each commit. Let's look at the commit history:
 ~~~
 git log --oneline
 ~~~
 Seems like we've added parts of the famous nursery rhyme "Baa, baa, black sheep". Since this is a very simple repostitory, let's take a look at the contents of every commit, we can do this with by asking log for patches
 ~~~
 git log -p
 ~~~
 This command would likely be too much information for all but a simple repository, but in this case it's exactly what we need.

# Reset soft
Let's say that we decide after creating the commits that this is too granular. We created the last three commits independently when we were writing the file, but actually, since they're on the same line, it now makes sense to us to group them logically into a single commit. Let's do this with the reset command
~~~
git reset --soft HEAD~3
~~~
The reset command, with --soft specified, is the simplest variation of the reset command. It simply moves or sets the tip of the current branch to point to a specified commit. In this case, it points it back by three commits, effectively discarding the later commits. Let's take a look
~~~
git status
~~~
Since the staging area and working directory are not touched by git reset --soft, we still have some changes ready to commit.
Let's see what they are:
~~~
git diff --staged
~~~
We see that the change to commit, i.e. the difference between the files in the staging area and the files in the last commit of the current branch, is indeed all of the changes made in the last three commits. Let's not commit these as one change to get the change history we wanted:
~~~
git commit -m 'Added: Yes, sir, yes, sir, three bags full!'
~~~
Let's take a look at our log to check what has happened
~~~
git log -p
~~~
There are now only two commits, and each one adds a complete line to the file. Note that we created a whole new commit. The old commits are still there if we want them, we can change the repository back to the way it was before by resetting the current branch to the commit which we first downloaded. Let's do that now:
~~~
 git reset --soft origin/master
~~~
And let's check the repository again, with
~~~
git log -p
~~~

>## Reset and commit IDs
> Use git reset to throw away the last commit, but keep the changes in the index, like this:
> ~~~
> git reset HEAD~
> ~~~
> Check that this has work successfully with using a git log command. Recreate the commit with the same commit message, like this:
> ~~~
> git commit -m ', three bags full'
> ~~~
> What do you notice that is different about the commit.
>
> You can use
> ~~~
> git cat-file -p <some-commit-id>
> ~~~
>where <some-commit-id> is the ID of a commit, to show all the information that git knows about that commit (and many other objects). Can you guess by running this command why the commit id might be different? Can you guess what might happen if someone else tried to pull your work after you change a commit ID?
>>## Solution
>>Recreating a commit changes the commit ID. You should not do this if this is a commit that you have already shared with others, as git will see these as two independent commits. If you push this to a repository, other people may not be able to integrate it with their work.
>{: .solution}
>
{: .challenge}

# Reset HEAD and the staging area
 What happens when we leave out the --soft option? The default in that case is to perform a "mixed" reset. Let's see how this works:
~~~
 git reset HEAD~2
~~~
Let's see what this has done
~~~
git status
~~~
This time the changes appear to be in the working directory as before, but not in the staging area.
Running git log,
~~~
git log --oneline origin/master
~~~
shows us that HEAD has indeed moved back by two commits. Let's check the files out with:
~~~
git diff
~~~
It appears that the changes from the last two commits indeed waiting to be staged. This is because the contents of the commit that HEAD has been moved to has also been copied into the staging area. This is useful if we want to rewind, to change a set of commits, but actually want to manually add just the files you're interested in.

>## Back to a clean slate
> Copying the contents of a file from the current commit is often the opposite action to adding some changes. Make some changes to a file, add that file to the staging area, and use git reset to undo the action of git add.
>
>>## Solution
>>Add changes to a file with
>>~~~
>> git add <file>
>>~~~
>>then reset the files with
>>~~~
>> git reset <file>
>>~~~
>>or
>>~~~
>> git reset HEAD <file>
>>~~
>>or
>>~~~
>> git reset HEAD -- <file>
>>~~
>>Note how if we leave out HEAD, then git will assume we want to pull from the HEAD reference by default.
>{: .solution}
>
{: .challenge}

What happens if we have two files? Make changes to two files, add them both to the staging area, then use
~~~
git reset
~~~
to undo the addition to the staging area. Not that not specifying a commit will use HEAD by default. What happens to the second file? What happens to the working directory files?

# Reset everything : treat with care
The final type of reset we can do is called a "hard" reset. Hard is the "next level up" from mixed. Let's first move our repository back to the way it was before with a mixed reset
~~~
 git reset origin/master
~~~
We'll check that this is the case.
~~~
git status
~~~
Some of you will probably see a status message showing no changes, so the working directory, staging area and current commit are identical. Those of you who've changed files will probably see some changes ready to commit. Don't worry. Let's open the file blacksheep.txt and add the line:
~~~
One for the faster and one of same.
~~~
We check what is ready to commit:
~~~
git diff
~~~
Let's add this file to commit, maybe we hadn't spotted the typos yet. And, let's create a commit
~~~
git commit -m 'Added another line'
~~~
And check that it behaved as we expected
~~~
git log -p
~~~
Ahhh....but now we spot our mistake!

We could use a mixed reset to step back by one commit, and then change the files - but maybe we would rather just go back to before we made the changes in the first place and reset the files as well. This is where a hard reset comes in. It does everything a mixed reset does, but also drops all the changes. Let's try it
~~~
git reset --hard HEAD~
~~~
We expect no changes in the working directory, let's check that
~~~
git status
~~~
We also expect the file to be back as it was before we made the changes
~~~
cat blacksheep.txt
~~~
And finally, we expect the final commit to have disappeared, let us check the log
~~~
git log
~~~

Be VERY, VERY careful with a hard reset. If there are changes in your working directory that haven't been committed yet, you can very easily lose them. It is one of the very few commands in git that will allow you to delete some of your work. If you use this command, it is very likely that you are *trying* to lose changed - make sure this is what you want.

>## Back to a clean slate
>
> reset --hard is most useful to throw away all the changes in the current working directory (and the staging area) and start again from the files in the last commit (HEAD). Make some changes in your repository, without adding them to the staging area, check them with git status, then blow away the changes by doing a hard reset to HEAD.
> Use git status to check that the changes have gone.
>
>Do the same thing again, but this time try add changes to the staging area before doing a hard reset.
>>## Solution
>>Make some changes to any files in the current directory. Verify that changes have been made with
>>~~~
>> git status
>>~~~
>>then reset the files with
>>~~~
>> git reset --hard HEAD
>>~~~
>>you will lose your changes in this way. Check that the changes have gone with
>>~~~
>> git status
>>~~~
>>The files in both the working directory and the index will be reset.
>{: .solution}
>
{: .challenge}


>## Without a HEAD
>
> What happens if we do a hard reset, but leave out the place to copy files from, like this
> ~~~
> git reset --hard
> ~~~
>
>Can you work out where the files come from
>Hint: it may help to make some changes to the files in the current directory first.
>>## Solution
>>If the origin of the files is not specified, it is assumed to be HEAD by default.
>{: .solution}
>
{: .challenge}

Note that if you don't tell reset where to take files from, the files are taken from HEAD by default.
What happens if you make some modification to README.mdown, add these changes to the staging area with
# Commit-level Checkout
 git reset --hard origin/master
 We'll add some content to the file README.txt.
 ~~~
 A sample repository containing the nursery rhyme "Baa, baa, black sheep"
 Let's make some changes to the README.txt in our working directory.
 ~~~
 Let's now grab the changes as they where three commits ago, maybe we want to have a look at that version of the repository because we know it was working.
 ~~~
 git checkout -q HEAD~3
 ~~~
 Git hasn't complained about the changes in the working directory, what has it done with them?
 ~~~
 git status
 ~~~
 There are some changes to README.txt, let's see what they are
 ~~~
 git diff
 ~~~
 Git has checkout out the files as they were three commits ago, but has left the changes in our local repository, because these changes were made to another file. Let's verify that the contents of the repository has in fact changed
 ~~~
 cat blacksheep.txt
 ~~~
 and the log
 ~~~
 git log -2 --oneline origin/master
 ~~~
 We can see that the current commit, HEAD, has been moved back by three commits, but that master (and origin/master) are in the same place. This is useful if we want to move around and look around, without changing the branches themselves. We can go back to where we were with
 ~~~
 git checkout master
 ~~~
 Let's get rid of our changes, and this time make changes to blacksheep.txt
 ~~~
 git reset --hard
 ~~~
 And we edit the file to look like this
 ~~~
 Baa, baa, black sheep, have you any wool?
 Yes, sir, yes, sir, three bags full!
 One for me and one for you
 ~~~
 And we run the exact same checkout command again
 ~~~
 git checkout -q HEAD~3
 ~~~
 This time, git has refused to do the checkout, because the file we have been changing would also have been changed by the checkout. This is much safer than using a reset --hard, as it preserves our work and prevents us from losing current changes.

## Checkout without -q
 The -q we've seen in the previous section stands for "quiet", it tells git that we're not interested in hearing about any problems. This normallly *isn't* the behaviour we would like. Let's see what happens with the same checkout commands without the -q option.

First we move back to master
~~~
git checkout master
~~~
This appears to behave exactly the same as before. Next we move back three commits, as we did previously
~~~
git checkout HEAD~3
~~~
Now we can see that we get a long warning message about a detached HEAD. This means that we're not on any branch, if we continue from where we are now, we will be creating and "alternate past", with a different set of parallel changes. Unless these we create a branch to keep these, we will lose them. Git helpfully tells us that what we probably want is to use the -b option to create a new branch that will hold this information.

>## a-HEAD or not on a-HEAD
> What happens when we use reset to move when we're in a detached HEAD state? How does it differ from when we use reset when a branch is checked out? Run the following two sets of commands - what do they do differently? What is different in output of the final log command? Why?
>~~~
>git checkout master
>git checkout HEAD~1
>git reset --hard <commit-id>
>git log --oneline origin/master
>~~~
>
>~~~
>git checkout master
>git reset  --hard <commit-id>
>git log --oneline origin/master
>~~~
>>## Solution
>>When reset is run and we are not on any branch (e.g. in a detached HEAD state), then the reset command cannot change the current branch. It is an operation that doesn't make sense when we have no current branch. In this case, reset will simply move the pointer HEAD, leaving the branch where it is.
>{: .solution}
>
{: .challenge}
# Checkout of only specific files
 Both the checkout and reset commands can take files as arguments, in this case they behave quite differently. Let's reset our repository to the way it is on the remote server
 ~~~
 git reset --hard origin/master
 ~~~
 Let us take a look at the content of the commit-number.txt
 ~~~
 cat commit-number.txt
 ~~~
 Now, let's perform a checkout, this time specifying the commit-number.txt file.
 ~~~
 git checkout HEAD~3 -- commit-number.txt
 ~~~
 We check what has happened with
 ~~~
 git log --oneline origin/master
 ~~~
 We see that we're still on the same commit, HEAD hasn't moved this time. It doesn't make sense to move HEAD for some files and keep it in the same place for others, that would get confusing very quickly. Only the file copy operations have been performed. Let's see what effect this has had.
 ~~~
 git status
 ~~~
 The file commit-number.txt has been copied from the previous commit HEAD~3 into both our working directory as well and into the staging area. We can verify the changes with
 ~~~
 git diff --staged
 ~~~
 The file commit-number.txt has changed and nothing else has. In this case git checkout with a file behaves very much like we would expect git reset --hard to behave with files. It overrides the file in the staging area and working directory and resets any changes. For this reason
 ~~~
 git reset --hard HEAD~3 -- commit-number.txt
 ~~~
 This is not a valid command, since it would perform the same operation as the git checkout command. Using git reset however does allow us to copy specific files to and from the index, leaving the working directory unchanged.
 Let's reset our repository to the way it was at the beginning of this lesson
 ~~~
 git reset --hard origin/master
 ~~~
 Let's make some changes to README.txt
 ~~~
 A sample repository containing the nursery rhyme "Baa, baa, black sheep".
 This repository is used to demonstrate reset and checkout for git.
 ~~~
 and copy them to the staging area.
 ~~~
 git add README.txt
 ~~~
 We can use git reset to copy the version in the repository back, effectively undoing the add. First we check the status of the file we changed
 ~~~
 git status
 ~~~
 Now we can unstage the file with
 ~~~
 git reset HEAD -- README.txt
 ~~~
 If we leave out the specification of the commit, HEAD in this case, git will default to HEAD. Let's add the file again
 ~~~
 git add README.txt
 ~~~
 and check the status
 ~~~
 git status
 ~~~
 Now we reset, or unstage, the file with
 ~~~
 git reset README.txt
 ~~~
 Note, only the mixed (default) version of reset makes sense with files. Changing the position of the branch tip (i.e. --soft) doesn't make sense with files, and --hard is equivalent ot checkout.

>## The dangers of checkout
>
> What happens if you make some modification to README.mdown, add these changes to the staging area with
> ~~~
> git add README.mdown
> ~~~
> and then try to checkout the file with
> ~~~
> git checkout HEAD -- README.mdown
> ~~~
> Can you guess what will happen? Is this potentially dangerous to do?
>
>>## Solution
>>The command
>>~~~
>> git checkout HEAD -- <filename>
>>~~~
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
>>~~~
>> git checkout HEAD~4 -- README.mdown
>>~~~
>>All that remains is to create a new commit, with a command such as
>>~~~
>>git commit -m 'README.mdown as it was in HEAD~4'
>>~~~
>{: .solution}
>
{: .challenge}

>## Without a HEAD
>
> Can you work out what the following command does
>>~~~
>> git checkout -- README.mdown
>>~~~
> Hint: try making some changes to README.mdown and running the command.
>>## Solution
>>This command will revert the file README.mdown to the state it is in the current commit. This is equivalent to running
>>~~~
>> git checkout HEAD -- README.mdown
>>~~~
>>If the commit is not specified, git defaults to using HEAD.
>{: .solution}
>
{: .challenge}
# The Reference Log
 Let's change directory back to the gitflow repository from earlier
 ~~~
 cd ~/example-gitflow
 ~~~
 Let's check we're on the master branch, with
 ~~~
 git checkout master
 ~~~
 And we'll create a file in our repository
 ~~~
 touch this-file-will-be-lost.txt
 ~~~
 And add it
 ~~~
 git add this-file-will-be-lost.txt
 ~~~
 Bit we won't commit it, let's check the state of the repository
 ~~~
 git status
 ~~~
 And let's take a look at the history
 ~~~
 git log --oneline --graph -10
 ~~~
 OK, I don't like this, I'm going to delete it all and go back to the way it was before we started this morning.
 ~~~
 git reset --hard origin/master
 ~~~
 Bam! We appear to have lost all the hard work we put in this morning. Is there a way to get it back? The branch master has changed, so it's no good looking at that. Remember, a commit doesn't know its children, so it's no good starting from the current commit to look for later commits. Let's use the following command
 ~~~
 git log -g
 ~~~
 This looks just like the output of git log, but in fact shows all the actions which have changed the reference HEAD (i.e. the current commit). If we wanted all the actions which have changed the branch master, we could run
 ~~~
 git log -g master
 ~~~
 Once we identify the commit we want, we can refer to it either with the commit ID or with its position in the appropriate reflog. Let's take a look at the commit before we move to it
 ~~~
 git show HEAD@{5}
 ~~~
 That looks like the commit we want, let's reset the current branch to that point
 git reset --hard HEAD@{1}
 This means "go back to the state HEAD was in one moves ago". We could also have used a reference such as master@{1} here, if we wanted the master branch.
 We can verify that the current branch has changed in the way we wanted with
 ~~~
 git log --oneline --graph --all
 ~~~

 We can also use references anywhere we would normally use a commit, for example
 ~~~
 git log master@{yesterday}
 ~~~
 or
 ~~~
 git show master@{2.hours.ago}
 ~~~

# Referring to Commits
 We've seen a bunch of different type of arguments passed to commands such as git checkout. For example, references to HEAD
 ~~~
 git log -1 HEAD
 ~~~
 or to a local branch
 ~~~
 git log -1 master
 ~~~
 or a remote branch
 ~~~
 git log -1 origin/master
 ~~~
 or a tagged commit
 ~~~
 git log -1 0.4.1
 ~~~
 or a reference log entry
 ~~~
 git log -1 HEAD@{5}
 ~~~
 or a reference as it was some time ago
 ~~~
 git log -1 master@{1.hour.10.minutes.ago}
 ~~~
 or an abbreviated commit ID
 ~~~
 git log -1 1ffb
 ~~~
 or a stash references
 ~~~
 git log stash@{1}
 ~~~
 or an ancestry reference
 ~~~
 git log HEAD~3
 ~~~

 Git is clever about allow you to use any way is most convenient, and will ultimately (in most cases) translate them all to a commit reference behind the scenes.
