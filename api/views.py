from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from appbase.models import District
from .serializers import DistrictSerializer
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os
import json

def get_temperatures(chunk):
    try:
        latitude_parameters_chunk = ",".join(map(lambda district: str(district['lat']), chunk))
        longitude_parameters_chunk = ",".join(map(lambda district: str(district['long']), chunk))

        hour = 14
        endpoint = "https://api.open-meteo.com/v1/forecast"
        url_parameters = f"latitude={latitude_parameters_chunk}&longitude={longitude_parameters_chunk}&hourly=temperature_2m"
        api_request = f"{endpoint}?{url_parameters}"
        meteo_data = requests.get(api_request).json()

        temperatures = [
            [data['hourly']['temperature_2m'][hour + 24 * day] for day in range(7)]
            for data in meteo_data
        ]

        return temperatures
    except Exception as e:
        print(f"Error in get_temperatures: {e}")
        return []
    
@api_view(['GET'])
def getCoolestDistricts(request):
    try:
        districts_data = cache.get('districts_data')
        if districts_data is None:
            try:
                with open('static/districts_data.json', 'r') as json_file:
                        districts = json.load(json_file)
                serializer = DistrictSerializer(data=districts, many=True)
                serializer.is_valid(raise_exception=True)
                districts_data = serializer.data
            except FileNotFoundError:
                return Response({"error": "District data file not found. Make sure the file exists at the specified location"}, status=status.HTTP_400_BAD_REQUEST)
            cache.set('districts_data', districts_data, timeout=15778463)

        if not districts_data:
                return Response({"error": "No district data available."}, status=status.HTTP_400_BAD_REQUEST)
        
        num_chunks = 4
        chunk_len = len(districts_data) // num_chunks
        chunks = [districts_data[i:i + chunk_len] for i in range(0, len(districts_data), chunk_len)]
        if len(districts_data) % num_chunks != 0:
            chunks[-1].extend(districts_data[chunk_len * num_chunks:])

        with ThreadPoolExecutor(max_workers=os.cpu_count()//2) as executor:
            temperatures_lists = list(executor.map(get_temperatures, chunks))
        
        temperatures = [temp for sublist in temperatures_lists for temp in sublist]

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

def is_valid_lat_long(latitude, longitude):
    try:
        return -90 <= latitude <= 90 and -180 <= longitude <= 180
    except ValueError:
        return False
    
@api_view(['POST'])
def travelRecommendation(request):
    try:
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
        if not (is_valid_lat_long(departure_latitude, departure_longitude) and is_valid_lat_long(destination_latitude, destination_longitude)):
            return Response({"error": "Invalid latitude or longitude data."}, status=status.HTTP_400_BAD_REQUEST)


        endpoint = "https://api.open-meteo.com/v1/forecast"
        api_request = f"{endpoint}?latitude={departure_latitude},{destination_latitude}&longitude={departure_longitude},{destination_longitude}&hourly=temperature_2m&start_date={travelling_date}&end_date={travelling_date}"
        meteo_data = requests.get(api_request).json()
        
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
