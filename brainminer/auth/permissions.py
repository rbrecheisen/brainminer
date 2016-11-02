from brainminer.auth.exceptions import PermissionDeniedException


# ----------------------------------------------------------------------------------------------------------------------
def has_permission(principal, permission):
    return principal.has_permission(permission)


# ----------------------------------------------------------------------------------------------------------------------
def check_permission(principal, permission):
    if not has_permission(principal, permission):
        raise PermissionDeniedException()
