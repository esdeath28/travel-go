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
    return Response(coolest_district[:10])

@api_view(['GET'])
def getAllDistrictTemperatureAt2PM(request):
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

@api_view(['POST'])
def getTemperatureAt2PM(request):
    # https://open-meteo.com/en/docs#latitude=23.7104&longitude=90.4074&hourly=temperature_2m&forecast_days=1&start_date=2024-01-06&end_date=2024-01-06&time_mode=time_interval
    # {"latitude": 23.7104, "longitude": 90.4074, "start_date": "2024-01-07", "end_date": "2024-01-07", "hour": 14}
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    hour = request.data.get('hour')

    endpoint = "https://api.open-meteo.com/v1/forecast"
    api_request = f"{endpoint}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&start_date={start_date}&end_date={end_date}"
    meteo_data = requests.get(api_request).json()
    temp = meteo_data['hourly']['temperature_2m'][hour]
    print(meteo_data)

    return Response(temp)
