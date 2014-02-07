import logging
LOGGER = logging.getLogger('ftw.avatar')

from ftw.avatar.patches import apply_patches
apply_patches()
