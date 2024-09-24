from rest_framework import routers
from .views import UserViewset

router=routers.DefaultRouter()

router.register('users',UserViewset,basename="users")


urlpatterns = router.urls()