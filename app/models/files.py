from utils.general_model import GeneralModel
from django.db import models


class FileBlog(GeneralModel):
    file=models.FileField(upload_to="news/files/")
    tag=models.CharField(max_length=100,null=True,blank=True)
    target=models.IntegerField(default=0)