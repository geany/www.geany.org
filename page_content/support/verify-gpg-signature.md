Verifying GPG signatures of Geany and Geany-Plugins releases
==========

You can use the `gpg` utility. On Debian based distributions, if you don't have it, you can get it with `sudo apt install gpg`. On other operating systems, see https://gnupg.org/download/index.html and https://gnupg.org/download/integrity_check.html.

### Here is how to use `gpg` on Linux-like distributions

First, you need to import the public GPG key used to sign the packages. You can download the used public key from: https://download.geany.org/colombanw-pubkey.txt

To import the key use:
```Bash
gpg --import < colombanw-pubkey.txt
```

To actually verify the downloaded archive, use one of the following commands according to the archive you have downloaded:

For tar.bz2:
```Bash
gpg --verify geany-1.34.tar.bz2.sig geany-1.34.tar.bz2
```

For tar.gz:
```Bash
gpg --verify geany-1.34.tar.gz.sig geany-1.34.tar.gz
```

The command's output should state something like "Good signature" and should return with an exit code of 0. If you get another exit code, something went wrong.

A complete example:
```Bash
wget https://download.geany.org/colombanw-pubkey.txt
gpg --import < colombanw-pubkey.txt
gpg --verify geany-1.34.tar.bz2.sig geany-1.34.tar.bz2
```
