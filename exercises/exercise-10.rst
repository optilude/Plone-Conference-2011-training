Exercise 10 - Making releases
-----------------------------

For repeatability and control, we will normally create releases of our custom
packages (or any non-releasable internal modifications to third-party packages).

Packages need to be deployed to an egg index. For the purposes of this
exercise, we'll create a local egg index server, though normally this would be
running on a shared development server. We will also be making use of local
git repositories for tagging and source code management. Again, these would
more commonly be on a shared server.

Before starting, please make sure that it is possible to ssh into your host. You
may need to enable SSH / remote login::

    $ ssh localhost

1. Create a location that will serve as a dummy git repository server::

    $ mkdir ~/git-repos

Up to now, we have kept our source code inside the build and used ``fs`` source
locations in the ``[sources]`` list for ``mr.developer``. Normally, we would
version each package separately, using ``mr.developer`` to pull them into the
from the appropriate sources.

Let us now organise our build accordingly by create two repositories in the
directory above.

2. Copy the ``acme.policy`` and ``acme.custom`` packages there, and give each
   a ``.gitignore`` file::

    $ cp -r src/acme.policy ~/git-repos
    $ cp -r src/acme.custom ~/git-repos
    $ cp .gitignore ~/git-repos/acme.policy/
    $ cp .gitignore ~/git-repos/acme.custom/

3. Initialise the repositories, add the soruces and commit the changes::

    $ cd ~/git-repos/acme.policy
    $ git init
    $ git add .gitignore CHANGES.txt CONTRIBUTORS.txt README.txt bootstrap.py buildout.cfg docs setup.py src
    $ git commit -m "Policy package"
    $ cd -

    $ cd ~/git-repos/acme.custom
    $ git init
    $ git add .gitignore CHANGES.txt CONTRIBUTORS.txt README.txt bootstrap.py buildout.cfg docs setup.py src
    $ git commit -m "Custom views"    
    $ cd -

4. Remove the directories from their original location in the build::
    
    $ git rm -r src/acme.policy src/acme.custom
    $ rm -r src/acme.policy src/acme.custom

5. Update the ``mr.developer`` configuration in ``packages.cfg`` to reflect the
   new locations::

    [sources]
    acme.policy = git /<homedir>/git-repos/acme.policy
    acme.custom = git /<homedir>/git-repos/acme.custom

Replace ``<homedir>`` with the full path to your home directory.

6. Verify that this works by running the development build. The packages should
   appear as git clones in ``src/``::

    $ cd src/acme.policy
    $ git remote -v
    origin  /Users/optilude/git-repos/acme.policy (fetch)
    origin  /Users/optilude/git-repos/acme.policy (push)
    $ cd -

7. Commit the changes to the build::

    $ git commit -a -m "Move to decentralised model"

8. Create a location from which we can serve our dummy egg index::

    $ mkdir ~/egg-index

We are now ready to make releases of our custom packages.

9. Verify that you are ready to release each egg:

   * The version number in ``setup.py`` is correct
   * The ``CHANGES.txt`` file contains the appropriate changelog entries to
     describe what has changed since the last release
   * All the tests pass

10. Release the eggs using ``jarn.mkrelease`` and SCP::

    $ cd src/acme.policy
    $ ../../bin/mkrelease -d localhost:~/egg-index/
    $ cd -

    $ cd src/acme.custom
    $ ../../bin/mkrelease -d localhost:~/egg-index/
    $ cd -

Again, the SCP location (``localhost:~/egg-index``) would usually be for a
remote server, not localhost.

See http://pypi.python.org/pypi/jarn.mkrelease for the other options and usage
modes of ``jarn.mkrelease``.

11. Start an egg index server.

This is simply an HTTP server that will allow
Buildout to locate and download the newly created archives of our two
packages. In a production scenario, you may want to use ``nginx`` or
``Apache`` configured to serve the directory where the eggs are being SCP'd
*with a directory listing*. However, we can also use a server built into Python.

In a separate terminal, let the following command run::

    $ cd ~/egg-index
    $ python -m SimpleHTTPServer

To verify that it works, open::

    http://localhost:8000

The two zip archives should be available for download.

12. Tell buildout about the index server. In ``deployment.cfg`` uncomment and
    modify this line::

        find-links = http://localhost:8000/

13. Make sure the packageas are not in the ``auto-checkout`` list::

        auto-checkout =

14. Add the packages with the correct version numbers to ``versions.cfg``::
    
        [versions]
        # Custom packages
        acme.policy = 1.0
        acme.custom = 1.0

15. Verify that the build works::

        $ bin/buildout -c deployment.cfg


If you inspect e.g. ``bin/instance1``, you should see the reference to an
installed (non-develop) egg for ``acme.policy`` and ``acme.custom``::

        $ cat bin/instance1 | grep acme  
        '/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.policy/src',
        '/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src',

16. Tag the build

        $ git commit -a -m "Getting ready to tag build v1.0"
        $ git tag "1.0"

In a real-world scenario where the build was checked out from a remote server,
we would also push the tag::

        $ git push --tags

We would then use this for a deployment, by checking out the tag on the relevant
server and running the build, which will download our custom eggs from the
internal egg index and build everything from stable packages. To roll back to a
previous version, you can check out an older tag of the build and re-run
buildout, which will use whatever versions of custom (and third-party) packages
were pinned in ``versions.cfg`` at the time.

If we now revert to the development build, it will use the development
checkouts, since we haven't cleared ``auto-checkout`` in ``buildout.cfg``. This
may be appropraite, but for larger projects or organisations with shared
packages used across multiple projects, it is probably best to clear out the
``auto-checkout`` list in ``buildout.cfg`` (and any other files) when an
appropriate release has been made.

If development then resumes on a package, it can be checked out with
``mr.developer``::

    $ bin/develop activate acme.custom
    $ bin/develop rebuild

If this checkout then needs to be shared by all developers (e.g. if a
development version is required for the build to work), it can be added back to
the ``auto-checkout`` list.
