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
    AGENTS = (
        ("UEFI_SS_USC", "UEFI_SS_USC"),
        ("CusOsUp", "CusOsUp"),
        ("UEFI_Inventory", "UEFI_Inv"),
        ("iDRAC", "iDRAC"),
        ("UEFI_DCS", "UEFI_DCS"),
        ("SEL", "SEL"),
        ("RACLOG", "RACLOG"),
        ("DE", "DE"),
        ("WSMAN", "WSMAN"),
        ("RACADM", "RACADM"),
        ("iDRAC_GUI", "iDRAC_GUI"),
        ("CMC", "CMC"),
    )
    CATEGORIES = (
        ("System", "System"),
        ("Storage", "Storage"),
        ("Worknotes", "Worknotes"),
        ("Config", "Config"),
        ("Updates", "Updates"),
        ("Audit", "Audit"),
    )
    SEVERITY = (
        ("Warning", "Warning"),
        ("Critical", "Critical"),
        ("Info", "Info"),
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    seqnumber = models.PositiveSmallIntegerField()
    message_id = models.CharField(max_length=6)
    agent_id = models.CharField(max_length=14, choices=AGENTS)
    category = models.CharField(max_length=9, choices=CATEGORIES)
    severity = models.CharField(max_length=8, choices=SEVERITY)
    timestamp = models.DateTimeField()
    message = models.CharField(max_length=255)
    raw_data = models.CharField(max_length=255)
    fqdd = models.CharField(max_length=255)

    def __str__(self):
        return str(self.seqnumber)
