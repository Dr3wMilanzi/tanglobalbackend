# serializers.py

from rest_framework import serializers
from .models import Cargo, CargoType, CargoDocument, CargoImage, CargoTracking
from accounts.models import CustomUser

class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'

class CargoDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoDocument
        fields = '__all__'

class CargoImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoImage
        fields = '__all__'

class CargoTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoTracking
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    sender_name = serializers.PrimaryKeyRelatedField(read_only=True)
    cargo_documents = CargoDocumentSerializer(many=True, read_only=True)
    images = CargoImageSerializer(many=True, read_only=True)
    tracking_info = CargoTrackingSerializer(many=True, read_only=True)

    class Meta:
        model = Cargo
        fields = '__all__'
