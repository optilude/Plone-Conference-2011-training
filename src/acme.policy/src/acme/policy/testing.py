from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class AcmePolicy(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import acme.policy
        xmlconfig.file('configure.zcml',
                       acme.policy,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'acme.policy:default')

ACME_POLICY_FIXTURE = AcmePolicy()
ACME_POLICY_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(ACME_POLICY_FIXTURE, ),
                       name="AcmePolicy:Integration")