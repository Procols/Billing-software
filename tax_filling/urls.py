from django.urls import path
from . import views

app_name = "tax_filling"

urlpatterns = [
    path("", views.tax_filing_view, name="tax_filling"),
]
