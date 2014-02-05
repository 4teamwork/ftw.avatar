from Products.CMFCore.utils import getToolByName
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from unittest2 import TestCase


class TestAutomaticalAvatarGeneration(TestCase):
    layer = AVATAR_FUNCTIONAL_TESTING

    def test_avatar_is_generated_for_new_users(self):
        hugo = create(Builder('user').named('Hugo', 'Boss'))
        mtool = getToolByName(self.layer['portal'], 'portal_membership')
        portrait = mtool.getPersonalPortrait(hugo.getId())
        self.assertEquals(
            'http://nohost/plone/portal_memberdata/portraits/hugo.boss',
            portrait.absolute_url())

    def test_effective_default_avatar_size(self):
        # When setting the portrait, some scaling is involed.
        # Verify that we actually have a big avatar available.
        hugo = create(Builder('user').named('Hugo', 'Boss'))
        mtool = getToolByName(self.layer['portal'], 'portal_membership')
        portrait = mtool.getPersonalPortrait(hugo.getId())
        self.assertEquals((220, 220),
                          (portrait.width, portrait.height))
