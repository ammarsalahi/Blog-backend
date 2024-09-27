from rest_framework import viewsets,views,response,status
from app.models import *
from .serializers import *
from .paginations import NewsPagination
from .filters import NewsFilter
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count
from django.db.models.functions import TruncMonth
import calendar

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
        

class NewsViewsViewset(viewsets.ModelViewSet):
    queryset = NewsView.objects.all()
    serializer_class = NewsViewSerializer

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
        files  = request.FILES.getlist('files')
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
            link_blog = LinkBlog.objects.create(href=link_url,text=link_url)
            news.links.add(link_blog)

        for f in files:
            file_blog = FileBlog.objects.create(file=f)
            news.files.add(file_blog)
        news.save()

        return response.Response({"message": "News post created successfully"}, status=status.HTTP_201_CREATED)    


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class NewsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        news = News.objects.get(id=pk)
        serializer = NewSerializer(news)
        ip = get_client_ip(request)
        try:

            if not NewsView.objects.filter(news=news, ip_address=ip).exists():
                NewsView.objects.create(news=news, ip_address=ip)
                news.views += 1
        except HttpException as e:
            print(f"${str(e)}")   
        finally:
            news.save()
            return response.Response(serializer.data)           

class NewsChartView(views.APIView):
    def get(self,request,format=None):
        post_views = (NewsView.objects
                  .annotate(month=TruncMonth('created_at'))
                  .values('month')
                  .annotate(view_count=Count('id'))
                  .order_by('month'))

        data = {
            'months': [calendar.month_name[item['month'].month] for item in post_views],
            'view_counts': [item['view_count'] for item in post_views]
        }

        return response.Response(data)
               


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import calendar
# from .models import BlogPostView

# @api_view(['GET'])
# def blog_post_views_by_month_api(request):
#     # Aggregate view counts by month for all blog posts
#     post_views = (BlogPostView.objects
#                   .annotate(month=TruncMonth('timestamp'))
#                   .values('month')
#                   .annotate(view_count=Count('id'))
#                   .order_by('month'))

#     # Format data to return month names and counts
#     data = {
#         'months': [calendar.month_name[item['month'].month] for item in post_views],
#         'view_counts': [item['view_count'] for item in post_views]
#     }

#     return Response(data)

# from rest_framework.response import Response
# import calendar
# from .models import BlogPostView

# @api_view(['GET'])
# def blog_post_views_by_month_api(request, post_id):
#     post_views = (BlogPostView.objects.filter(post_id=post_id)
#                   .annotate(month=TruncMonth('timestamp'))
#                   .values('month')
#                   .annotate(view_count=Count('id'))
#                   .order_by('month'))

#     # Format data to return month names and counts
#     data = {
#         'months': [calendar.month_name[item['month'].month] for item in post_views],
#         'view_counts': [item['view_count'] for item in post_views]
#     }

#     return Response(data)
