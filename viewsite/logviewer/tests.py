from datetime import datetime
from django.utils import timezone, dateformat
from logging import critical
from django.test import TestCase
from .models import Asset, Log

# Create your tests here.


class LogModelTests(TestCase):
    def setUp(self):
        Asset.objects.create(name="tot-n01",
                             IP="10.49.28.147", type="SVR", site="TOT", phase=1)
        Asset.objects.create(name="tot-n02",
                             IP="10.49.28.148", type="SVR", site="TOT", phase=1)
        Asset.objects.create(name="psc-n01",
                             IP="10.41.28.146", type="SVR", site="PSC", phase=1)
        Asset.objects.create(name="psc-n02",
                             IP="10.41.28.147", type="SVR", site="PSC", phase=1)

    def test_log_string_output(self):
        """
        log string output should display timestamp, seqno, severity, message.
        """
        pk = 1
        severity = "critical"
        seqnumber = 1
        timestamp = timezone.now()
        formatted_timestamp = dateformat.format(timestamp, 'Y-m-d H:m')
        message = "Critical message"
        out = str(formatted_timestamp) + ": " + str(seqnumber) + \
            " - " + severity + " - " + message
        asset = Asset.objects.get(pk=pk)
        asset.log_set.create(
            seqnumber=seqnumber, timestamp=timestamp, severity=severity,
            message=message)
        asset.save()

        log_str = str(Log.objects.filter(asset=pk).latest())

        self.assertEqual(log_str, out)
