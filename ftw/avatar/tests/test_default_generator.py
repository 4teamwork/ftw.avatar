from PIL import Image
from StringIO import StringIO
from ftw.avatar.default import DefaultAvatarGenerator
from unittest2 import TestCase


class TestDefaultAvatarGenerator(TestCase):

    def test_generates_220x220_image(self):
        output = StringIO()
        DefaultAvatarGenerator().generate('Foo Bar', output)
        output.seek(0)
        self.assertEquals((220, 220), Image.open(output).size)

    def test_text_is_capital_first_letters_of_first_two_words(self):
        self.assertEquals('FB', DefaultAvatarGenerator().text('Foo bar'))
        self.assertEquals('AB', DefaultAvatarGenerator().text('Aaa Bbb Ccc'))

    def test_text_is_two_letters_of_word_when_only_one_word_given(self):
        self.assertEquals('FO', DefaultAvatarGenerator().text('Foo'))

    def test_text_is_only_one_letter(self):
        self.assertEquals('X', DefaultAvatarGenerator().text('x'))

    def test_text_is_dash_if_no_names_defined(self):
        self.assertEquals('-', DefaultAvatarGenerator().text(None))
        self.assertEquals('-', DefaultAvatarGenerator().text(''))

    def test_foreground_color_is_white_by_default(self):
        self.assertEquals((255, 255, 255),
                          DefaultAvatarGenerator().foreground_color())

    def test_background_color_is_valid_color_tuple(self):
        self.assertEquals(
            [int, int, int],
            map(type, DefaultAvatarGenerator().background_color()))

    def test_text_with_leading_and_trailing_spaces(self):
        self.assertEquals('HB', DefaultAvatarGenerator().text(' Hugo Boss '))
