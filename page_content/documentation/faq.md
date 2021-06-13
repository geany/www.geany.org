Frequently Asked Questions
====================

[TOC]

## Can I make Geany behave like Emacs/Vim?

As its default, Geany uses the standard GTK+ keybindings that most desktop users are
familiar with. Although you can remap **most** keybindings to suit your taste,
Geany cannot currently fully emulate Emacs or Vim, nor is it currently a goal
of the core project developers to make it do so.

And if really necessary, there is a Vim-mode plugin: https://plugins.geany.org/vimode.html


## Geany does not display underscores anymore

On some systems in combination with some fonts (e.g. "DejaVu Sans Mono" on Ubuntu but
also others), Geany does not properly display underscore (`_`) as well as other
characters which are drawn at the very top or the very bottom of the line.

There are a couple of ways to work around the issue:

  - try to choose another font
  - change the line height via: `Tools` -> `Configuration Files` -> `filetypes.common`
    and add or update the following section:

		[styling]
		line_height=1;1;

    This will add a little extra space at the top (first value) and bottom (second value)
    on each line (see https://www.geany.org/manual/dev/index.html for more details).


**This issue has been fixed in Geany 1.37.**


## Can Geany show me multiple files at the same time?

Geany provides a tabbed main editor window, but does not support
split windows in the core. There is a Split Window plugin which
should work fine for viewing another document next to the main
editor notebook. You can also run several instances of Geany simultaneously.


## Does Geany have incremental search?

Case-insensitive forward incremental search is via the `search field` in the toolbar.
For reverse incremental search, start a forward search then use your key for `Find Previous`.


## Can I add custom filetypes by creating a filetypes.foo configuration file?

You can add a `filetypes.Name.conf` file and use an existing
filetype's syntax highlighting and tag parsing.
See https://www.geany.org/manual/index.html#custom-filetypes.


## How do I add full filetype support for language Foo?

Please see the [HACKING][1] document.


## Can I extend Geany myself?

Yes! You can write your own plugins in C, in Lua (using the [GeanyLua][10] plugin)
or in Python (using the [GeanyPy][11] plugin).
For more information about plugins, see the [Plugins][2] page.

Also note the `Format->Send Selection` to command is useful for
piping text through a script/external program.


## How can I change the colors used for syntax highlighting?

Geany reads the colors to use for syntax highlighting from filetype definition files.
Detailed information on how to find and edit these files can be found in the [manual][3].

There is a tool for configuring color schemes, and a set of
dark color schemes available can be found in the [Wiki][4].


## How can I contribute to Geany?

See [Contribute to Development][5].


## Does Geany support editing files remotely through FTP or SSH?

No, Geany doesn't support any remote file editing. But you can easily mount
remote filesystems through FTP, SSH or whatever with Fuse or LUFS.
This is even better because the remote filesystem will become available
for all your applications transparently.

If you have GVfs (Gnome >= 2.22) you may already have a Fuse mountpoint
in `~/.gvfs/` (or `/run/user/<uid>/gvfs`) which you can tell Geany to
open remote files from, after mounting the connection from a Gnome program
such as Nautilus.

To avoid slow responsiveness, it is recommended to disable checking files
for changes to not query the file's modification time. To do so, open the
preferences dialog and set `Disk check timeout` in the Files tab to 0 which
will disable it.


## How can I change the language of the user interface?

#### On Windows

The easiest way to use English instead of your system's locale is to deselect
the "Language Files" (a.k.a translations) option when running the Windows installer.
Then no translation files are installed and Geany will use English as language.

In case you have already installed Geany, there are a few possible workarounds to consider:

The easiest way is to change the Geany shortcut that was created
during the installation. It is recommended to create a copy of the Geany
shortcut for the desired UI language.

To force English (`en`) UI language, for example, right-click on Geany shortcut
to open the Shortcut Properties dialog and in the `Target` field put:

	cmd.exe /c "set ^"LANG=en^" & start /D ^"C:\installed-path\Geany\bin\^" geany.exe"

Adjust the `C:\installed-path\Geany` according to your Geany installation.
Take care to put the `^"` (carrot-quote) as shown. This is the way to escape
the quotes-within-the-quotes. There is a blank space before `geany.exe`.

Optionally, click on `Change Icon ...` and browse to the Geany installation
folder, then to the Geany executable file: `bin\geany.exe`. Click on the
"Magic Lamp" icon.

Accept the Property changes; if Windows requires, confirm as Administrator.
In general, this could be also done on user-level without need for
Administrator rights.

Alternatively, you may download https://download.geany.org/contrib/geany_english.bat
and put it into the `bin` subdirectory in the folder where you have Geany installed,
next to Geany.exe. Then open the file, edit the line `set LANG=C` and replace C
with your the language code of your locale (e.g. 'nl for Dutch, 'pt_BR' for
'Portuguese Brazilian'). Save the file and execute it. It should start Geany
with the desired language assuming there is an existing translation.
See also the [list of available translations][6].

#### On non-Windows systems

Simply start Geany like this:

`LANG=C geany`

and of course, change "C" to your language code (see above) or set
your locale specific environment variables accordingly.

If your system supports launcher shortcuts then Geany's shortcut can be updated
to add language setting. For example, in 
[modern `.desktop` files](https://developer.gnome.org/desktop-entry-spec/#exec-variables),
this usually goes into the `Exec` line:

	Exec=/bin/sh -c "LANGUAGE=en_IN /usr/bin/geany %F"

As alternative, you can create a shell script in any directory in your `$PATH` to 
override the default `geany` binary. As example, one can create a file at
`~/.local/bin/geany` (remember to make it executable):

	#!/bin/sh
	export LANGUAGE=en_US
	exec /usr/bin/geany $@


## I get build errors after updating from Git, why?

It's possible it's a bug, but first try this:

	make distclean
	./autogen.sh

If there are still errors, contact the mailing list.


## How can I use `urxvt` or `konsole` as terminal application when executing files?

Open the preferences tab, Tools tab and enter the following
command in the field Terminal:

	urxvt -e sh -c

	or

	konsole -e sh -c

	or (in case the above failed)

	konsole --workdir . -e sh geany_run_script.sh


## I changed my project/general indent prefs but my document still uses the old settings!

The project or general prefs for indentation only apply when opening new documents,
because documents in your current session may have different overridden
indent settings - i.e. you might want one document indented with tabs whilst
another is open with spaces indentation. See the [manual][8] for details.


## How do you pronounce Geany?

`ʒeːniː`

(pronounced like "genie") But of course, it's up to you how you pronounce it.


## How do I get my question answered?

Please first have a look at our [comprehensive manual][3].
If that doesn't answer your question, the quickest and best way is to ask on the [mailing list][9].


[1]: https://geany.org/manual/hacking.html#adding-a-filetype
[2]: /support/plugins/
[3]: /documentation/manual/
[4]: https://wiki.geany.org/
[5]: /contribute/development/
[6]: /contribute/translation/statistics/
[7]: /news/gtk-symbol-completion-data-removed-from-geany-016/
[8]: https://www.geany.org/manual/index.html#indentation
[9]: /support/mailing-lists/
[10]: https://plugins.geany.org/geanylua/geanylua-index.html
[11]: https://plugins.geany.org/geanypy.html
