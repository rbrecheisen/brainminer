from flask import g
from brainminer.auth.dao import PermissionDao
from brainminer.auth.exceptions import UserNotAdminException, UserNotSuperUserException, PermissionDeniedException


# ----------------------------------------------------------------------------------------------------------------------
def is_superuser(principal):
    return principal.is_superuser


# ----------------------------------------------------------------------------------------------------------------------
def check_superuser(principal):
    if not is_superuser(principal):
        raise UserNotSuperUserException(principa.username)
    
    
# ----------------------------------------------------------------------------------------------------------------------
def is_admin(principal):
    return principal.is_admin


# ----------------------------------------------------------------------------------------------------------------------
def check_admin(principal):
    if not is_admin(principal):
        raise UserNotAdminException(principal.username)
    
    
# ----------------------------------------------------------------------------------------------------------------------
def has_permission(principal, permission):
    return principal.has_permission(permission)


# ----------------------------------------------------------------------------------------------------------------------
def check_permission(principal, permission):
    if not has_permission(principal, permission):
        raise PermissionDeniedException(permission)


# ----------------------------------------------------------------------------------------------------------------------
def add_permission(principal, permission):
    
    # First check whether principal already has this permission or
    # a permission with wider scope. If so, there's no need to create
    # smaller-scope permission.
    if has_permission(principal, permission):
        return
    # Extract permission fields from permission string
    resource_id = None
    action, resource_class = permission.split(':')
    if '@' in resource_class:
        resource_class, resource_id = resource_class.split('@')
    # Create argument dictionary
    args = dict()
    args['action'] = action
    args['resource_class'] = resource_class
    args['resource_id'] = resource_id
    args['principal'] = principal
    # Create permission
    permission_dao = PermissionDao(g.db_session)
    permission_dao.create(**args)
