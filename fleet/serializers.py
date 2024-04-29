from rest_framework import serializers
from .models import Vehicle, VehicleType, VehicleImage

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = ('id', 'image')

class VehicleSerializer(serializers.ModelSerializer):
    vehicle_types = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all(), many=True)
    images = VehicleImageSerializer(many=True)

    class Meta:
        model = Vehicle
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        vehicle = Vehicle.objects.create(**validated_data)
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=vehicle, **image_data)
        return vehicle

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)
        instance.images.all().delete()  # Remove existing images
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=instance, **image_data)
        return instance

        return vehicle