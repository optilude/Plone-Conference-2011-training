from datetime import date
from zope.publisher.browser import BrowserView

class AcmeInfo(BrowserView):
    """Some helpful information
    """
    
    def copyrightYear(self):
        return date.today().year
