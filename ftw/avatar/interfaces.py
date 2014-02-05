from zope.interface import Interface


class IAvatarGenerator(Interface):
    """Adapter for generating a default avatar.
    """

    def generate(name, output_stream):
        """Generates a default avatar image for a user with the passed
        ``name`` and writes to the ``output_stream``, which is expected
        to be a file-like object.
        """
