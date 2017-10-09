from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


# Create your views here.
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_contact(request):
    # ----- YAML below for Swagger -----
        return Response("Testing POST")


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_contact(request):
    # ----- YAML below for Swagger -----
    return Response("Testing GET")