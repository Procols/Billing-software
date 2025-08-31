# setting/models.py
from django.db import models

class SiteConfig(models.Model):
    """
    Simple site configuration table — you can expand as needed.
    We'll keep only one row (singleton-like). Admins can edit values from UI.
    """
    site_name = models.CharField(max_length=200, default="KC Resort Billing")
    support_email = models.EmailField(blank=True, null=True)
    support_phone = models.CharField(max_length=50, blank=True, null=True)
    last_backup = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"
