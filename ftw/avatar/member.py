from ftw.avatar.interfaces import IAvatarGenerator
from ftw.avatar.utils import SwitchedToSystemUser
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from zope.component.hooks import getSite
from zope.component import getUtility


def get_user_id(userid):
    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    member = membership.getMemberById(userid)

    if member:
        return member.getId()

    acl_users = getToolByName(portal, 'acl_users')
    user = acl_users.getUser(userid)
    if user:
        return user.getId()

    return None


def user_has_portrait(userid):
    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    memberdata = getToolByName(portal, 'portal_memberdata')
    safe_id = membership._getSafeMemberId(userid)
    return memberdata._getPortrait(safe_id) is not None


def create_default_avatar(userid):
    userid = get_user_id(userid)
    if user_has_portrait(userid):
        return

    portrait = StringIO()
    generator = getUtility(IAvatarGenerator)
    if not generator.generate(userid, portrait):
        return
    portrait.seek(0)
    setattr(portrait, 'filename', 'default.png')

    portal = getSite()
    membership = getToolByName(portal, 'portal_membership')
    with SwitchedToSystemUser():
        membership.changeMemberPortrait(portrait, id=userid)
