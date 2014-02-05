from PIL import Image
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from ftw.avatar.interfaces import IAvatarGenerator
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from ftw.avatar.utils import SwitchedToSystemUser
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from unittest2 import TestCase
from zope.component import getUtility
import hashlib
import transaction


def image_size():
    return Image.open(StringIO(browser.contents)).size


def image_hash():
    return hashlib.md5(browser.contents).hexdigest()


class TestPortraitScalingView(TestCase):

    layer = AVATAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.hugo = create(Builder('user').named('Hugo', 'Boss'))
        self.mtool = getToolByName(self.layer['portal'], 'portal_membership')
        self.portrait = self.mtool.getPersonalPortrait(self.hugo.getId())
        self.portrait_url = self.portrait.absolute_url()
        transaction.commit()  # portrait was generated

    @browsing
    def test_default_scaling_is_original_size(self, browser):
        browser.visit(self.portrait_url)
        self.assertEquals((220, 220), image_size())

    @browsing
    def test_scaling_with_s_parameter(self, browser):
        browser.visit(self.portrait_url + '?s=100')
        self.assertEquals((100, 100), image_size())

    @browsing
    def test_scaling_with_size_parameter(self, browser):
        browser.visit(self.portrait_url + '?size=150')
        self.assertEquals((150, 150), image_size())

    @browsing
    def test_max_scaling_returns_original(self, browser):
        browser.visit(self.portrait_url + '?s=9999')
        self.assertEquals((220, 220), image_size())

    @browsing
    def test_scaling_is_changed_when_image_changes(self, browser):
        browser.visit(self.portrait_url + '?s=100')
        hash_before = image_hash()
        self.regenerate_portrait()
        browser.visit(self.portrait_url + '?s=100')
        hash_after = image_hash()
        self.assertNotEquals(
            hash_before, hash_after,
            'Image scaling cache is not cleared when changing portrait.')

    def regenerate_portrait(self):
        portrait = StringIO()
        getUtility(IAvatarGenerator).generate('AB', portrait)
        portrait.seek(0)
        setattr(portrait, 'filename', 'default.png')
        with SwitchedToSystemUser():
            self.mtool.changeMemberPortrait(portrait, self.hugo.getId())
        transaction.commit()
