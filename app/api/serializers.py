from rest_framework import serializers
from app.models import *




class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ImageBlog
        fields="__all__"        


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileBlog
        fields="__all__"  


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=LinkBlog
        fields="__all__"        
        

class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model=News
        fields="__all__"

    def to_representation(self, instance):
        data = super(PostSerializer, self).to_representation(instance)   
        data['images'] = ImageSerializer(instance=instance.images.all(),many=True).data
        data['links'] = LinkSerializer(instance=instance.links.all(),many=True).data
        data['files'] = FileSerializer(instance=instance.files.all(),many=True).data
        return data 
