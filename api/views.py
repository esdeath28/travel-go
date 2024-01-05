from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getDistrictData(request):
    district = {
        "id": "1",
        "division_id": "3",
        "name": "Dhaka",
        "bn_name": "ঢাকা",
        "lat": "23.7115253",
        "long": "90.4111451"
    }
    return Response(district)