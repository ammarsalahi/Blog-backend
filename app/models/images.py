from utils.general_model import GeneralModel
from django.db import models


class ImageBlog(GeneralModel):
    image=models.ImageField(upload_to="news/images/")