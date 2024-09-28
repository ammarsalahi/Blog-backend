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
from django.core.files import File


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
        profile=Profile.objects.get(user=user)
        serializer=ProfileSerializer(instance=profile)
        return response.Response(data=serializer.data)

        # secret = pyotp.random_base32()        
        # profile=Profile.objects.get(user=user)
        # profile.otp_code=secret
        # profile.save()
        
        # totp = pyotp.TOTP(secret)
        
        # qr_url = totp.provisioning_uri(user.email, issuer_name="BlogApp")
        
        # qr_img = qrcode.make(qr_url)
        
        # buffer = BytesIO()
        # qr_img.save(buffer, format="PNG")
        # buffer.seek(0)
        # file_name = f'{user.username}_otp_qr.png'  # You can customize the file name
        # profile.qrcode_image.save(file_name, File(buffer), save=True)  # Save to the ImageField

        
        # return HttpResponse(buffer, content_type="image/png")

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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_new_otp(request):
    secret = pyotp.random_base32()        
    profile=Profile.objects.get(user=user)
    profile.otp_code=secret
    profile.save()    
    totp = pyotp.TOTP(secret)
    qr_url = totp.provisioning_uri(user.email, issuer_name="BlogApp")
    qr_img = qrcode.make(qr_url)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    file_name = f'{user.username}_otp_qr.png'  # You can customize the file name
    profile.qrcode_image.save(file_name, File(buffer), save=True)
    serializer=ProfileSerializer(instance=profile)
    return response.Response(data=serializer.data)  # Save to the ImageField    
    # return HttpResponse(buffer, content_type="image/png")






# class GenerateQRCodeView(APIView):
#     def get(self, request, format=None):
#         user = request.user
        
#         # Step 1: Generate the TOTP secret (or retrieve it from the user's profile)
#         secret = pyotp.random_base32()  # Generate a new secret
        
#         # Step 2: Optionally, save the secret in the user's profile
#         profile = Profile.objects.get(user=user)
#         profile.otp_code = secret
#         profile.save()

#         # Step 3: Create a TOTP object and generate the provisioning URI (for the QR code)
#         totp = pyotp.TOTP(secret)
#         qr_url = totp.provisioning_uri(user.email, issuer_name="BlogApp")

#         # Step 4: Generate the QR code from the URI
#         qr_img = qrcode.make(qr_url)

#         # Step 5: Convert the QR image to a BytesIO buffer
#         buffer = BytesIO()
#         qr_img.save(buffer, format="PNG")
#         buffer.seek(0)  # Go to the start of the buffer

#         # Step 6: Save the QR code to the ImageField
#         file_name = f'{user.username}_otp_qr.png'  # You can customize the file name
#         profile.qr_code_image.save(file_name, File(buffer), save=True)  # Save to the ImageField

#         # Optionally, return the QR code URL in the response or some success message
#         return Response({"qr_code_url": profile.qr_code_image.url})

