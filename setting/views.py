
import shutil
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .decorators import admins_only

from .models import SiteConfig
from .forms import SiteConfigForm, UserEditForm

User = get_user_model()

def _is_admin_or_subadmin(user):
    # Safe check for custom user methods
    return getattr(user, 'is_admin', lambda: False)() or getattr(user, 'is_subadmin', lambda: False)()

@admins_only
def index(request):
    profile = request.user
    site_config, _ = SiteConfig.objects.get_or_create(id=1)

    # If admin or subadmin, show full user list
    users = User.objects.all() if _is_admin_or_subadmin(request.user) else None

    if request.method == "POST" and 'save_site_config' in request.POST:
        if not _is_admin_or_subadmin(request.user):
            messages.error(request, "You don't have permission to update site configuration.")
            return redirect('setting:index')

        form = SiteConfigForm(request.POST, instance=site_config)
        if form.is_valid():
            form.save()
            messages.success(request, "Site configuration updated.")
            return redirect('setting:index')
    else:
        form = SiteConfigForm(instance=site_config)

    context = {
        'profile': profile,
        'site_config': site_config,
        'form': form,
        'users': users,
    }
    return render(request, 'setting/index.html', context)



@admins_only
def user_edit(request, pk):
    """ Edit user — Admin/Subadmin only """
    if not _is_admin_or_subadmin(request.user):
        return HttpResponse("Forbidden", status=403)

    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated.")
            return redirect('setting:index')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'setting/user_edit.html', {'form': form, 'edit_user': user})


@admins_only
def download_db_backup(request):
    """
    Provide a copy of the current DB file as an attachment.
    Works for SQLite (development). Admin/Subadmin only.
    """
    if not _is_admin_or_subadmin(request.user):
        return HttpResponse("Forbidden", status=403)

    db_setting = settings.DATABASES.get('default', {})
    db_name = db_setting.get('NAME')
    if not db_name:
        raise Http404("Database path not configured")

    # If NAME is a relative path, resolve against BASE_DIR
    db_path = os.path.abspath(db_name)

    if not os.path.exists(db_path):
        raise Http404("Database file not found")

    # We will stream the file: set appropriate filename
    filename = f"db_backup_{timezone.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"

    # Update last_backup in SiteConfig
    site_config, _ = SiteConfig.objects.get_or_create(id=1)
    site_config.last_backup = timezone.now()
    site_config.save()

    # Return file response
    # Use FileResponse for efficient streaming
    response = FileResponse(open(db_path, 'rb'), as_attachment=True, filename=filename)
    return response
