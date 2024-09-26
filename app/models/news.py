from django.db import models
from utils.general_model import GeneralModel
from django.contrib.auth import get_user_model
from datetime import datetime,timedelta

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
  
    links=models.ManyToManyField(
        'app.LinkBlog',
        related_name="link_news",
        blank=True,
    )
    is_timer_enabled = models.BooleanField(
        default=False
    )
    # released_at = models.DateTimeField()
    timer_duration = models.IntegerField(
        default=0
    )

    publish_date=models.DateTimeField(
        blank=True
    )


    creator = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING
    )
    types=models.CharField(
        max_length=100,
        default="center"
    )
    
    def save(self, *args, **kwargs):

        if self.publish_date is None:
            self.publish_date = datetime.now() + timedelta(days=duration_days,hours=duration_hours,minutes=duration_minutes)
            
        super().save(*args, **kwargs)
        
    def __str__(self)->str:
        return self.title

    @property
    def get_full_next(self)->str:
        return f"{next_days}days's {next_hours}hour's and {next_minutes}minutes"

    # @property 
    # def time_duration(self):
    #     full_time = (self.next_hours*3600) + (self.next_minutes*60)
    #     return full_time
    @property
    def total_size(self):
        total=0
        for img in self.images.all():
            if img.image:
                total+=img.image.size 
        total_kb=round(total/1024,2)
        total_mb=round(total_kb/1024)
        total_gb=round(total_mb/1024)
        if total_kb > 1000:
            return f"{total_mb} MB"
        elif total_mb > 1000:
            return f"{total_gb} GB"
        else:
            return f"{total_kb} KB"

    @property
    def duration_days(self):
        if self.is_timer_enabled:
            return self.timer_duration // 86400
        return 0    

    @property
    def duration_hours(self):
        if self.is_timer_enabled:
            remaining = self.timer_duration // 86400
            minutes = remaining //3600
        return 0

    @property
    def duration_minutes(self):
        if self.is_timer_enabled:
            remaining = self.timer_duration // 3600
            minutes = remaining //3600
        return 0

    @property
    def is_published_now(self):    
        now_date= datetime.now()
        if now_date > self.publish_date:
            return True
        else:
            return False    

        
