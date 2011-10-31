Exercise 2 - Advanced buildout
------------------------------

In this exercise, we will turn our minimal buildout into a more modular and
manageable one. At the cost of a bit more complexity, we get builds that work
better in a release process where multiple environments and versions are
involved.

1. In the buildout root, create a file ``versions.cfg`` containing::

	[versions]

2. In the buildout root, create a file ``packages.cfg``::

	[buildout]
	extensions = mr.developer buildout.dumppickedversions
	extends = 
	# Known good sets of eggs we may be using
	    http://dist.plone.org/release/4.1.2/versions.cfg
	    versions.cfg

	versions = versions
	unzip = true

	# Egg sets
	[eggs]
	main =
	    Plone
	test = 
	    
	devtools =
	    bpython
	    plone.reload
	    Products.PDBDebugMode
	    Products.PrintingMailHost
	    Products.DocFinderTab

	# Checkout locations
	[sources]
	
3. Replace the contents of the ``buildout.cfg`` file with::

	# Development environment buildout
	# ================================

	[buildout]
	parts =
	    lxml
	    instance
	    test
	    coverage-report
	    omelette
	    zopepy
	    zopeskel
	    checkversions
	    mkrelease

	extends =
	    packages.cfg

	# Packages to check out/update when buildout is run
	auto-checkout =

	# Make sure buildout always attempts to update packages
	always-checkout = force

	[lxml]
	recipe = z3c.recipe.staticlxml
	egg = lxml

	# Development Zope instance. Installs the ``bin/instance`` script
	[instance]
	recipe = plone.recipe.zope2instance
	http-address = 8080
	user = admin:admin
	verbose-security = on
	eggs =
	    ${eggs:main}
	    ${eggs:devtools}

	# Test runner. Run: ``bin/test`` to execute all tests
	[test]
	recipe = zc.recipe.testrunner
	eggs = ${eggs:test}
	defaults = ['--auto-color', '--auto-progress']

	# Coverage report generator.
	# Run: ``bin/test --coverage=coverage``
	# and then: ``bin/coveragereport``
	[coverage-report]
	recipe = zc.recipe.egg
	eggs = z3c.coverage
	scripts = coveragereport
	arguments = ('parts/test/coverage', 'coverage')

	# Installs links to all installed packages to ``parts/omelette``.
	# On Windows, you need to install junction.exe first
	[omelette]
	recipe = collective.recipe.omelette
	eggs = 
	    ${eggs:main}
	    ${eggs:devtools}

	# Installs the ``bin/zopepy`` interpreter.
	[zopepy]
	recipe = zc.recipe.egg
	eggs = 
	    ${eggs:main}
	    ${eggs:devtools}
	interpreter = zopepy

	# Installs ZopeSkel, which can be used to create new packages
	# Run: ``bin/zopeskel``
	[zopeskel]
	recipe = zc.recipe.egg
	eggs = ZopeSkel

	# Tool to help check for new versions.
	# Run: ``bin/checkversions versions.cfg``
	[checkversions]
	recipe = zc.recipe.egg
	eggs = z3c.checkversions [buildout]

	# Tool to make releases
	# Run: ``bin/mkrelease --help``
	[mkrelease]
	recipe = zc.recipe.egg
	eggs = jarn.mkrelease

If you are on Windows:

 * Skip the ``[lxml]`` part and its entry in the ``parts`` list
 * Skip the ``[omelette]`` part and its entry in the ``parts`` list unless you
   have ``junction.exe`` installed and a reasonably fast computer

This file contains various development tools, all of which we will consider
later.

4. Run the buildout::

	$ bin/buildout

5. Observe that some package versions were picked by Buildout - they are not in
   any KGS. To pin them down, we can copy these into ``versions.cfg``, e.g.::

  	[versions]
  	Cheetah = 2.2.1
	Products.DocFinderTab = 1.0.5
	Products.PDBDebugMode = 1.3.1
	Products.PrintingMailHost = 0.7
	Pygments = 1.4
	ZopeSkel = 3.0a1
	bpython = 0.10.1
	collective.recipe.omelette = 0.12
	jarn.mkrelease = 3.2
	z3c.recipe.staticlxml = 0.8

	#Required by:
	#jarn.mkrelease 3.2
	lazy = 1.0

	#Required by:
	#jarn.mkrelease 3.2
	setuptools-git = 0.4.2

	#Required by:
	#jarn.mkrelease 3.2
	setuptools-hg = 0.2.1

	#Required by:
	#templer.plone 1.0a1
	#templer.zope 1.0a2
	#ZopeSkel 3.0a1
	templer.buildout = 1.0a2

	#Required by:
	#templer.plone 1.0a1
	#templer.buildout 1.0a2
	#templer.zope 1.0a2
	#ZopeSkel 3.0a1
	templer.core = 1.0b3

	#Required by:
	#ZopeSkel 3.0a1
	templer.plone = 1.0a1

	#Required by:
	#templer.plone 1.0a1
	#ZopeSkel 3.0a1
	templer.zope = 1.0a2

	#Required by:
	#z3c.recipe.staticlxml 0.8
	zc.recipe.cmmi = 1.3.5

6. To test that Plone is still working, start up Zope::

	$ bin/instance fg

7. To test that our version pins worked, run buildout again::

	$ bin/buildout

This time, there should be no picked packages.