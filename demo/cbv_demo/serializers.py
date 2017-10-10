from rest_framework import serializers
from .models import Contact


class ContactDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'