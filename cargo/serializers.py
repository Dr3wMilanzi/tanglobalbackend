from rest_framework import serializers
from .models import Cargo, CargoType, CargoDocument

class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ['id', 'name', 'slug']

class CargoDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoDocument
        fields = ['id', 'documentName', 'documentFile']

class CargoSerializer(serializers.ModelSerializer):
    cargo_type = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    cargo_document = CargoDocumentSerializer()  # Allow input/select for cargo_document

    class Meta:
        model = Cargo
        fields = ['id', 'cargo_type', 'uuid', 'weight', 'dimensions', 'cargo', 'fragile', 'temperature_sensitive',
                  'special_handling_instructions', 'origin', 'destination', 'sender_name', 'receiver_name',
                  'receiver_contact', 'added_at', 'pickupdate', 'delivery_date', 'actual_delivery_date',
                  'status', 'cargo_document']

    def create(self, validated_data):
        cargo_document_data = validated_data.pop('cargo_document')
        cargo = Cargo.objects.create(**validated_data)

        CargoDocument.objects.create(cargo=cargo, **cargo_document_data)

        return cargo
