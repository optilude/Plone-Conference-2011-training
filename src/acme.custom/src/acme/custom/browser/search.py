from zope.component import getMultiAdapter
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName

class AcmeSearch(BrowserView):
    """Acme Corp search form
    """
    
    def _setup(self):
        self.request.set('disable_border',1)
        self.request.set('disable_plone.leftcolumn',1)
        self.request.set('disable_plone.rightcolumn',1)

        self.results = None

    def __call__(self):

        self._setup()
        
        form = self.request.form

        if 'form.button.Search' in form:
            helpers = getMultiAdapter((self.context, self.request,), name=u"acme_search_helpers")
            catalog = getToolByName(self.context, 'portal_catalog')

            try:
                count = int(form['count'])
            except ValueError:
                count = form['count'] = 10

            query = {
                'portal_type': helpers.acmeTypes,
                'SearchableText': form['searchText'],
                'sort_limit': count,
                'sort_on': 'sortable_title',
            }
            
            self.results = catalog(query)[:count]
        
        return self.index()
