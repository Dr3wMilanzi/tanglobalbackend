from rest_framework import serializers
from .models import CargoType, Cargo, CargoDocument, CargoImage, CargoTracking

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

class CargoSerializer(serializers.ModelSerializer):
    cargo_documents = CargoDocumentSerializer(many=True, read_only=False, required=False)
    images = CargoImageSerializer(many=True, read_only=False, required=False)
    cargo_type = serializers.PrimaryKeyRelatedField(queryset=CargoType.objects.all())

    class Meta:
        model = Cargo
        fields = '__all__'

    def create(self, validated_data):
        documents_data = validated_data.pop('cargo_documents', [])
        images_data = validated_data.pop('images', [])
        cargo = Cargo.objects.create(**validated_data)

        for document_data in documents_data:
            CargoDocument.objects.create(cargo=cargo, **document_data)

        for image_data in images_data:
            CargoImage.objects.create(cargo=cargo, **image_data)

        return cargo

class CargoTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoTracking
        fields = '__all__'