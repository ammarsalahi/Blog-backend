from utils.general_model import GeneralModel
from django.db import models
import os

docs=['docx','pdf','txt','html']
sounds=['mp3','wav']
movies=['mp4','mkv','mpeg']
zips=['zip','rar']
pictures=['png','gif','jpg','jpeg','bmp']

class FileBlog(GeneralModel):
    file=models.FileField(upload_to="news/files/")
    tag=models.CharField(max_length=100,null=True,blank=True)
    states= models.CharField(default="",max_length=100)
    filetype=models.CharField(null=True,blank=True,max_length=100)

    def save(self, *args, **kwargs):
        if self.file:
            _, extension = os.path.splitext(self.file.name)
            if extension[1:] in docs:
                self.filetype="docs"
            elif extension[1:] in sounds:
                self.filetype="sounds"
            elif extension[1:] in movies:
                self.filetype="movies"
            if extension[1:] in zips:
                self.filetype="zips"    
            if extension[1:] in pictures:
                self.filetype="pictures"     
            else:
                self.filetype="files"     
        super(FileBlog, self).save(*args, **kwargs)
    @property
    def name(self):
        return os.path.basename(self.file.name)
    @property
    def file_format(self):
        _, extension = os.path.splitext(self.file.name)
        return extension[1:]