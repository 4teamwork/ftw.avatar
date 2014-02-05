import AccessControl


class SwitchedToSystemUser(object):
    """Context manager for switching temporarily to a system user.
    """

    def __init__(self):
        self._original_security = None

    def __enter__(self):
        assert self._original_security is None, \
            'Context manager is not reusable'
        self._original_security = AccessControl.getSecurityManager()
        _system_user = AccessControl.SecurityManagement.SpecialUsers.system
        AccessControl.SecurityManagement.newSecurityManager(
            None, _system_user)

    def __exit__(self, _exc_type, _exc_value, _traceback):
        AccessControl.SecurityManagement.setSecurityManager(
            self._original_security)
        self._original_security = None
