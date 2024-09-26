from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()


app_name="blogs"

router.register('news',NewsModelset,basename="app_news")
router.register('images',ImageViewset,basename="app_images")
router.register('links',LinkViewset,basename="app_links")


urlpatterns = router.urls

urlpatterns += [
    path('add-news/',NewsCreateView.as_view()),
]

