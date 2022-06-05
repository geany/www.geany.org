# LICENCE: This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.urls import re_path
from django.views.generic.base import RedirectView


URL_MAPPING = {
    # old urls mapped to new ones
    '/Category/DocumentationToDo': 'https://github.com/geany/geany/issues/',
    '/Category/Manual': '/documentation/manual/',
    '/Contribute/Developers': '/contribute/development/',
    '/Contribute/Documentation': '/contribute/documentation/',
    '/Contribute/Support': '/contribute/support/',
    '/Contribute/Translators': '/contribute/translation/',
    '/i18n': '/contribute/translation/statistics/',
    '/Developers/Developers': '/contribute/development/',
    '/Documentation/ChangeLog': 'https://github.com/geany/geany/commits/master',  # page dropped
    '/Documentation/Documentation': '/documentation/manual/',
    '/Documentation/FAQ': '/documentation/faq/',
    '/Documentation/FAQdata': '/documentation/faq/',
    '/Documentation/Manual': '/documentation/manual/',
    '/Documentation/Questions': '/documentation/faq/',
    '/Documentation/ReleaseNotes': '/documentation/releasenotes/',
    '/Documentation/ReleaseNotesOld': '/documentation/releasenotes/',
    '/Documentation/Screenshots': '/documentation/screenshots/',
    '/Documentation/ToDo': 'https://github.com/geany/geany/issues/',
    '/Download/Extras': 'https://wiki.geany.org/',  # page dropped
    '/Download/Git': '/download/git/',
    '/Download/OldExtras': 'https://wiki.geany.org/',  # page dropped
    '/Download': '/download/releases/',
    '/Download/Releases': '/download/releases/',
    '/Download/SVN': '/download/git/',
    '/Download/ThirdPartyPackages': '/download/third-party/',
    '/Gallery/Main': '/documentation/screenshots/',
    '/Gallery/Test': '/documentation/screenshots/',
    '/Geany/ChangeLog': 'https://github.com/geany/geany/commits/master',  # page dropped
    '/Geany/FAQ': '/documentation/faq/',
    '/Geany/Screenshots': '/documentation/screenshots/',
    '/Geany/Support': '/support/',
    '/Geany/Troubleshooting': '/support/',
    '/Main/About': '/about/geany/',
    '/Main/AboutThisSite': '/',
    '/Main/AllFiletypes': '/about/filetypes/',
    '/Main/Authors': '/about/geany/',
    '/Main/Blog': '/news/',
    '/Main/BlogArchive': '/news/',
    '/Main/HomePage': '/',
    '/main/homepage': '/',
    '/Main/Reviews': '/',  # page dropped
    '/Main/Thanks': '/',  # page dropped
    '/Main/WikiSandbox': '/',  # page dropped
    '/Site/AllRecentChanges': '/news/feed/',
    '/Site/Authors': '/about/geany/',
    '/Support/Bugs': '/support/bugs/',
    '/Support/BuildingFromSource': 'https://www.geany.org/manual/index.html#installation',
    '/Support/BuildingOnWin32': 'https://wiki.geany.org/howtos/win32/msys2',
    '/Support/Contributions': '/contribute/',
    '/Support/CrossCompile': 'https://wiki.geany.org/howtos/win32/crosscompile',
    '/Support/Developers': '/contribute/development/',
    '/Support/Hacking': '/documentation/hacking/',
    '/Support/I18N': '/contribute/translation/',
    '/Support/IRC': '/support/',
    '/support/irc/': '/support/',
    '/Support/MailingList': '/support/mailing-lists/',
    '/Support/PluginWishlist/':
        'https://github.com/geany/geany-plugins/issues?q=is%%3Aissue+label%%3Afeature+',
    '/Support/Plugins': '/support/plugins/',
    '/Support/RunningOnWindows': 'https://wiki.geany.org/howtos/win32/running',
    '/Support/VerifyGPGSignature': '/support/verify-gpg-signature/',

    # migrated news items
    '/Main/20060117': '/news/geany-in-linuxuser/',
    '/Main/20060128': '/news/geany-05-is-out/',
    '/Main/20060310': '/news/geany-06-is-under-heavy-development/',
    '/Main/20060430': '/news/geany-06-released/',
    '/Main/20060505': '/news/changed-from-cvs-to-subversion/',
    '/Main/20060519': '/news/geany-has-got-an-additional-developer/',
    '/Main/20060604': '/news/geany-07-released/',
    '/Main/20060608': '/news/windows-build-of-geany-07/',
    '/Main/20060623':
        '/news/new-website-launched-with-some-new-content-and-new-layout-driven-by-a-wiki/',
    '/Main/20060625': '/news/geany-071-released/',
    '/Main/20060809': '/news/geany-08-released/',
    '/Main/20060929': '/news/geany-09-released/',
    '/Main/20061210': '/news/new-svn-binary-for-windows-available/',
    '/Main/20061221': '/news/geany-010-released/',
    '/Main/20070223': '/news/geany-0101-released/',
    '/Main/20070225': '/news/geany-0102-released/',
    '/Main/20070416': '/news/windows-built-of-svn-version-available/',
    '/Main/20070521': '/news/geany-011-released/',
    '/Main/20070912': '/news/geany-012-pre-release/',
    '/Main/20070930': '/news/new-website-look/',
    '/Main/20071010': '/news/geany-012-released/',
    '/Main/20071014': '/news/lua-plugin-03/',
    '/Main/20071123': '/news/windows-build-of-svn-version-available/',
    '/Main/20071201': '/news/again-new-windows-svn-build/',
    '/Main/20071205': '/news/another-new-and-important-windows-svn-build/',
    '/Main/20080205': '/news/geany-013-released/',
    '/Main/20080419': '/news/geany-014-released/',
    '/Main/20080507': '/news/new-mailing-lists-for-developers/',
    '/Main/20080521': '/news/new-windows-build-for-testing-available/',
    '/Main/20080817': '/news/new-windows-build/',
    '/Main/20080901': '/news/wwwgeanyorg/',
    '/Main/20081019': '/news/geany-015-released/',
    '/Main/20090122': '/news/wanted-maintainers-for-geanylua-and-geanygdb-plugins/',
    '/Main/20090215': '/news/geany-016-released/',
    '/Main/20090217': '/news/gtk-symbol-completion-data-removed-from-geany-016/',
    '/Main/20090418': '/news/miscellaneous-development-news/',
    '/Main/20090502': '/news/geany-017-released/',
    '/Main/20090714': '/news/geany-plugins-017-released/',
    '/Main/20090721': '/news/geany-plugins-0171-released/',
    '/Main/20090816': '/news/geany-018-released/',
    '/Main/20091028': '/news/geany-plugins-018-released/',
    '/Main/20100214': '/news/geany-0181-released/',
    '/Main/20100320': '/news/geany-01811-windows-only-released/',
    '/Main/20100612': '/news/geany-019-released/',
    '/Main/20100614': '/news/geany-plugins-019-released/',
    '/Main/20100819': '/news/geany-0191-released/',
    '/Main/20101201': '/news/geany-0192-released/',
    '/Main/20110106': '/news/geany-020-released/',
    '/Main/20110113': '/news/geany-plugins-020-released/',
    '/Main/20110302': '/news/welcome-a-new-geany-developer-colomban-wendling/',
    '/Main/20110313': '/news/first-geany-newsletter-sent-out/',
    '/Main/20110522': '/news/geany-newsletter-issue-2-sent-out/',
    '/Main/20110829': '/news/geany-newsletter-issue-3-released/',
    '/Main/20111002': '/news/geany-021-released/',
    '/Main/20111010': '/news/geany-switched-to-git/',
    '/Main/20111024': '/news/geany-plugins-021-released/',
    '/Main/20111111': '/news/say-welcome-to-a-new-geany-developer-matthew-brush/',
    '/Main/20120119': '/news/wiki-for-geany/',
    '/Main/20120618': '/news/geany-122-is-out/',
    '/Main/20120712': '/news/geany-plugins-122-are-out/',
    '/Main/20130310': '/news/geany-123-is-out/',
    '/Main/20130519': '/news/geany-1231-is-out/',
    '/Main/20140413': '/news/geany-124-is-out/',
    '/Main/20140416': '/news/geany-1241-is-out/',
    '/Main/20150712': '/news/geany-125-is-out/',
    '/Main/20150713': '/news/geany-plugins-125-released/',
    '/Main/20151115': '/news/geany-126-is-out/',
    '/Main/20160313': '/news/geany-127-is-out/',
    '/Main/20160710': '/news/geany-128-is-out/',
    '/Main/20161113': '/news/geany-129-is-out/',
    '/Main/20170305': '/news/geany-130-is-out/',
    '/Main/20170319': '/news/geany-1301-is-out/',
    '/Main/20170717': '/news/geany-131-is-out/',
    '/Main/20171119': '/news/geany-132-is-out/',
    '/Main/20180225': '/news/geany-133-is-out/',
    '/Main/20181216': '/news/geany-134-is-out/',
    '/Main/20190104': '/news/geany-1341-is-out/',
    '/Main/20190428': '/news/geany-135-is-out/',
}


URL_MAPPING_CATCH_ALL = {
    # various old deep links (catch all)
    '/images/.*.png/': '/media/uploads/screenshots/geany_light_2019-05-20.png',
    '/uploads/Gallery/.*.png/': '/media/uploads/screenshots/geany_light_2019-05-20.png',
    '/Category.*': '/',
    '/Developers.*': '/',
    '/Documentation.*': '/',
    '/Download.*': '/',
    '/Geany.*': '/',
    '/PmWiki.*': '/',
    '/Profiles.*': '/',
    '/Site.*': '/',
    '/Support.*': '/',
    '/ToDo.*': '/',
    # catch all for everything else (spiders tend to query even non-existent URLs)
    '/Main/.*': '/news/geany-135-is-out/',
}


# ----------------------------------------------------------------------
def _add_url_mappings(mapping, urlpatterns_):
    for old_url, new_url in mapping.items():
        if old_url.startswith('/'):
            old_url = old_url[1:]

        url_pattern = re_path(
            fr'^{old_url}$',
            RedirectView.as_view(url=new_url, permanent=True))
        urlpatterns_.append(url_pattern)
        # add pattern variant with trailing slash
        if old_url[-1] != '/':
            url_pattern = re_path(
                fr'^{old_url}/$',
                RedirectView.as_view(url=new_url, permanent=True))
            urlpatterns_.append(url_pattern)


urlpatterns = []  # pylint: disable=invalid-name
# first add specific items to let them match first
_add_url_mappings(URL_MAPPING, urlpatterns)
# now add catch all items
_add_url_mappings(URL_MAPPING_CATCH_ALL, urlpatterns)
