from utils.general_model import GeneralModel
from django.db import models


class LinkBlog(GeneralModel):
    text=models.CharField(
        max_length=300,
        blank=True
    )
    href=models.URLField(blank=True)
