def is_owner_or_admin(user, obj):
    """
    Returns True if the user is the owner of the given object
    or if the user is staff. Returns False otherwise.
    """
    has_permission = obj == user or getattr(obj, 'owner', None) == user
    return has_permission or user.is_staff
