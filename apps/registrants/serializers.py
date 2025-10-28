from rest_framework import serializers
from .models import Registrant

class RegistrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrant
        fields = ['id', 'full_name', 'email', 'phone']

