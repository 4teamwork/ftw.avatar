from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from ftw.avatar.interfaces import IAvatarGenerator
from ftw.avatar.utils import SwitchedToSystemUser
from zope.component import getUtility
from zope.component.hooks import getSite


def get_name_of_user(userid):
    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    member = membership.getMemberById(userid)
    return member.getProperty('fullname', None)


def user_has_portrait(userid):
    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    memberdata = getToolByName(portal, 'portal_memberdata')
    safe_id = membership._getSafeMemberId(userid)
    return memberdata._getPortrait(safe_id) is not None


def create_default_avatar(userid):
    if user_has_portrait(userid):
        return

    portrait = StringIO()
    getUtility(IAvatarGenerator).generate(get_name_of_user(userid), portrait)
    portrait.seek(0)
    setattr(portrait, 'filename', 'default.png')

    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    with SwitchedToSystemUser():
        membership.changeMemberPortrait(portrait, id=userid)
