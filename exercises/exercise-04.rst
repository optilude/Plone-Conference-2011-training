Exercise 4 - Using mr.developer
-------------------------------

In this exercise, we will add Products.RedirectionTool as a dependency, but
track it from source so that we can work on it.

1. Edit ``setup.py`` in ``acme.policy`` to add the dependency::

      install_requires=[
          'setuptools',
          'Plone',
          'Products.RedirectionTool',
          # -*- Extra requirements: -*-
      ],

2. Edit ``profiles/default/metadata.xml`` in ``acme.policy`` to install the
   dependency::

        <?xml version="1.0"?>
        <metadata>
          <version>0001</version>
          <dependencies>
            <dependency>profile-Products.RedirectionTool:default</dependency>
          </dependencies>
        </metadata>

3. Run the build to see it installed:

    $ bin/buildout

Let's pretend we now noticed a bug that we want to fix. We can track
Products.RedirectionTool from source easily with ``mr.developer``.

4. Edit ``packages.cfg`` to add the source location::

    # Checkout locations
    [sources]
    acme.policy = fs acme.policy
    Products.RedirectionTool = svn http://svn.plone.org/svn/collective/RedirectionTool/trunk

Note: See the ``mr.developer`` documentation for other supported version
control systems, including Git and Mercurial.

5. We can now see this in the list of available develop packages::

    $ bin/develop list
    Products.RedirectionTool
    acme.policy

6. Let's activate it::

    $ bin/develop activate Products.RedirectionTool
    $ bin/buildout

Check out the contents of e.g. ``bin/instance`` to verify that this egg is now
being loaded from ``src`` instead of an egg.

Other commands
~~~~~~~~~~~~~~

We can now work on this package in src, and check in changes when necessary.

We can check the status of all our packages at once with::

    $ bin/develop status

This will show any dirt packages, for example.

We can rebuild with the last buildout parameters using::

    $ bin/develop rebuild

This is particularly useful if we've used a number of parameters to
``bin/buildout``, such as ``-c`` to pick a different configuration file than
``buildout.cfg``.

To check out the package every time we run the buildout (and so share the fact
that this package is checked out among all members of the team), we can add it
to the ``auto-checkout`` list in ``buildout.cfg``::
    
    # Packages to check out/update when buildout is run
    auto-checkout =
        acme.policy
        Products.RedirectionTool

To deactivate, but leave checked out::

    $ bin/develop deactivate Products.RedirectionTool
    $ bin/develop rebuild

This should now pick an egg instead of using the develop distribution.

We should add this to ``versions.cfg`` to pin it down!

