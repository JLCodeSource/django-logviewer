from django.utils import timezone, dateformat
from django.test import TestCase
from django.contrib.auth.models import User
from logviewer.models import Asset, Log
from django.urls import reverse
from rest_framework import status
from rest_framework import request
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
import json
import pytest

# Create your tests here.


class AssetModelTests(TestCase):
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

    def test_asset_string_output(self):
        """
        asset string output should display asset name.
        """
        asset = Asset.objects.get(pk=1)
        self.assertEqual(str(asset), "tot-n01")

    def test_log_string_output(self):
        """
        log string output should display timestamp, seqno, severity, message.
        """
        pk = 1
        severity = "Critical"
        seqnumber = 1
        timestamp = timezone.now()
        formatted_timestamp = dateformat.format(timestamp, "Y-M-d H:i:s")
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
            + ": Id:"
            + str(id)
            + " Seq:"
            + str(seqnumber)
            + " "
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
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity="Critical",
            message=message,
            resolved=True,
        )
        resolved_log.save()
        id = log.id

        self.assertEqual(asset.get_latest_log(), id)

    def test_log_get_latest_resolved_warning_with_unresolved_info_log(self):
        """
        get_latest_log should return the id of the latest unresolved Warning
        severity log, even if there are unresolved Information severity logs.
        """
        pk = 1
        severity = "Warning"
        seqnumber = 1
        timestamp = timezone.now()
        message = "Information message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity=severity,
            message=message,
            resolved=True,
        )
        log.save()
        timestamp = timezone.now()
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            timestamp=timestamp,
            severity="Info",
            message=message,
        )
        resolved_log.save()
        id = log.id

        self.assertEqual(asset.get_latest_log(), id)


class AssetTestCase(APITestCase):
    def setUp(self):
        asset = Asset.objects.create(
            name="tot-n01",
            IP="10.49.28.147",
            type="SVR",
            site="TOT",
            phase=1,
        )
        Log.objects.create(
            asset=asset,
            seqnumber=1,
            timestamp=timezone.now(),
            severity="Info",
            message="information message",
        )
        User.objects.create_user("admin", "admin@admin.com", "admin")

    def test_get_logs(self):
        client = APIClient()
        test_url = "http://127.0.0.1:8000/logviewer/logs/"
        response = client.get(test_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_log(self):
        client = APIClient()
        user = User.objects.get(username="admin")
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        client.force_authenticate(user=user)
        test_url = reverse("log-list")
        pk = 1
        severity = "Warning"
        timestamp = timezone.now()
        message = "Warning message"

        response = client.post(
            test_url,
            data={
                "asset": pk,
                "seqnumber": 1,
                "timestamp": str(timestamp),
                "severity": severity,
                "message": message,
            },
            user=user,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_logs(self):
        client = APIClient()
        user = User.objects.get(username="admin")
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        client.force_authenticate(user=user)
        test_url = reverse("log-list")
        pk = 1
        severity = "Warning"
        timestamp = timezone.now()
        message = "Warning message"

        for i in range(1000):
            # test auto setting sequence
            response = client.post(
                test_url,
                data={
                    "asset": pk,
                    "seqnumber": i,
                    "timestamp": str(timestamp),
                    "severity": severity,
                    "message": message,
                },
                user=user,
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
