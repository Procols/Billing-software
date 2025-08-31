from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def admins_only(view_func):
    """
    Custom decorator: Allow only Admin and Sub Admin users.
    """
    @wraps(view_func)
    @login_required  # First check: user must be logged in
    def _wrapped(request, *args, **kwargs):
        user = request.user

        # If user has is_admin or is_subadmin attribute and it is True → Allow
        if getattr(user, "is_admin", False) or getattr(user, "is_subadmin", False):
            return view_func(request, *args, **kwargs)

        # Otherwise block
        raise PermissionDenied("You do not have permission to access this page.")

    return _wrapped
