Exercise 12 - Load testing
--------------------------

In this exercise, we will create a simple load testing script using Funkload.
See http://funkload.nuxeo.org/ for more details.

To see the load testing graphs, ensure you have ``gnuplot`` installed.

1. Update ``buildout.cfg`` to add the following part::

    [buildout]
    parts =
        ...
        funkload
    
    ...

    [funkload]

2. Re-run buildout::

    $ bin/buildout
    
3. Add the relevant pins to ``version.cfg``::
    
    [versions]
    funkload = 1.16.1
    tcpwatch = 1.3.1
    webunit = 1.3.10

4. We will begin by recording some tests using ``fl-record``. First, start up
   the development build. Leave this running for now::

    $ bin/instance fg

5. Create a directory for the load tests::

    $ mkdir loadtests

6. In a separate console, start up ``fl-record`` from within this directry::

    $ cd loadtests
    $ PATH=$PATH:$(pwd)/../bin ../bin/fl-record search

We need to trick it into finding the ``tcpwatch`` script that was installed in
the ``bin`` directory.

6. In your browser of choice, add set the HTTP proxy to::

    http://localhost:8090

7. Open the Plone site and perform a few content searches.

8. Press ``Ctrl+C`` in the terminal running ``fl-record``. It will write out
   two files: ``Search.conf`` and ``test_Search.py``.

9. Edit ``Search.conf`` to set better descriptions for the test cases or change
   the base URL.

10. Edit ``test_search.py`` if you want to change or parameterise the test. For
    now, just strip out the ``livesearch_reply`` call, which we do not need to
    test.

Notice how the test is just a ``unittest`` that uses some Funkload APIs to
make requests.

11. You can run the test once through with::

        $ ../bin/fl-run-test -dv test_Search.py 

12. Next, run an actual benchmark::

        $ ../bin/fl-run-bench -c 1:10:20 -D 10 test_Search.py Search.test_search

This will run three test cycles, each of 10 seconds, with 1, 10 and 20
concurrent users simulated, respectively. You will see reports about the success
rate of tests (e.g. if the server stopped responding), and the current directory
will contain test outputs. The main output file is ``search-bench.xml``, which
contains the actual test results.

13. Let's generate a report::

        $ ../bin/fl-build-report --html search-bench.xml

Watch the output to understand which file it generated (there is an automatic
timestamp). Open it in a browser, e.g.::

        $ open test_search-20111031T001005/index.html

Try to understand the report:

 * What is the difference between requests per second and pages per second?
 * What could be causing slow requests?
 * Which pages are fastest?
 * Are pages being cached?
 
We have cheated here and tested against the development build. In the real
world, we would most likely test against a remote server (using the ``--url``
parameter to ``fl-run-bench``) running the deployment configuration of our
code.

This really just scratches the surface of what Funkload can do. For example:

 * You can add test assertions to ensure the site's behaviour is correct
   under load.
 * You can distribute test cycles across multiple testing nodes for more
   realistic (or simply more intensive) testing.
 * Funkload can monitor key statistics (CPU, memory usage, disk activity, 
   network activity) on each server in the deployment configuration and/or
   the testing nodes and correlate these with load test results to help you
   understand what resources are constraining your site's performance.
 * You can use the Funkload credentials server to manage and distribute
   login details among tests so that you can effectively test concurrent
   logins without using the same username/password for every test thread.
 * Consider running load tests in a separate build in a CI server like
   Jenkins.

Read more at http://funkload.nuxeo.org.