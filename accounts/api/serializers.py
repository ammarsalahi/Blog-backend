from rest_framework import serializers
from accounts.models import User,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('last_login',)
    def to_representation(self,instance):
        data=super().to_representation(instance)
        data.pop('password',None)
        return data    


class UserTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["username"] = user.username
        data['is_admin']=user.is_superuser
        data['is_otp'] = user.is_two_factor_auth
        return data          

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields="__all__"        