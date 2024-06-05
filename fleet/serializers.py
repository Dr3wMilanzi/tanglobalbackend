from rest_framework import serializers
from .models import Vehicle, VehicleType, VehicleImage

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, required=False)

    class Meta:
        model = Vehicle
        fields = '__all__'

    def create(self, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        vehicle = Vehicle.objects.create(**validated_data)
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=vehicle, image=image_data)
        return vehicle

    def update(self, instance, validated_data):
        images_data = self.context['request'].FILES.getlist('images')
        instance = super().update(instance, validated_data)
        instance.images.all().delete()  # Remove existing images
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=instance, image=image_data)
        return instance

