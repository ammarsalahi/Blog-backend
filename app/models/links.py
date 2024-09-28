from utils.general_model import GeneralModel
from django.db import models


class LinkBlog(GeneralModel):
    href=models.URLField(blank=True)
    tag=models.CharField(max_length=100,null=True,blank=True)
    states= models.CharField(default="",max_length=100)
