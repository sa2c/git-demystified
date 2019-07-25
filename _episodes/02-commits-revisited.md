---
title: "Commits Revisited"
teaching: 45
exercises: 0
questions:
- How do commits work?
objectives:
- "Gentle reminder of basic git usage"
- "Understanding of how git handles changes"
keypoints:
- "Learnt how files end up in the staging area"
- "Learnt how the staging area is turned into a commit"
- "Learnt how to inspect commits, blobs and trees"
---
{% include links.md %}

In this section we'll start by talking about things that may be familiar, such as adding and commit, and then moving into talking about branching workflows.

# A simple personal git workflow
Let's create a copy of a repository that we can work on, available at
<a href='https://github.com/sa2c/example-gitflow'>
    https://github.com/sa2c/example-gitflow
</a>
We clone the repository with
~~~
$ git clone git@github.com:sa2c/example-gitflow.git ~/example-gitflow
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
$ cd ~/example-gitflow
~~~
{: .language-bash}
Let's start making a few changes around here. We're working on a example repo, so to avoid confusion we're writing the in the README.mdown file
~~~
$ nano README.mdown
~~~
{: .language-bash}
We change the first line from
~~~
git-flow
~~~
to
~~~
git-flow-example
~~~
We where also a bit clumsy along the way, and we added a file by mistake. Let's fo that now:
~~~
touch whoops-I-did-it-again
~~~
{: .language-bash}
> ## How touching
> If you haven't come across accross the touch command before, it creates a new empty file with the name supplied
{: .callout}
Since we've been very busy making changes (and we've checked with the maintainer) we'll add ourselves to the end of the list of authors in the AUTHORS file. Let's do this by typing
~~~
$ nano AUTHORS
~~~
{: .language-bash}
and adding our name to the bottom of the author list.

We've been busy making changes, let's take a look at the state of the repository.
~~~
$ git status
~~~
{: .language-bash}
We'll see something like:
~~~
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   AUTHORS
	modified:   README.mdown

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	whoops-I-did-it-again

no changes added to commit (use "git add" and/or "git commit -a")

~~~
{: .language-bash}

The status command tells us that the AUTHORS and README.mdown file have been modified, but not added to the repository. There is also one new file which is not trackes.

> ## The three trees
>  It can be helpful to think of git as manipulating three sets of files, like three folders. The *working directory*, the *staging area* (or index) and the *current commit* (known as HEAD). The working directory is the folder that we see, the other two are invisible. Typing `git status` asks git to compares these three sets of files, and tell us about the differences.
If we always think of git in this way, many operations will seem less mysterious.
{: .callout}
Let's add the AUTHORS file to the staging area:
~~~
$ git add README.mdown
~~~
{: .language-bash}
We can think of this action as copying the file AUTHORS into the staging area "folder". The staging area is what we think of as the "next proposed commit".

Let's look at the state of our repository, with
~~~
$ git status
~~~
{: .language-bash}
We will see something like the following:
~~~
$ git status
On branch master
Your branch is up-to-date with 'origin/master'.

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   README.mdown

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   AUTHORS

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	whoops-I-did-it-again
~~~
{: .language-bash}
 
* The *Changes to be committed* heading lists the files which are differences between the current commit and the staging area, and also between the staging area and the current commit. In other words, the file is different in all three areas. We see the AUTHORS file here, since `git commit` is an operation that copies files from the working directory to staging area, and these files are different from the current commit (HEAD).

* The *Changes not staged for commit* heading lists the files which are different between the staging area and the current commit. The README.mdown file is here, since it was changed in the working directory, but we didn't run commit to copy it to the next proposed commit (staging area).

* The final heading, *Untracked files* shows files that are in the working directory, but are not in the current commit. Git doesn't know about them yet. A special case of this is before we create out first commit. In this case, all files will be untracked files.

Lets make some further changes to the working directory files, by deleting the line we added to the top of the AUTHORS file.

We're feeling very polite today, so let's add the word please to some of the section of README.mdown. We can open the file with nano:
~~~
nano README.mdown
~~~
{: .language-bash}
We'll make four changes to this file.
Firstly, we'll change the FAQ section to be:
~~~
FAQ
---
Please see the [FAQ](http://github.com/nvie/gitflow/wiki/FAQ) section of the project
Wiki.
Thank you.
~~~
Note how we've added the word please to both sections, and "Thank you." to the next line.
Thirdly, we change the "Contribution" section title to be:
~~~
Please consider contribution
----------------------------
~~~
Just before we close the file, we realise that the URLs have all changed, so we search search and replace all instances of the string `nvie` with `sa2c`.


Looking at the status now
~~~
$ git status
~~~
{: .language-bash}
We see the following:
~~~
On branch master
Your branch is up-to-date with 'origin/master'.

Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   README.mdown

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   AUTHORS
	modified:   README.mdown

Untracked files:
  (use "git add <file>..." to include in what will be committed)

	whoops-I-did-it-again
~~~
{: .language-bash}

Note how the README.mdown files is file both under *Changes to be committed* and under *Changes not staged for commit*. This means that there are differences between the file in the current commit and the staging area, as well as between the staging are and the working directory. In other words, each of the three trees has a different version of the file.

We can see the differences between the working directory and the staging area with:
~~~
$ git diff
~~~
{: .language-bash}
This shows us the changes not staged yet. Changes to a line are shown as the line being removed (prepended with a `-`) and then the new line being added again (lines prepended with a `+`).

What about the changes which are already staged?

We see the differences between the staging area and the current commit with:
~~~
$ git diff --staged
~~~
{: .language-bash}

This will show only change which are about to be committed. Let's say that we're happy with these changes, we can commit them with:
~~~
$  git commit -m 'Changed title of README.mdown'
~~~
{: .language-bash}
We have now created a new current commit, by copying the files as they were in the staging area. We verify this with:
~~~
$  git log
~~~
Note: you can exit git log by typing the <kbd>Q</kbd> key.

After a commit, the files in the staging area and the current commit are always going to be the be same. We'll verify this with:
~~~
$ git status
~~~
{: .language-bash}
We see the same differences between the working directory and staging areas as before, but no differences between staging area and the current commit. This makes sense, since one was just copied the contents of the staging area into a new commit, which has become the current commit.

The problem with this is that we've made two unrelated set of changes, what if we want to create this in two commits? One for the URL changes and one for the politeness changes. Let's add the file, but this time we do it with
~~~
$ git add -p README.mdown
~~~
{: .language-bash}
This looks confusing. Let's hit the <kbd>?</kbd> key to review out options. We choose changes to keep with <kbd>y</kbd> and reject all other changes with <kbd>n</kbd>. Let's do this and add all the URL changes for our first commit.

For some commits (e.g. FAQ), we may need to split the commit with <kbd>s</kbd>, and edit it with <kbs>e</kbd>.

 Now that we have crafted a proposed commit, let's see what git status says.
~~~
$ git status
~~~
{: .language-bash}
We see that we have three versions of README.mdown, in the working directory, the staging area and the current commit.

In the working directory it has all of our changes, in the staging area it has the changes we selected with `git add -p`, and in the current commit it is the same as it was previously (for now).
> ## Manipulating files, not changes
> Git hasn't chosen parts of the file or checked changes into the staging area. It just created for us a version of the file with only some of the changes, the file in the staging area. This file probably never existed with that exact same contents in the working directory.
{: .callout}
Let's see how the files in the staging look compared to the latest commit.
~~~
$ git diff --staged
~~~
{: .language-bash}
These are the differences which will be commited. They should be URL changes only. Note the content of the FAQ section in particular. And how does the working directory looks compared to the staging area?
~~~
$ git diff
~~~
{: .language-bash}
These are changes which haven't been added yet, they'll go into future commits.  We're happy now, so we can commit:
~~~
$ git commit -m 'Changes to URLs'
~~~
{: .language-bash}
Let's take a look at the files which differ now
~~~
$ git status
~~~
{: .language-bash}
and, we'll check that the changes are the ones we expect
~~~
$ git diff
~~~
{: .language-bash}
Once we're happy that this can all go into one commit, we can add the whole file with
~~~
$ git add README.mdown
~~~
{: .language-bash}
and
~~~
$ git commit -m 'More politeness in README.mdown'
~~~
{: .language-bash}
Let's have a look at our history as it is currently with
~~~
$ git log
~~~
{: .language-bash}

## Git internals
Git seems to do a lot for us, and it can seem to work in mysterious ways. The aim of this short section is to give some insight into the magic that git does for us.

What is a commit, and how does it all work? Git is based on the idea of creating unique (or almost unique) 40 character "fingerprints" for everything (or almost everything) that it knows about. You've probably seen these everywhere. Git has three types of object referenced by these IDs: commits, trees and blobs. We'll explore these one at a time, you'll often see these mentioned in the documentation, and this can be intimidating.

### Blobs
Blobs are just the word git uses for the content of a file without its name. If two files contained the exact same content, they would both point to the same blob with a different filename. Let's take a look at a blob. I happen to know that there is a blob with an ID of `aded955fca44f9199b340667048f7a4f7504e4e6`. Let's see what git can tell us about it.

~~~
$ git cat-file -p aded
~~~
{: .language-bash}
This is *everything* that git knows about this blob.
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
This is the content of the file AUTHORS, but just the content. Notice, there is not reference to a filename. It's just a nameless blob of information. The ID of the blob is the name git uses for it, and that is derived from this content. Like a fingerprint. We'll see how this is a very powerful idea. Note that this means that two files with the same content, by definition reference the same blob. Note also that a blob is a specific version of the file content. A different versiono f the same file will have a different blob.

### Trees
A tree is how git organises files name with names and directories, since a blob is just content. I happen to know that there is a tree with ID `d570b2c26081ff4794e72fa3dd2cc38062df9910`.
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
Note how the AUTHORS entry in the tree has the same fingerprint as the blob previously. I happened to pick the tree that had that blob. Trees are how git connects blobs to their file names. If the file is renamed, git only changes the name in the tree, the blob stays the same.

Note also how the tree contains another tree object, called `contrib`. This is how git managed folder and sub-folders. Note also that since a tree contains specific blobs, it must refer to the structure of folders at a particular instant in time (i.e. in a given commit).

### Commit
A commit is a bunch of information about a commit, connected to a tree. Let's look at everything git knows about a commit
~~~
$ git cat-file -p 15aab
~~~
{: .language-bash}
Finally we can see understand what a commit actually contains.
~~~
tree d570b2c26081ff4794e72fa3dd2cc38062df9910
parent 5bca8d9358f5b08af40ac32f289bb14b18965cec
author Jerome Baum <jerome@jeromebaum.com> 1348580812 +0200
committer Jerome Baum <jerome@jeromebaum.com> 1348580812 +0200

Use git_do where appropriate
~~~
{: .output}
Notice that the tree here is the tree we saw a second ago. It also contains some other metadata. If any of this information changes, the commit ID (or fingerprint) will also change. All of this should to be exactly identical for an identical commit ID. If we change any of these things, we will by definition have a commit with a different ID.

Importantly, a commit only knows about its parents, not its children. This makes sense. We didn't know the children of a commit when we created it, and if we added this information later, it would changing the commit ID or fingerprint.

If the content of a file or its name changes, then the tree object will change. This results in a different commit fingerprint, since the tree is part of the data in the commit.

>## Commit-ish and Tree-ish
> In documentation you might see many references to things that are commit-ish or tree-ish. Git has a powerful translation mechansim, that can convert any number of differnt ways of referring to a commit into a commit object or tree obeject (if it needs them). We say these different ways of references commits or trees are commit-ish or tree-ish. Examples of this that we'll see today would be:
>~~~ 
>$ git checkout master
>~~~
>{: .language-bash}
>or
>~~~
>$ git checkout HEAD
>~~~
>{: .language-bash}
>most of the time, git is simply looking up the commit that master or HEAD currently point to, and performing the operation on that commit.
{: .callout}

So, anything you do to change a commit in any way will result in a new commit with a different ID, even if all the contents is the same but only author is different.

Let's look at our previous commit history:
~~~
$ git log --oneline
~~~
{: .language-bash}
Note here that for commits 15aab and below, we all have the same commit ID. It's the same object exactly. But the commits above, even if you copied what I did exactly, are different because they have a different author and possibly a different time, and if contents of the files, and therefore the blobs and trees, are identical.

>## Branches
>Each commit is some metadata about the author, a pointer to files/contents, a commit message and a pointer to the previous commit. This creates a chain of commits extending back in time. We could imagine how we could follow this chain back to the start if we know the last commit. This is exactly what a branch is, a pointer to the latest commit.
{: .callout}

>## Patching
>First, make as many changes as you like to README.mdown, in different parts of the file. From these changes use `git add -p` to create three or four difference commits that each contain only some of the changes. You can practice:
>* choosing sections to add/remove to a commit with <kbd>y</kbd> and <kbd>n</kbd>
>* splitting up changes grouped together using <kbd>s</kbd>
>* splitting up changes on the same line into different commits using <kbd>e</kbd>
{: .challenge}

>## Finding trees
>First, consider would you expect the top level directory tree of this commit and the last commit to be the same or different?
>Verify your guess using `git log` and `cat -p <thing-id>`
>>## Solution
>>* use `git log` to find the ID of the current and last commits (the 40-character string in git log).
>>* write down the first six characters of both, let's say (for example) they are `a12345` and `b56789`.
>>* `git cat-file -p a12345` will then show you the commit content. This will contain the tree ID
>>* `git cat-file -p b56789` will then show you the commit content of the second commit. 
>>* Compare the ID shown for tree in both.
>{: .solution}
{: .challenge}

>## Finding blobs
>Use `git cat-file -p` to see the content of both trees from the last excercise. What can you tell about which files have changed and which have not from the tree? Did this match your expectation? Does the blob ID change for files which have the same content?
>>## Solution
>>Files with the same content should have the same blob ID in the tree. Files with different content will have different blob IDs.
>{: .solution}
{: .challenge}
