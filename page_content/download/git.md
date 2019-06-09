Git Repository
==========

We use Git(https://git-scm.com/) for version control when developing Geany.
You can use it to test the latest source code, even between releases.

To check out Geany make sure you have the git package installed on your system.
Then checkout either the [GitHub repository][1]:

	git clone git://github.com/geany/geany.git geany

or the [geany.org mirror][2]:

	git clone https://git.geany.org/git/geany geany

This creates a subdirectory "geany" and puts all files in it.

To build with Autotools, change to that subdirectory and run:

	./autogen.sh

This will create and run the configure script for you.
You must have installed various GNU Autotools packages - if not,
the script will print out what you need to install.
In particular you need at least Autoconf version 2.60 and Automake version 1.7 or later.

For more details, check [the manual][3].


## Make Problems

When updating and rebuilding, Autotools can sometimes fail to regenerate the Makefiles correctly. You may need to run:

	make distclean
	./autogen.sh


## Git Commands

If you find any problems with the Git version, please tell us the revision number.

- Run `git rev-parse --short HEAD` to find what revision you checked out
- Run `git pull` to update to the latest revision
- Run `git diff` to see local modifications - see [Hacking][4] for how to make patches


See https://schacon.github.com/git/gittutorial.html and https://www.git-scm.com/documentation for more information.


## Web-Based Interface

There is also a web-based interface to the Git repository,
on which you can browse the code and view each file.

https://github.com/geany/geany/


## Nightly Tarballs

There are also nightly tarballs available.
These tarballs are generated each night from the current Git version.

You can download them at https://download.geany.org/ .


[1]: https://github.com/geany/geany/
[2]: https://git.geany.org/geany/
[3]: https://www.geany.org/manual/index.html#installation
[4]: /documentation/hacking/
