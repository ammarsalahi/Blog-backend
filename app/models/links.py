from utils.general_model import GeneralModel
from django.db import models


class LinkBlog(GeneralModel):
    url=models.URLField(unique=True)
