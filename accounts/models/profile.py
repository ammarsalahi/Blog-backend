from utils.general_model import GeneralModel
from django.db import models

class Profile(GeneralModel):
    user=models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )
    otp_code=models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    def __str__(self)->str:
        return self.otp_code