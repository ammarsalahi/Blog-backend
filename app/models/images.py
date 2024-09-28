from utils.general_model import GeneralModel
from django.db import models


class ImageBlog(GeneralModel):
    image=models.ImageField(upload_to="news/images/")
    tag=models.CharField(max_length=100,blank=True,null=True)
    target=models.IntegerField(default=0)