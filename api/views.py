from rest_framework.response import Response
from rest_framework.decorators import api_view
from appbase.models import District
from .serializers import DistrictSerializer

@api_view(['GET'])
def getDistricts(request):
    districts = District.objects.all()
    serializer = DistrictSerializer(districts, many=True)
    return Response(serializer.data)

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