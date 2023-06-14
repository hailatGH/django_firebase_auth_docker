from rest_framework import serializers
from django.contrib.auth.models import Permission, Group

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        permissions = validated_data.pop('user_permissions', None)
        groups = validated_data.pop('groups', None)
        user = CustomUser.objects.create(**validated_data)
        
        if permissions:
            user.user_permissions.set(permissions)
        if groups:
            user.groups.set(groups)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        permissions = validated_data.pop('user_permissions', None)
        groups = validated_data.pop('groups', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if permissions:
            instance.user_permissions.set(permissions)
        if groups:
            instance.groups.set(groups)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"