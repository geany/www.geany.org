# -*- coding: utf-8 -*-
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


docker-run:
	docker run \
		--rm \
		--interactive=true \
		--tty=true \
		--user "$$(id --user):$$(id --group)" \
		--mount "type=bind,src=$$(pwd),dst=/app" \
		--publish 8000:8000 \
		--name geany_dev \
		geany_dev:latest


docker-build:
	docker build \
		--file docker/Dockerfile \
		--tag geany_dev \
		.


docker-clean:
	rm -rf docker/data
