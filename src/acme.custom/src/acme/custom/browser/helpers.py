from zope.interface import implements
from zope.publisher.browser import BrowserView

from acme.custom.interfaces import ISearchHelpers

from Products.ZCatalog.interfaces import ICatalogBrain
from Products.CMFCore.utils import getToolByName

class SearchHelpers(BrowserView):
    """Helper view registered as @@acme_search_helpers.
    """

    implements(ISearchHelpers)

    acmeTypes = ['Document', 'News Item']

    def dictify(self, item):

        if ICatalogBrain.providedBy(item):
            return {
                'title': item.Title,
                'description': item.Description,
                'url': item.getURL(),
                'review_state': item.review_state,
            }
        
        else:

            wftool = getToolByName(self.context, 'portal_workflow')

            return {
                'title': item.Title(),
                'description': item.Description(),
                'url': item.absolute_url(),
                'review_state': wftool.getInfoFor(item, 'review_state', None)
            }
