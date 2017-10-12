from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Medical
from rest_framework import status


@api_view(['POST'])
def save_medical(request):
    # ----- YAML below for Swagger -----
    """
    description: This API deletes/uninstalls a device.
    parameters:
      - name: name
        type: string
        required: true
        location: form
      - name: bloodgroup
        type: string
        required: true
        location: form
      - name: birthmark
        type: string
        required: true
        location: form
    """
    name = request.POST.get('name')
    bloodgroup = request.POST.get('bloodgroup')
    birthmark = request.POST.get('birthmark')

    try:
        Medical.objects.create(name= name, bloodgroup = bloodgroup, birthmark = birthmark)
        return Response("Data Saved!", status=status.HTTP_201_CREATED)

    except Exception as ex:
        return Response(ex, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_medical(request):
    return Response(Medical.objects.all().values(), status=status.HTTP_200_OK)