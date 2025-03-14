"""
URL configuration for DjangoSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
       path('admin/', admin.site.urls, name='admin'),
       path('home/', views.home, name='home'),
       path('about/', views.about, name='about'),
       path('adresses/', views.adresses, name='adresses'),
       path('product/<int:product_id>', views.product, name='product'),
       path('basket_adding/', views.basket_adding, name='basket_adding'),
       path('checkout/', views.checkout, name='checkout'),
       path('', views.home, name='home'),
] \
       + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
       + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

