from rest_framework import viewsets,views
from accounts.models import User
from .serializers import UserSerializer



class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-created_at')
    serializer_class=UserSerializer


class UserSignin(views.APIView):
    pass