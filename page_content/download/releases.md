Releases
==========

Distribution      | File          | GPG Signature | GPG Key
----------------- | ------------- | ------------- | -------------
Source (tar.gz)   | [{{ release_versions.source_gzip_version }}](https://download.geany.org/{{ release_versions.source_gzip_version }}) | [{{ release_versions.source_gzip_version }}.sig](https://download.geany.org/{{ release_versions.source_gzip_version }}.sig) ([Instructions][4]) | [colombanw-pubkey.txt][1]
Source (tar.bz2)  | [{{ release_versions.source_bzip2_version }}](https://download.geany.org/{{ release_versions.source_bzip2_version }}) | [{{ release_versions.source_bzip2_version }}.sig](https://download.geany.org/{{ release_versions.source_bzip2_version }}.sig) ([Instructions][4]) | [colombanw-pubkey.txt][1]
Windows           | [{{ release_versions.windows_version }}](https://download.geany.org/{{ release_versions.windows_version }}) | [{{ release_versions.windows_version }}.sig](https://download.geany.org/{{ release_versions.windows_version }}.sig) ([Instructions][4]) | [eht16-pubkey.txt][2]
Mac OSX           | [{{ release_versions.macos_version }}](https://download.geany.org/{{ release_versions.macos_version }}) | - | -

[Release notes for Geany {{ geany_latest_version.version }}][3]


## Plugins

Geany has a few plugins included (Classbuilder, Export, Filebrowser, HTML Characters, Save Actions and Split Window)
but many more plugins are available in the [Geany-Plugins][5] project.

For more details, see the [plugin page][5].


## Older versions

For older versions, please see https://download.geany.org/.

- Note: Tarballs before 1.34 used another GPG Key: https://download.geany.org/eht16-pubkey_old.txt
- Note: Tarballs before 1.32 used another GPG Key: https://download.geany.org/colombanw-pubkey.txt
- Note: Tarballs before 1.25 used another GPG Key: https://download.geany.org/colombanw-pubkey-pre-1.25.txt
- Note: Tarballs before 0.21 used another GPG Key: https://download.geany.org/ntrel-pubkey.txt
- Note: Tarballs before 0.20 used another GPG Key: https://download.geany.org/eht16-pubkey_old.txt

[1]: https://download.geany.org/colombanw-pubkey.txt
[2]: https://download.geany.org/eht16-pubkey.txt
[3]: /documentation/releasenotes/
[4]: /support/verify-gpg-signature/
[5]: /support/plugins/
