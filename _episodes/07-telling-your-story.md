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
First we need to switch to some code
~~~
$ cd ~/git-demystified/episode_7.1
~~~
{: .language-bash}

Lets look at the history of the current branch.
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

## Reverting changes
We see a commit "Phantom commit" in our history. Remember that this adds the file phantom_file. Let us remove this file, by undoing all the changes in this commit.

~~~
$ cd ~/git-demystified/episode_7.1
~~~
{: .language-bash}

Check the file is there
~~~
$ ls
~~~
{: .language-bash}

And undo the change
~~~
$ git revert e93c7
~~~
{: .language-bash}
check the log
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}
Show the latest commit
~~~
$ git show HEAD
~~~
{: .language-bash}

Notice that `git revert` creates a new commit. This is done
intentionally, so that we don't have to change any of the commits
already pushed to the remote (which other people may have access to).

> ## Pushing
> Changing commits which other people have access to is a bad idea, because they won't be able to build on those commits. Never change history further back than where you have pushed. You can normally see this with the label `origin/current-branch-name` (e.g. `origin/master`) in your git log.
{: .callout}


## Rebasing
In git we have two options on how to integrate changes: *merging* and *rebasing*. Merges we've already encountered, and is by far the most common option. Always default to a merge if in doubt, but rebase gives you additional options with how to shape your git history.

Let us redo the previous merge as a rebase.
~~~
$ cd ~/git-demystified/episode_7.2
~~~
{: .language-bash}

~~~
$ git checkout another-phantom-tracker
~~~
{: .language-bash}

And try a rebase instead of merge this time. As before, we have a merge conflict that we have to resolve.
~~~
$ git rebase phantom-tracker
~~~
{: .language-bash}


~~~
$ git status
~~~
{: .language-bash}

Edit the merged file, choosing the lower option and a `Goblin`.
~~~
$ nano phantom_file
~~~
{: .language-bash}


add the merged file
~~~
$ git add phantom_file
~~~
{: .language-bash}
continue the rebase
~~~
$ git rebase --continue
~~~
{: .language-bash}

Have a look at the log
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

Look at the file
~~~
$ cat phantom_file
~~~
{: .language-bash}

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
$ git log --oneline --all --graph
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
