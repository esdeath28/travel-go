from django.urls import path
from . import views

urlpatterns = [
    path('addDistrict', views.addDistrict),
    path('getDistricts', views.getDistricts),
    path('getTemperatureAt2PM', views.getTemperatureAt2PM),
    path('getCoolestDistrict', views.getCoolestDistrict),

]