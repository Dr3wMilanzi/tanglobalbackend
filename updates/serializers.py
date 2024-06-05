# serializers.py

from rest_framework import serializers
from .models import UpdateType, Update, SelectedUpdatesByUser, UpdateView

class UpdateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateType
        fields = ['id', 'name', 'slug']

class UpdateSerializer(serializers.ModelSerializer):
    update_type = serializers.PrimaryKeyRelatedField(queryset=UpdateType.objects.all(), write_only=True)

    class Meta:
        model = Update
        fields = ['id', 'name', 'slug', 'update_type', 'content', 'isapproved', 'created_at']
        read_only_fields = ['update_type']

    # def create(self, validated_data):
    #     update_type_id = validated_data.pop('update_type')
    #     update_type = UpdateType.objects.get(id=update_type_id)
    #     validated_data['update_type'] = update_type
    #     return super().create(validated_data)


class SelectedUpdatesByUserSerializer(serializers.ModelSerializer):
    update_type = UpdateTypeSerializer(read_only=True)

    class Meta:
        model = SelectedUpdatesByUser
        fields = ['id', 'update_type']

class UpdateViewSerializer(serializers.ModelSerializer):
    update = UpdateSerializer(read_only=True)

    class Meta:
        model = UpdateView
        fields = ['id', 'update', 'viewed_at']
