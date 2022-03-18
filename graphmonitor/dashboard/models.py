from django.db import models
from django.core.validators import RegexValidator
from encrypted_model_fields.fields import EncryptedCharField

from dashboard.validators import validate_domain_or_ipv4, validate_query, validate_regex_capture_groups, validate_regex_capture_detail


# Create your models here.
class Switches(models.Model):
    name = models.CharField(max_length=255, default="Unknown")
    interval = models.DurationField(help_text="How often to poll the switch for data.")
    autostart = models.BooleanField(default=True)
    address = models.CharField(max_length=255, unique=True, validators=[validate_domain_or_ipv4], help_text="The domain or IPv4 address of the switch.")
    username = models.CharField(max_length=255)
    password = EncryptedCharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.address})"
    

class Commands(models.Model):
    # Unit choices for easy parsing
    UNIT_CHOICES = [
        ('auto', 'Auto'),
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
        ('telnet', 'Telnet'),
        ('ssh', "SSH"),
    ]

    TRAFFIC_DIRECTION = [
        ('input', 'Input'),
        ('output', 'Output')
    ]

    # Priority Options to limit number of fallbacks to 5, lower priority is preferred
    PRIORITY_OPTIONS = [(i, i) for i in range(1, 6)]


    switch = models.ForeignKey(Switches, on_delete=models.CASCADE)
    protocol = models.CharField(max_length=10, choices=PROTOCOL_CHOICES, default='telnet')
    port = models.IntegerField(default=23, help_text="The port to connect on.")

    # Priority to allow fallback connections with differing protocols 
    priority = models.IntegerField(choices=PRIORITY_OPTIONS, default=1, help_text="The priority for fallback connections, lower is preferred.")
    query = models.CharField(max_length=255, validators=[validate_query], help_text="The command to pull info for a port.")
    query_regex = models.CharField(max_length=255, validators=[validate_regex_capture_groups, validate_regex_capture_detail], help_text="A regex capturing transfer size and unit info in capture groups as needed.")
    rate = models.BooleanField(help_text="Whether the data should be interpreted as a rate")
    query_interval = models.DurationField(help_text="The interval that the query covers.")

    # blank=True on these as they are only needed when using telnet
    bash_prompt = models.CharField(max_length=255, blank=True, help_text="The bash prompt displayed by a telnet connection.")
    login_prompt = models.CharField(max_length=255, blank=True, help_text="Unique charectors that match the login prompt, for telnet connections.")
    password_prompt = models.CharField(max_length=255, blank=True, help_text="Unique charectors that match the password prompt, for telnet connections.")

    def __str__(self):
        return f"{self.switch.name} {self.protocol} ({self.priority})"

    class Meta():
        unique_together = ['switch', 'priority']


class Devices(models.Model):
    switch = models.ForeignKey(Switches, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Unknown')
    port = models.CharField(max_length=20, help_text="The port as identified by the switch.") # Validate w/ query, ensure command is filled

    def __str__():
        return f"{name} ({port})"

    class Meta:
        unique_together = ['switch', 'port']


class DataPoints(models.Model):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE)
    interval = models.DurationField()
    input = models.BooleanField()
    bytes = models.BigIntegerField() # IntegerField caps at ~287 MB
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name}: {self.bytes / 1000.0} KB over {self.interval.total_seconds()} seconds"