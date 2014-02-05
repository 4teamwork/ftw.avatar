from ftw.avatar.member import create_default_avatar
import logging


LOGGER = logging.getLogger('ftw.avatar')
MEMBER_IMAGE_SCALE = (300, 300)


def apply_patches():
    apply_member_image_scale_patch()
    apply_getPersonalPortrait_patch()


def apply_member_image_scale_patch():
    LOGGER.info('Patching maxmimum member scale in Products.PlonePAS.config'
                ' to %s' % str(MEMBER_IMAGE_SCALE))
    from Products.PlonePAS import config
    config.MEMBER_IMAGE_SCALE = MEMBER_IMAGE_SCALE
    config.IMAGE_SCALE_PARAMS['scale'] = MEMBER_IMAGE_SCALE


def apply_getPersonalPortrait_patch():
    LOGGER.info('Patching Products.PlonePAS.tools.membership.MembershipTool'
                '.getPersonalPortrait for generating a default portrait')
    from Products.PlonePAS.tools.membership import MembershipTool
    getPersonalPortrait = MembershipTool.getPersonalPortrait

    def getPersonalPortraitWrapper(self, id=None, verifyPermission=0):
        create_default_avatar(id or self.getAuthenticatedMember().getId())
        return getPersonalPortrait(self, id=id,
                                   verifyPermission=verifyPermission)

    MembershipTool.getPersonalPortrait = getPersonalPortraitWrapper
