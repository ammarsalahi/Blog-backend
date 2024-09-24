from rest_framework import viewsets
from app.models import *
from .serializers import *
from .paginations import NewsPagination
from .filters import NewsFilter

class NewsModelset(viewsets.ModelViewSet):
    queryset=News.objects.all()
    serializer_class=NewSerializer
    pagination_class=NewsPagination
    filter_backends= [NewsFilter]

class ImageViewset(viewsets.ModelViewSet):
    queryset = ImageBlog.objects.all() 
    serializer_class = ImageSerializer

class LinkViewset(viewsets.ModelViewSet):
    queryset = LinkBlog.objects.all()
    serializer_class = LinkSerializer

class FileViewset(viewsets.ModelViewSet):
    queryset = FileBlog.objects.all()
    serializer_class = FileSerializer