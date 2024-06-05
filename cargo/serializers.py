from rest_framework import serializers
from .models import Cargo, CargoType, CargoDocument


class CargoTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoType
        fields = ['id', 'name', 'slug']


class CargoDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoDocument
        fields = ('id', 'documentName', 'documentFile')
        extra_kwargs = {
            'documentName': {'required': False},
            'documentFile': {'required': False}
        }


class CargoSerializer(serializers.ModelSerializer):
    cargo_type = serializers.PrimaryKeyRelatedField(queryset=CargoType.objects.all(), many=True)
    cargo_documents = CargoDocumentSerializer(many=True, required=False)

    class Meta:
        model = Cargo
        fields = '__all__'
    
    def create(self, validated_data):
        print(validated_data)
        cargo_type_data = validated_data.pop('cargo_type', [])
        cargo_documents_data = validated_data.pop('cargo_documents', [])

        cargo = Cargo.objects.create(**validated_data)

        for cargo_type_item in cargo_type_data:
            cargo_type_obj = CargoType.objects.create(**cargo_type_item)
            cargo.cargo_type.add(cargo_type_obj)

        for cargo_document_data in cargo_documents_data:
            CargoDocument.objects.create(cargo=cargo, **cargo_document_data)

        return cargo

    def update(self, instance, validated_data):
        cargo_type_data = validated_data.pop('cargo_type', [])
        cargo_documents_data = validated_data.pop('cargo_documents', [])

        cargo_type_instances = []
        for cargo_type_item in cargo_type_data:
            cargo_type_obj, created = CargoType.objects.get_or_create(**cargo_type_item)
            cargo_type_instances.append(cargo_type_obj)

        cargo_documents_instances = []
        for cargo_document_data in cargo_documents_data:
            cargo_document_obj, created = CargoDocument.objects.update_or_create(cargo=instance, **cargo_document_data)
            cargo_documents_instances.append(cargo_document_obj)

        instance.cargo_type.set(cargo_type_instances)

        # If you want to remove any existing cargo documents not in the updated data
        instance.cargo_documents.exclude(id__in=[cd.id for cd in cargo_documents_instances]).delete()

        return instance