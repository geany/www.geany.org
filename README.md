www.geany.org
=============

## About

This is the website code for <https://www.geany.org>.
It's based on Django and uses Mezzanine (<https://mezzanine.jupo.org/>, the coolest Django CMS)
for content management.


## Management And Maintenance

### Admin Area

To enter the Django admin area, just open <https://geany.org/admin/>.
In case you forgot your username and/or password or when it never had been set before,
use the password reset form with your registered email address.

### Set Latest Version on release time

When releasing Geany, the website should be updated as well.
This is easily done by editing the version number at
<https://geany.org/admin/latest_version/latestversion/1/change/>.
After the latest version has been updated in the admin area, it may take
a few minutes until cached contents have expired.

Afterwards, all references on the website where the version number
is used, are up to date.

### Deploy Content Changes from GIT to the website

To change any content on the website, find and edit the corresponding
Markdown source file in this repository's `page_content` directory.
The directories and files in therein represent the website page structure.

After you made your changes, commit and push the changed file(s) to GIT.

Then open <https://geany.org/admin/mezzanine_sync_pages/mezzaninesyncpages/>,
check `Execute "git pull"` and press `Sync Pages`.
Then the current website's pages are synced with the file contents in the
GIT repository. For your convenience, after the sync has finished you are
presented with an overview and diff of all made changes.

Please note, there is no dry-run, preview or rollback of the performed changes.
Only the diff of the changes *after* they have been applied.

#### Special Pages

There are a few special pages which cannot be synced the way described above.
This is because those pages are partially or completely rendered dynamically
with non-static content.

  * contribute/translation/statistics.md: generate nightly from source code
  * documentation/releasenotes.md: generated from Github upon request
  * documentation/todo.md: generated from Github upon request
  * download/nightly-builds.md: generated upon request
  * fake.md: dummy page for various non-CMS pages like pastebin.geany.org and more

#### Supported Markdown Extensions

There are a couple of Markdown extensions enabled for the website, mainly
to support similar features like Github Flavored Markdown provides:

  * pymdownx.magiclink
  * pymdownx.betterem
  * pymdownx.tilde
  * pymdownx.tasklist
  * pymdownx.superfences
  * nl2br (transform line breaks to HTML `<br>` tags)
  * tables
  * toc

For details and usage instructions of the listed extensions, please see
the documentation at <https://facelessuser.github.io/pymdown-extensions/>.

#### Page Content Management Commands

  * `venv/bin/python manage.py sync_pages`
    This command can be used to sync the website's pages with the
    file contents in the GIT repository (like described above).

  * `venv/bin/python manage.py dump_pages`
    Perform a backwards sync, i.e. read the current website's pages
    content and write it as Markdown files into the repository's
    `page_content` directory.
    Be careful, this command should only be executed initially or
    only if you really know what you are doing.
    It will overwrite any previous contents in the `page_content`
    directory without confirmation.

## Deployment

To be able to deploy the code, you need a working SSH connection
to the geany.org server. Obviously, this implies an user account
on the server.

### Using Fabric

To deploy the code the following steps are necessary:

  * Install Fabric (<https://www.fabfile.org/>, version 2 or later) on your
    local machine: `pip install fabric` or use the system package manager
  * `cd <path-to-the-code-repository>`
  * `fab deploy`
  * Done.

### Alternative Way (remote only)

You can also deploy the code to the website using a SSH shell
on the server and perform the commands manually which would have
been executed by Fabric otherwise.

  * Login to geany.org with your user via SSH: `ssh geany.org`
  * Switch to the Django user: `sudjango`
  * Execute all or only some of the following commands:

      ```sh
      cd /srv/django/www.geany.org
      git pull
      venv/bin/python manage.py clean_pyc
      venv/bin/python manage.py compile_pyc
      venv/bin/python manage.py check
      venv/bin/python manage.py pygments_styles
      venv/bin/python manage.py collectstatic --clear --no-input --verbosity 0
      venv/bin/python manage.py compress --verbosity 0
      venv/bin/python manage.py migrate --run-syncdb
      venv/bin/python manage.py clear_cache
      ```

  * Exit the shell session for user "django"
  * Restart the Uwsgi server: `sudo systemctl restart geany.org.service`
  * Done.
