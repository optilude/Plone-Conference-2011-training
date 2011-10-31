Exercise 9 - Deployment buildout
--------------------------------

For this exercise, we have copied a number of common buildout recipes to the
directory ``buildout.d``. The ``buildout.d/temlates`` directory contains
template configuration files.

1. Install MySQL if you do not have it already and create a database ``zodb``
   accessible as the user ``zope`` with the password ``secret``.

    $ mysql -u root
    > create user 'zope'@'localhost' identified by 'secret';
    > create database zodb;
    > grant all on zodb.* to 'zope'@'localhost';

Note: You will need MySQL development headers installed as well!

2. Create a top level directory ``etc``::

    $ mkdir etc

3. Create a self-signed SSL certificate. You will need OpenSSL installed. Answer
   the questions with dummy values as you wish::

    $ cd etc
    $ openssl req -new -x509 -nodes -out server.crt -keyout server.key
    $ cd ..

4. Create a top-level directory ``htdocs``, containing a directory
   ``system_error``::

    $ mkdir -p htdocs/system_error

5. In this directory, create a file ``index.html``::

    <html>
    <head>
        <title>System error</title>
    </head>
    <body>
        <h1>Panic!!!1111eleven</h1>
    </body>
    </html>

6. Create a new top-level buildout file called ``deployment.cfg`` containing::

    # Deployment buildout
    # ===================

    [buildout]
    parts =
        instance1
        instance2
        instance3
        instance4
        zodbpack
        zodbpack-config
        supervisor

        ${buildout:memcached-parts}
        ${buildout:haproxy-parts}
        ${buildout:varnish-parts}
        ${buildout:nginx-parts}

    extends =
        packages.cfg
        buildout.d/memcached.cfg
        buildout.d/haproxy.cfg
        buildout.d/varnish.cfg
        buildout.d/nginx.cfg

    # Create local caches so that we get completely self-contained buildouts.
    # These directories must be created before the buildout is run the first time.

    # eggs-directory = ${buildout:directory}/var/cache/eggs
    # download-cache = ${buildout:directory}/var/cache/downloads
    # extends-cache  = ${buildout:directory}/var/cache/extends

    # If you release internal eggs to an internal server, you should reference
    # a page that lists all those eggs here. The easiest way is to allow scp
    # access to a directory that's served by nginx or Apache and enable automatic
    # directory indexing/listing of that directory. Then use ./bin/mkrelease to
    # release your internal eggs here, and add to the [versions] block in
    # versions.cfg.
     
    # find-links = http://my-internal-server/eggs

    # Packages to check out/update when buildout is run
    # Clear this out if you want to stick to internally released eggs - see above.
    auto-checkout =
        acme.policy
        acme.custom

    # Make sure buildout never attempts to update packages automatically for
    # production use.
    always-checkout = false

    # Host names/IP addresses. See below for corresponding ports.
    [hosts]
    # The public hostname used in virtual hosting, i.e. the public facing domain
    public          = localhost
    # The host that nginx proxies to
    nginx-backend   = ${:varnish}
    # The hostname/address that Varnish binds to
    varnish         = localhost
    # The hosts that are allowed to issue PURGE reuqests to Varnish
    allow-purge     = localhost
    # The IP address that Varnish proxies to (do not use a hostname)
    varnish-backend = 127.0.0.1
    # The hostname that HAProxy binds to
    haproxy         = localhost
    # The IP addresses of each Zope instance
    instance1       = 127.0.0.1
    instance2       = 127.0.0.1
    instance3       = 127.0.0.1
    instance4       = 127.0.0.1
    # Where to find the syslog deamon to log to
    syslog          = localhost
    # The hostname that memcached binds to
    memcached       = localhost
    # The hostname where the database server is found
    database        = localhost
    # The hostname that supervisord binds to
    supervisor      = localhost

    # Port corresponding to the hostnames above. Note that to bind to ports
    # < 1024, you will need to run ./bin/supervisord as root!
    [ports]
    http            = 8000
    https           = 8443
    nginx-backend   = ${:varnish}
    varnish         = 8100
    varnish-backend = ${:haproxy}
    haproxy         = 8200
    haproxy-stats   = 8222
    instance1       = 8001
    instance2       = 8002
    instance3       = 8003
    instance4       = 8004
    syslog          = 514
    memcached       = 11211
    database        = 3306
    supervisor      = 9001

    [users]
    # Process owners for nginx, varnish, haproxy, memcached and Zope
    nginx            = nobody
    varnish          = nobody
    haproxy          = nobody
    zope-process     = nobody
    memcached        = nobody

    # System user accounts for Zope root admin, database access and Supervisor
    zope-admin       = admin
    database         = zope
    supervisor-admin = admin

    # Passwords for the accounts above
    [passwords]
    zope-admin       = secret
    database         = secret
    supervisor-admin = secret

    # Database instances for SQLAlchemy and RelStorage
    [databases]
    zodb    = zodb

    # How should varnish store its cache? Increase thesize, in megabytes, as required
    [varnish-options]
    storage = malloc,128M

    [limits]
    # How many open files are allowed? This affects the number of concurrent
    # connections. On some operating systems, this is set on startup per user
    # as the ulimit
    open-files = 100
    # Timeout of inactivity for Beaker sessions
    session-timeout = 600

    [urls]
    # This URL is used in the nginx configuration to serve an error page when
    # HAProxy detects no viable backend
    fallback = /system_error

    [sites]
    # Plone site ids - used in virtual hosting
    main = Plone

    # Zope instance template
    [instance]
    recipe = plone.recipe.zope2instance
    user = ${users:zope-admin}:${passwords:zope-admin}
    debug-mode = off
    verbose-security = off
    effective-user = ${users:zope-process}
    http-fast-listen = off
    zserver-threads = 2
    zodb-cache-size = 10000
    eggs =
        ${eggs:main}
        RelStorage
        MySQL-python
    # Configure logging to syslog
    # event-log-custom = 
    #     <syslog>
    #         level all
    #         format zope[%(process)s]: [%(levelname)s] %(name)s: %(message)s
    #         facility local1
    #         address ${hosts:syslog}:${ports:syslog}
    #     </syslog>
    # Configure RelStorage
    rel-storage =
        type mysql
        blob-dir ${buildout:directory}/var/blobstorage
        cache-servers ${hosts:memcached}:${ports:memcached}
        db ${databases:zodb}
        user ${users:database}
        passwd ${passwords:database}
    # Configure BLOB storage
    shared-blob = on

    [instance1]
    <= instance
    http-address = ${hosts:instance1}:${ports:instance1}

    [instance2]
    <= instance
    http-address = ${hosts:instance2}:${ports:instance2}

    [instance3]
    <= instance
    http-address = ${hosts:instance3}:${ports:instance3}

    [instance4]
    <= instance
    http-address = ${hosts:instance4}:${ports:instance4}

    # Install the bin/zodbpack script
    # Run: ``bin/zodbpack etc/zodbpack.conf``
    [zodbpack]
    recipe = zc.recipe.egg
    eggs =
        RelStorage
        MySQL-python
    scripts = zodbpack

    # Generate ``etc/zodbpack.conf``
    [zodbpack-config]
    recipe = collective.recipe.template
    input = ${buildout:directory}/buildout.d/templates/zodbpack.conf
    output = ${buildout:directory}/etc/zodbpack.conf

    # Install supervisor, which runs on port 9001
    # Run: ``bin/supervisord``
    # Run: ``bin/supervisorctl --help``
    [supervisor]
    recipe = collective.recipe.supervisor
    port = ${ports:supervisor}
    user = ${users:supervisor-admin}
    password = ${passwords:supervisor-admin}
    serverurl = http://${hosts:supervisor}:${ports:supervisor}
    programs =
        0  memcached  ${memcached-build:location}/bin/memcached true ${users:memcached}
        
        10 instance1  ${buildout:directory}/bin/instance1 [console] true ${users:zope-process}
        10 instance2  ${buildout:directory}/bin/instance2 [console] true ${users:zope-process}
        10 instance3  ${buildout:directory}/bin/instance3 [console] true ${users:zope-process}
        10 instance4  ${buildout:directory}/bin/instance4 [console] true ${users:zope-process}
        
        20 haproxy    ${buildout:directory}/bin/haproxy       [-f ${buildout:directory}/etc/haproxy.conf] true ${users:haproxy}
        30 varnish    ${varnish-build:location}/sbin/varnishd [-F -s ${varnish-options:storage} -f ${buildout:directory}/etc/varnish.vcl -a ${hosts:varnish}:${ports:varnish} ${varnish-options:tuning}] true ${users:varnish}
        40 nginx      ${nginx-build:location}/sbin/nginx true

7. Run the build with this file::

    $ bin/buildout -c deployment.cfg

8. Make sure version pins are added to ``versions.cfg``::

    MySQL-python = 1.2.3
    RelStorage = 1.5.0
    collective.recipe.supervisor = 0.17
    collective.recipe.template = 1.9
    hexagonit.recipe.cmmi = 1.5.0
    meld3 = 0.6.7
    plone.recipe.haproxy = 1.1.1
    pylibmc = 1.2.2
    supervisor = 3.0a10

    #Required by:
    #hexagonit.recipe.cmmi 1.5.0
    hexagonit.recipe.download = 1.5.0

9. Run Supervisor to start the various processes::

    $ bin/supervisord

10. Observe the supervisor control panel (the credentials are in the config file
   above)::

    http://localhost:9001

11. Connect to the first Zope instance to create the Plone site in the new
   database. Install the ``acme.policy`` profile, and ensure the site is called
   ``Plone`` (referenced in ``${sites:main}`` above).

12. Now test the full stack on::

    http://localhost:8000

This is running nginx -> varnish -> haproxy -> Zope -> MySQL

Note: You'd normally change ``${ports:http}`` to ``80`` and ``${ports:https}``
to ``443`` for the final deployment, which will require you to start supervisor
as root. Runtime privileges will then be dropped (to ``nobody`` in most cases,
configurable in the ``[users]`` section). You must ensure this user has
appropriate permissions to read the code, write log files, etc.

13. From the supervisor control panel, stop the Zope instances one by one.
    Observe the HAProxy statistics on ``http://localhost:8222``, and verify
    that you can still access the site from ``http://localhost:8000`` until 
    the last one goes down. At that point, you should see the panic message.

14. Stop everything using::

    $ bin/supervisorctl shutdown

Status overview
~~~~~~~~~~~~~~~

* Supervisor overview can be found on::

    http://localhost:9001

* HAProxy statistics can be seen on::

    http://localhost:8222

* Varnish statistics can be viewed via::

    $ parts/varnish-build/bin/varnishstat

* nginx statistics can be seen on::

    http://localhost:8000/_nginx_status_
