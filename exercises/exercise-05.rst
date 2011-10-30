Exercise 5 - Debugging and reloading
------------------------------------

For this and subsequent exercises, we will use a package called ``acme.custom``,
which contains some custom views. It was created with ``zopeskel`` much like
``acme.policy`` from Exercise 3, and is installed as a dependency of
``acme.policy`` (see ``setup.py`` and ``metadata.xml`` in that package). It
is also listed in ``auto-checkout`` in ``buildout.cfg`` and as a test-enabled
package in ``packages.cfg``.

1. Run the buildout and start Zope in debug mode::

    $ bin/buildout
    $ bin/instance fg

2. Create a new Plone site with the Acme Policy package installed from
   http://localhost:8080

3. Create a few Pages and News Items to test the search with.

4. Open the custom search page at http://localhost:8080/Plone/@@acme-search

(Adjust for the name of the Plone site as necessary)

5. Enter some text in the 'Search text' field and search - you should see some
   results appearing underneath the search criteria box.

Let's take a look at the code now. Find ``search.pt`` in the ``acme.custom``
package (it's in the ``browser`` sub-package). It contains some code like
this::

        <dl tal:condition="nocall:results">
            <tal:block repeat="result results">
                <dt>
                    <a 
                        tal:content="python:helpers.dictify(result)['title']"
                        tal:attributes="href python:helpers.dictify(result)['url']"
                        />
                </dt>
                <dd tal:content="python:helpers.dictify(result)['description']" />
            </tal:block>
        </dl>

6. This is rather inefficient. Let's fix it whilst Zope is running. You can
   rewrite it as you wish, but something like this may work::

        <dl tal:condition="nocall:results">
            <tal:block repeat="result results">
                <tal:block define="info python:helpers.dictify(result)">
                    <dt>
                        <a 
                            tal:content="info/title"
                            tal:attributes="href info/url"
                            />
                    </dt>
                    <dd tal:content="info/description" />
                </tal:block>
            </tal:block>
        </dl>

   Now, without restarting Zope or otherwise reloading anything, try the search
   again. In Zope debug mode, the template changes should be picked up
   instantly.

7. Let's do some more testing. Do another search, but this time put some
   non-numeric text into the "Result limit" field and attempt a search.

Zope now appears to hang. What's happened?

Take a look in the terminal, and you will see that you've been dropped to a
PDB prompt like this::

    Traceback (innermost last):
      Module ZPublisher.Publish, line 126, in publish
      Module ZPublisher.mapply, line 77, in mapply
      Module Products.PDBDebugMode.runcall, line 70, in pdb_runcall
      Module ZPublisher.Publish, line 46, in call_object
      Module acme.custom.browser.search, line 25, in __call__
    ValueError: invalid literal for int() with base 10: 'aads'
    > /Users/optilude/Development/Plone/ploneconf2011/exercies/src/acme.custom/src/acme/custom/browser/search.py(25)__call__()
    -> count = int(form['count'])
    (Pdb) 

8. Let's get some context. Press 'l' then enter::

    (Pdb) l
     20     
     21             if 'form.button.Search' in form:
     22                 helpers = getMultiAdapter((self.context, self.request,), name=u"acme_search_helpers")
     23                 catalog = getToolByName(self.context, 'portal_catalog')
     24     
     25  ->             count = int(form['count'])
     26     
     27                 query = {
     28                     'portal_type': helpers.acmeTypes,
     29                     'SearchableText': form['searchText'],
     30                     'sort_limit': count,
    (Pdb) 

9. So, something is wrong. Let's see what's in the ``form`` dict, using 
   pretty-printing with ``pp``::

    (Pdb) pp form
    {'count': 'aads', 'form.button.Search': 'Search', 'searchText': ''}

10. Clearly, this is not good. Let's exit the debugger whilst we fix the
    problem, using ``c``::

    (Pdb) c

11. Let's make the code a bit safer (feel free to use a more sophisticated
    solution, such as one that gives the user better error handling)::

            try:
                count = int(form['count'])
            except ValueError:
                count = form['count'] = 10

12. If you try the bogus search again, it will still blow up: our code changes
    are not automatically picked up. However, you can now reload the code using
    ``plone.reload``, by visiting ``http://localhost:8080/@@reload`` and
    clicking the ``Reload Code`` button. It should report that it reloaded
    the module, e.g.::

        Code reloaded:

        /Users/optilude/Development/Plone/ploneconf2011/exercies/src/acme.custom/src/acme/custom/browser/search.py

13. Now try the request again - it should work.

14. For bonus points, write an automated test to prove the defect and guard
    against regressions in the future.
