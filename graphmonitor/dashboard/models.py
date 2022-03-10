from django.db import models
from encrypted_model_fields import EncryptedCharField


# Create your models here.
class Devices(models.Model):
    name = models.CharField(max_length=255, default='Unknown')
    port = models.CharField(max_length=20, unique=True)

    def __str__():
        return f"{name} ({port})"


class DataPoints(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    interval = models.DurationField()
    bytes = models.BigIntegerField()


class Switches(models.Model):
    address = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = EncryptedCharField(max_length=255)
