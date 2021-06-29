from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    class Meta:
        model = CustomUser
        fields = ('email', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

     

class ViewCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'wishlist') 