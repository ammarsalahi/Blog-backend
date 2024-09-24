from rest_framework import viewsets,views
from accounts.models import User
from .serializers import UserSerializer,UserTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-created_at')
    serializer_class=UserSerializer

class UserSigninView(TokenObtainPairView):
    serializer_class=UserTokenSerializer 

class UserSignupView(views.APIView):
    def post(self,request,format=None):
        pass
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
