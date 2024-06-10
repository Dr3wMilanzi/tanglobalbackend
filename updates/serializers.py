# serializers.py

from rest_framework import serializers
from .models import UpdateType, Update, SelectedUpdatesByUser, UpdateView

class UpdateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateType
        fields = ['id', 'name', 'slug']

class UpdateSerializer(serializers.ModelSerializer):
    # TrackSerializer(many=True, read_only=True)
    update_type = serializers.PrimaryKeyRelatedField(queryset=UpdateType.objects.all())

    class Meta:
        model = Update
        depth=1
        fields = ['id', 'name', 'slug', 'update_type', 'content', 'is_approved', 'created_at']
        read_only_fields = ['update_type']


class SelectedUpdatesByUserSerializer(serializers.ModelSerializer):
    update_type = serializers.PrimaryKeyRelatedField(queryset=UpdateType.objects.all())

    class Meta:
        model = SelectedUpdatesByUser
        fields = ['id', 'update_type','user']

class UpdateViewSerializer(serializers.ModelSerializer):
    update = UpdateSerializer(read_only=True)

    class Meta:
        model = UpdateView
        fields = ['id', 'update', 'viewed_at']
