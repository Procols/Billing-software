# setting/urls.py
from django.urls import path
from . import views

app_name = 'setting'

urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('download-db/', views.download_db_backup, name='download_db'),
]
