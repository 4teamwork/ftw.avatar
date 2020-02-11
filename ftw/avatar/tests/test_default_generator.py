from ftw.avatar.default import DefaultAvatarGenerator
from ftw.avatar.testing import AVATAR_FUNCTIONAL_TESTING
from ftw.builder import Builder
from ftw.builder import create
from PIL import Image
from six import BytesIO
from unittest2 import TestCase
from zope.component.hooks import getSite


class TestDefaultAvatarGenerator(TestCase):
    layer = AVATAR_FUNCTIONAL_TESTING

    def setUp(self):
        super(TestDefaultAvatarGenerator, self).setUp()
        self.portal_membership = getSite().portal_membership

    def test_generates_220x220_image(self):
        user = create(Builder('user').named('Hugo', 'Boss'))
        output = BytesIO()
        DefaultAvatarGenerator().generate(user.getId(), output)
        output.seek(0)
        self.assertEquals((220, 220), Image.open(output).size)

    def test_text_is_capital_first_letters_of_first_two_words(self):
        user = create(Builder('user').named('Foo', 'Bar'))
        user2 = create(Builder('user').named('Foo', 'Goo Poo'))
        self.assertEquals('BF', DefaultAvatarGenerator().text(user.getId()))
        self.assertEquals('GP', DefaultAvatarGenerator().text(user2.getId()))

    def test_text_is_two_letters_of_word_when_only_one_word_given(self):
        user = create(Builder('user').named('Foo', 'Bar'))
        member = self.portal_membership.getMemberById(user.getId())
        member.setMemberProperties(mapping={"fullname": "Foo"})
        self.assertEquals('FO', DefaultAvatarGenerator().text(user.getId()))

    def test_text_is_only_one_letter(self):
        user = create(Builder('user').named('Foo', 'Bar'))
        member = self.portal_membership.getMemberById(user.getId())
        member.setMemberProperties(mapping={"fullname": "x"})
        self.assertEquals('X', DefaultAvatarGenerator().text(user.getId()))

    def test_text_is_dash_if_no_names_defined(self):
        self.assertEquals('-', DefaultAvatarGenerator().text(None))
        self.assertEquals('-', DefaultAvatarGenerator().text(''))

    def test_foreground_color_is_white_by_default(self):
        self.assertEquals((255, 255, 255),
                          DefaultAvatarGenerator().foreground_color())

    def test_background_color_is_valid_color_tuple(self):
        self.assertEquals(
            [int, int, int],
            list(map(type, DefaultAvatarGenerator().background_color())))

    def test_text_with_leading_and_trailing_spaces(self):
        user = create(Builder('user').named('Foo', 'Bar'))
        member = self.portal_membership.getMemberById(user.getId())
        member.setMemberProperties(mapping={"fullname": " Hugo Boss "})
        self.assertEquals('HB', DefaultAvatarGenerator().text(user.getId()))

    def test_text_of_user_without_fullname_is_userid(self):
        self.assertEquals('AD', DefaultAvatarGenerator().text('admin'))

    def test_text_of_non_existent_user(self):
        self.assertEquals('UN', DefaultAvatarGenerator().text('unkown.user'))

    def test_text_of_non_existent_user_with_leading_spaces(self):
        self.assertEquals('UU', DefaultAvatarGenerator().text('  unkown user  '))
