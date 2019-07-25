---
title: "Telling your story"
teaching: 30
exercises: 0
questions:
- How can we change the apparent git history to make it clearer
objectives:
- "Learn to change the way history appears"
keypoints:
- "Learnt to use git to revert changes and modify the last commit"
- "Learnt to change history in any way that we like to clean up our development story"
- "Learnt to continue from the last commit in master with `git pull --rebase`"
---
{% include links.md %}

## Episode setup
First we need to pull down some code from a remote repository, let's change directory to our Desktop
~~~
$ cd ~/Desktop
~~~
{: .language-bash}
and clone the code
~~~
$ git clone git@github.com:sa2c/example-gitflow-modified.git
~~~
{: .language-bash}
This is the gitflow repository with the changes we applied to it earlier in the workshop, but without merging the branches.
~~~
$ cd example-gitflow-modified
~~~
{: .language-bash}
Let's take a look at the remote branches in this repository
~~~
$ git branch -vv -a
~~~
{: .language-bash}
We've got one tracking branch (`master`) and a number of remote
branches, with some changes. Let's look at the history of the current
branch.
~~~
$ git log --oneline --graph -10
~~~
{: .language-bash}

## Reverting changes
We see a commit "added to AUTHORS file". Let's imagine that I'm feeling shy, and I would like to remove my name from the `AUTHORS` file. I can undo the effect of a previous commit with the `git revert` command

~~~
$ git revert e38a
~~~
{: .language-bash}
Git has added a commit which does the inverse of the commit we specified. Let's take a look at this
~~~
$ git show HEAD
~~~
{: .language-bash}
Notice that `git revert` creates a new commit. This is done
intentionally, so that we don't have to change any of the commits
already pushed to the remote (which other people may have access to).

## Rebasing
Let's have another look at our history of all branches
~~~
$ git log --oneline --graph -10 --all
~~~
{: .language-bash}
I created a feature branch `update-docs`, but let's imagine that
`update-docs` was much smaller than I intended. In git we have two
options on how to integrate changes: *merging* and *rebasing*. Merges
we've already encountered; with rebasing, rather than join two
branches together, we add commits from one branch to another, making
it look like the work was done on that branch all along.
Let's checkout `update-docs` with
~~~
$ git checkout update-docs
~~~
{: .language-bash}
and we'll rebase this onto `master`
~~~
$ git rebase master
~~~
{: .language-bash}
Git tried to move the commits, but it found that some of them modified the same line of text, so we've been dropped into a state similar to a merge. Let's take a look at the problem with
~~~
$ git status
~~~
{: .language-bash}
We can look in the file affected with
~~~
$ nano README.mdown
~~~
{: .language-bash}
We pick the second line, but change `nvie` to `sa2c`. Then we add the
file
~~~
$ git add README.mdown
~~~
{: .language-bash}
just as we would in a merge conflict. This time however, we ask the rebase to continue with
~~~
$ git rebase --continue
~~~
{: .language-bash}
We see the rebase applying the next commit, this time successfully. We
can see the result of the rebase using the same `git log` command
~~~
$ git log --oneline --graph -10 --all
~~~
{: .language-bash}
The `origin/update-docs` branch still exits, but git has moved the
changes on the local tracking branch to the end of the master branch,
as if we had been working there all along. Note that `master` and
`update-docs` are still different branches. Let's merge them
~~~
$ git checkout master
~~~
{: .language-bash}
and
~~~
$ git merge update-docs
~~~
{: .language-bash}
and see what happened with
~~~
$ git log --graph --oneline -5
~~~
{: .language-bash}
Looks like `master` and `update-docs` both now point to the same
commit. `master` has been fast-forwarded, because git noticed that the
history is linear and therefore there is no need for a merge.
> ## Beware the rebase
> <strong>Never rebase any commits which anyone else may have based any work off (i.e. commits that you have pushed)</strong>
>
> This is because rebase changes commit IDs, creating a parallel
> history of commits which contain similar content but are in fact not
> identically the same. This can cause problems to others.
>
> If you follow this simple rule, and only rebase your own personal
> branches, then you can rebase as much as you like.
{: .callout}

## Amending commits
Let's say we would like to make some changes to the last commit, let's say we want to add a new file and change the wording of the commit. We create a new file
~~~
$ touch newfile.txt
~~~
{: .language-bash}
We add it
~~~
$ git add newfile.txt
~~~
{: .language-bash}
and we commit it with `--amend` and a new message
~~~
$ git commit --amend -m 'This commit message has been changed'
~~~
{: .language-bash}
and we verify we've made a change with
~~~
$ git log --oneline -5
~~~
{: .language-bash}
This is an easy way to make changes immediately after we've made a
commit, and is perfectly safe provided we have not pushed the changes
yet. It's a great way of saving some "Oops" moments!

## Interactive rebasing
There is one more use of rebasing, the interactive rebase. This allows us to make arbitrary changes to our history before we push, to have commits appear exactly as we'd like them. Let's change the last 5 commits interactively
~~~
$ git checkout master
$ git rebase -i HEAD~5
~~~
{: .language-bash}
Let's make `AUTHORS` appear as if we'd done it last, but moving that
to the end of the list. And we save the file. Let's see our log
~~~
$ git log --oneline -10
~~~
{: .language-bash}
We can see that the `AUTHORS` commit now appears to have happened
last, despite the fact that in reality this is not the case.
Let's say that now we think we want to merge the merges which change
`README.mdown` text into one commit.
~~~
$ git rebase -i HEAD~5
~~~
{: .language-bash}
We edit the file to change the action on the last but one entry to be squash rather than pick. When prompted, we set the message to "Change wording in README.mdown". Let's look at the log again
~~~
$ git log --oneline -10
~~~
{: .language-bash}
Let's now say we want to change commit message. We've spotted "URLS",
and we prefer "URLs". We run the rebase command again
~~~
$ git rebase -i HEAD~5
~~~
{: .language-bash}
And change the action of the commit with URLS to reword. This pops up a message to reword the commit. We can check that the rewording was a success with
~~~
$ git log --oneline -10
~~~
{: .language-bash}
> ## Remember: we're changing commits
> Remember that every time we rebase, and change anything in any way,
> we're changing commit IDs. Never every do this to code that has been
> pushed or shared elsewhere.
{: .callout}

> ## A friendly warning
> Rebasing seems like a very powerful tool, but is best when used
> sparingly. Extensive rebases which change the order of commits, and
> cause many conflicts, can easily be prone to human error and can
> cause some of the intermediate commits in history to be in
> inconsistent states without the developer noticing. It's often best
> to avoid heavy rewrites of history, and reordering, and restrict
> rebasing to rewording and minor squashing commits where possible.
{: .callout}

## Pull with rebase
One of the most useful uses of rebase is if we have changes on our local version of master, and we would rather have a linear history rather than merges. In this case, when we pull, we can do a pull with a rebase. Let's see this in action. We'll checkout master
~~~
$ git checkout master
~~~
{: .language-bash}
And reset it back to the way it is was one commit before `origin/master`
~~~
$ git reset --hard origin/master~
~~~
{: .language-bash}
Let's make some changes and pull and see what happens. We add a new file
~~~
$ cat test.txt
~~~
{: .language-bash}
add the file and commit
~~~
$ add test.txt
$ git commit -m 'test commit'
~~~
{: .language-bash}
Let's look at our commits
~~~
$ git log --oneline --graph -10 origin/master master
~~~
{: .language-bash}
OK, so `master` and `origin/master` have diverged with one new commit
each. What happens if we pull now?
~~~
$ git pull
~~~
{: .language-bash}
Let's look at our commits
~~~
$ git log --oneline --graph -10 origin/master master
~~~
{: .language-bash}
We see that git has create a merge commit for us, merging the remote
and local versions of `master`. But, for a single commit, wouldn't it
be nicer if the commit just appeared after all the work that has been
done on `master`? Let's reset our repository before merge and try
again. We'll use the reflog to do that with
~~~
$ git reset --hard <commit-id>
~~~
{: .language-bash}
Let's check we've got the repository back to before the merge.
~~~
$ git log --oneline --graph -10 origin/master master
~~~
{: .language-bash}
So we could pull again, but how do we avoid those merge commits. The answer is a pull with rebase.
~~~
$ git pull --rebase
~~~
{: .language-bash}
Let's look at our history now
~~~
$ git log --oneline --graph -10 --all
~~~
{: .language-bash}
Rather than a merge commit, git has replayed our local changes on top of the current state of master, it looks as if all the changes happened in a linear history.

> ## It's safe to `pull --rebase`
> Pulling with rebase doesn't have many of the drawbacks of a normal
> rebase. Since our local changes are the ones which get rewritten, we
> know that with `git pull --rebase` that we won't cause problems to
> other people as we're re-writing history.
{: .callout}

## The good the bad and the ugly: rebase vs merge
There are two schools of though on the utility of rebasing.

On the one hand, you could view the commit history is a record of what actually happened. Changing it invalidates the validity of this historical record.

The other point of view is that the history should be a clear story, but not necessarily a historically accurate one, which describes in a useful way how the software came to be.

There is no right or wrong answer, but if we wish to do so, we can use rebasing to clean up own own *story* before we push to the world, as long as we never rebase anything we've already shared.
