from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class AcmeCustom(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import acme.custom
        xmlconfig.file('configure.zcml',
                       acme.custom,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'acme.custom:default')

ACME_CUSTOM_FIXTURE = AcmeCustom()
ACME_CUSTOM_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(ACME_CUSTOM_FIXTURE, ),
                       name="AcmeCustom:Integration")