from ftw.avatar import LOGGER

MEMBER_IMAGE_SCALE = (300, 300)


def apply_patches():
    apply_member_image_scale_patch()


def apply_member_image_scale_patch():
    LOGGER.info('Patching maximum member scale in Products.PlonePAS.config'
                ' to %s' % str(MEMBER_IMAGE_SCALE))
    from Products.PlonePAS import config
    config.MEMBER_IMAGE_SCALE = MEMBER_IMAGE_SCALE
    config.IMAGE_SCALE_PARAMS['scale'] = MEMBER_IMAGE_SCALE
