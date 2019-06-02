Bugs and Features
==========

If you think you found a bug in Geany or if you have a feature to request, please file bugs at the Github issue tracker(see below).
You can also feel free to subscribe and write to our [mailing list][1].

### Github issue tracker

The issue tracker can be used for bugs as well as feature requests:

https://github.com/geany/geany/issues

Sometimes a bug is not caused by Geany itself but by a plugin.
If you know or assume it might be a plugin, please refer to the Geany-Plugins project for reporting:

https://github.com/geany/geany-plugins/issues


### Bug reports

Please try to give us reliable instructions to reproduce the bug, so we can diagnose the cause. We also need:

  - The version number of Geany
  - The version number of GTK+ (can be printed with `geany -V`)
  - Your OS details
  - The filetype the bug occurred with (if applicable)

### Other useful information

Geany prints useful information on the command-line when run with the `-v` switch.
This can be useful to diagnose a bug.

Sometimes you might find a bug that only occurs with a certain configuration - in this case it can be helpful if you send us your `~/.geany/geany.conf` and any other concerned configuration file (where `~` is your home directory).

### Getting a backtrace

If Geany crashed, it would also help us a lot if you can give us a backtrace made using `gdb`:

  - Run `gdb /path/to/geany` (Note: the usual path can be found by running `which geany`)
  - Type `run -v` (followed by any command-line arguments you used with Geany when the bug occurred) in the `gdb` prompt
  - Reproduce the segfault - it will be caught by `gdb`
  - Type `bt` and press enter if prompted

Send us everything from the `run` command - thanks.

In some cases the backtrace may not be that useful.
This mostly happens when Geany was built without debug information, useful information was removed by using `-fomit-frame-pointer` or the binary was stripped (but it may still be worth sending it to us).

In this case it would be great if you could either:

  - Get a backtrace from a debug package of Geany (if your distro has one) or
  - Get a backtrace from a fresh Geany build with appropriate debug flags:

     * `make clean`
     * `./configure CFLAGS=-g`
     * Then build Geany with `make`, etc.

This also prevents optimization flags (usually enabled e.g. `-O2`) from inlining static functions where the bug might be hiding.

Note: a default source configure with gcc should include the `-g` debug flag, but on some systems CFLAGS is already set either by autoconf or in the shell environment, so it may need overriding.


  [1]: /support/mailing-lists/
