#!/bin/bash
#
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
#

set -e

mkdir -p /app/docker/data

# setup database if it does not exist
if [ ! -f "/app/docker/data/geany_dev.db" ]; then
	echo "==== Setup database ===="
	/venv/bin/python manage.py reset_db --noinput
	/venv/bin/python manage.py migrate --run-syncdb --noinput
	echo 'DELETE FROM auth_permission;
		  DELETE FROM django_content_type;
		  DELETE FROM django_site;' | /venv/bin/python manage.py dbshell
	/venv/bin/python manage.py loaddata database.json
fi
if [ ! -f "/app/docker/data/geany_dev_nightlybuilds.db" ]; then
	/venv/bin/python manage.py migrate --database nightlybuilds --run-syncdb --noinput
	/venv/bin/python manage.py loaddata --database nightlybuilds database_nightlybuilds.json
fi

# screenshots
echo "==== Download screenshots ===="
SCREENSHOTS="$(sqlite3 docker/data/geany_dev.db 'select file from galleries_galleryimage;')"
# add homepage screenshots
SCREENSHOTS="${SCREENSHOTS}
uploads/screenshots/homepage/geany_dark_2019-05-20.png
uploads/screenshots/homepage/geany_light_php-2019-06-15.png
uploads/screenshots/homepage/geany_windows_classic-2019-06-09.png
"
pushd /app/docker/data
for screenshot in ${SCREENSHOTS}; do
	if [ ! -f "/app/docker/data/${screenshot}" ]; then
		mkdir -p $(dirname "/app/docker/data/${screenshot}")
		wget \
			--no-verbose \
			--output-document="/app/docker/data/${screenshot}" \
			"https://www.geany.org/media/${screenshot}"
	fi
done
popd

# generate i18n stats if not already available
if [ ! -d "/app/docker/data/i18n" ]; then
	echo "==== Update I18N statistics ===="
	wget --no-verbose https://download.geany.org/geany_git.tar.gz -O /tmp/geany_git.tar.gz
	/venv/bin/python manage.py generate_i18n_statistics
	rm -f /tmp/geany_git.tar.gz
fi

# sync page contents from GIT back to the database
echo "==== Sync page contents ===="
/venv/bin/python /app/manage.py sync_pages

# start the server
/venv/bin/python /app/manage.py runserver 0.0.0.0:8000
