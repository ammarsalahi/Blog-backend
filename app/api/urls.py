from rest_framework import routers
from .views import *
router = routers.DefaultRouter()


app_name="Apps"

router.register('news',NewsModelset,basename="app_news")
router.register('images',ImageViewset,basename="app_images")
router.register('links',LinkViewset,basename="app_links")
router.register('files',FileViewset,basename="app_files")


urlpatterns = router.urls()

