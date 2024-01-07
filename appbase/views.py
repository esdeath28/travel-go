from django.shortcuts import render
import requests

# Create your views here.
def travelGo(request):
    response = requests.get('http://127.0.0.1:8000/getCoolestDistricts')
    api_data = response.json()
    return render(request, 'base.html', {'api_data': api_data})