from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def admins_only(view_func):
    """
    Allow only Admin and Sub Admin.
    """
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        u = request.user
        if getattr(u, 'is_admin', lambda: False)() or getattr(u, 'is_subadmin', lambda: False)():
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped
