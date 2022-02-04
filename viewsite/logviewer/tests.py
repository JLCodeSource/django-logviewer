import io
from django.utils import timezone, dateformat
from django.test import TestCase
from django.contrib.auth.models import User
from logviewer.models import Asset, Log
from logviewer.services import get_lc_log_number, get_lc_logs
from django.urls import reverse
from rest_framework import status
from rest_framework import request
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.parsers import JSONParser
import json
import pytest
import requests

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
        created = timezone.now()
        message = "Critical message"
        formatted_created = dateformat.format(created, "Y-M-d H:i:s")
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
            severity=severity,
            message=message,
        )
        log.save()
        id = log.id

        out = (
            str(formatted_created)
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
        created = timezone.now()
        message = "Critical message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
            severity=severity,
            message=message,
        )
        log.save()

        seqnumber = 2
        created = timezone.now()
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
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
        created = timezone.now()
        message = "Critical message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
            severity=severity,
            message=message,
        )
        log.save()
        created = timezone.now()
        resolved = True
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
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
        created = timezone.now()
        message = "Warning message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
            severity=severity,
            message=message,
        )
        log.save()
        created = timezone.now()
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
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
        created = timezone.now()
        message = "Information message"
        asset = Asset.objects.get(pk=pk)
        log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
            severity=severity,
            message=message,
            resolved=True,
        )
        log.save()
        created = timezone.now()
        resolved_log = Log.objects.create(
            asset=asset,
            seqnumber=seqnumber,
            created=created,
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
            created=timezone.now(),
            severity="Info",
            message="information message",
        )
        User.objects.create_user("admin", "admin@admin.com", "admin")

    def test_get_logs(self):
        client = APIClient()
        test_url = reverse("log-list")
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
        created = timezone.now()
        message = "Warning message"

        response = client.post(
            test_url,
            data={
                "asset": pk,
                "seqnumber": 1,
                "created": str(created),
                "severity": severity,
                "message": message,
            },
            user=user,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_2_logs(self):
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
        message = "Warning message"
        created = timezone.now()

        data = [
            {
                "asset": pk,
                "seqnumber": 1,
                "created": str(created),
                "severity": severity,
                "message": message,
            }
            for i in range(2)
        ]

        # test auto setting sequence
        response = client.post(
            test_url,
            data=data,
            user=user,
            format="json",
        )

        out = Log.objects.filter(
            asset=pk,
            seqnumber=1,
            created=created,
            severity=severity,
            message=message,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(out), len(data))

    def test_create_many_logs(self):
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
        message = "Warning message"
        test_size = 1000

        data = [
            {
                "asset": pk,
                "seqnumber": i,
                "created": str(timezone.now()),
                "severity": severity,
                "message": message,
            }
            for i in range(test_size)
        ]

        # test auto setting sequence
        response = client.post(
            test_url,
            data=data,
            user=user,
            format="json",
        )

        out = Log.objects.filter(
            asset=pk,
            severity=severity,
            message=message,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(out), len(data))


class ServicesTestCase(APITestCase):
    def setUp(self):
        Asset.objects.create(
            name="redfish",
            IP="127.0.0.1",
            port="5000",
            type="TST",
            site="TOT",
            phase=1,
        )
        User.objects.create_user("admin", "admin@admin.com", "admin")

    def test_services_get_lc_log_number(self):
        data = {
            "Members@odata.count": 2,
            "Name": "Log Service Collection",
        }
        logs = get_lc_log_number(data)
        self.assertEqual(logs, 2)

    def test_services_get_lc_logs(self):
        client = APIClient()
        user = User.objects.get(username="admin")
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        client.force_authenticate(user=user)

        asset = Asset.objects.get(name="redfish")
        logs = get_lc_logs(asset)

        test_url = reverse("log-list")
        headers = {"Content-type": "application/json"}

        response = client.post(
            test_url,
            data=logs,
            user=user,
            headers=headers,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_services_get_lc_logs_ignore_existing(self):
        client = APIClient()
        user = User.objects.get(username="admin")
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        client.force_authenticate(user=user)

        asset = Asset.objects.get(name="redfish")
        logs = get_lc_logs(asset)
        max_log = 0
        for log in logs:
            m = max(log["seqnumber"])
            m = int(m)
            if m > max_log:
                max_log = m

        test_url = reverse("log-list")
        headers = {"Content-type": "application/json"}

        response = client.post(
            test_url,
            data=logs,
            user=user,
            headers=headers,
            format="json",
        )

        latest_log = Log.objects.filter(asset=asset, seqnumber=max_log)
        if latest_log.exists:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        else:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
