""" from logviewer.models import (
    Asset,
    Log,
) """
import requests, json, sys, re, time, os, warnings, argparse
from datetime import datetime


def get_lc_logs(ip, username, password):
    """
    Given an asset
    when the admin checks the logs
    then the service populates the database
    and an entry is added to the system log
    """
    d = datetime.now()
    current_date_time = "- Data collection timestamp: %s-%s-%s %s:%s:%s\n" % (
        d.year,
        d.month,
        d.day,
        d.hour,
        d.minute,
        d.second,
    )
    print(current_date_time)
    response = requests.get(
        "http://%s/redfish/v1/Systems/437XR1138R2/LogServices/Log1/Entries" % ip
    )
    data = response.content
    data = json.loads(data)
    print(data["Members@odata.count"])
    for i in data["Members"]:
        for j in i.items():
            log = "%s: %s" % (j[0], j[1])
            print(log)


get_lc_logs("127.0.0.1:5000", "", "")
