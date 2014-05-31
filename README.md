SimpleWebPaste
==============

A small pyramid webapp for self-hosted pastebin-like service


Configuration
-------------

  - ```development.ini``` contains a version suitable for testing, you might want to change ```debugtoolbar.hosts``` to something suitable.
  - ```production.ini``` contains a version suitable for deployment, and disables testing functions and removes the toolbar.
  - By default, a user _test_ with password _test_ is enabled. Edit ```security.py``` to add users and passwords.

Templates
---------
The template used for the login page is ```templates/login.jinja2```, for the paste page it is ```paste.jinja2```, and finally the viewer uses a placeholder ```view.jinja2```. All of them rely on css files located in ```static/css```.

Acknowledgments
---------------
The code to convert input into pretty output was done by Ninjifox and can be found at https://github.com/Ninjifox/SimplePaste
