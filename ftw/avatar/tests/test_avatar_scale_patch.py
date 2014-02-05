from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from unittest2 import TestCase


class TestAutomaticalAvatarGeneration(TestCase):
    layer = AVATAR_FUNCTIONAL_TESTING

    def test_scale_size_is_patched(self):
        from Products.PlonePAS import utils
        self.assertDictContainsSubset({'scale': (300, 300)},
                                      utils.IMAGE_SCALE_PARAMS)
