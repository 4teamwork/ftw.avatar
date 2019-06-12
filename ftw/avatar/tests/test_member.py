from ftw.avatar.member import create_default_avatar
from ftw.avatar.member import get_user_id
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
import hashlib


class TestCreateDefaultAvatar(TestCase):
    layer = AVATAR_FUNCTIONAL_TESTING

    def test_get_user_id_by_username(self):
        self.assertEquals(TEST_USER_ID, get_user_id(TEST_USER_NAME))

    def test_get_user_id_of_unkown_user(self):
        self.assertEquals(None, get_user_id('unkown'))

    def test_creates_default_avatar_for_users_without_avatar(self):
        hugo = create(Builder('user').named('Hugo', 'Boss'))
        self.assertEquals(None, self.portrait_md5(hugo.getId()))
        create_default_avatar(hugo.getId())
        self.assertTrue(self.portrait_md5(hugo.getId()))

    @browsing
    def test_csrf_is_disabled_for_default_avatar_creation(self, browser):
        hugo = create(Builder('user').named('Hugo', 'Boss'))

        self.assertEquals(None, self.portrait_md5(hugo.getId()))
        request = self.layer['request']
        self.assertFalse(IDisableCSRFProtection.providedBy(request))

        create_default_avatar(hugo.getId())

        self.assertTrue(IDisableCSRFProtection.providedBy(request))
        self.assertTrue(self.portrait_md5(hugo.getId()))

    def test_does_not_override_existing_avatars(self):
        hugo = create(Builder('user').named('Hugo', 'Boss'))
        create_default_avatar(hugo.getId())
        first_hash = self.portrait_md5(hugo.getId())
        create_default_avatar(hugo.getId())
        second_hash = self.portrait_md5(hugo.getId())
        self.assertEquals(first_hash, second_hash,
                          'Existing portrait was overriden by default'
                          ' portrait generator.')

    def portrait_md5(self, userid):
        mship = getToolByName(self.layer['portal'], 'portal_membership')
        mdata = getToolByName(self.layer['portal'], 'portal_memberdata')
        safe_id = mship._getSafeMemberId(userid)
        portrait = mdata._getPortrait(safe_id)
        if not portrait:
            return None

        return hashlib.md5(portrait.data).hexdigest()
