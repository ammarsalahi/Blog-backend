from django.db import models
from utils.general_model import GeneralModel
from django.contrib.auth import get_user_model


class News(GeneralModel):
    
    title = models.CharField(
        max_length=1000,
    )

    description = models.TextField()

    images=models.ManyToManyField(
       'app.ImageBlog',
        related_name="link_news",
        blank=True,
    )
    files=models.ManyToManyField(
        'app.FileBlog',
        related_name="file_news",
        blank=True,
    )
    links=models.ManyToManyField(
        'app.LinkBlog',
        related_name="link_news",
        blank=True,
    )

    released_at = models.DateTimeField()

    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING
    )

    def __str__(self)->str:
        return self.title

    @property
    def total_size(self):
        total=0
        for fileojbect in self.files.all():
            if fileobject.file:
                total+=fileojbect.file.size 
        total_kb=total/1024
        total_mb=total_kb/1024
        total_gb=total_mb/1024
        return total_mb         
