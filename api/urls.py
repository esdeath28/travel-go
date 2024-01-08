from django.urls import path
from . import views

urlpatterns = [
    path('getCoolestDistricts', views.getCoolestDistricts),
    path('travelRecommendation', views.travelRecommendation),
]