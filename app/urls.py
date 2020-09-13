# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import include, path, re_path
from . import views
from rest_framework import routers

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('loadinvoice/', views.loadInvoice),
    path('loadvendor/', views.loadVendor),
    path('remittance/', views.remittance),
    path('vendor/', views.vendors),
    path('invoice/', views.invoices ),
    path('email/', views.sendEmailBatchJob ),
]
