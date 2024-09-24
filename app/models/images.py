from utils.general_model import GeneralModel
from django.db import models


class Imagelog(GeneralModel):
    image=models.ImageField()