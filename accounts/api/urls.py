from rest_framework import routers
from .views import UserViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router=routers.DefaultRouter()

router.register('users',UserViewset,basename="users")


urlpatterns = router.urls()

urlpatterns+=[

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]