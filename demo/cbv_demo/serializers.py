from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    class Meta:
        fields = ('name', 'address', 'email')