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
#
# Docker container to run the Geany website locally for development.
# This is not intended for production!!
# Before using this image, please get yourself familiar with Docker and
# carefully review this Dockerfile before using it!
#
# Build image:
# docker build -f docker/Dockerfile -t geany_dev .
# Run container:
# docker run --rm -it --user "$(id --user):$(id --group)" --mount "type=bind,src=$(pwd),dst=/app" -p 8000:8000 --name geany_dev geany_dev:latest

# Intermediate build container
FROM debian:bullseye-slim AS builder

ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    # Extra python env
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_FORMAT="columns" \
    PIP_CACHE_DIR="/tmp/pip" \
    PIP_TIMEOUT=60

RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends \
        python3 \
        build-essential \
        git \
        python3-pip \
        python3-wheel \
        python3-venv \
        python3-dev \
        default-libmysqlclient-dev \
        libffi-dev \
        libjpeg-dev \
        libmemcached-dev \
        zlib1g-dev \
        libssl-dev && \
        mkdir -p /app /data /venv && \
        chown -R nobody:nogroup /app /data /venv

WORKDIR /app
USER nobody:nogroup
COPY requirements.txt /data/
# Install Python deps
RUN python3 -m venv --copies /venv && \
    /venv/bin/pip install -U pip setuptools wheel && \
    /venv/bin/pip install -r /data/requirements.txt


# App container
FROM debian:bullseye-slim AS app

ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive \
    # Extra python env
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Path to local settings
    LOCAL_SETTINGS_PY=/app/docker/local_settings.docker.py

# do all of this in one RUN to limit final image size
RUN apt-get update && \
    apt-get install --assume-yes --no-install-recommends \
        ca-certificates \
        intltool \
        libjpeg62-turbo \
        default-mysql-client \
        libmemcached11 \
        libssl1.1 \
        python3 \
        sqlite3 \
        wget \
        zlib1g && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
USER nobody:nogroup

# copy in Python environment
COPY --from=builder /venv /venv
# copy helpers and configs
COPY ./docker/entrypoint.sh /data/

EXPOSE 8000
CMD ["/bin/bash", "/data/entrypoint.sh"]
