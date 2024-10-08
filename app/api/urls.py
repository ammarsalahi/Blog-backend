from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()


app_name="blogs"

router.register('news',NewsModelset,basename="app_news")
router.register('images',ImageViewset,basename="app_images")
router.register('links',LinkViewset,basename="app_links")
router.register('files',FileViewset,basename="app_files")
router.register('news-view',NewsViewsViewset,basename="news-view")
# router.register('news-review',NewsViewSet,basename="news-reviews")

urlpatterns = router.urls

urlpatterns += [
    path('add-news/',NewsCreateView.as_view()),
    path('edit-news/<int:pk>/',NewsUpdateView.as_view()),
    path('news-review/<int:pk>/',NewsViewSet.as_view({'get':'retrieve'})),
    path("chart-news/",NewsChartView.as_view())
]

