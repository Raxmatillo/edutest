from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'full_name',
            'password',
            'role',
            'phone_number',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            full_name=validated_data.get('full_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'role',
            'phone_number',
            'profile_picture',
            'language_preference',
            'job_title',
            'workplace',
            'school',
        ]
        read_only_fields = ['id', 'username', 'role']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()