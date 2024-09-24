from utils.general_model import GeneralModel
from django.db import models


class FileBlog(GeneralModel):
    file=models.FileField()