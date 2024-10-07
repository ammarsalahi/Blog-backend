from rest_framework import serializers
from app.models import *




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageBlog
        fields="__all__"        


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=LinkBlog
        fields="__all__"        

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileBlog
        fields="__all__" 
    def to_representation(self, instance):
        data = super(FileSerializer, self).to_representation(instance)     
        data['filename']=instance.name      
        data['fileformat']=instance.file_format   
        data['filesize']=instance.filesize
        return data
                
class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Timer
        fields="__all__"          

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model=News
        fields="__all__"

    def to_representation(self, instance):
        data = super(NewSerializer, self).to_representation(instance)   
        # many-to-many data
        data['images'] = ImageSerializer(instance=instance.images.all(),many=True).data
        data['links'] = LinkSerializer(instance=instance.links.all(),many=True).data
        data['files'] = FileSerializer(instance=instance.files.all(),many=True).data
        # counts
        data['images_count']= instance.images.count()
        data['links_count'] = instance.links.count()
        data['files_count'] = instance.files.count()

        #size
        data['total_size']=instance.total_size

        #publish data
        data['days'] = instance.duration_days
        data['hours'] = instance.duration_hours
        data['minutes'] = instance.duration_minutes
        data['is_published'] = instance.is_published_now
        data['last_duration']=instance.duration_last_time


        
        return data 

class NewsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsView
        fields="__all__"  

