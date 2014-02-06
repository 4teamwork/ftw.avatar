from Products.CMFCore.utils import getToolByName
from ftw.avatar.member import create_default_avatar
from ftw.avatar.member import get_name_of_user
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import SITE_OWNER_NAME
from unittest2 import TestCase
import hashlib


class TestCreateDefaultAvatar(TestCase):
    layer = AVATAR_FUNCTIONAL_TESTING

    def test_name_of_user(self):
        user = create(Builder('user').named('Hugo', 'Boss'))
        self.assertEquals('Boss Hugo', get_name_of_user(user.getId()))

    def test_name_of_user_with_no_fullname(self):
        self.assertEquals('admin', get_name_of_user(SITE_OWNER_NAME))

    def test_creates_default_avatar_for_users_without_avatar(self):
        hugo = create(Builder('user').named('Hugo', 'Boss'))
        self.assertEquals(None, self.portrait_md5(hugo.getId()))
        create_default_avatar(hugo.getId())
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
