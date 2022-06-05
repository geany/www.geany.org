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

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import CONTENT_STATUS_CHOICES, CONTENT_STATUS_PUBLISHED
from mezzanine.utils.models import get_user_model_name
from mezzanine.utils.urls import slugify


class PublishedManager(models.Manager):
    """
    Provides filter for restricting items returned by status and
    publish date when the given user is not a staff member.
    """
    # this is a clone of mezzanine.core.managers.PublishedManager but with the
    # 'expiry_date' field removed

    # ----------------------------------------------------------------------
    def published(self, for_user=None):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """
        if for_user is not None and for_user.is_staff:
            return self.all()
        return self.filter(
            models.Q(publish_date__lte=now()) | models.Q(publish_date__isnull=True),
            models.Q(status=CONTENT_STATUS_PUBLISHED))

    # ----------------------------------------------------------------------
    def recently_published(self, count=5, for_user=None):
        return self.published(for_user).order_by('-publish_date')[:count]


class NewsPost(models.Model):

    slug = models.CharField(_('Slug'), max_length=255, editable=False, db_index=True)
    title = models.CharField(_('Title'), max_length=255, blank=True)
    content = RichTextField(_('Content'))
    user = models.ForeignKey(
        get_user_model_name(),
        verbose_name=_('Author'),
        related_name='%(class)ss',
        on_delete=models.PROTECT)
    status = models.IntegerField(
        _('Status'),
        choices=CONTENT_STATUS_CHOICES,
        default=CONTENT_STATUS_PUBLISHED,
        db_index=True,
        help_text=_('With Draft chosen, will only be shown for admin users on the site.'))
    entry_date = models.DateTimeField(
        _('Published'),
        editable=False,
        auto_now_add=True,
        db_index=True)
    publish_date = models.DateTimeField(
        _('Published on'),
        blank=True,
        db_index=True,
        default=timezone.now)

    # add a 'published' method to the Manager to filter by published status
    objects = PublishedManager()

    class Meta:
        ordering = ('-publish_date',)
        verbose_name = _('News')
        verbose_name_plural = _('News')

    # ----------------------------------------------------------------------
    def save(self, *args, **kwargs):  # pylint: disable=signature-differs
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # ----------------------------------------------------------------------
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'newspost_slug': self.slug})

    # ----------------------------------------------------------------------
    def __str__(self):
        return self.title
