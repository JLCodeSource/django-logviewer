""" from logviewer.models import (
    Asset,
    Log,
) """
from email.headerregistry import MessageIDHeader
import requests, json, sys, re, time, os, warnings, argparse
from datetime import datetime


def get_lc_logs(ip, username, password):
    """
    Given an asset
    when the admin checks the logs
    then the service populates the database
    and an entry is added to the system log
    """
    response = requests.get(
        "http://%s/redfish/v1/Systems/437XR1138R2/LogServices/Log1/Entries" % ip
    )
    data = response.content
    data = json.loads(data)
    num_logs = get_lc_log_number(data)
    print("Number of logs: %s" % num_logs)
    for i in data["Members"]:
        log = get_lc_log(i)
        print(log)


def get_lc_log_number(data):
    return data["Members@odata.count"]


def get_lc_log(log):
    odata_id = log["@odata.id"]
    name = log["Name"]
    seqnumber = log["Id"]
    messageid = log["MessageID"]
    message = log["Message"]
    created = log["Created"]
    severity = log["Severity"]
    log = {
        "odata_id": odata_id,
        "name": name,
        "seqnumber": seqnumber,
        "messageid": messageid,
        "message": message,
        "created": created,
        "severity": severity,
    }
    return json.dumps(log)


get_lc_logs("127.0.0.1:5000", "", "")
