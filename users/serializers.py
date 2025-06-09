from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'nickname', 'name', 'phone_number', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            name=validated_data['name'],
            phone_number=validated_data.get('phone_number', ''),
            password=validated_data['password']
        )
        return user
