# serializers.py
from rest_framework import serializers
from .models import Cargo, CargoDocument, CargoType
from django.utils import timezone

class CustomDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        # Convert datetime to date while preserving timezone information
        if value is not None:
            return timezone.localtime(value).date()
        return None
    


class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = '__all__'

class CargoDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoDocument
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    added_at = CustomDateField()
    cargo_type = CargoTypeSerializer(many=True, read_only=True)
    cargo_document = CargoDocumentSerializer(many=True, required=False)

    class Meta:
        model = Cargo
        fields = '__all__'

    def create(self, validated_data):
        cargo_documents_data = validated_data.pop('cargo_document', [])
        cargo = Cargo.objects.create(**validated_data)
        
        for cargo_document_data in cargo_documents_data:
            CargoDocument.objects.create(cargo=cargo, **cargo_document_data)
        
        return cargo
    

    def update(self, instance, validated_data):
        cargo_types_data = validated_data.pop('cargo_type', [])
        cargo_documents_data = validated_data.pop('cargo_document', [])
        instance.name = validated_data.get('name', instance.name)
        # Update other fields similarly
        instance.save()

        instance.cargo_type.clear()
        for cargo_type_data in cargo_types_data:
            cargo_type, created = CargoType.objects.get_or_create(**cargo_type_data)
            instance.cargo_type.add(cargo_type)

        instance.cargo_document.all().delete()
        for cargo_document_data in cargo_documents_data:
            CargoDocument.objects.create(cargo=instance, **cargo_document_data)
        return instance
