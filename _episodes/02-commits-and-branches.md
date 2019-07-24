---
title: "Committing and Branching"
teaching: 45
exercises: 0
questions:
- How do commits work and how do I create branches?
objectives:
- "Gentle reminder of basic git usage"
- "Understanding of how git handles changes"
keypoints:
- "Understand how files end up in the staging area"
- "Understand how the staging area is turned into a commit"
- "Being able to inspect commits blobs and trees"
---
{% include links.md %}

In this section we'll start by talking about things that may be familiar, such as adding and commit, and then moving into talking about branching workflows.

## A simple git branching workflow
Let's create a copy of a repository that we can work on, by visiting the repository at
<a href='https://github.com/sa2c/example-gitflow'>
    https://github.com/sa2c/example-gitflow
</a>
and clicking on the fork icon in the top right corner. We then change to our home directory with the following command
~~~
$ cd ~/
~~~
{: .language-bash}
Once the repository has forked with can clone it with
~~~
$ git clone git@github.com:<your-github-username>/example-gitflow.git
~~~
{: .language-bash}
This command will output something like
~~~
$ git clone git@github.com:<your-github-username>/example-gitflow.git
Cloning into 'example-gitflow'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 1410 (delta 0), reused 2 (delta 0), pack-reused 1407
Receiving objects: 100% (1410/1410), 484.97 KiB | 295.00 KiB/s, done.
Resolving deltas: 100% (796/796), done.
~~~
{: .output}
If you see a message which says something like
~~~
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
~~~
{: .output}
then there is an issue with your ssh setup. Take another look at the
previous episode, or ask a helper to check if with you. Once you've
cloned the respository, change into that directory with
~~~
$ cd example-gitflow
~~~
{: .language-bash}
Let's say that the first thing we would like to do is to add ourselves to the AUTHORS list, seeing as we'll be making some changes. Let's assume we've talked to the maintainer, and they're happy for us to do so.
~~~
$ nano AUTHORS
~~~
{: .language-bash}
Add your name to the end of the list. We check that git has seen the change
~~~
$ git status
~~~
{: .language-bash}
The status command tells us that the AUTHORS file has been modified, but not added to the repository. It can be helpful to think of git as manipulating three sets of files, the working directory, the staging area and the current commit (known as HEAD). Asking git for its status simply compares these three sets of files, and highlights the differences to us. If we always think of git as copying files between these three areas, what it does will seem much less mysterious.
~~~
$ git add AUTHORS
~~~
{: .language-bash}
We can think of this action as copying the file AUTHORS into the staging area. The staging area is a set of files that we think of as the "next proposed commit".

Let's  the state of our repository, with
~~~
$ git status
~~~
{: .language-bash}
We now see the AUTHORS file under "Changes to be committed", which tells us that it's different between the staging area and the current commit. But it is not under "Changes not staged for commit", so it is the same between the working directory and the staging area.
Lets make some further changes to the working directory files, by deleting the line we added to the top of the AUTHORS file.
Looking at the status now
~~~
$ git status
~~~
{: .language-bash}
shows us the file both under "Changes to be committed" as well as "Changes not staged for commit", indicating that the file is different in all three areas. We can create a commit from the changes as they are in the staging are, by typing:
~~~
$  git commit -m 'Added to the AUTHORS list'
~~~
{: .language-bash}
We have now created a new current commit, by copying the files as they were in the staging area. We therefore expect that the files in the staging area and the current commit are the same. Running git status will verify this:
~~~
$ git status
~~~
{: .language-bash}
We see the same differences between the working directory and staging areas as before, but no differences between staging area and the current commit. This makes sense, since one was just created from the other.

Let's try and do this all again, but this time, imagine that we're starting a long running feature, which might have many commits and might break the state of the repository whilst we're doing it. Let's imagine that we're changing the documentation, to make it more friendly and informative.

We add a sentence to the end of the introductory section
~~~
git-flow
========

A collection of Git extensions to provide high-level repository operations
for Vincent Driessen's [branching model](http://nvie.com/git-model "original
blog post"). These scripts automate the management of branches.
~~~

We also want to feel like a community, so we change the installation section to look like this
~~~
Installing git-flow

-------------------
See our Wiki for up-to-date [Installation Instructions](https://github.com/nvie/gitflow/wiki/Installation).
~~~
(Note we changed "the Wiki" to "our Wiki".) Let's check that git has picked up our changes with. 
~~~
$ git status
~~~
{: .language-bash}
Let's add our changes, but let's divide it into two commits
~~~
$ git add -p README.mdown
~~~
{: .language-bash}
This looks confusing. Let's hit the <kbd>?</kbd> key to review out options. We choose video content related changes with <kbd>y</kbd> and reject all other changes with <kbd>n</kbd>. Now that we have crafted a commit, let's see what git status says.
~~~
$ git status
~~~
{: .language-bash}
We now see the file both under "Changes to be committed" and under "Changes not staged for commit", so like before the file is different in all of the three areas. In the working directory it has all of our changes, in the staging area it has the changes we selected with `git add -p`, and in the current commit it has no changes at all (yet).
> ## Manipulating files, not changes
Git hasn't chosen parts of the file or checked changes into the staging area. It just created for us a version of the file with only some of the changes, the file in the staging area may never have existed with the exact same contents in the working directory.
{: .callout}
Let's see how the files in the staging look compared to the latest commit.
~~~
$ git diff --staged
~~~
{: .language-bash}
And how the working directory looks compared to the staging area
~~~
$ git diff
~~~
{: .language-bash}
We're happy, so we can commit
~~~
$ git commit -m 'Expanded on the introduction'
~~~
{: .language-bash}
Let's take a look at the differences which are left with
~~~
$ git status
~~~
{: .language-bash}
and
~~~
$ git diff
~~~
{: .language-bash}
Once we're happy that this can all go into one commit, we'll add it and commit, using
~~~
$ git add README.mdown
~~~
{: .language-bash}
and
~~~
$ git commit -m 'Changed wording to be more inclusive'
~~~
{: .language-bash}
Let's have a look at our history as it is currently with
~~~
$ git log
~~~
{: .language-bash}
Let's say that we notice that the URL in the documentation is wrong. This is a small change, and we're happy to make this change directly in master so that everyone sees the change immediately. We will do it using the sed command
~~~
$ sed -i 's&github.com/nvie&github.com/sa2c&g' README.mdown
~~~
{: .language-bash}
Let's see what this command has done
~~~
$ git diff
~~~
{: .language-bash}
You should see only changes to README.mdown. We want to add this and create a commit, we can add the files to the staging area and commit with
~~~
$ git add README.mdown
$ git commit -m 'Fixed URLS in README.mdown'
~~~
{: .language-bash}
Let's have a look at our changes now, we use
~~~
$ git log --oneline
~~~
{: .language-bash}
This only shows us the changes in the current branch, we can show multiple branches with
~~~
$ git log --oneline master update-docs
~~~
{: .language-bash}
All the commits are shown, but they are in chronological order. It's difficult for us to tell which commits are in which branch. Fortunately, git log can help us.
~~~
$ git log --graph --oneline master update-docs
~~~
{: .language-bash}
We've got two branches now, let's say that we want to make some changes to the code now, let's say we add a new command to the library called "git-party". We want to create and checkout a branch as before. This time we'll use a shortcut to do so
~~~
$ git checkout -b git-party
~~~
{: .language-bash}
We verify we're on a new branch with
~~~
$ git branch -v
~~~
{: .language-bash}
Let's create a placeholder for our new script
~~~
$ touch git-party
~~~
{: .language-bash}
and check that the file exists with
~~~
$ git status
~~~
{: .language-bash}
Next we want to add the file and commit it in this branch, we can add all files and commit in a single step with
~~~
$ git add git-party
$ git commit -m 'Added git-party script'
~~~
{: .language-bash}
We can check that the last commit contains what we thought it did by looking at it with
~~~
$ git show git-party --
~~~
{: .language-bash}
This shows the commit that git-party points to. We can use a branch name here because branches are only handy human-readable names that we assign to commits. Let's have a look at our branches
~~~
$ git log --graph --oneline --all -10
~~~
{: .language-bash}
We can see we're currently in the party branch. Next, we want to merge all of our changes back to master. First we change onto the master branch,
~~~
$ git checkout master
~~~
{: .language-bash}
Then we merge in the changes from git-party
~~~
$ git merge git-party
~~~
{: .language-bash}
We look at the history of commits
~~~
$ git log --graph --oneline --all
~~~
{: .language-bash}
We can see that a merge commit has been automatically created. This performs a merge by looking at how the files at the tips of the branches have changed since the branches forked. It then creates a single set of files which contains all of the changes. This is often called a three-way merge because there are three sets of files involved. Let's say that your supervisor approved the change of documentation. We can merge those in next
~~~
$ git merge update-docs
~~~
{: .language-bash}
This time, we see that git has automatically resolved most of the changes for us, but one particular line was changed in both branches differently, so git doesn't know what to do with this line. We're in a merge conflict, running
~~~
$ git log --graph --oneline --all
~~~
{: .language-bash}
We see that the branches are still not merged, let's look at
~~~
$ git status
~~~
{: .language-bash}
We see that the files in the working directory have been changed to match the changes from the merge, but we have some conflicts that need to be resolved before we can merge. Let's look at them with
~~~
$ git diff
~~~
{: .language-bash}
Let's keep the line from the update-docs branch, we can do this by editing the file. We'll check this out again with
~~~
$ git diff --staged
~~~
{: .language-bash}
Looks good! Or does it? Actually, we've accidentally reverted the change to the nvie repo, but we noticed the mistake too late. We can get the change back to the state we were before with
~~~
$ git checkout --conflict=merge README.mdown
~~~
{: .language-bash}
This checks the conflict file our of the repository. Let's look at the staged file again with
~~~
$ nano README.mdown
~~~
{: .language-bash}
We see the file is back to the way it was before. Sometimes, it is useful to see the difference between the original copy of the line and the two lines that we see. In this case, we can use a similar command to get this information.
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
to pick our file, we can see that the changes from the update-docs have now been discarded by running
~~~
$ git diff --staged
~~~
{: .language-bash}
or we could choose only their changes, discarding all of ours
~~~
$ git checkout --theirs -- README.mdown
~~~
{: .language-bash}
This is equivalent to copying the files from the tip of each branch. This is often useful with binary files or files not created by humans (e.g. XML config files or data files).
## Is it just magic?
Git seems to do a lot for us, and some people thing it works in mysterious ways. The aim of this short section is to give some insight into the magic that git does for us.

What is a commit, and how does it all work? Git is based on the idea of creating unique (or almost unique) 40 character "fingerprints" for everything (or almost everything) that it knows about. You've probably seen these everywhere. Git has three types of object referenced by these IDs: commits, trees and blobs.

### Blobs
Blobs are just the word git uses for the content of a file without its name. If two files contained the exact same content, they would both point to the same blob with a different filename. Let's take a look at a blob
~~~
$ git cat-file -p aded
~~~
{: .language-bash}
This is *everything* that git knows about the blob
`d570b2c26081ff4794e72fa3dd2cc38062df9910`. This is the output
~~~
Authors are (ordered by first commit date):

- Vincent Driessen
- Benedikt Böhm
- Daniel Truemper
- Jason L. Shiffer
- Randy Merrill
- Rick Osborne
- Mark Derricutt
- Nowell Strite
- Felipe Talavera
- Guillaume-Jean Herbiet
- Joseph A. Levin
- Jannis Leidel
- Konstantin Tjuterev
- Kiall Mac Innes
- Jon Bernard
- Olivier Mengué
- Emre Berge Ergenekon
- Eric Holmes
- Vedang Manerikar
- Myke Hines

Portions derived from other open source works are clearly marked.
~~~
{: .output}
This is simply the content of the file AUTHORS. But notice, the blob is just the content, doesn't seem to know anything about the filename. It's just a nameless blob of information.

### Trees
A tree is a list of file names and an ID of their content. Git uses trees to refer to directories. Let's take a look at a tree.
~~~
$ git cat-file -p d570
~~~
{: .language-bash}
We see the information in a tree object
~~~
100644 blob 8d038485fc10058d4e078954e17eb262f8263cfe    .gitignore
100644 blob 85665678e4acc7a6961bc989073a217e8f0e815b    .gitmodules
100644 blob aded955fca44f9199b340667048f7a4f7504e4e6    AUTHORS
100644 blob 2281f2307d8123fc13f157953b3c69dd935aaaee    Changes.mdown
100644 blob cedd1823140299f7862bf84afa0f217e2b1ac9e7    LICENSE
100644 blob fbbfd2c00016b174c351addde78985f7064ddb3d    Makefile
100644 blob a01079b4baae9ea3af2c9e05ead57f2667f0460c    README.mdown
100755 blob f7494c9b82d892323d951156d863c39f8b7cd47d    bump-version
040000 tree b5369782e23c81adbcabbf388504690d9217d7ba    contrib
100755 blob fd16d5168d671b8f9a8a8a6a140d3f7b5dacdccd    git-flow
100644 blob 55198ad82cbfe7249951aa75f1373a476997d33a    git-flow-feature
100644 blob ba485f6fe4b7d9c35bc01d2a6bd4ae201bccc9bd    git-flow-hotfix
100644 blob 5b4e7e807423279d5983c28b16307e40dfdb51d7    git-flow-init
100644 blob cb95bd486deb7089939362705d78b2197893f578    git-flow-release
100644 blob cdbfc717c0f1eb9e653a4d10d7c4df261ed40eab    git-flow-support
100644 blob 8c314996c0ac31f1396c48af5c6511124002dab7    git-flow-version
100644 blob 33274053347f4eec2f27dd8bceca967b89ae02d5    gitflow-common
120000 blob 7b736c183c7f6400b20ea613183d74a55ead78b5    gitflow-shFlags
160000 commit 2fb06af13de884e9680f14a00c82e52a67c867f1  shFlags
~~~
{: .output}
Note how the AUTHORS entry in the tree has the same fingerprint as the blob previously. Trees are how git connects blobs to their file names. If the file is renamed, git only changes the name in the tree, the blob stays the same.

Note also how the tree contains another tree object, called `contrib`. This is how git managed folder and sub-folders.

### Commit
A commit is a bunch of information about a commit, connected to a tree. Let's look at everything git knows about a commit
~~~
$ git cat-file -p 15aab
~~~
{: .language-bash}
Finally we can understand what a commit actually contains.
~~~
tree d570b2c26081ff4794e72fa3dd2cc38062df9910
parent 5bca8d9358f5b08af40ac32f289bb14b18965cec
author Jerome Baum <jerome@jeromebaum.com> 1348580812 +0200
committer Jerome Baum <jerome@jeromebaum.com> 1348580812 +0200

Use git_do where appropriate
~~~
{: .output}
Notice that the tree here is the tree we saw a second ago. It also contains some other metadata. If any of this information changes, the commit ID (or fingerprint) will also change. All of this should to be exactly identical for an identical commit ID.

Importantly, a commit only knows about its parents, not its children. This makes sense. We didn't know the children of a commit when we created it, and if we added this information later, it would changing the commit ID or fingerprint.

If the content of a file or its name changes, then the tree object will change. This results in a different commit fingerprint, since the tree is part of the data in the commit.

So, anything you do to change a commit in any way will result in a new commit with a different ID, even if all the contents is the same but only author is different.

Let's look at our previous commit history:
~~~
$ git log --oneline master
~~~
{: .language-bash}
Note here that for commits 15aab and below, we all have the same commit ID. It's the same object exactly. But the commits above, even if you copied what I did exactly, are different because they have a different author and possibly a different time, and if contents of the files, and therefore the blobs and trees, are identical.

Each commit is just some data about the author, a pointer to files/contents, a commit message and a pointer to the previous commit. This creates a chain of commits extending back in time. We could imagine how we could follow this chain back to the start if we know the most recent commit. This is exactly what a branch is. A branch is simply a pointer to a commit which is moved forward every time we create a new commit on that branch. When you type
~~~
$ git checkout master
~~~
{: .language-bash}
or
~~~
$ git checkout HEAD
~~~
{: .language-bash}
most of the time, git is simply looking up the commit that master or HEAD currently point to, and performing the operation on that commit.
