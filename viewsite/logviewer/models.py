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

    def get_latest_log(self):
        """Get latest log either critical or warning where not resolved."""
        severity = ["Critical", "Warning", "Info"]

        for bool in [False, True]:
            for sev in severity:
                logs = Log.objects.filter(asset=self.pk, severity=sev, resolved=bool)
                if logs.exists():
                    log = logs.latest()
                    return log.id

        return -1

    def get_latest_severity(self):
        logid = self.get_latest_log()
        if logid == -1:
            return "-"
        else:
            log = Log.objects.filter(id=logid).latest()
            return log.severity


class Log(models.Model):
    """Log provides the model for logs."""

    """TODO: Update below to 'Enumeration Types'.
    https://docs.djangoproject.com/en/4.0/ref/models/fields/
    """
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
        ("Critical", "Critical"),
        ("Warning", "Warning"),
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
    resolved = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        out = str(self.seqnumber) + ": " + self.severity + " - " + self.message
        return out

    def is_resolved(self):
        return self.resolved
