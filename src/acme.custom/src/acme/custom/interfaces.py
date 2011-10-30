from zope.interface import Interface
from zope import schema

class ISearchHelpers(Interface):
    """A view registered as @@acme_search_helpers, providing useful information
    and helper functions for custom searches.
    """

    acmeTypes = schema.Tuple(
            title=u"ACME types",
            description=u"A list of portal types commonly used in searches",
        )
    
    def dictify(item):
        """Given a catalogue brain or object, return a dict with keys
        ``title``, ``description``, ``url``, ``review_state``.
        """
