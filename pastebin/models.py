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

from datetime import timedelta
import random
import re
import time

from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pastebin.highlight import LEXER_DEFAULT


CHARS = 'abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890'
CACHE_KEY_SNIPPET_LIST_NO_CONTENT = 'snippet_list_no_content'
CACHE_KEY_SNIPPET_LIST_FULL = 'snippet_list_full'


# ----------------------------------------------------------------------
def generate_secret_id(length=5):
    return ''.join([random.choice(CHARS) for i in range(length)])  # pylint: disable=unused-variable


class Snippet(models.Model):
    secret_id = models.CharField(_('Secret ID'), max_length=255, blank=True)
    title = models.CharField(_('Title'), max_length=120, blank=True)
    author = models.CharField(_('Author'), max_length=30, blank=True)
    content = models.TextField(_('Content'), )
    content_highlighted = models.TextField(_('Highlighted Content'), blank=True)
    lexer = models.CharField(_('Lexer'), max_length=30, default=LEXER_DEFAULT)
    published = models.DateTimeField(_('Published'), blank=True, db_index=True)
    expires = models.DateTimeField(_('Expires'), blank=True, db_index=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.PROTECT)

    class Meta:
        ordering = ('-published',)

    # ----------------------------------------------------------------------
    def age(self):
        age = time.mktime(self.published.timetuple())
        return self._readable_delta(age)

    # ----------------------------------------------------------------------
    def _readable_delta(self, from_seconds, until_seconds=None):
        '''Returns a nice readable delta.

        readable_delta(1, 2)           # 1 second ago
        readable_delta(1000, 2000)     # 16 minutes ago
        readable_delta(1000, 9000)     # 2 hours, 133 minutes ago
        readable_delta(1000, 987650)   # 11 days ago
        readable_delta(1000)           # 15049 days ago (relative to now)
        '''

        if not until_seconds:
            until_seconds = time.time()

        seconds = until_seconds - from_seconds
        delta = timedelta(seconds=seconds)

        # deltas store time as seconds and days, we have to get hours and minutes ourselves
        delta_minutes = delta.seconds // 60
        delta_hours = delta_minutes // 60

        # show a fuzzy but useful approximation of the time delta
        if delta.days:
            return f'{delta.days} days ago'
        elif delta_hours:
            return f'{delta_hours} hours ago'
        elif delta_minutes:
            return f'{delta_minutes} minutes ago'
        else:
            return f'{delta.seconds} seconds ago'

    # ----------------------------------------------------------------------
    def get_linecount(self):
        return len(self.content.splitlines())

    # ----------------------------------------------------------------------
    def content_splitted(self):
        return self.content_highlighted.splitlines()

    # ----------------------------------------------------------------------
    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        if not self.pk and not self.secret_id:
            self.secret_id = generate_secret_id()
        if not self.published:
            self.published = timezone.now()

        self.content_highlighted = self.content
        super().save(*args, **kwargs)
        # invalidate cache
        cache.delete_many([CACHE_KEY_SNIPPET_LIST_NO_CONTENT, CACHE_KEY_SNIPPET_LIST_FULL])

    # ----------------------------------------------------------------------
    def delete(self, *args, **kwargs):  # pylint: disable=signature-differs
        super().delete(*args, **kwargs)
        # invalidate cache
        cache.delete_many([CACHE_KEY_SNIPPET_LIST_NO_CONTENT, CACHE_KEY_SNIPPET_LIST_FULL])

    # ----------------------------------------------------------------------
    def get_absolute_url(self):
        return reverse('snippet_details', kwargs={'snippet_id': self.secret_id})

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'{self.secret_id}'


class SpamwordManager(models.Manager):

    # ----------------------------------------------------------------------
    def get_regex(self):
        return re.compile(
            r'|'.join((i[1] for i in self.values_list())),
            re.MULTILINE)


class Spamword(models.Model):
    word = models.CharField(max_length=100)
    objects = SpamwordManager()

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'{self.word}'
