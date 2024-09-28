from rest_framework import routers
from .views import *
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router=routers.DefaultRouter()

router.register('users',UserViewset,basename="users")
router.register('profiles',ProfileViewset,basename="profiles")



urlpatterns = router.urls

urlpatterns+=[

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',UserSignupView.as_view(),name="signup"),
    path('signin/',UserSigninView.as_view(),name="signin"),
    path('otp/',OtpGenerateView.as_view()),
    path('new-otp/',get_new_otp),
    path("check-token/",check_jwt_token),
]