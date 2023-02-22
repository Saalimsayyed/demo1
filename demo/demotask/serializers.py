from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'mobile', 'otp')