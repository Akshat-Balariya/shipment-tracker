"""
URL configuration for shipment_tracker project.

Django's built-in admin lives at /django-admin/ so it does not collide with
the app's own /admin-panel/ routes, which are defined in tracking/urls.py.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('tracking.urls')),
]
