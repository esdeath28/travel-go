from django.urls import path
from . import views

urlpatterns = [
    path('addDistrict', views.addDistrict),
    path('getDistricts', views.getDistricts),
    path('getAllDistrictTemperatureAt2PM', views.getAllDistrictTemperatureAt2PM),
    path('getCoolestDistrict', views.getCoolestDistrict),
    path('getTemperatureAt2PM', views.getTemperatureAt2PM),
]