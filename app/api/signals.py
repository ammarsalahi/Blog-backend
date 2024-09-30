# signals.py
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from app.models import *

@receiver(post_delete, sender=ImageBlog)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        # Get the full path of the image
        image_path = os.path.join(settings.MEDIA_ROOT, instance.image.path)
        
        try:
            if os.path.isfile(image_path):
                os.remove(image_path)
        except Exception as e:
            print(f"{str(e)}")        

@receiver(post_delete, sender=FileBlog)
def delete_text_file(sender, instance, **kwargs):
    if instance.file:
        # Get the full path of the image
        file_path = os.path.join(settings.MEDIA_ROOT, instance.file.path)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        # instance.image.delete(save=False)        
        except Exception as e:
            print(f"{str(e)}")  
