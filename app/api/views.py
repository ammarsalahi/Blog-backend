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
from rest_framework.filters import SearchFilter



User=get_user_model()
class NewsModelset(viewsets.ModelViewSet):
    queryset=News.objects.all()
    serializer_class=NewSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for img in instance.images.all():
            img.delete()
        for link in instance.links.all():
            link.delete()
        for file in instance.files.all():
            file.delete()        
        instance.delete()


class TimerModelset(viewsets.ModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

class ImageViewset(viewsets.ModelViewSet):
    queryset = ImageBlog.objects.all() 
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]
    search_fields = ['tag']

class LinkViewset(viewsets.ModelViewSet):
    queryset = LinkBlog.objects.all()
    serializer_class = LinkSerializer
    filter_backends = [SearchFilter]
    search_fields = ['tag']

class FileViewset(viewsets.ModelViewSet):
    queryset = FileBlog.objects.all()
    serializer_class = FileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['tag']
        

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
        is_file_show = request.data.get('is_file_show') == 'true'
        timer_duration = int(request.data.get('timer_duration', 0))
        days=int(request.data.get('days',0))
        hours=int(request.data.get('hours',0))
        minutes=int(request.data.get('minutes',0))
        uid = request.data.get('uid')
        user = request.user  # Assumes authentication is in place
        news = News.objects.create(
            title=title,
            description=content,
            is_timer_enabled=is_timer_enabled,
            creator=user,
        )
        if is_timer_enabled:
            news.timer=Timer.objects.create(
                    timer_duration=timer_duration,
                    days=days,
                    hours=hours,
                    minutes=minutes,
                    is_files_in_times=is_file_show
            )

               
        news.images.set(ImageBlog.objects.filter(tag=uid))
        news.links.set(LinkBlog.objects.filter(tag=uid))
        news.files.set(FileBlog.objects.filter(tag=uid))
        for img in news.images.all():
            img.tag=f"{news.id}-{news.title}"
            img.save()

        for file in news.files.all():
            file.tag=f"{news.id}-{news.title}"
            file.save()   

        for link in news.links.all():
            link.tag=f"{news.id}-{news.title}"
            link.save() 
        # images=ImageBlog.objects.filter(target=)
        news.save()

        return response.Response({"message": "News post created successfully"}, status=status.HTTP_201_CREATED)    


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class NewsUpdateView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # For handling file uploads

    def patch(self, request,pk, *args, **kwargs):
        print(request.data)
        title = request.data.get('title')
        content = request.data.get('description')
        is_timer_enabled = request.data.get('is_timer_enabled') == 'true'
        is_file_show = request.data.get('is_file_show') == 'true'
        timer_duration = int(request.data.get('timer_duration', 0))
        days=int(request.data.get('days',0))
        hours=int(request.data.get('hours',0))
        minutes=int(request.data.get('minutes',0))
        uid = request.data.get('uid')
        user = request.user 

        try:
            news=News.objects.get(pk=pk)
            news.title=title
            news.description=content
            news.is_timer_enabled=is_timer_enabled
            news.is_files_in_times=is_file_show
            
            news.timer=Timer.objects.create(
                timer_duration=timer_duration,
                days=days,
                hours=hours,
                minutes=minutes
            )
           
            for img in ImageBlog.objects.filter(tag=uid):
                news.images.add(img)    

            for file in FileBlog.objects.filter(tag=uid):
                news.files.add(file)  

            for link in LinkBlog.objects.filter(tag=uid):
                news.links.add(link)
            news.save()
            return response.Response(status=status.HTTP_200_OK)
        except News.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

       



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
               

class DownloadFileView(views.APIView):
    def get(self,request,pk,format=None):
        try:
            news=News.objects.get(id=pk)
            return response.Response(
                data=NewSerializer(instance=news).data
            )
        except News.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)    

class DeleteOneFile(views.APIView):
    def get(self,request,tag,format=None):
        try:
            files=FileBlog.objects.filter(tag=tag)
            for f in files:
                f.delete()
            return response.Response(status=status.HTTP_200_OK)    
        except FileBlog.DoesNotExist:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
