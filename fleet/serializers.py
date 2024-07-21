from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Vehicle, VehicleType, VehicleImage, Driver, Trip

User = get_user_model()

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleImage
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    images = VehicleImageSerializer(many=True, read_only=True)
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Vehicle
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('image_files', [])
        vehicle = Vehicle.objects.create(**validated_data)
        for image_data in images_data:
            VehicleImage.objects.create(vehicle=vehicle, image=image_data)
        return vehicle

    def update(self, instance, validated_data):
        images_data = validated_data.pop('image_files', [])
        instance = super().update(instance, validated_data)
        if images_data:
            instance.images.all().delete()  # Clear existing images
            for image_data in images_data:
                VehicleImage.objects.create(vehicle=instance, image=image_data)
        return instance

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())

    class Meta:
        model = Trip
        fields = '__all__'

    def create(self, validated_data):
        trip = Trip.objects.create(**validated_data)
        return trip

    def update(self, instance, validated_data):
        instance.driver = validated_data.get('driver', instance.driver)
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
