from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),  # Dashboard with invoices included
    path("invoice/<int:booking_id>/", views.invoice_detail, name="invoice_detail"),  # Invoice detail
]
