## Geany Releases

Distribution          | File          | GPG Signature | GPG Key
--------------------- | ------------- | ------------- | -------------
Source (tar.gz)       | [{{ release_versions.source_gzip_version }}](https://download.geany.org/{{ release_versions.source_gzip_version }}) | [{{ release_versions.source_gzip_version }}.sig](https://download.geany.org/{{ release_versions.source_gzip_version }}.sig) ([Instructions][4]) | [colombanw-pubkey.txt][1]
Source (tar.bz2)      | [{{ release_versions.source_bzip2_version }}](https://download.geany.org/{{ release_versions.source_bzip2_version }}) | [{{ release_versions.source_bzip2_version }}.sig](https://download.geany.org/{{ release_versions.source_bzip2_version }}.sig) ([Instructions][4]) | [colombanw-pubkey.txt][1]
Windows (64-bit[^1])  | [{{ release_versions.windows_version }}](https://download.geany.org/{{ release_versions.windows_version }}) | [{{ release_versions.windows_version }}.sig](https://download.geany.org/{{ release_versions.windows_version }}.sig) ([Instructions][4]) | [eht16-pubkey.txt][2]
macOS                 | [{{ release_versions.macos_version }}](https://download.geany.org/{{ release_versions.macos_version }})<br>[{{ release_versions.macos_version_arm64 }}](https://download.geany.org/{{ release_versions.macos_version_arm64 }}) | - | -

[Release notes for Geany {{ geany_latest_version.version }}][3]

For instructions on installing GTK themes on Windows and macOS see the [corresponding FAQ entry](/documentation/faq/#how-to-change-the-gtk-theme).

## Geany-Plugins Releases

Geany has a few plugins included (Classbuilder, Export, Filebrowser, HTML Characters, Save Actions and Split Window)
but many more plugins are available in the [Geany-Plugins][5] project:

Distribution          | File          | GPG Signature | GPG Key
--------------------- | ------------- | ------------- | -------------
Source (tar.gz)       | [{{ plugins_release_versions.source_gzip_version }}](https://plugins.geany.org/geany-plugins/{{ plugins_release_versions.source_gzip_version }}) | [{{ plugins_release_versions.source_gzip_version }}.sig](https://plugins.geany.org/geany-plugins/{{ plugins_release_versions.source_gzip_version }}.sig) ([Instructions][4]) | [frlan-pubkey.txt][6]
Source (tar.bz2)      | [{{ plugins_release_versions.source_bzip2_version }}](https://plugins.geany.org/geany-plugins/{{ plugins_release_versions.source_bzip2_version }}) | [{{ plugins_release_versions.source_bzip2_version }}.sig](https://plugins.geany.org/geany-plugins/{{ plugins_release_versions.source_bzip2_version }}.sig) ([Instructions][4]) | [frlan-pubkey.txt][6]
Windows (64-bit[^1])  | [{{ plugins_release_versions.windows_version }}](https://plugins.geany.org/geany-plugins/{{ plugins_release_versions.windows_version }}) | [{{ plugins_release_versions.windows_version }}.sig](https://plugins.geany.org/geany-plugins/{{ plugins_release_versions.windows_version }}.sig) ([Instructions][4]) | [frlan-pubkey.txt][6]
macOS                 | (included in `{{ release_versions.macos_version }}` above) | - | -

[Release notes for Geany-Plugins {{ geany_plugins_latest_version.version }}][7]

For more details, see the [plugin page][5].


## Older versions

For older versions, please see https://download.geany.org/.

- Note: Tarballs before 1.34 used another GPG Key: https://download.geany.org/eht16-pubkey_old.txt
- Note: Tarballs before 1.32 used another GPG Key: https://download.geany.org/colombanw-pubkey.txt
- Note: Tarballs before 1.25 used another GPG Key: https://download.geany.org/colombanw-pubkey-pre-1.25.txt
- Note: Tarballs before 0.21 used another GPG Key: https://download.geany.org/ntrel-pubkey.txt
- Note: Tarballs before 0.20 used another GPG Key: https://download.geany.org/eht16-pubkey_old.txt
- Note: Geany-Plugins downloads use the following GPG Key: https://download.geany.org/frlan-pubkey.txt

[1]: https://download.geany.org/colombanw-pubkey.txt
[2]: https://download.geany.org/eht16-pubkey.txt
[3]: /documentation/releasenotes/
[4]: /support/verify-gpg-signature/
[5]: /support/plugins/
[6]: https://download.geany.org/frlan-pubkey.txt
[7]: https://raw.githubusercontent.com/geany/geany-plugins/{{ geany_plugins_latest_version.version }}/NEWS

[^1]: *The Windows installers require a 64-bit system. Older releases work also on 32-bit Windows systems.*
