"""Hotel_Billing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('rooms/', include('rooms.urls', namespace='rooms')),
    path('booking/', include('booking.urls', namespace='booking')),
    path('foods_drinks/', include('foods.urls', namespace='foods')),
    path("checkin_checkout/", include("checkin_checkout.urls")),
    path('', include('core.urls', namespace='core')),
    path('invoices/', include('invoices.urls', namespace='invoices')),
    path('transaction/', include('transaction.urls', namespace='transaction')),
    path('report/', include('report.urls', namespace='report')),
    path('products/', include('products.urls', namespace='products')),
    path('setting/', include('setting.urls', namespace='setting')),
    path('tax_filling/', include('tax_filling.urls', namespace='tax_filling')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
