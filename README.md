SimpleWebPaste
==============

A small pyramid webapp for self-hosted pastebin-like service


Configuration
-------------

  - ```development.ini``` contains a version suitable for testing, you might want to change ```debugtoolbar.hosts``` to something suitable.
  - ```production.ini``` contains a version suitable for deployment, and disables testing functions and removes the toolbar.
  - By default, a user _test_ with password _test_ is enabled. Edit ```security.py``` to add users and passwords.

Installation
------------

  - First, get the contents of this repository : git clone git://github.com/epithumia/SimpleWebPaste
  - Edit the files mentioned above
  - Run ```pip setup -e .``` (or better yet, make a virtualenv first, then ```$venv/bin/pip setup -e .```)
  - Start the server with ```pserve development.ini``` (or ```$venv/bin/pserve development.ini```).
  - The development.ini and production.ini files are usable as-is with nginx, but will run fine without.

Templates
---------
The template used for the login page is ```templates/login.jinja2```, for the paste page it is ```paste.jinja2```, the pastes are generated using ```render.jinja2``` and finally the viewer uses a placeholder ```view.jinja2``` to either display the paste or an error message. All of them rely on css files located in ```static/css```.

Acknowledgments
---------------
The code to convert input into pretty output was done by Ninjifox and can be found at https://github.com/Ninjifox/SimplePaste
