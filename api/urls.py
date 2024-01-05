from django.urls import path
from . import views

urlpatterns = [
    path('addDistrict', views.addDistrict),
    path('getDistricts', views.getDistricts),
    path('getCoolestDistrict', views.getCoolestDistrict),
]