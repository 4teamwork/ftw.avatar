from ftw.avatar.interfaces import IAvatarGenerator
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from unittest2 import TestCase
from zope.component import queryUtility
from zope.interface.verify import verifyObject


class TestDefaultAvatarGeneratorUtility(TestCase):

    layer = AVATAR_FUNCTIONAL_TESTING

    def test_utility_is_registered(self):
        self.assertTrue(queryUtility(IAvatarGenerator),
                        'IAvatarGenerator utility is not registered.')

    def test_component_implements_interface(self):
        utility = queryUtility(IAvatarGenerator)
        self.assertTrue(IAvatarGenerator.providedBy(utility))
        verifyObject(IAvatarGenerator, utility)
