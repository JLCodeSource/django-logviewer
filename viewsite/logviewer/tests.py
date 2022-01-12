from django.utils import timezone, dateformat
from django.test import TestCase
from .models import Asset, Log

# Create your tests here.


class LogModelTests(TestCase):
    def setUp(self):
        Asset.objects.create(
            name="tot-n01",
            IP="10.49.28.147",
            type="SVR",
            site="TOT",
            phase=1,
        )
        Asset.objects.create(
            name="tot-n02",
            IP="10.49.28.148",
            type="SVR",
            site="TOT",
            phase=1,
        )
        Asset.objects.create(
            name="psc-n01",
            IP="10.41.28.146",
            type="SVR",
            site="PSC",
            phase=1,
        )
        Asset.objects.create(
            name="psc-n02",
            IP="10.41.28.147",
            type="SVR",
            site="PSC",
            phase=1,
        )

    def test_log_string_output(self):
        """
        log string output should display timestamp, seqno, severity, message.
        """
        pk = 1
        severity = "Critical"
        seqnumber = 1
        timestamp = timezone.now()
        formatted_timestamp = dateformat.format(timestamp, "Y-m-d H:m")
        message = "Critical message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
        )
        log.save()
        id = log.id

        out = (
            str(formatted_timestamp)
            + ": "
            + str(id)
            + "-"
            + str(seqnumber)
            + " - "
            + severity
            + " - "
            + message
        )

        log_str = str(Log.objects.filter(asset=asset).latest())

        self.assertEqual(log_str, out)

    def test_log_get_latest_critical_log(self):
        """
        get_latest_log should return the id of latest critical severity log.
        """
        pk = 1
        severity = "Critical"
        seqnumber = 1
        timestamp = timezone.now()
        message = "Critical message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
        )
        log.save()

        seqnumber = 2
        timestamp = timezone.now()
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
        )
        log.save()
        id = log.id

        self.assertEqual(asset.get_latest_log(), id)

    def test_log_get_latest_critical_unresolved_log(self):
        """
        get_latest_log should return id of latest unresolved critical sev log.
        """
        pk = 1
        severity = "Critical"
        seqnumber = 1
        timestamp = timezone.now()
        message = "Critical message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
        )
        log.save()
        timestamp = timezone.now()
        resolved = True
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
            resolved=resolved,
        )
        resolved_log.save()
        id = log.id

        self.assertEqual(asset.get_latest_log(), id)

    def test_log_get_latest_warning_unresolved_log(self):
        """
        get_latest_log should return the id of the latest unresolved Warning
        severity log, even if there are resolved Critical severity logs.
        """
        pk = 1
        severity = "Warning"
        seqnumber = 1
        timestamp = timezone.now()
        message = "Warning message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
        )
        log.save()
        timestamp = timezone.now()
        resolved = True
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity="Critical",
            message=message,
            resolved=resolved,
        )
        resolved_log.save()
        id = log.id

        self.assertEqual(asset.get_latest_log(), id)
