from utils.general_model import GeneralModel
from django.db import models


class UrlBlog(GeneralModel):
    url=models.URLField()
