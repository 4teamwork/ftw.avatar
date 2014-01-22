from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class AvatarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import ftw.avatar
        xmlconfig.file('configure.zcml',
                       ftw.avatar,
                       context=configurationContext)


AVATAR_FIXTURE = AvatarLayer()
AVATAR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(AVATAR_FIXTURE, ),
    name="ftw.avatar:functional")
