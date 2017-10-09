from rest_framework.views import APIView
from demo.cbv_demo.serializers import ContactSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class Contact(APIView):
    serializer_class = ContactSerializer
    permission_classes = IsAuthenticated


    def get(self, request, format=None):
        return Response("Testing GET")

    def post(self, request):
        serializer = ContactSerializer(request.data)

        return Response("Testing POST")