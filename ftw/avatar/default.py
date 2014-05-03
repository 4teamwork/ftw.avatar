from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from ftw.avatar import LOGGER
from ftw.avatar.interfaces import IAvatarGenerator
from random import random
from zope.interface import implements
import os.path


from PIL.ImageFont import _imagingft_not_installed
from PIL.ImageFont import core
if core.__class__ is _imagingft_not_installed:
    FREETYPE_MISSING = (
        'The "_imagingft" C module is not installed, '
        ' which is part of "freetype".'
        ' Install the freetype library and reinstall Pillow with freetype support.'
        ' The avatar generation is disabled now.')
    LOGGER.error(FREETYPE_MISSING)
else:
    FREETYPE_MISSING = False


class DefaultAvatarGenerator(object):
    implements(IAvatarGenerator)

    # The resulting image size (square_size * square_size)
    square_size = 220

    def generate(self, name, output_stream):
        if FREETYPE_MISSING:
            return False
        image = Image.new('RGBA', (self.square_size, self.square_size),
                          self.background_color())
        self.draw_text(image, self.text(name), self.font())
        image.save(output_stream, 'PNG')
        return True

    def text(self, name):
        """Returns the text to draw.
        """
        if not name:
            return '-'

        words = name.split(' ', 1)
        if len(words) == 1:
            return words[0][:2].upper()
        else:
            return ''.join([word[0] for word in words]).upper()

    def background_color(self):
        """Pick a random color background color.
        The background color should not be too bright, since the foreground
        font color defaults to white.
        """
        while True:
            red = int(random() * 150) + 50
            green = int(random() * 150) + 50
            blue = int(random() * 150) + 50
            color = red, green, blue

            if max(color) - min(color) > 30:
                return color

    def foreground_color(self):
        """Returns the font color, which is white by default.
        """
        return (255, 255, 255)

    def font(self):
        """Return a PIL ImageFont instance.
        """
        path = os.path.join(os.path.dirname(__file__), 'font',
                            'FantasqueSansMono-Bold.ttf')
        size = int(self.square_size * 0.8)
        return ImageFont.truetype(path, size=size)

    def draw_text(self, image, text, font):
        """Draw the text on the image.
        """
        draw = ImageDraw.Draw(image)
        draw.text(self.text_position(text, font),
                  text,
                  fill=self.foreground_color(),
                  font=font)

    def text_position(self, text, font):
        """Return the top-left point where the text should be placed.
        """
        textwidth, textheight = font.getsize(text)
        left = ((self.square_size - textwidth) / 2.0)
        top = (self.square_size - textheight) / (2 * 1.2)
        return left, top
