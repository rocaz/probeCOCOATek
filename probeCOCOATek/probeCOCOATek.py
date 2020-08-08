#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import io
from urllib.parse import urlparse
from datetime import datetime, timedelta, date
from pytz import timezone
from tzlocal import get_localzone
import argparse
import json
import requests
import zipfile
import pandas as pd

from TemporaryExposureKey.TemporaryExposureKey_pb2 import TemporaryExposureKeyExport

import probeCOCOATek

__version__ = '1.20200808'

_tek_url = "https://covid19radar-jpn-prod.azureedge.net/c19r/440/list.json"
_tek_key = "export.bin"
_tek_sig = "export.sig"


class Error(Exception):
  pass
class GitHubTokenError(Error):
  def __init__(self, message):
        self.message = message
class AugumentError(Error):
  def __init__(self, message):
        self.message = message
class ValueCleansingError(Error):
  def __init__(self, message):
        self.message = message
class NoneValueError(Error):
  def __init__(self, message):
        self.message = message

def _isURL(url) -> bool:
    try:
        u = urlparse(url)
    except:
        return False
    return True

def get_tek_json(tek_url) -> dict:
    return requests.get(tek_url).json()

def extract_key_zip(_zip_url):
    r = requests.get(_zip_url, stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    return z.read(_tek_key).strip("{:16}".format("EK Export v1").encode('utf-8')), z.read(_tek_sig)


def normalize_dataframe(js) -> pd.DataFrame:
    tek_list = []
    for item in js:
        tek = {"created":datetime.fromtimestamp(round(item["created"] / 1000)).astimezone(), "url": item["url"]}
        tek_list.append(tek)
    df = pd.DataFrame(tek_list)
    df.index.name = "no"
    df.reset_index(inplace=True)
    df.set_index("created", inplace=True)
    df.index = pd.to_datetime(df.index)
    df.reset_index(inplace=True)
    return df


def print_tek_bin_full(tek_bin):
    print("start_timestamp: [{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(tek_bin.start_timestamp).astimezone()))
    print("end_timestamp:   [{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(tek_bin.end_timestamp).astimezone()))
    print("region:          [{:}]".format(tek_bin.region))
    print("batch_num:       [{:}]".format(tek_bin.batch_num))
    print("batch_size:      [{:}]".format(tek_bin.batch_size))
    print("signature_infos:")
    print("    verification_key_version:      [{:}]".format(tek_bin.signature_infos[0].verification_key_version))
    print("    verification_key_id:           [{:}]".format(tek_bin.signature_infos[0].verification_key_id))
    print("    signature_algorithm:           [{:}]".format(tek_bin.signature_infos[0].signature_algorithm))
    print("keys:  (Total:      [{:}])".format(len(tek_bin.keys)))
    for i, k in enumerate(tek_bin.keys):
        print("    [{:03d}]:[{:}]".format(i+1, k.key_data.hex()))
        print("       [{:30}]:[{:}]".format("transmission_risk_level", str(k.transmission_risk_level)))
        print("       [{:30}]:[{:}]".format("rolling_start_interval_number", str(k.rolling_start_interval_number)))
        print("       [{:30}]:[{:}]".format("rolling_period", str(k.rolling_period)))



def main():
    parser = argparse.ArgumentParser(description='Probe TemporaryExposureKeys and Files of Exposure Notifications System in Japan a.k.a. "COCOA".', prefix_chars='-/')
    parser.add_argument('TEK', default=None, nargs='?', help="TEK Zip URL. If not set, print TEK distributed list")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(sys.argv[1:])

    try:
        if args.TEK is None:
            df = normalize_dataframe(get_tek_json(_tek_url))
            df_dict = df.to_dict(orient="records")

            print("{0:4}  {1:28} {2:}".format("#", "Created", "TEK URL"))
            for item in df_dict:
                print("{0:4}  [{1:%Y-%m-%d %H:%M:%S%z}]   [{2:}]".format(item["no"], item["created"], item["url"]))
            print("Total:{:>10}".format(len(df_dict)))

        elif _isURL(args.TEK):
            key_bin, _ = extract_key_zip(sys.argv[1])
            tek_bin = TemporaryExposureKeyExport()
            tek_bin.ParseFromString(key_bin)
            print_tek_bin_full(tek_bin)
        else:
            print("Argument should be valid URL for TEK.")
            sys.exit(1)

    
    except Exception as e:
            print("Error happens, when getting TEK JSON.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            sys.exit(1)


if __name__ == '__main__':
    main()