from rest_framework import serializers
from .models import Cargo, CargoType

class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ['id', 'name', 'slug']

class CargoSerializer(serializers.ModelSerializer):
    cargo_type = CargoTypeSerializer()

    class Meta:
        model = Cargo
        fields = '__all__'
