import unittest2 as unittest

from acme.custom.testing import\
    ACME_CUSTOM_INTEGRATION_TESTING

class TestHelperView(unittest.TestCase):

    layer = ACME_CUSTOM_INTEGRATION_TESTING
    
    def test_dictify(self):
        from plone.app.testing import TEST_USER_ID
        from plone.app.testing import setRoles

        from acme.custom.browser.helpers import SearchHelpers
        from Products.CMFCore.utils import getToolByName

        portal = self.layer['portal']
        request = self.layer['request']

        # Create some test content

        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.invokeFactory('Document', 'doc1',
                title=u"Document one",
                description=u"This is document one",
            )
        setRoles(portal, TEST_USER_ID, ['Member'])
        
        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog(portal_type='Document', title='Document one')
        item = results[0]

        view = SearchHelpers(portal, request)
        d = view.dictify(item)

        self.assertEqual(d['title'], u"Document one")
        self.assertEqual(d['description'], u"This is document one")
        self.assertEqual(d['url'], item.getURL())
    
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
