from utils.general_model import GeneralModel
from django.db import models
import os

class FileBlog(GeneralModel):
    file=models.FileField(upload_to="news/files/")
    tag=models.CharField(max_length=100,null=True,blank=True)
    states= models.CharField(default="",max_length=100)

    @property
    def name(self):
        return os.path.basename(self.file.name)
    @property
    def file_format(self):
        _, extension = os.path.splitext(self.file.name)
        return extension[1:]