
from rest_framework import serializers
from django.conf import settings
from uuid import uuid4

from .models import File, Folder, EncryptionUser


class EncryptionUserSerializer(serializers.ModelSerializer):
    # http_method_names = ['get', 'post', 'patch', 'delete']

    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(
        source='user.date_joined', read_only=True)

    class Meta:
        model = EncryptionUser
        fields = ['id', 'key', 'user_id', 'username',
                  'first_name', 'last_name', 'email', 'date_joined']
        # depth = 1


class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ['id', 'files', 'name', 'parent']
        depth = 1


class FileSerializer(serializers.ModelSerializer):
    # uid = serializers.UUIDField('hex-verbose')

    class Meta:
        model = File
        fields = ['uid', 'name', 'type', 'file_owner']
        # depth = 1

    def create(self, validated_data):
        folder_id = self.context['folder_id']
        return File.objects.create(folder_id=folder_id, **validated_data)
