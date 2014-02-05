from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class AvatarLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import ftw.avatar
        xmlconfig.file('configure.zcml',
                       ftw.avatar,
                       context=configurationContext)


AVATAR_FIXTURE = AvatarLayer()
AVATAR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(AVATAR_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.avatar:functional")
