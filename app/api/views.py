from rest_framework import viewsets
from app.models import *
from .serializers import *

class NewsModelset(viewsets.ModelViewSet):
    queryset=News.objects.all().order_by('-created_at')
    serializer_class=NewSerializer

class ImageViewset(viewsets.ModelViewSet):
    queryset = ImageBlog.objects.all().order_by('-created_at')
    serializer_class = ImageSerializer

class LinkViewset(viewsets.ModelViewSet):
    queryset = LinkBlog.objects.all().order_by('-created_at')
    serializer_class = LinkSerializer

class FileViewset(viewsets.ModelViewSet):
    queryset = FileBlog.objects.all().order_by('-created_at')
    serializer_class = FileSerializer