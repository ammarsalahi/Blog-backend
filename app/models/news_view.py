from utils.general_model import GeneralModel
from django.db import models

class NewsView(GeneralModel):
    news = models.ForeignKey('app.News', related_name='news_views', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()  # Store the IP address
    viewed_at = models.DateTimeField(auto_now_add=True)  # When it was viewed

    class Meta:
        unique_together = ('news', 'ip_address') 


 