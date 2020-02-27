from ftw.avatar.interfaces import IAvatarGenerator
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from ftw.avatar.utils import SwitchedToSystemUser
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from OFS.Image import Pdata
from PIL import Image
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.events import UserLoggedInEvent
from six import BytesIO
from unittest2 import TestCase
from zope.component import getUtility
from zope.event import notify
import hashlib
import transaction


def image_size():
    return Image.open(BytesIO(browser.contents)).size


def image_hash():
    return hashlib.md5(browser.contents).hexdigest()


class TestPortraitScalingView(TestCase):

    layer = AVATAR_FUNCTIONAL_TESTING

    def setUp(self):
        self.hugo = create(Builder('user').named('Hugo', 'Boss'))
        notify(UserLoggedInEvent(self.hugo))
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

    @browsing
    def test_pdata_portrait_scaling(self, browser):
        """Some files are stored as Pdata objects instead of strings.
        """
        getToolByName(self.layer['portal'], 'portal_memberdata')._setPortrait(
            Pdata(self.generate_portrait().getvalue()), self.hugo.getId())
        transaction.commit()
        try:
            browser.visit(self.portrait_url + '?s=100')
        except AttributeError:
            self.fail('See commit 743d243861b40e8a96028574179794d8d9a3372a for more details.')

    def regenerate_portrait(self):
        portrait = self.generate_portrait()
        with SwitchedToSystemUser():
            self.mtool.changeMemberPortrait(portrait, self.hugo.getId())
        transaction.commit()

    def generate_portrait(self):
        portrait = BytesIO()
        getUtility(IAvatarGenerator).generate('AB', portrait)
        portrait.seek(0)
        setattr(portrait, 'filename', 'default.png')
        return portrait
