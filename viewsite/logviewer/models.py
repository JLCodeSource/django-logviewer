from django.contrib import admin
from django.db import models
from django.db.models.fields import IPAddressField
from django.utils import timezone, dateformat

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
    PHASES = (
        (1, "Phase 1"),
        (2, "Phase 2"),
    )
    name = models.CharField(max_length=30)
    IP = models.GenericIPAddressField()
    type = models.CharField(max_length=8, choices=TYPES)
    site = models.CharField(max_length=10, choices=SITES)
    phase = models.SmallIntegerField(choices=PHASES)

    def __str__(self):
        return self.name

    @admin.display(description="log")
    def get_latest_log(self):
        """Get latest log either critical or warning where not resolved."""
        severity = ["Critical", "Warning"]

        for bool in [False, True]:
            for sev in severity:
                logs = Log.objects.filter(
                    asset=self,
                    severity=sev,
                    resolved=bool,
                )
                if logs.exists():
                    log = logs.latest()
                    return log.id
        for bool in [False, True]:
            logs = Log.objects.filter(
                asset=self,
                severity="Info",
                resolved=bool,
            )
            if logs.exists():
                log = logs.latest()
                return log.id
        return -1

    @admin.display(description="severity", ordering="severity")
    def get_latest_severity(self):
        logid = self.get_latest_log()
        if logid == -1:
            return "-"
        else:
            log = Log.objects.filter(id=logid).latest()
            return log.severity

    @admin.display(description="timestamp")
    def get_latest_timestamp(self):
        logid = self.get_latest_log()
        if logid == -1:
            return "-"
        else:
            log = Log.objects.filter(id=logid).latest()
            return log.timestamp

    @admin.display(description="message")
    def get_latest_message(self):
        logid = self.get_latest_log()
        if logid == -1:
            return "-"
        else:
            log = Log.objects.filter(id=logid).latest()
            return log.message


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
    seqnumber = models.PositiveSmallIntegerField(null=True, blank=True)
    message_id = models.CharField(max_length=6, blank=True)
    agent_id = models.CharField(max_length=14, choices=AGENTS, blank=True)
    category = models.CharField(max_length=9, choices=CATEGORIES, blank=True)
    severity = models.CharField(max_length=8, choices=SEVERITY, blank=True)
    timestamp = models.DateTimeField(blank=True)
    message = models.CharField(max_length=255, blank=True)
    raw_data = models.CharField(max_length=255, blank=True)
    fqdd = models.CharField(max_length=255, blank=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self):
        timestamp = self.timestamp
        formatted_timestamp = dateformat.format(timestamp, "Y-M-d H:i:s")
        out = (
            formatted_timestamp
            + ": Id:"
            + str(self.id)
            + " Seq:"
            + str(self.seqnumber)
            + " "
            + self.severity
            + " - "
            + self.message
        )
        return out

    def is_resolved(self):
        return self.resolved
