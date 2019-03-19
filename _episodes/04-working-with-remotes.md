---
title: "Working with remotes"
teaching: 0
exercises: 0
questions:
- How can I work in remote teams and with remotely hosted code?
objectives:
- ""
keypoints:
- ""
---
{% include links.md %}

# Multiple remotes
For much of this section, we will work in pairs, so find another person in the room. The first step is for everyone to grab a copy of the code at https://github.com/sa2c/gitflow. You can do this with
~~~
git clone https://github.com/sa2c/gitflow.git
~~~
Let's change to the gitflow repository we downloaded earlier.
~~~
cd ~/example-gitflow
~~~
Let's check that we're in the master branch with
~~~
git checkout master
~~~
We run the command
~~~
git remote -v
~~~
We see a single remote, named origin. This is set up for us by git clone when we create a new repository. It points to the place we downloaded the code for, in this case our fork of the code. Often, we may want to be able to pull changes directly from the repository we forked. For example if some other developers push some code there. We first need to add this as a second remote, with
~~~
git remote add upstream git@github.com:sa2c/example-gitflow
~~~
We now see two repositories, origin and upstream. We can add the -vv and -a flags to the git branch command to see all branches
~~~
git branch -vv -a
~~~
we can now pull from upstream with
~~~
git pull upstream master
~~~
This will pull from upstream/master into the current branch (master), we can then push any changes we've pulled down to own repository (origin), using.
~~~
git push origin master 
~~~
This was not very exiting, because there are no new changes in the master branch of upstream. But, there is in fact a hello-gitters branch which contains a small change based off master, that we can pull instead. Let's first fetch all the latest changes
~~~
git fetch -a
~~~
And take a look at upstream/hello-gitters
~~~
git log --oneline upstream/hello-gitters -5
~~~
This is based off master, so we should have no difficulty pulling it into master. Let's check what it contains
~~~
git diff upstream/hello-gitters master
~~~
Now that we're happy we want to merge it, we can pull with
~~~
git pull upstream hello-gitters
~~~
We could also choose to use git merge upstream/hello-gitters. We now push these changes to our repository with
~~~
git push
~~~

We can configure as many remotes as we like. If you work closely with friends or colleagues, it could be common for you to want to pull interesting changes from their remotes, incorporate those into your current branches, and push those changes to your remote.

# Creating new branches
What about branches other than master? Can we check those out and start work on them. Let's try it
~~~
git branch -vv -a
~~~
There's a branch called develop. We can check this out in a local branch, with
~~~
git checkout --track upstream/develop
~~~
Let's have a look at the result
~~~
git branch -vv -a
~~~
We can see that we are now on a local branch develop, which is configured to track the develop branch in upstream. Running git push and git pull in this branch will automatically push to the upstream branch. We can verify this with
~~~
git pull -v
~~~
We can also create new branches locally and push those to a specific remote. In this case, let's create a new branch 
~~~
git checkout -b test-branch
~~~
and check it was created
~~~
git branch -vv
~~~
We notice it doesn't push anywhere by default. What happens when we type git push?
~~~
git push
~~~
Git helpfully tells us there is no branch configured for push, and suggests how to set one
~~~
git push --set-upstream origin test-branch
~~~
Let's look at our branches, we see a local test-branch and a remotes/origin/test-branch which has been created locally. We probably want to make some changes to test-branch, let's add the git-party script again.
~~~
touch git-party
git add git-party
git commit -m 'Added git party'
~~~
And we can push these changes, this time git knows that these changes should go directly to origin/test-branch, so we can simply type
~~~
git push
~~~
Let's say we're finished working with test-branch locally, we could then delete the local branch
~~~
git checkout master
git branch -d test-branch
~~~
and check the branches
~~~
git branch -vv -a
~~~
We can see that the remote branch is still there, but the local branch is gone. If we did want to checkout the branch again, git provides a shortcut. Since only one of our remotes contains a branch called test-branch, and we have no local branches called test-branch, we can run
~~~
git checkout test-branch
~~~
Git will guess that in fact we probably wanted to checkout a local copy of the remote branch origin/test-branch. We can check that our work is still there with
~~~
git log
~~~
### Excercies:
Get in pairs, and add the repository of your partner to your repository as a new remote called "partner". Add a single commit to your develop branch. Can your partner tell you what you changed?
### Excercies:
Create a new branch, for-merge, and add a single commit to it, making any change of your choosing. What do the commands
git branch --merged master
and
git branch --un-merged master
show? Now merge the branch, using
git checkout master
git merge for-merge
What do the --merged and --un-merged options show now?

# Dangers of pushing
Note, many operations in git will modify the commit ID. This creates a completely independent and parallel history of commits. This is fine if we're the only person with access to these commits, but we should never do anything to commits that we've shared with the world which changes commit IDs. People will end up with versions of history that don't match outs. Fortunately, git will warn us if we try to rewrite history that already exists on a remote server with git push.
# Remote-tracking branches
 git fetch remote (to sync/update)
 git push <remote> <branchname>
 git push <remote> <branchname>:<branchname>
 checkout a remote branch:
 git checkout -b <localname> <remote>/<remotebranchname>
 -> gives a local branch, starts where remote/remotenbranchname is, can work with it, and it "tracks" remote branch
 -> "tracks" is much more fancy than it sounds, think "is associated with".
 ==> i.e. git pull auto-knows where to pull from

 master tracking branch auto-created on clone

 for convenience

 git checkout <remotebranchname>
 ==> creates a tracking branch if one doesn't exist

 set/change tracked branch with:
 git branch -u origin/trackedbranch

 note: you can use @{u} or @{upstream} to reference the remote tracked branch

 git branch -vv
 => what all the branches are up to (good to demo this when some are behind, some are ahead etc - not sure how to arrange this)

 done with a branch
 git push origin --delete branchname

# Tags [ needs to be after multiple remotes (so that one of the remotes is already set up) ]
 git tag <- show tags
 git tag -l "v1.8.5" <- show specific tags
 git tag -l "v1.8.*" <- show wildcard matching tag
 git tag -a "my-shiny-tag" -m "this is a shiny new tag"
 git show "my-shiny-tag" <- shows info about the tag
*** lightweight tags
  git tag "my-slightly-less-shiny-tag"
  git show "my-slightly-less-shiny-tag" <- just points directly to a commit, it doesn't have any special info
*** tag commits after i've moved past them
 git log --pretty=oneline
 git tag -a v1.2 <commit-id>  ==> would be nice if we had one repo, everyone the same
*** pushing tags
 git push <- push the tag
 - go on github => there is no tag here....!!!
 git push origin <tagname>
 - note that it shows in the output "[new tag] tag-name -> tag-name"
 - go on github, see that the new tag is there now
 what if we had LOADS of tags
 git push origin --tags
 - go on github and show that both the lightweight and the non-lightweight tags are there
*** Excercise
 => pick any historic commit in your shared repository, tag it (with either an annotated or normal tag) push it, get your partner to pull it, and checkout the same tag.
 => get your partner to tell you what the commit ID and commit message is. note: an identical commit message ALWAYS means an identical commit
 => checkout the tag with "git checkout <tag-name>" or "git checkout -b <tag-name>"
 => go back to where we were with "git checkout --force master"
 => need to do this after multiple remotes...
# Submodules
 In our repo:
 git submodule add https://github.com/chaconinc/DbConnector [DbConnector]
 git status
 -> note there are two files, .gitmodules, DBConnector
 Let's look inside the DBConnector directory
 ls DBConnector
 it contains the stuff we expected
 What if we do a diff
 git diff --cached
 We see that some content is added to the .gitmodules, but git knows to ignore the contents of the directory, and doesn't copy it.
 To add the submodule we need to commit this, we could also add other things to this commit, but we won't for now
 git commit -m 'added submodule'
*** Downloading submodules
 What happens when we download something with submodules? Let's do taht
 git clone ... some-name
 ls DBConnector/
 There is some content here
 git submodule init
 ls DbConnector
 ...git status....?
 ... QQQ: What happens when a connector does stuff...

*** Excercies:
 git clone --recurse-submodules https://github.com/chaconinc/MainProject
 is an alternative, do this. Call the file another-file. Check that you get the same as git submodule init
# fetching
do a git fetch
 - talk about fetch and merge first (manually)
 - then talk about pull (which does both)
git grep --heading --line-number 'foo bar'
