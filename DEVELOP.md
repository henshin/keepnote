Developing KeepNote
===================

## Linux/Mac OS X development.

Follow the install instructions to install all third-party libraries. Next,
a development enviroment can be setup by using the provided `Makefile`:

```sh
make dev
```

This should create a Python virtualenv directory `env` and install
several javascript related directories `node_modules` and
`bower_components`.

Tests can be run using:

```sh
make test
```

and code-quality can be checked using:

```sh
make cq
```


## Windows Build

Most people will just want to install KeepNote.  For basic
installation, see the [Windows Install instructions](INSTALL.md).  These
instructions are for developers who want to *build* the windows
installer.
  
### Fork Update 
I've spent an incredible amount of time of testing to find the right setup for compiling Keepnote on Windows.
These are the updated instructions on how to compile KeepNote on Windows with Python 2.6.6. This is the latest working version of Python that allows you to compile the code without major changes. I tried to compile it with Python 2.7 too but a lot of things have changed from 2.6 to 2.7 and I couldn't get it to work.

Here are the updated list of packages you need to install:
```
python-2.6.6.msi
gtk-dev-2.12.9-win32-2.exe

py2exe-0.6.9.win32-py2.6.exe
pycairo-1.4.12-2.win32-py2.6.exe
pygobject-2.14.2-2.win32-py2.6.exe
pygtk-2.12.1-3.win32-py2.6.exe
pywin32-210.win32-py2.6.exe

isetup-5.2.3.exe (Inno Setup - This is optional)
```
**Note:** Most of the packages can be downloaded from the site https://ftp.gnome.org/pub/GNOME/binaries/win32/. Py2exe can be downloaded from https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/

You need to readjust the PATH variable to include the following Python directories:
```
c:\python26;c:\python26\scripts
```

Verify that python can be run from any directory:
```
C:\> python -V
Python 2.6.6
```
Additionally I had to install a few more Python packages required by the Syntax Highlighting extension.
Download the following modules from the official PyPi (https://pypi.org/) website:
```
setuptools-0.6c11-py2.6.egg
Pygments-1.6-py2.6.egg
html-1.16.tar.gz
pip-9.0.3.tar.gz
colorama-0.3.9-py2.py3-none-any.whl
```

Download the [ez_setup.py](http://peak.telecommunity.com/dist/ez_setup.py)
Make sure you put it on the same directory as the modules above, then do: 
```
python .\ez_setup.py
```

This will install the `setuptools-0.6c11-py2.6.egg` mentioned above. From this point onwards we can use the `easy_install` script to install the other modules:

```
easy_install .\pip-9.0.3.tar.gz
easy_install .\Pygments-1.6-py2.6.egg
easy_install .\html-1.16.tar.gz
```
The module missing is `colorama` which for some strange reason couldn't be installed using the normal method. That is why we need a primitive version of `pip` here.
```
pip install colorama-0.3.9-py2.py3-none-any.whl
```
If you are thinking on why haven't we used `pip` to install everything automatically it's because Python 2.6 does not support the latest versions of TLS (which PyPi uses) so you will run into a lot of problems when trying to download things.
### -- End of Fork Update --
Once third-party packages are installed, execute in the KeepNote
source directory:

```sh
python setup.py py2exe
```

If everything runs smoothly, you should have your freshly compiled version of KeepNote on the `dist` directory. You can them copy it anywhere else and use it normally.

Use Inno to compile `installer.iss` into the final installer `*.exe`.

The `Makefile` includes a target `winebuild` to cross-compile the Windows
installer from Linux using [Wine](https://www.winehq.org/).

```sh
make winebuild
```
