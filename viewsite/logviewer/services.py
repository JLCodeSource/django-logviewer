from logviewer.models import (
    Asset,
)
import requests, json, sys, re, time, os, warnings, argparse
from datetime import datetime


def get_lc_logs(asset):
    """
    Given an asset
    when the admin checks the logs
    then the service populates the database
    and an entry is added to the system log
    """
    ip = asset.IP
    port = asset.port
    type = asset.type
    if type == "TST":
        logtarget = "redfish/v1/Systems/437XR1138R2/LogServices/Log1/Entries"
    elif type == "SVR":
        logtarget = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Lclog/Entries"
    response = requests.get("http://%s:%s/%s" % (ip, port, logtarget))
    data = json.loads(response.content)
    logs = []
    for i in data["Members"]:
        log = get_lc_log(i)
        logs.append(log)
    return logs


def get_lc_log_number(data):
    return data["Members@odata.count"]


def get_lc_log(log):
    odata_id = log["@odata.id"]
    name = log["Name"]
    seqnumber = log["Id"]
    message_id = log["MessageID"]
    message = log["Message"]
    created = log["Created"]
    severity = log["Severity"]
    log = {
        "asset": 1,
        "odata_id": odata_id,
        "name": name,
        "seqnumber": seqnumber,
        "message_id": message_id,
        "message": message,
        "created": created,
        "severity": severity,
    }
    return log
