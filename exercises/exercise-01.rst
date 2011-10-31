Exercise 1 - Minimal buildout
-----------------------------

Plone can be installed as an egg, so long as we we use the right Known Good Set
(KGS) of packages to lock down the correct versions of all of its dependencies.
In this exercise we'll show the smallest possible buildout that produces a
usable Plone site.

Before we start, we should ensure we have a shared cache for eggs and downloads
that buildout fetches from the internet. This helps reduce download times
without compromising repeatability.

If you don't have one already, create a ~/.buildout/default.cfg file::

	[buildout]
	eggs-directory = /<homedir>/.buildout/eggs
	download-cache = /<homedir>/.buildout/downloads
	extends-cache  = /<homedir>/.buildout/extends

To work out your home directory path, run::

	$ python -c "import os.path; print os.path.expanduser('~')"

Create the ``~/.buildout/eggs``, ``~/.buildout/downloads`` and
``~/.buildout/extends`` folders as required.

Let's now create a buildout in a new directory::

	$ mkdir build
	$ cd build

1. In the top level exercise folder, download ``bootstrap.py``::

	$ curl -O http://python-distribute.org/bootstrap.py

2. Create a ``buildout.cfg`` file like so::

	[buildout]
	parts = instance
	extends =
	    http://dist.plone.org/release/4.1.2/versions.cfg

	[instance]
	recipe = plone.recipe.zope2instance
	http-address = 8080
	user = admin:admin
	eggs = Plone

3. Run ``bootstrap.py`` with a Python 2.6 binary::

	$ python2.6 bootstrap.py

4. Run the buildout::

	$ bin/buildout

5. Start Zope in the foreground (debug mode)::

	$ bin/instance fg

6. Open a browser at http://localhost:8080 and create a new Plone site
