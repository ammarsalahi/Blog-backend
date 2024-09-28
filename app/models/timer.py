from utils.general_model import GeneralModel
from django.db import models
from django.utils import timezone # Use timezone-aware datetime
from datetime import timedelta


class Timer(GeneralModel):

    days=models.IntegerField(default=0)
    hours=models.IntegerField(default=0)
    minutes=models.IntegerField(default=0)
    timer_duration = models.IntegerField(default=0)
    publish_date = models.DateTimeField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.publish_date is None:
            self.publish_date = timezone.now() + timedelta(
                days=self.days,
                hours=self.hours,
                minutes=self.minutes
            )
        super().save(*args, **kwargs)


