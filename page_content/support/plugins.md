Geany Plugins
==========

Geany has a plugin system which allows to get more features into Geany and developers can easily add new features and/or improve existing ones.

### Plugins shipped with Geany:

 - Classbuilder - Creates source files for new class types
 - Export - Exports the current file into different formats
 - Filebrowser - Adds a file browser tab to the sidebar
 - HTML Characters - Inserts HTML character entities like '&amp;'
 - Save Actions - Provides different actions related to saving files (autosave, instantsave, backupcopy)
 - Split Window - Splits the editor view into two windows

### The Geany-Plugins project

The Geany-Plugins project is a combined release for each matching Geany release.
It includes a huge number of plugins for different purposes.
Please have a look at https://plugins.geany.org/ for more information.

You can file bugs and request features for the Geany-Plugins project at https://github.com/geany/geany-plugins/issues.
The source code and more information can be found on https://github.com/geany/geany-plugins.

### Other Plugins

If you wrote a plugin and it should be listed here, please email the project admins.


### Developer Information

The Plugin API documentation is currently incomplete, but already contains useful information. Please read the [HACKING][1] file for instructions on how to generate it and any related information.

Currently, Geany Plugins can be written in:
- C
- in Lua using the [GeanyLua plugin][2]
- in Python and Lua when using the [Peasy plugin][3]

The generated API documentation can also be viewed online at https://www.geany.org/manual/reference/.

In case of any questions, feel free to ask us on the mailing list.


  [1]: https://raw.github.com/geany/geany/master/HACKING
  [2]: https://plugins.geany.org/geanylua/geanylua-index.html
  [3]: https://github.com/kugel-/peasy
