from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("track/<str:tracking_number>/", views.track_shipment, name="track_shipment"),
    path("admin-panel/", views.admin_home, name="admin_home"),
    path("admin-panel/create/", views.admin_create, name="admin_create"),
    path("admin-panel/<str:tracking_number>/update/", views.admin_update_status, name="admin_update_status"),
]
