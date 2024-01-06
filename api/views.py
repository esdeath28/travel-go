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
    average_temperatures = [sum(temp_list) / len(temp_list) for temp_list in temperatures]
    result = [
    {
        "district": district['name'],
        "temperatures_at_2pm": temp_data,
        "average_temperature_at_2pm": avg_temp
    }
    for district, temp_data, avg_temp in zip(districts_data, temperatures, average_temperatures)
    ]
    coolest_district = sorted(result, key=lambda x: x['average_temperature_at_2pm'])
    return Response({"Coolest Districts": coolest_district[:10]})

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
    # temperatures = [data['hourly']['temperature_2m'][hour] for data in meteo_data]
    # result = [{"district": district['name'], "temperatures_at_2pm": temperatures} for district in districts_data]
    temperatures = [
        [data['hourly']['temperature_2m'][hour + 24 * day] for day in range(7)]
        for data in meteo_data
    ]
    result = [
        {"district": district['name'], "temperatures_at_2pm": temp_data}
        for district, temp_data in zip(districts_data, temperatures)
    ]
    return Response({"temperatures": result})
