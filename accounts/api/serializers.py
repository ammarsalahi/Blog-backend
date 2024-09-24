from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(
            'first_name','last_name','username',
            'email','is_superuser','is_staff',
            'is_active','created_at','updated_at'
        )


class UserTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["username"] = user.username
        data['id']=user.id
        return data          