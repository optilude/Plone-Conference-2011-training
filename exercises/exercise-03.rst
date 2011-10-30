Exercise 3 - Policy package
---------------------------

1. Run ZopeSkel from the src directory::

    $ cd src
    $ ../bin/zopeskel plone_basic acme.policy

   Answer 'True' when asked whether to register a profile.

2. Edit the generated ``acme.policy/setup.py`` to add ``Plone`` as an egg
   dependency::

      install_requires=[
          'setuptools',
          'Plone',
          # -*- Extra requirements: -*-
      ],

3. Edit the generated ``acme.policy/src/acme/policy/configure.zcml`` to remove
   the ``<five:registerPackage />`` line and add an ``<includeDependencies />``
   directive::

        <configure
            xmlns="http://namespaces.zope.org/zope"
            xmlns:five="http://namespaces.zope.org/five"
            xmlns:i18n="http://namespaces.zope.org/i18n"
            xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
            i18n_domain="acme.policy">

          <includeDependencies package="." />

          <genericsetup:registerProfile
              name="default"
              title="acme.policy"
              directory="profiles/default"
              description="Installs the acme.policy package"
              provides="Products.GenericSetup.interfaces.EXTENSION"
              />
          <!-- -*- extra stuff goes here -*- -->
          
        </configure>

   The ``<five:registerPackage />`` directive should be kept for packages
   containing Archetypes content types.


4. Empty out the file ``src/acme.policy/src/acme/policy/__init__.py``. Again,
   this is only useful for things like Archetypes content types that need magic
   initialisation.

5. Edit the top level ``packages.cfg`` file, replacing the ``[eggs]`` and
   ``[sources]`` parts with::

        # Egg sets
        [eggs]
        main =
            acme.policy
        test = 
            acme.policy [test]
            
        devtools =
            bpython
            plone.reload
            Products.PDBDebugMode
            Products.PrintingMailHost
            Products.DocFinderTab

        # Checkout locations
        [sources]
        acme.policy = fs acme.policy

6. Edit the top level ``buildout.cfg`` file, changing the ``auto-checkout``
   line to::

        # Packages to check out/update when buildout is run
        auto-checkout =
            acme.policy

7. Re-run buildout::
    
    $ bin/buildout
    
