from rest_framework.response import Response
from rest_framework.decorators import api_view
from appbase.models import District
from .serializers import DistrictSerializer
import requests

def get_districts_data():
    districts = District.objects.all()
    serializer = DistrictSerializer(districts, many=True)
    return serializer.data

@api_view(['GET'])
def getDistricts(request):
    districts_data = get_districts_data()
    return Response(districts_data)

@api_view(['POST'])
def addDistrict(request):
    serializer = DistrictSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getCoolestDistrict(request):
    coolestDistrict = {
        "id": "1",
        "division_id": "3",
        "name": "Dhaka",
        "bn_name": "ঢাকা",
        "lat": "23.7115253",
        "long": "90.4111451"
    }
    return Response(coolestDistrict)

@api_view(['GET'])
def getTemperatureAt2PM(request):
    districts_data = get_districts_data()

    latitude = [float(district['lat']) for district in districts_data]
    longitude = [float(district['long']) for district in districts_data]
    hour = 14

    endpoint = "https://api.open-meteo.com/v1/forecast"
    url_parameters = "&".join([f"latitude={lat}&longitude={lon}&hourly=temperature_2m" for lat, lon in zip(latitude, longitude)])
    api_request = f"{endpoint}?{url_parameters}"

    meteo_data = requests.get(api_request).json()

    temperatures = [
        [data['hourly']['temperature_2m'][hour + 24 * day] for day in range(7)]
        for data in meteo_data
    ]
    result = [
        {"district": district['name'], "temperatures_at_2pm": temp_data}
        for district, temp_data in zip(districts_data, temperatures)
    ]
    return Response({"temperatures": result})
