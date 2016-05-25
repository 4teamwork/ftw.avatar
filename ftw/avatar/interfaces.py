from zope.interface import Interface


class IAvatarGenerator(Interface):
    """Adapter for generating a default avatar.
    """

    def generate(userid, output_stream):
        """Generates a default avatar image for a user with the passed
        ``userid`` and writes to the ``output_stream``, which is expected
        to be a file-like object.
        """
