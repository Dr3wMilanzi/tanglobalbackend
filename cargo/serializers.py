from rest_framework import serializers
from .models import Cargo, CargoType, CargoDocument

class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'

class CargoDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoDocument
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    cargo_type = CargoTypeSerializer()
    cargo_document = CargoDocumentSerializer()

    class Meta:
        model = Cargo
        fields = '__all__'
