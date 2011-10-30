Exercise 7 - Sphinx documentation
---------------------------------

Documenting a project can be a chore. To make it easier, we can keep the docs
with our build, which has the added advantage that they are versioned with the
build. We can use Sphinx for this. See http://sphinx.pocoo.org/ for more.

1. Add the following to ``buildout.cfg``::

    [buildout]
    ...
    parts = 
        ...
        build-docs
    
    [build-docs]
    recipe = collective.recipe.sphinxbuilder
    source = ${buildout:directory}/docs-source
    build = ${buildout:directory}/docs
    interpreter = ${buildout:directory}/bin/zopepy
    eggs = repoze.sphinx.autointerface

2. Create a simple project::

    $ mkdir docs-source
    $ cd docs-source
    $ ../bin/sphinx-quickstart
    $ cd ..

Answer the questions with defaults, except where project-specific information
is required.

Answer 'n' when asked if you want to create a makefile.

3. Run the documentation builder from the buildout root:

    $ bin/build-docs

The default documentation can now be found in ``docs/html/index.html``.

4. Edit ``index.rst`` to update the documentation. See 
   http://docutils.sourceforge.net/docs/user/rst/quickstart.html for details
   about the reStructuredText syntax.

5. Edit ``docs/conf.py`` and change the list of extension to::

    extensions = ['sphinx.ext.autodoc',
                  'sphinx.ext.doctest',
                  'repoze.sphinx.autointerface']

6. Edit ``index.rst`` to add a reference to a new file, ``acme.custom.rst``,
   where we will begin to document the ``acme.custom`` package::

    Welcome to Acme Corp's documentation!
    =====================================

    Contents:

    .. toctree::
       :maxdepth: 2

       acme.custom

7. Add an ``acme.custom.rst`` in the ``docs-source`` folder, containing::

    :mod:`acme.custom` - Custom Acme Corp views
    ===========================================

    This package contains custom views used in the Acme Corp website.

    Interfaces
    ----------

    .. autointerface:: acme.custom.interfaces.ISearchHelpers
        :members:

    Views
    -----

    .. autoclass:: acme.custom.browser.helpers.SearchHelpers
        :members:
    
    .. autoclass:: acme.custom.browser.search.AcmeSearch
        :members:


8. Run the docs builder again. Look out for errors in the console output::

    $ bin/build-docs

The documentation should now be updated with the new page, plus docstrings for
the interface. The ``SearchHelpesr`` and ``AcmeSearch`` view classes are
sparsely, documented, however, because they don't have docstrings.

9. Add some docstrings to these views and their methods and re-run the docs
   builder to see the documentation take shape.
