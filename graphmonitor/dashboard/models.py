from django.db import models
from django.core.validators import RegexValidator, URLValidator
from encrypted_model_fields.fields import EncryptedCharField


# Create your models here.
class Switches(models.Model):
    name = models.CharField(max_length=255, default="Unknown")
    address = models.CharField(max_length=255, validators=[URLValidator])
    username = models.CharField(max_length=255)
    password = EncryptedCharField(max_length=255)
    

class Commands(models.Model):
    # Unit choices for easy parsing
    UNIT_CHOICES = [
        ('full', 'Auto (Full: bytes)'),
        ('short', 'Auto (Short: B)'),
        ('GB', 'Gigabytes'),
        ('Gb', 'Gigabits'),
        ('MB', 'Megabytes'),
        ('Mb', 'Megabits'),
        ('KB', 'Kilobytes'),
        ('Kb', 'Kilobits'),
        ('B', 'Bytes'),
        ('b', 'Bits'),
    ]

    # Protocol choices for expandability though I don't think its needed
    PROTOCOL_CHOICES = [
        ('ssh', "SSH"),
        ('telnet', 'Telnet'),
    ]

    # Priority Options to limit number of fallbacks to 5, lower priority is preferred
    PRIORITY_OPTIONS = [(i, i) for i in range(5)]

    switch = models.ForeignKey(Switches, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=10, choices=PROTOCOL_CHOICES)
    port = models.IntegerField()

    # Priority to allow fallback connections with differing protocols 
    priority = models.IntegerField(choices=PRIORITY_OPTIONS)
    query = models.CharField(max_length=255)
    query_unit = models.CharField(max_length=255, choices=UNIT_CHOICES)
    query_regex = models.CharField(max_length=255, validators=[RegexValidator])

    # blank=True on these as they are only needed when using telnet
    query_end = models.CharField(max_length=255, blank=True)
    login_prompt = models.CharField(max_length=255, blank=True)
    password_prompt = models.CharField(max_length=255, blank=True)

    class Meta():
        unique_together = ['switch', 'priority']


class Ports(models.Model):
    switch = models.ForeignKey(Switches, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Unknown')
    port = models.CharField(max_length=20) # Validate w/ query, ensure command is filled

    def __str__():
        return f"{name} ({port})"

    class Meta:
        unique_together = ['switch', 'port']


class DataPoints(models.Model):
    device = models.ForeignKey(Ports, on_delete=models.CASCADE)
    interval = models.DurationField()
    bytes = models.BigIntegerField() # IntegerField caps at ~287 MB
    datetime = models.DateTimeField(auto_now_add=True)