from rest_framework import viewsets,views,response,status
from app.models import *
from .serializers import *
from .paginations import NewsPagination
from .filters import NewsFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


User=get_user_model()
class NewsModelset(viewsets.ModelViewSet):
    queryset=News.objects.all()
    serializer_class=NewSerializer
    # pagination_class=NewsPagination
    # filter_backends= [NewsFilter]

class ImageViewset(viewsets.ModelViewSet):
    queryset = ImageBlog.objects.all() 
    serializer_class = ImageSerializer

class LinkViewset(viewsets.ModelViewSet):
    queryset = LinkBlog.objects.all()
    serializer_class = LinkSerializer

class FileViewset(viewsets.ModelViewSet):
    queryset = FileBlog.objects.all()
    serializer_class = FileSerializer

class NewsCreateView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # For handling file uploads

    def post(self, request, *args, **kwargs):
        title = request.data.get('title')
        content = request.data.get('description')
        is_timer_enabled = request.data.get('is_timer_enabled') == 'true'
        timer_duration = int(request.data.get('timer_duration', 0))

        images = request.FILES.getlist('images')
        links = request.data.getlist('links') 

        user = request.user  # Assumes authentication is in place

        # Create the News object
        news = News.objects.create(
            title=title,
            description=content,
            is_timer_enabled=is_timer_enabled,
            timer_duration=timer_duration,
            creator=user,
        )

        # Save the uploaded images
        for image_file in images:
            image_blog = ImageBlog.objects.create(image=image_file)
            news.images.add(image_blog)

        # Save the provided links
        for link_url in links:
            link_blog = LinkBlog.objects.create(url=link_url)
            news.links.add(link_blog)

        news.save()

        return response.Response({"message": "News post created successfully"}, status=status.HTTP_201_CREATED)    