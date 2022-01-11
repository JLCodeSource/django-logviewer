from datetime import datetime
from django.utils import timezone
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

    def test_get_latest_log_priorities(self):
        """
        get_latest should return latest log by severity & not resolved.
        """
        asset = Asset.objects.get(pk=1)
        # asset.log_set.create(severity="critical",
        #                     seqnumber="1", timestamp=timezone.now())
        # asset.save()

        self.assertIs(asset.get_latest_log(), -1)
