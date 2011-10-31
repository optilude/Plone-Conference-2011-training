Exercise 8 - Continuous Integration
-----------------------------------

Continous Integration is used to run all the tests of a projcet each time the
code is changed, to notify of regressions quickly. The most popular open source
CI tool is Jenkins (formerly Hudson).

For the purposes of this exercise, we will assume the build is in a local git
repository.

1. Download the Java Web Archive build of Jenkins from http://jenkins-ci.org.

2. Run it in its own terminal::

    $ java -jar jenkins.war

This will create some files in ~/.jenkins initially. Note that builds go here
by default, so this directory can get large after a while.

3. Go to "Manage Jenkins" at http://localhost:8080 and install the following
   plugins through the web interface:
   
   * Git plugin
   * HTML publisher plugin

4. Edit ``buildout.cfg`` to add the following parts::

    [buildout]
    parts =
        ...
        ci-test
        ci-coverage
    
    ...

    # CI test
    [ci-test]
    recipe = collective.xmltestreport
    eggs = ${eggs:test}
    defaults = ['--auto-color', '--auto-progress', '--xml', '--coverage=coverage']

    [ci-coverage]
    recipe = zc.recipe.egg
    eggs = z3c.coverage
    scripts = coveragereport
    arguments = ('parts/ci-test/coverage', 'coverage')

Ensure the changes are committed in your Git repository checkout: Jenkins needs
to be able to check it out.

Alternatively, you can run the examples below against the GitHub location of
these exercies, with the ``exercise-08-answer`` branch.

5. In the Jenkins console on ``http://localhost:8080``, create a new job using
   the "free-style software project" template, called e.g. ``acme``.

Note: Do not put spaces in the project name!

6. Set up Git source code management. In the "URL of repository" box, enter the
   path to your local repository. In the "branch specifier", enter the branch
   you are working on, e.g. "execise-08".

7. Add a build step of type
   "Execute shell" with the following commands::

    python bootstrap.py
    bin/buildout
    bin/ci-test
    bin/ci-coverage
    bin/build-docs

8. Enable "Publish HTML reports" and add two reports::

    Directory   Index file  Report title

    docs/html   index.html  Documentation
    coverage    all.html    Coverage report

9. Enable "Publish JUnit test result report" and set it to::

    parts/ci-test/testreports/*.xml

10. Trigger the build from the Jenkins front page (click the project and then
   build now). You can see the console output while it runs.

11. Observe the output and published test results, documentation and coverage
    report.

Normally, we would set up Jenkins to poll for changes in the source control
system or run the tests on a timer. Refer to the Jenkins Documentation for
details.