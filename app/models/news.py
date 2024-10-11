from django.db import models
from utils.general_model import GeneralModel
from django.utils import timezone  # Use timezone-aware datetime
from datetime import timedelta

class News(GeneralModel):
    
    title = models.CharField(
        max_length=1000,
    )

    description = models.TextField()

    images=models.ManyToManyField(
       'app.ImageBlog',
        related_name="image_news",
        blank=True,
    )
  
    links=models.ManyToManyField(
        'app.LinkBlog',
        related_name="link_news",
        blank=True,
    )

    files=models.ManyToManyField(
       'app.FileBlog',
        related_name="file_news",
        blank=True,
    )

    is_timer_enabled = models.BooleanField(
        default=False
    )
    


    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    types=models.CharField(
        max_length=100,
        default="center"
    )
    views=models.IntegerField(
        default=0
    )

    timer=models.ForeignKey(
        'app.Timer',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )  
    is_files_in_times = models.BooleanField(
        default=False
    )
    def __str__(self)->str:
        return self.title

    @property
    def get_full_next(self)->str:
        return f"{next_days}days's {next_hours}hour's and {next_minutes}minutes"

    
    @property
    def total_size(self):
        total=0
        for f in self.files.all():
            if f.file:
                total+=f.file.size 
        total_kb=round(total/1024,0)
        total_mb=round(total_kb/1024,0)
        total_gb=round(total_mb/1024,0)

        if total_kb > 1000:
            return f"{total_mb} MB"
        elif total_mb > 1000:
            return f"{total_gb} GB"
        else:
            return f"{total_kb} KB"
    
    @property
    def duration_days(self):
        if self.timer:
            return self.timer.get_days()
        return 0    

    @property
    def duration_hours(self):
        if self.timer:
            return self.timer.get_hours()
        return 0

    @property
    def duration_minutes(self):
        if self.is_timer_enabled:
            if self.timer:
                return self.timer.get_minutes()
        return 0

    @property
    def is_published_now(self):    
        now_date = timezone.now() 
        if self.timer:
            if self.timer.publish_date is not None:
                if now_date > self.timer.publish_date:
                    return True
                else:
                    return False    
            return False
        return True    
            
    @property
    def duration_last_time(self):
        now_date=timezone.now()
        if self.timer:
            if self.timer.publish_date > now_date:
                result= self.timer.publish_date - now_date
                return round(result.total_seconds())
            return 0   
        return 0         



