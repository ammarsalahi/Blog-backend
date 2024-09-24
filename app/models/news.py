from django.db import models
from utils.general_model import GeneralModel

class News(GeneralModel):
    
    title = models.CharField(
        max_length=1000,
    )
    
    description = models.TextField()

    images=models.ManyToManyField(
        null=True,
        blank=True
    )
    files=models.ManyToManyField(
        null=True,
        blank=True
    )
    links=models.ManyToManyField(
        blank=True,
        null=True
    )

    release_time = models.DateTimeField()

    def __str__(self)->str:
        return self.title

    #images
    #files
    #updated
    #created 
    #release time
    #links