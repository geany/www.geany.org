Documentation
============

## Introduce yourself as an author

Subscribe to the [Geany Devel mailing list][1] and write a short mail to the list so that everyone knows you are there, and would like to contribute as an author for the documentation.

## Prepare for your work

Note that you will need several tools installed on your system. In particular these are:

 - GIT
 - Python docutils

The packages are named `git` and `python-docutils` on Debian and Fedora systems.

## Writing Documentation

### Check out current documentation from Git

The documentation is included in the source distribution. Thus, most current documentation is available in Geany's Git repository. To make sure you have the most recent version, check out the master branch of Geany as described on the [Git page][2] and then change to the directory `doc` in the Geany source tree.

### Edit geany.txt

You will find a file called `geany.txt`, which is the basis of all documentation. It is written in [reStructuredText][3] (or "reST"). Feel free to improve this file as you like. To build the related HTML document to see what your changes look like, run:

    make geany.html

in the `doc` directory to create or update the generated HTML documentation.

### Publish your changes for review and inclusion

If you are finished, just open a pull request on GitHub: https://github.com/geany/geany/pull/.


  [1]: /support/mailing-lists/#geany-devel
  [2]: /download/git/
  [3]: http://docutils.sourceforge.net/rst.html
  [4]: https://geany.org/manual/dev/hacking.html#patches
  [5]: https://github.com/geany/geany/pulls
