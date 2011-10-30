Exercise 1 - Minimal buildout
-----------------------------

0. Create a ~/.buildout/default.cfg file::

	[buildout]
	eggs-directory = /<homedir>/.buildout/eggs
	download-cache = /<homedir>/.buildout/downloads
	extends-cache  = /<homedir>/.buildout/extends

To work out your home directory path, run::

	$ python -c "import os.path; print os.path.expanduser('~')"

Create the ~/.buildout/eggs, ~/.buildout/downloads and ~/.buildout/extends folders.

1. In the top level exercise folder, download bootstrap.py::

	$ curl -O http://python-distribute.org/bootstrap.py

2. Create a buildout.cfg file like so::

	[buildout]
	parts = instance
	extends =
	    http://dist.plone.org/release/4.1.2/versions.cfg

	[instance]
	recipe = plone.recipe.zope2instance
	http-address = 8080
	user = admin:admin
	eggs = Plone

3. Run bootstrap with a Python 2.6 binary::

	$ python2.6 bootstrap.py

4. Run the buildout::

	$ bin/buildout

5. Start Zope in the foreground (debug mode)::

	$ bin/instance fg

6. Open a browser at http://localhost:8080 and create a new Plone site
