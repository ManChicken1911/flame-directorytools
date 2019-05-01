# Flame DirectoryTools
by Bob Maple (bobm-matchbox [at] idolum.com)

This script is licensed under the Creative Commons Attribution-ShareAlike [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)


## What

DirectoryTools is a Python script for **Autodesk Flame 2020 and above** that
adds a context menu to the MediaHub letting you TAR or ZIP directories
from within the Flame file browser.


## Installing

In Flame 2020 these hook scripts are more flexible and no longer need to be
manually merged into the main hooks file.

To install, simply copy DirectoryTools.py to /opt/Autodesk/shared/python for
access by everyone:

`cp DirectoryTools.py /opt/Autodesk/shared/python/`

then either restart Flame or use the Flame hotkey **Shift-Control-H-P** to
reload all Python hooks.


## Using

From within MediaHub, select a directory or directories and right-click to
bring up the context menu. You should see a new item called **Directory Tools**
at or near the bottom of the menu, and can choose to either TAR or ZIP the
selected directories. If multiple directories are selected, each one will be
tarred or zipped separately in their own archive.

### Notes on TAR files
After the .tar file is created, a companion file called .tar.list is created
showing the contents of the archive.

### Notes on ZIP files
You may optionally encrypt the .zip with a password; simply enter the desired
password when asked. If you do not want a password-protected zip, leave it
blank or hit the Cancel button.

**SECURITY NOTE:** Please be aware that the password is passed to zip on the
commandline and is therefore insecure; if other users are logged in to
the workstation at the same time, they can potentially see the process running
with all its arguments including the password, and/or get it from the
temporary script file DirectoryTools makes in /tmp/ while it's running, or
afterwards if for some reason it fails to delete its self.

### Notes for all files
The tar or zip process is run in the background and there is no GUI
indication when it's done. However, while the archive is being created
it will have "_busy" on the end of the filename which gets removed
once the archive is complete.
