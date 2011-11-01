Exercise 6 - Test runner and coverage reporting
-----------------------------------------------

The ``acme.custom`` package has some tests in ``tests/test_views.py``, and a
layer setting up its configuration and installing its extension profile in
``testing.py`` (please see http://pypi.python.org/pypi/plone.app.testing/ for
more details). We have also made sure its tests are part of the standard test
run by adding this to ``packages.cfg``::

    # Egg sets
    [eggs]
    main =
        acme.policy
    test = 
        acme.policy [test]
        acme.custom [test]

Let's now run the tests.

1. Assuming you have a build from Exercise 5, run the tests with::

    $ bin/test
    ...
    Running acme.custom.testing.AcmeCustom:Integration tests:
      Set up plone.testing.zca.LayerCleanup in 0.000 seconds.
      Set up plone.testing.z2.Startup in 0.208 seconds.
      Set up plone.app.testing.layers.PloneFixture in 7.671 seconds.
      Set up acme.custom.testing.AcmeCustom in 0.387 seconds.
      Set up acme.custom.testing.AcmeCustom:Integration in 0.000 seconds.
      Running:
                    
      Ran 1 tests with 0 failures and 0 errors in 0.117 seconds.
    Running acme.policy.testing.AcmePolicy:Integration tests:
      Tear down acme.custom.testing.AcmeCustom:Integration in 0.000 seconds.
      Tear down acme.custom.testing.AcmeCustom in 0.003 seconds.
      Set up acme.policy.testing.AcmePolicy in 0.681 seconds.
      Set up acme.policy.testing.AcmePolicy:Integration in 0.000 seconds.
      Running:
                    
      Ran 1 tests with 0 failures and 0 errors in 0.019 seconds.
    Tearing down left over layers:
      Tear down acme.policy.testing.AcmePolicy:Integration in 0.000 seconds.
      Tear down acme.policy.testing.AcmePolicy in 0.003 seconds.
      Tear down plone.app.testing.layers.PloneFixture in 0.091 seconds.
      Tear down plone.testing.z2.Startup in 0.007 seconds.
      Tear down plone.testing.zca.LayerCleanup in 0.003 seconds.
    Total: 2 tests, 0 failures, 0 errors in 9.615 seconds.

We have snipped some of the deprecation warnings that appear in the test run,
but this shows two tests from two layers running successfully.

2. Are two tests enough? This really depends on how much code we have! We can
   use test coverage reporting to check. First, run the test runner in coverage
   mode::

        $ bin/test --coverage=coverage
        ...
        lines   cov%   module   (path)
            1   100%   acme.custom.__init__   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/__init__.py)
           21    71%   acme.custom.browser.helpers   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/browser/helpers.py)
           26    23%   acme.custom.browser.search   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/browser/search.py)
            8   100%   acme.custom.interfaces   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/interfaces.py)
           18   100%   acme.custom.testing   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/testing.py)
            1   100%   acme.custom.tests.__init__   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/tests/__init__.py)
           24   100%   acme.custom.tests.test_views   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.custom/src/acme/custom/tests/test_views.py)
            1   100%   acme.policy.__init__   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.policy/src/acme/policy/__init__.py)
           18   100%   acme.policy.testing   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.policy/src/acme/policy/testing.py)
            1   100%   acme.policy.tests.__init__   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.policy/src/acme/policy/tests/__init__.py)
           14   100%   acme.policy.tests.test_example   (/Users/optilude/Development/Plone/ploneconf2011/exercises/src/acme.policy/src/acme/policy/tests/test_example.py)

Apart from printing these stats to the console, this will create a coverage test
report in ``parts/test/coveage``. You may also notice that it runs much slower!
This is why we don't necessarily keep coverage reporting on always.

The report shows that we have pretty poor test coverage in two modules:
``acme.custom.browser.helpers`` and ``acme.custom.browser.search``, which is
pretty bad news considering those are the only two that contain any custom
logic!

3. Let's get a better view of where the problems are. We'll first create a
   coverage report::

    $ bin/coveragereport

The settings in ``buildout.cfg`` ensure this finds the coverage reports from
the test runner (in ``parts/test/coverage``) and puts them in a top-level
folder called ``coverage``.

4. Open ``coverage/all.html`` in a browser to see the report. Drill into
   ``helpers.py``, and it should be obvious which code path isn't covered: the
   entire 'else' statement is missing tests!

5. Let's add some. Find ``tests/test_views.py`` in ``acme.custom`` and add a
   test like this::

    def test_dictify_obj(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles

        from acme.custom.browser.helpers import SearchHelpers

        portal = self.layer['portal']
        request = self.layer['request']

        # Create some test content

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Document', 'doc1',
                title=u"Document one",
                description=u"This is document one",
            )
        setRoles(portal, TEST_USER_ID, ['Member'])
        
        item = portal['doc1']

        view = SearchHelpers(portal, request)
        d = view.dictify(item)

        self.assertEqual(d['title'], u"Document one")
        self.assertEqual(d['description'], u"This is document one")
        self.assertEqual(d['url'], item.absolute_url())

This is basically just a copy of the ``test_dictify()`` test, but changed to
look up an object instead of a catalog brain.

6. Let's run this test on its own, to speed up the test run::

    $ bin/test -s acme.custom -t test_dictify_obj

The ``-s`` option restricts the package to test (i.e. we don't want to test
``acme.policy`` as well). The ``-t`` does a regular expression search on the
test name to restrict the actual test cases run.

Unfortunately, this didn't work - we got an error::

    Error in test test_dictify_obj (acme.custom.tests.test_views.TestHelperView)
    Traceback (most recent call last):
      File "/Users/optilude/.buildout/eggs/unittest2-0.5.1-py2.6.egg/unittest2/case.py", line 340, in run
        testMethod()
      File "/Users/optilude/Development/Plone/ploneconf2011/exercies/src/acme.custom/src/acme/custom/tests/test_views.py", line 61, in test_dictify_obj
        d = view.dictify(item)
      File "/Users/optilude/Development/Plone/ploneconf2011/exercies/src/acme.custom/src/acme/custom/browser/helpers.py", line 32, in dictify
        'review_state': wftool.getInfoFor(item, 'review_state')
      File "/Users/optilude/.buildout/eggs/Products.CMFCore-2.2.4-py2.6.egg/Products/CMFCore/WorkflowTool.py", line 266, in getInfoFor
        raise WorkflowException(msg)
    WorkflowException: No workflow provides '${name}' information.

This is happening because the code assumes the item has a workflow, and in the
test runner, there is no workflow by default.

7. Let's  make the code more resilient. In ``helpers.py``, we can change the
   ``else`` clause of ``dictify()`` to add a default parameter in the call
   to ``getInfoFor()``::

        else:

            wftool = getToolByName(self.context, 'portal_workflow')

            return {
                'title': item.Title(),
                'description': item.Description(),
                'url': item.absolute_url,
                'review_state': wftool.getInfoFor(item, 'review_state', None)
            }

8. We'll run the tests again, but this time we get a test failure::

    $ bin/test -s acme.custom -t test_dictify_obj
    Failure in test test_dictify_obj (acme.custom.tests.test_views.TestHelperView)
    Traceback (most recent call last):
      File "/Users/optilude/.buildout/eggs/unittest2-0.5.1-py2.6.egg/unittest2/case.py", line 340, in run
        testMethod()
      File "/Users/optilude/Development/Plone/ploneconf2011/exercies/src/acme.custom/src/acme/custom/tests/test_views.py", line 65, in test_dictify_obj
        self.assertEqual(d['url'], item.absolute_url())
      File "/Users/optilude/.buildout/eggs/unittest2-0.5.1-py2.6.egg/unittest2/case.py", line 521, in assertEqual
        assertion_func(first, second, msg=msg)
      File "/Users/optilude/.buildout/eggs/unittest2-0.5.1-py2.6.egg/unittest2/case.py", line 514, in _baseAssertEqual
        raise self.failureException(msg)
    AssertionError: <bound method ATDocument.absolute_url of <ATDocument at /plone/doc1>> != 'http://nohost/plone/doc1'

10. What's happened here? We may need to do a bit of debugging to find out.
    We'll put a breakpoint in the test::

      def test_dictify_obj(self):
          from plone.app.testing import TEST_USER_ID
          from plone.app.testing import setRoles

          from acme.custom.browser.helpers import SearchHelpers

          portal = self.layer['portal']
          request = self.layer['request']

          # Create some test content

          setRoles(portal, TEST_USER_ID, ['Manager'])
          portal.invokeFactory('Document', 'doc1',
                  title=u"Document one",
                  description=u"This is document one",
              )
          setRoles(portal, TEST_USER_ID, ['Member'])
          
          item = portal['doc1']

          view = SearchHelpers(portal, request)

          import pdb; pdb.set_trace( )
          d = view.dictify(item)

          self.assertEqual(d['title'], u"Document one")
          self.assertEqual(d['description'], u"This is document one")
          self.assertEqual(d['url'], item.absolute_url())

Notice the line ``import pdb; pdb.set_trace()``. Run the tests again, and you'll
end up at a (Pdb) prompt::

    $ bin/test -s acme.custom -t test_dictify_obj
    -> d = view.dictify(item)
    (Pdb) 

11. Use ``s`` to step into the call, then ``l`` and ``n`` several times to get
    into the ``else`` statement. Be careful not to step past the ``return``
    statement::

      (Pdb) l
       23             
       24             else:
       25     
       26                 wftool = getToolByName(self.context, 'portal_workflow')
       27     
       28  ->             return {
       29                     'title': item.Title(),
       30                     'description': item.Description(),
       31                     'url': item.absolute_url,
       32                     'review_state': wftool.getInfoFor(item, 'review_state', None)
       33                 }
      (Pdb) 

12. Let's see what's happening with the ``url`` parameter::

      (Pdb) pp item.absolute_url
      <bound method ATDocument.absolute_url of <ATDocument at /plone/doc1>>

Aha! We've accessed the method, but forgotten to call it.

13. Press ``c`` the enter to continue the test, then let's fix the call in
    ``helpers.py`` and remove the ``import pdb; pdb.set_trace()`` line in
    ``test_views.py``::

            return {
                'title': item.Title(),
                'description': item.Description(),
                'url': item.absolute_url(),
                'review_state': wftool.getInfoFor(item, 'review_state', None)
            }

Our tests have paid off - they found a bug we didn't find through the web.

14. Run the tests again to make sure they work, then re-generate the coverage
    report::
    
      $ bin/test --coverage=coverage
      $ bin/coveragereport

The new report should look better, at least for the ``helpers`` module.

For bonus points, improve the test coverage for the ``search`` module as well.
