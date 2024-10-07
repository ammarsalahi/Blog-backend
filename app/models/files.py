from utils.general_model import GeneralModel
from django.db import models
import os

# docs=['docx','pdf','txt','html']
# sounds=['mp3','wav']
# movies=['mp4','mkv','mpeg']
# zips=['zip','rar']
# pictures=['png','gif','jpg','jpeg','bmp']

class FileBlog(GeneralModel):
    file=models.FileField(upload_to="news/files/")
    tag=models.CharField(max_length=100,null=True,blank=True)
    states= models.CharField(default="",max_length=100)
    filetype=models.CharField(null=True,blank=True,max_length=100)

    def save(self, *args, **kwargs):
        if self.filetype is None:
            self.filetype="Files"     
        super(FileBlog, self).save(*args, **kwargs)
    @property
    def name(self):
        return os.path.basename(self.file.name)
    @property
    def file_format(self):
        _, extension = os.path.splitext(self.file.name)
        return extension[1:]
    @property
    def filesize(self):
        size=self.file.size
        if size<=0:
            return f"{0}KB"
        else:
            total_kb=round(size/1024,0)
            total_mb=round(total_kb/1024,0)
            total_gb=round(total_mb/1024,0)

            if total_kb > 1000:
                return f"{total_mb} MB"
            elif total_mb > 1000:
                return f"{total_gb} GB"
            else:
                return f"{total_kb} KB"            
        