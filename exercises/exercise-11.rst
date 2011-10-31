Exercise 11 - Cache response headers
-------------------------------------

In this exercise, we will learn how to debug cache response headers using
Firebug or Chrome Developer Tools and ``plone.app.caching``.

Note that for simplicity, the code in this exercise is based on the outputs
of Exercise 9, so ``acme.policy`` and ``acme.custom`` are back inside the build.

1. Build and start the deployment configuration if you haven't done so already::
    
    $ bin/buildout -c deployment.cfg
    $ bin/supervisord

2. Access one of the Zope intances directly and ensure that the Plone site
   called ``Plone`` has both ``acme.policy`` and ``HTTP Caching supporting``
   (i.e. ``plone.app.caching``) installed, via::

    http://localhost:8001/Plone

   Log in as ``admin`` with password ``secret``.

3. Log out and then access::

    http://localhost:8000

4. Open Firebug / Chrome Developer Tools and enable the ``Net`` tab. Perform a
   hard refresh and observe the requests. Try to understand what HTTP response
   headers are being returned, and what, if anything, is being fetched from a
   cache or from Varnish.

Questions:

 * Which HAProxy cluster is being used? Look at ``etc/haproxy.conf``.
 * What happened in Varnish? Look at ``etc/varnish.vcl``.

5. Compare the headers with an equilvanet request to::

    http://localhost:8001/Plone

What's different? Is any caching being applied?

So far, these requests have not involved any tweaking of the cache. Consider
what you would like to see happening. A good starting point may be:

 * Anonymous content pages cached with conditional 304 responses and ETags
 * CSS and JavaScript resources cached with a long expiry time

Let's enable a ``plone.app.caching`` profile and see what's changed.

6. Using another browser, log in and go to the ``Caching`` control panel. Under
   ``Import settings`` import the ``With caching proxy`` profile. Then go back
   to the ``Change settings`` tab and enable caching. Leave ``GZip compression``
   off.

Take a look at the ``Caching operations`` and ``Detailed settings`` tabs to
understand better what caching rules are being applied.

7. Go back to http://localhost:8000 and reload the page.

Questions:

 * What's changed in the response headers?
 * What ``plone.app.caching`` rulesets are being applied to what resources?
 * What Etags are being used? What information do they comprise?
 * What would cause a 304 response vs. a 200 response?

We have prepared another view, called ``@@acme-info``, containing only some
static text. Try to load it from http://localhost:8000/@@acme-info.

8. Observe the response headers and caching of ``@@acme-info``. Does it seem
   appropriate, compared with, say, the ``Accessibility`` page in Plone? Try
   a few reloads to compare if and when 304 responses kick in.

Because we haven't told ``plone.app.caching`` about our custom page, it is being
conservative, resulting in a 200 response and a hit to the server every time.

9. To rectify this, we can declare a cache ruleset for the ``@@acme-info`` view.
   Add a file ``browser/caching.zcml`` in ``acme.custom`` containing::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:cache="http://namespaces.zope.org/cache"
        i18n_domain="acme.custom">

        <include package="z3c.caching" file="meta.zcml" />
        <include package="plone.app.caching" file="caching.zcml" />

        <cache:ruleset
            ruleset="plone.content.itemView"
            for=".info.AcmeInfo"
            />

    </configure>


   This declares the view with the class ``AcmeInfo`` should use the rulset
   ``plone.itemView``, which we have mapped to the relevant rules in the
   ``Caching`` control panel.
    
   Next, open ``browser/configure.zcml`` in ``acme.custom`` and add the
   following::

        <include file="caching.zcml" />

10. Restart the Zope instances so we can test the new configuration::

    $ bin/supervisorctl restart instance1 instance2 instance3 instance4

11. Reload the ``@@acme-info`` page a few times and observe the difference.

Note that for more fine-grained control, it is possible to define your own
caching ruleset types, which can then be mapped to caching operations with
specific configuration. See http://pypi.python.org/pypi/plone.app.caching for
more details.