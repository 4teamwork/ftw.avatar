from ftw.avatar.member import create_default_avatar


def check_avatar(event):
    create_default_avatar(event.principal.getId())
