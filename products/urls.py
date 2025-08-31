from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add/", views.add_product, name="add_product"),
    path("update/<int:pk>/", views.update_quantity, name="update_quantity"),
    path("delete/<int:pk>/", views.delete_product, name="delete_product"),
]
