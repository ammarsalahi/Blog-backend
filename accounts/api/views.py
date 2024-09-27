from rest_framework import viewsets,views,response
from accounts.models import User,Profile
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import pyotp
import qrcode
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class UserViewset(viewsets.ModelViewSet):
    queryset=User.objects.all().order_by('-created_at')
    serializer_class=UserSerializer
    lookup_field="username"

class ProfileViewset(viewsets.ModelViewSet):
    queryset=Profile.objects.all().order_by('-created_at')
    serializer_class=ProfileSerializer

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
        Profile.objects.create(
            user=user
        )
        refresh = RefreshToken.for_user(user)
        return response.Response(
            data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username':user.username
            }
        )

class OtpGenerateView(views.APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        user = request.user
        # Create a TOTP object with a secret key for the user
        # You can store the user's secret key in the database or generate it dynamically
        secret = pyotp.random_base32()  # This is a randomly generated secret
        
        # Optionally, save the secret in the user's profile for later verification
        profile=Profile.objects.get(user=user)
        profile.otp_code=secret
        profile.save()
        
        # Create a TOTP object
        totp = pyotp.TOTP(secret)
        
        # Generate the provisioning URI for Google Authenticator (QR code data)
        qr_url = totp.provisioning_uri(user.email, issuer_name="BlogApp")
        
        # Generate the QR code from the URL
        qr_img = qrcode.make(qr_url)
        
        # Convert QR image to bytes
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)
        
        return HttpResponse(buffer, content_type="image/png")
    def post(self,request,format=None):
        user = request.user
        otp = request.data.get('otp')
        
        # Retrieve the user's secret key (saved in profile or database)
        secret = Profile.objects.get(user=user).otp_code
        
        # Create a TOTP object using the saved secret
        totp = pyotp.TOTP(secret)
        
        # Verify the OTP entered by the user
        if totp.verify(otp):
            return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP'})    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_jwt_token(request):
    return response.Response({"message": "Token is valid", "user": request.user.username})            