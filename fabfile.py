# -*- coding: utf-8 -*-
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

from os.path import join

from fabric import task


DJANGO_HOME = '/srv/django'
PROJECT_DIRECTORY = join(DJANGO_HOME, 'www.geany.org')
PROJECT_VENV_BIN = join(PROJECT_DIRECTORY, 'venv/bin')
PYTHON_COMMAND = join(PROJECT_VENV_BIN, 'python')
MANAGE_PY = join(PROJECT_DIRECTORY, 'manage.py')
SYSTEMD_SERVICE_NAME = 'geany.org.service'
SUDO_USER = 'django'
REMOTE_HOST = ['geany.org']


# ----------------------------------------------------------------------
def _print_command(command):
    header = '-' * len(command)
    print('\033[1;32m')  # set color to green
    print(header)
    print(command)
    print(header)
    print(end='\033[0m', flush=True)  # reset color


# ----------------------------------------------------------------------
def _sudo_in_project_directory(connection, command):
    # Fabric 2 still misses lots of features, like combining cd() and sudo()
    # So, do it on our own :(
    _print_command(command)
    return connection.sudo(
        'bash -c "cd {} && {}"'.format(PROJECT_DIRECTORY, command),
        user=SUDO_USER)


# ----------------------------------------------------------------------
def _sudo_django_manage_command(connection, command):
    return _sudo_in_project_directory(
        connection,
        '{} {} {}'.format(PYTHON_COMMAND, MANAGE_PY, command))


# ----------------------------------------------------------------------
@task(hosts=REMOTE_HOST)
def deploy(connection):
    _sudo_in_project_directory(connection, 'git pull')
    # recompile bytecode
    _sudo_django_manage_command(connection, 'clean_pyc')
    _sudo_django_manage_command(connection, 'compile_pyc')
    # perform Django self checks
    _sudo_django_manage_command(connection, 'check')
    # regenerate code highlighting CSS styles
    _sudo_django_manage_command(connection, 'pygments_styles')
    # copy static files and compress CSS/JS
    _sudo_django_manage_command(connection, 'collectstatic --clear --no-input --verbosity 0')
    _sudo_django_manage_command(connection, 'compress --verbosity 0')
    # run Django database migrations
    _sudo_django_manage_command(connection, 'migrate --run-syncdb')
    # clear the cache
    _sudo_django_manage_command(connection, 'clear_cache')

    # restart UWSGI process
    _sudo_in_project_directory(connection, 'sudo systemctl restart {}'.format(SYSTEMD_SERVICE_NAME))
