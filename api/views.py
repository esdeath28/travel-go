from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from appbase.models import District
from .serializers import DistrictSerializer
import requests
from datetime import datetime

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
def getCoolestDistricts(request):
    try:
        districts_data = get_districts_data()
        if not districts_data:
                return Response({"error": "No district data available."}, status=status.HTTP_400_BAD_REQUEST)

        latitude_parameters = ",".join(map(lambda district: str(district['lat']), districts_data))
        longitude_parameters = ",".join(map(lambda district: str(district['long']), districts_data))
        hour = 14

        endpoint = "https://api.open-meteo.com/v1/forecast"
        url_parameters = f"latitude={latitude_parameters}&longitude={longitude_parameters}&hourly=temperature_2m"
        api_request = f"{endpoint}?{url_parameters}"
        meteo_data = requests.get(api_request).json()

        temperatures = [
            [data['hourly']['temperature_2m'][hour + 24 * day] for day in range(7)]
            for data in meteo_data
        ]
        average_temperatures = [round(sum(temp_list) / len(temp_list), 1) for temp_list in temperatures]
        result = [
        {
            "district": district['name'],
            "latitude": district['lat'],
            "longitude": district['long'],
            "average_temperature_at_2pm": avg_temp
        }
        for district, avg_temp in zip(districts_data, average_temperatures)
        ]
        coolest_district = sorted(result, key=lambda x: x['average_temperature_at_2pm'])[:10]
        return Response(coolest_district)
    except Exception as ex:
        print(ex)
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
def getOnDateTemperatureAt2PM(request):
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

def getTemperatureAt2PM(latitude, longitude, start_date, end_date, hour):
    try:
        endpoint = "https://api.open-meteo.com/v1/forecast"
        api_request = f"{endpoint}?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&start_date={start_date}&end_date={end_date}"
        meteo_data = requests.get(api_request).json()
        temp = meteo_data['hourly']['temperature_2m'][hour]
        return temp
    except (requests.RequestException, KeyError, IndexError) as e:
        print(e)
        return None

@api_view(['POST'])
def travelRecommendationOld(request):
    try:
        # {"departure_latitude": 23.7104, "departure_longitude": 90.4074, "destination_latitude": 24.3745, "destination_longitude": 88.6042, "travelling_date": "2024-01-07"}
        
        departure_latitude = request.data.get('departure_latitude')
        departure_longitude = request.data.get('departure_longitude')
        destination_latitude = request.data.get('destination_latitude')
        destination_longitude = request.data.get('destination_longitude')
        travelling_date = request.data.get('travelling_date')
        hour = 14
        recommended = False

        if None in [departure_latitude, departure_longitude, destination_latitude, destination_longitude, travelling_date]:
                return Response({"error": "Incomplete input data."}, status=status.HTTP_400_BAD_REQUEST)
        
        departureTemperature = getTemperatureAt2PM(departure_latitude, departure_longitude, travelling_date, travelling_date, hour)
        travellingTemperature = getTemperatureAt2PM(destination_latitude, destination_longitude, travelling_date, travelling_date, hour)

        if departureTemperature is not None and travellingTemperature is not None:
            recommended = departureTemperature > travellingTemperature
            return Response({
                "departureTemperature": departureTemperature,
                "travellingTemperature": travellingTemperature,
                "Recommended": recommended
            })
        else:
            return Response({"error": "Error fetching temperature data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(e)
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def travelRecommendation(request):
    try:
        # {"departure_latitude": 23.7104, "departure_longitude": 90.4074, "destination_latitude": 24.3745, "destination_longitude": 88.6042, "travelling_date": "2024-01-07"}

        departure_latitude = request.data.get('departure_latitude')
        departure_longitude = request.data.get('departure_longitude')
        destination_latitude = request.data.get('destination_latitude')
        destination_longitude = request.data.get('destination_longitude')
        travelling_date = request.data.get('travelling_date')
        hour = 14
        recommended = False

        if None in [departure_latitude, departure_longitude, destination_latitude, destination_longitude, travelling_date]:
            return Response({"error": "Incomplete input data."}, status=status.HTTP_400_BAD_REQUEST)
        if datetime.strptime(travelling_date, "%Y-%m-%d").date() < datetime.now().date():
            return Response({"error": "Travelling date cannot be backdated from today."}, status=status.HTTP_400_BAD_REQUEST)

        endpoint = "https://api.open-meteo.com/v1/forecast"
        api_request = f"{endpoint}?latitude={departure_latitude},{destination_latitude}&longitude={departure_longitude},{destination_longitude}&hourly=temperature_2m&start_date={travelling_date}&end_date={travelling_date}"
        meteo_data = requests.get(api_request).json()
        # print(json.dumps(meteo_data, indent=2))
        
        if meteo_data is not None:
            recommended = meteo_data[0]['hourly']['temperature_2m'][hour] > meteo_data[1]['hourly']['temperature_2m'][hour]
            return Response({
                "Recommended": recommended 
            })
        else:
            return Response({"error": "Error fetching temperature data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(e)
        return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
