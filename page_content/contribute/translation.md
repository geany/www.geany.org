Translate Geany and Geany-Plugins
=============================

If you would like to translate Geany into another language, have a look at the [language statistics page][1] first to see if your desired language already exists. If it already exists, please read the Notes for updating translations section. Otherwise, get the Git version of Geany, change to the po directory and start the new translation with:

    msginit -l ll_CC -o ll.po -i geany.pot

Fill in ll with the language code and CC with the country code. For example, to translate Geany into Italian you would type:

    msginit -l it_IT -o it.po -i geany.pot

This will create a file it.po. This file can be opened with a text editor (e.g. Geany and its [PoHelper plugin][2] ;-)) or a graphical program like [PoEdit][3]. There are also several other GUI programs for working on translations.

You don't need to modify the file `po/LINGUAS`, it is regenerated automatically on the next build.

When you have finished editing the file, check the file with:

    msgfmt -c --check-accelerators=_ it.po

Please take care of menu accelerators(strings containing a "\_"). The "\_" character should also be in your translation. It also would be nice if these accelerators are not used twice within a dialog or sub menu.

When you have finished your work - which doesn't mean you finished the translation, you will not have to work alone - send the file to the [translation mailing list][4] or directly to [Frank Lanitz][5] and he will add the translation to Geany then.

Alternatively, you are also welcome to open a pull request with your translation updates on https://github.com/geany/geany/tree/master/po. You can also edit and start the pull request online.

It is a good idea to let any translator and Frank know before you start or while translating, because they can give you hints on translating and Frank can ensure that a translation is not already in progress.

The instructions here can be used also for translating Geany-Plugins (https://plugins.geany.org) which are managed in a separate code repository at https://github.com/geany/geany-plugins.

## Notes for adding or updating translations

If you want to update an existing translation, please contact the [translation mailing list][4] and/or [Frank Lanitz][5] directly. He is supervising all translation issues and will contact the maintainer of the translation you want to update to avoid any conflicts.

Alternatively, you are also welcome to open a pull request with your translation updates on https://github.com/geany/geany/tree/master/po. You can also edit and start the pull request online.

Translation statistics: https://www.geany.org/contribute/translation/statistics/


  [1]: /contribute/translation/statistics/
  [2]: https://plugins.geany.org/pohelper.html
  [3]: https://www.poedit.net/
  [4]: /support/mailing-lists/#geany-i18n
  [5]: mailto:frank@frank.uvena.de
