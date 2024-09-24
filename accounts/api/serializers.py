from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=("password",'last_login')


class UserTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["username"] = user.username
        data['is_admin']=user.is_superuser
        return data          