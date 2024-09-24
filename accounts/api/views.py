from rest_framework import viewsets,views,response
from accounts.models import User
from .serializers import UserSerializer,UserTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-created_at')
    serializer_class=UserSerializer
    lookup_field="username"


class UserSigninView(TokenObtainPairView):
    serializer_class=UserTokenSerializer 

class UserSignupView(views.APIView):
    def post(self,request,format=None):
        data=request.data
        user=User.objects.create_publicuser(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            full_name=data['fullname']
        )
        refresh = RefreshToken.for_user(user)
        return response.Response(
            data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username':user.username
            }
        )
