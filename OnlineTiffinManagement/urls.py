"""OnlineTiffinManagement URL Configuration

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
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("homepage.urls")),
    path('customerPlan/', include("customers.urls")),
    path('vendorPortal/', include("vendorPortal.urls")),
    
    # path('payment/', views.payment_form, name='payment_form'),
    # path('payment_success/', views.payment_success, name='payment_success'),
    # path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    # path('ipn_listener/', views.ipn_listener, name='ipn_listener'),  # For IPN verification
    
    
    # urls.py




      path('create-order/', views.create_order, name='create_order'),
      path('verify-payment/', views.verify_payment, name='verify_payment'),
    
    
    
    
    
]
