from django.db import models
from django.db.models.fields import IPAddressField

# Create your models here.


class Asset(models.Model):
    TYPES = (
        ("SVR", "Server"),
        ("STR", "Storage"),
        ("SWT", "Switch"),
    )
    SITES = (
        ("TOT", "Totowa"),
        ("PSC", "Piscataway"),
    )
    name = models.CharField(max_length=30)
    IP = models.GenericIPAddressField()
    type = models.CharField(max_length=8, choices=TYPES)
    site = models.CharField(max_length=10, choices=SITES)

    def __str__(self):
        return self.name


class Log(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    seqnumber = models.IntegerField()
    message_id = models.CharField(max_length=6)
    category = models.CharField(max_length=10)
    severity = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    message = models.CharField(max_length=255)
    raw_data = models.CharField(max_length=255)
    fqdd = models.CharField(max_length=255)

    def __str__(self):
        return self.asset
