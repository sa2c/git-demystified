---
title: "Commits and branches"
teaching: 30
exercises: 20
questions:
- How are commits stores?
objectives:
- "Be able to look at previous commits"
- "Explore the relationship a commit and its ancestors"
- "Understand master"
keypoints:
- "Understand HEAD, master, commits and branches"
---
{% include links.md %}

In the last episode, we saw only the latest commit, which we called `HEAD`. But if git worked this way, it wouldn't be much use at all. Clearly git needs to store commits to be useful.

Let's change into the folder for the second episode:

~~~
$ cd ~/git-demystified/episode_2
~~~
{: .language-bash}

And take a look at the commits so far
~~~
$ git log --oneline
~~~
{: .language-bash}

~~~
6ec2577 (HEAD -> master) Changes
e93c765 Added colour specification and blue.txt
805a6c8 Add lists of red and green objects
~~~
{: .output}

You should see exactly the same commit identifiers as I do, as there have been created on my machine.

Familiar? These are the same commits from the changes in the last episode.

Each commit has in it a complete snapshot of the files we saw in HEAD in the previous section. Every time we type `git commit`, the old contents of `HEAD` was filed away as a commit, and replaced by a new commit, with the contents of the staging area. This new commit becomes the new `HEAD`.

> ## Space Saving
> Storing the state of every file at every commit might seem inefficient from a storage point of view. But git gets around this with quite a few tricks to accomplish it as efficiently as possible.
{: .callout}

> ## Breadcrumbs
> Think of this as dropping breadcrumbs to find your way. Imagine that every commit is a breadcrumb. Next to each breadcrumb, you draw an arrow to point to the previous breadcrumb. This way, you can keep a trail without ever having to go back and change anything you've done for a previous breadcrumb.
>
> To be precise, maybe dropping USB sticks would be a better analogy, as every breadcrumb contains a snapshot of all your files at that point in time.
{: .callout}

# Looking at old commits
We can visit an old commit by using the commit identifier from the git commit log
~~~
$ git log
~~~
{: .language-bash}

~~~
$ git checkout e93c765
~~~
{: .language-bash}

We will get a long warning here, but we'll come back to this later.

We could type the full commit identifier here, but git will allow us to you an abbreviated version, down to a minimum of four characters, as long as it is unique. Typically, 7 characters is enough to avoid any clashes.

You can think of checkout of a commit as following back the breadcrumb trail to a specific crumb. Let's take another look at the log now
~~~
$ git log --oneline
~~~
{: .language-bash}

Think of git log as following the breadcrumbs back from teh current commit by default. We can tell it to show us a little bit more using
~~~
$ git log --oneline --all
~~~
{: .language-bash}

> ## Older versions of git
> Note that older version of git might need `git config log.decorate auto` in order to see the line decorations (e.g. `HEAD` and `master`).
> If you like this, you can make this type of output of `git log` the default on your current machine with `git config --global log.decorate auto`.
{: .callout}

>## Visit the past
> Checkout the three commits in the repository in any order you choose. First use `git log` to get the identifiers for the commit, then use `git checkout` to visit the commit.
>
> Do not change any files as you move around, but use `ls <filename>` and `cat <filename>` to check that the content of the files is what you expected.
>> ## Solution
>> Use `git log --oneline --all` to get the list of commit identifiers for this repository.
>>
>> You can then visit each of the three commits with `git checkout e93c765`, `git checkout 805a6c8` and `git checkout 6ec2577`.
>{: .solution}
>
{: .challenge}

>## Visiting master
> We can refer to commit `6ec2577` by another name, this is shown in `git log --oneline --all`. Can you guess what it is?
>
> Test your theory using `git checkout` and `git log --oneline --all`.
>> ## Solution
>> This commit is also referred to by the label `master`. You can visit it with `git checkout master`. The command `git log --oneline --all` and `git log --all` should show this on the same line as the commit identifier.
>> If the commit it checked out, it may also be labelled with the label `HEAD`. In which case you can do `git checkout HEAD`.
>{: .solution}
>
{: .challenge}

> ## Thinking in snapshots
> In our three trees model, we can think of this as simply copying the files from the commit we are referring to into both the working tree and the staging area. Then we change the current commit by moving the marker `HEAD` onto this new commit. Think of the marker head as a marker for our current position in the breadcrumb trail.
{: .callout}

# Branches
Git doesn't just support one linear history of your files, it support many complex ways in which your files can evolve. We'll explore this by starting with the middle commit
~~~
$ git checkout e93c765
~~~
{: .language-bash}

We get the same warning, which tells us not to modify files here. Let's ignore this warning to see what happens if we do.

We'll create a new file
~~~
$ touch phantom_file
~~~
{: .language-bash}

and add it
~~~
$ git add phantom_file
~~~
{: .language-bash}

And finally commit it
~~~
$ git commit -m "Phantom commit"
~~~
{: .language-bash}

And we'll see what has happened here with
~~~
$ git log
~~~
{: .language-bash}
So this shows a new commit, created following on from the previous commit. What happened to master?

Let us take a look with
~~~
$ git log --oneline --all
~~~
{: .language-bash}

That's odd, it isn't quite what we might have expected. That is because `git log` shows us the changes in chronological order. We add a new argument `--graph` to see the parent-child relationships of commits.
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}
~~~
* cd3a38a (HEAD) Phantom commit
| * 6ec2577 (master) Changes
|/  
* e93c765 Added colour specification and blue.txt
* 805a6c8 Add lists of red and green objects
~~~
{: .output}

> ## Breadcrumbs again
> We just created a commit with a parent that is the commit `e93c765`. Think of this as jumping to that breadcrumb, with `git checkout`. We then walked forward a bit (our analogy for making changes), and dropped a new breadcrumb, at a new location. We drew an arrow to the parent/previous breadcrumb. Since we've moved, the `HEAD` label will point to our current location.
{: .callout}


What happens if we jump back to the commit labelled `master`?
~~~
$ git checkout master
~~~
{: .language-bash}

And let's take a look at our log
~~~
$ git log --oneline
~~~
{: .language-bash}

~~~
9ce7a2c (HEAD -> master) Changes
563a9f8 Added colour specification and blue.txt
829a4fe Add lists of red and green objects
~~~
{: .output}

The commit has gone.

We created a commit in a new trail, but without adding a label. A working git repository could collect hundreds or thousands of hidden identifiers in regular use, so git won't show them all to us. We need to
tell it to track a trail of commits by giving it a label.

You may have seen a warning when typed `git checkout master`, telling you how to label the commit that you visited. We call this label a `branch`. Let's do that now:
~~~
$ git branch phantom-tracker <your commit ID here>
~~~
{: .language-bash}

Let us have a look now
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

The phantom commit is back, this time with the label `phantom-tracker`.

We'll switch to that commit with
~~~
$ git checkout phantom-tracker
~~~
{: .language-bash}

And look again with
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

Note how `HEAD` points to `phantom-tracker`, we say we're _on the phantom tracker branch_.

Lets create a new branch at the current commit with
~~~
$ git branch another-phantom-tracker
~~~
{: .language-bash}

And look at the git log
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

~~~
* cd3a38a (HEAD -> phantom-tracker, another-phantom-tracker) Phantom commit
| * 6ec2577 (master) Changes
|/  
* e93c765 Added colour specification and blue.txt
* 805a6c8 Add lists of red and green objects
~~~
{: .output}

Note how `HEAD` doesn't point to this branch, despite it being the same commit.
>## Moving the phantoms
> Can you guess what will if we add a new commit when we have `phantom-tracker` checked out? What happens to the `phantom-tracker` label? What happens to the `another-phantom-tracker` label?
>
> Checkout `phantom-tracker`, then add a new file called `phantom-tracker-file` to a new commit using `touch phantom-tracker-file`, `git add` and `git commit`.
>
> Did you guess correctly?
> 
Have a guess what you think and test it out with `git checkout` and `git commit`. Add a file 
>> ## Solution
>> 1. Switch to the branch `phantom-tracker` with `git checkout phantom-tracker`.
>> 2. Create a new file, for example with `touch phantom-tracker-file`.
>> 3. Add the file with `git add phantom-tracker-file`
>> 4. Commit the file with `git commit -m "phantom-tracker-file"` (or a message of your choosing)
>> 5. Look at the results with `git log --oneline --all --graph`.
>> 6. You should see that the `phantom-tracker` branch has a new commit, but `another-phantom-tracker` is in the same place.
>{: .solution}
>
{: .challenge}

>## One Step, Two Step
> Repeat the excercise above, this time adding a new file called `another-phantom-tracker-file` to the `another-phantom-tracker` branch. Take a look at the history, do these branches all share a common history?
>> ## Solution
>> 1. Switch to the branch `another-phantom-tracker` with `git checkout another-phantom-tracker`.
>> 2. Create a new file, for example with `touch another-phantom-tracker-file`.
>> 3. Add the file with `git add another-phantom-tracker-file`
>> 4. Commit the file with `git commit -m "another-phantom-tracker-file"` (or a message of your choosing)
>> 5. Look at the results with `git log --oneline --all --graph`.
>> 6. You should see that both `phantom-tracker` branch and `another-phantom-tracker` have one new commit each. We say that these branches have `diverged`.
>>
>> This will be shown with a split branch in the log, similar to this:
>> ~~~
>> * 9ed168d (HEAD -> another-phantom-tracker) another-phantom-tracker-file
>> | * 08a1c32 (phantom-tracker) phantom-tracker-file
>> |/  
>> * cd3a38a Phantom commit
>> | * 6ec2577 (master) Changes
>> |/  
>> * e93c765 Added colour specification and blue.txt
>> * 805a6c8 Add lists of red and green objects
>> ~~~
>> {: .output}
>{: .solution}
{: .challenge}

>## Merging Phantoms
> First checkout the `phantom-tracker` branch, and then merge in the `another-phantom-tracker` branch using `git merge another-phantom-tracker`. What has happened to the files? What do you see with `git log --oneline --all --graph`?
>> ## Solution
>> You should see a merge commit, which combines the changes from both previous divergent branches.
>> Both the `phantom-tracker-file` and `another-phantom-tracker-file` files should be in the working directory.
>> Note how merge commits are special in that they have multiple parent commits.
>>
>> The output of `git log --oneline --all --graph` should show two branches joining, i.e. the `HEAD` commit has two parents.
>> ~~~
>> *   c6f5e4c (HEAD -> phantom-tracker) Merge branch 'another-phantom-tracker' into phantom-tracker
>> |\  
>> | * 9ed168d (another-phantom-tracker) another-phantom-tracker-file
>> * | 08a1c32 phantom-tracker-file
>> |/  
>> * cd3a38a Phantom commit
>> | * 6ec2577 (master) Changes
>> |/  
>> * e93c765 Added colour specification and blue.txt
>> * 805a6c8 Add lists of red and green objects
>> ~~~
>> {: .output}
>{: .solution}
>
{: .challenge}

>## Leave no traces
> We don't need the `another-phantom-tracker` branch anymore. Delete it with `git branch -d another-phantom-tracker`.
> Use `git log --oneline --all --graph` to check that it has gone.
>> ## Solution
>> You should see a history similar to. Note that there is no another-phantom-tracker branch (other than in the commit message for the merge).
>> ~~~
>> *   c6f5e4c (HEAD -> phantom-tracker) Merge branch 'another-phantom-tracker' into phantom-tracker
>> |\  
>> | * 9ed168d another-phantom-tracker-file
>> * | 08a1c32 phantom-tracker-file
>> |/  
>> * cd3a38a Phantom commit
>> | * 6ec2577 (master) Changes
>> |/  
>> * e93c765 Added colour specification and blue.txt
>> * 805a6c8 Add lists of red and green objects
>> ~~~
>> {: .output}
>{: .solution}
>
{: .challenge}

# Resolving conflicts
Sometimes two branches will have changed the same line, in the same file. How does git deal with this?

Let's have a look at a prepared merge conflict, which changes the same files
~~~
$ cd ~/git-demystified/episode_2.1
~~~
{: .language-bash}

And look at git log
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

~~~
 b7945fb (another-phantom-tracker) Added phantoms
| * cbfc473 (HEAD -> phantom-tracker) Added phantoms
|/  
* cd3a38a Phantom commit
| * 6ec2577 (master) Changes
|/  
* e93c765 Added colour specification and blue.txt
* 805a6c8 Add lists of red and green objects
~~~
{: .output}

We can look at individual commits with `git show`. This can take either the commit identifier, or the branch label if the commit is at the end of a branch.
~~~
$ git show phantom-tracker
~~~
{: .language-bash}

And for the other branch
~~~
$ git show another-phantom-tracker
~~~
{: .language-bash}

Both files are the same change with slightly differences. We can merge `another-phantom-branch` into this branch with:
~~~
$ git merge another-phantom-tracker
~~~
{: .language-bash}

~~~
Auto-merging phantom_file
CONFLICT (content): Merge conflict in phantom_file
Automatic merge failed; fix conflicts and then commit the result.
~~~
{: .output}

~~~
$ git status
~~~
{: .language-bash}

We'll correct the issue, with
~~~
$ nano phantom_file
~~~
{: .language-bash}

And add the change
~~~
$ git add phantom_file
$ git commit
~~~
{: .language-bash}

Let's check that the file is as expected
~~~
$ cat phantom_file
~~~
{: .language-bash}

and that the history shows a merge
~~~
$ git log --oneline --all --graph
~~~
{: .language-bash}

> ## An alternative diff
> Often merges can be confusing. Sometimes we can use the following lines to add more information to a conflicted file.
> ~~~
> $ git checkout --conflict=diff3 <conflicted-file>
>~~~
> {: .language-bash}
>
> After running this command, <conflicted-file> will look something like:
> ~~~
> <<<<<<< HEAD
> Ghost
> Goul
> Banshee
> Beastie
> ||||||| cd3a38a
> Ghost
> Minotaur
> =======
> Ghost
> Minotaur
> Banshee
> Goul
> Beastie
> >>>>>>> another-phantom-tracker
> ~~~
> {: .output}
>
> Notice the additional middle section shows the state of the file in the last common ancestor.
{: .callout}

>## Branches == Labels
> We've mentioned that branches are just labels. Look at the files in the folder `.git/refs/heads/` with `ls` and `cat` to convince yourself that this is true.
>> ## Solution
>> Each file in the folder refers to the ID of a commit pointed to by a branch. These files define the branches.
> {: .solution}
{: .challenge}


# Git Inception

A real project will create a large number of branches, and merge them back when the feature they're working on is completed. Here is a section of the log of the source code for git.

~~~
* d4a392452 (HEAD -> master, tag: v2.29.0-rc1, origin/master, origin/HEAD) Git 2.29-rc1
*   62564ba4e Merge branch 'js/default-branch-name-part-3'
|\  
| * 538228ed2 tests: avoid using the branch name `main`
| * a15ad5d1b t1415: avoid using `main` as ref name
* |   20a00abe3 Merge branch 'js/ci-ghwf-dedup-tests'
|\ \  
| * | 4463ce75b ci: do not skip tagged revisions in GitHub workflows
| * | 7d78d5fc1 ci: skip GitHub workflow runs for already-tested commits/trees
| |/  
* |   d620daaa3 Merge branch 'ja/misc-doc-fixes'
|\ \  
| * | 9f443f553 doc: fix the bnf like style of some commands
| * | 89eed6fa9 doc: git-remote fix ups
| * | 49fbf9ed7 doc: use linkgit macro where needed.
| * | df49a806a git-bisect-lk2009: make continuation of list indented
| |/  
* |   e245b4e3b Merge branch 'dl/makefile-sort'
|\ \  
| * | 8474f2658 Makefile: ASCII-sort += lists
| |/  
* |   86e1007ab Merge branch 'js/no-builtins-on-disk-option'
|\ \  
| * | 722fc3749 help: do not expect built-in commands to be hardlinked
* | |   08f06e542 Merge branch 'js/ghwf-setup-msbuild-update'
|\ \ \  
| * | | 17c13069b GitHub workflow: automatically follow minor updates of setup-msbuild
| | |/  
| |/|   
* | |   c7ac8c0a7 Merge branch 'jk/index-pack-hotfixes'
|\ \ \  
| * | | ec6a8f970 index-pack: make get_base_data() comment clearer
| * | | bebe17194 index-pack: drop type_cas mutex
| * | | cea69151a index-pack: restore "resolving deltas" progress meter
* | | |   abac91e3a Merge branch 'dl/mingw-header-cleanup'
|\ \ \ \  
| * | | | fcedb379f compat/mingw.h: drop extern from function declaration
| | |/ /  
| |/| |   
* | | |   f491ce954 Merge branch 'hx/push-atomic-with-cert'
|\ \ \ \  
| |/ / /  
|/| | |   
| * | | 2cd6e1d55 t5534: split stdout and stderr redirection
* | | | d98273ba7 (tag: v2.29.0-rc0) Git 2.29-rc0
* | | |   542b3c257 Merge branch 'nl/credential-crlf'
|\ \ \ \  
| * | | | 356c47329 credential: treat CR/LF as line endings in the credential protocol
* | | | |   67af91027 Merge branch 'sn/fast-import-doc'
|\ \ \ \ \  
| * | | | | 3be01e5ab fast-import: fix typo in documentation
* | | | | |   9d19e1773 Merge branch 'pb/submodule-doc-fix'
~~~
{: .output}
