#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import io
from urllib.parse import urlparse
import time
from datetime import datetime, timedelta, date
from pytz import timezone
from tzlocal import get_localzone
import argparse
import json
import requests
import zipfile
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'TemporaryExposureKey'))
from TemporaryExposureKey_pb2 import TemporaryExposureKeyExport


__version__ = '5.20200811'


_interval_sec_in_japan = 1

_tek_distribution_url = "https://covid19radar-jpn-prod.azureedge.net/c19r/440/list.json"
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


def _isURL(url:str) -> bool:
    try:
        u = urlparse(url)
    except:
        return False
    return True


def get_url_content(url:str) -> bytes:
    time.sleep(_interval_sec_in_japan)
    return requests.get(url, stream=True).content


def extract_key_zip(zip_content:bytes) -> (bytes, bytes):
    z = zipfile.ZipFile(io.BytesIO(zip_content))
    return z.read(_tek_key).strip("{:16}".format("EK Export v1").encode('utf-8')), z.read(_tek_sig)


def normalize_dataframe(js_content:dict) -> pd.DataFrame:
    tek_list = []
    for item in js_content:
        tek = {"created":datetime.fromtimestamp(round(item["created"] / 1000)).astimezone(), "url": item["url"]}
        tek_list.append(tek)
    df = pd.DataFrame(tek_list)
    df.index.name = "no"
    df.reset_index(inplace=True)
    df.set_index("created", inplace=True)
    df.index = pd.to_datetime(df.index)
    df.reset_index(inplace=True)
    return df


def download_zips(tek_distribution_url:str, dir_base:str) -> None:
    dir_name = os.path.abspath(dir_base)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name, exist_ok=True)

    dtname = "{:%Y%m%d_%H%M%S}".format(datetime.now())
    js = get_url_content(tek_distribution_url).decode('utf-8')

    with open(os.path.join(dir_name, dtname+".json"), 'w') as f:
        f.write(js)

    df = normalize_dataframe(json.loads(js))
    tek_zip_list = df.to_dict(orient="records")
    text_lines = print_tek_zip_list(tek_zip_list, True)

    with open(os.path.join(dir_name, dtname+".txt"), 'w') as f:
        f.write(os.linesep.join(text_lines))
    
    for item in tek_zip_list:
        if not os.path.exists(os.path.join(dir_name, os.path.basename(item["url"]))):
            z = get_url_content(item["url"])
            with open(os.path.join(dir_name, os.path.basename(item["url"])), 'wb') as f:
                f.write(z)


def print_tek_zip_list(tek_zip_list:dict, ekc:bool) -> list:
    text_lines = []

    if ekc:
        text_lines.append("{0:4}  {1:28} {2:64}   {3:}".format("#", "Created", "ZIP URL", "Keys Count"))
    else:
        text_lines.append("{0:4}  {1:28} {2:64}".format("#", "Created", "ZIP URL"))
    for item in tek_zip_list:
        if ekc:
            zip_content = get_url_content(item["url"])
            key_bin, _ = extract_key_zip(zip_content)
            tek_bin = TemporaryExposureKeyExport()
            tek_bin.ParseFromString(key_bin)
            cnt = len(tek_bin.keys)
            text_lines.append("{0:4}  [{1:%Y-%m-%d %H:%M:%S%z}]   [{2:64}] [{3:4d}]".format(item["no"] + 1, item["created"], item["url"], cnt))
        else:
            text_lines.append("{0:4}  [{1:%Y-%m-%d %H:%M:%S%z}]   [{2:64}]".format(item["no"] + 1, item["created"], item["url"]))
    text_lines.append("ZIP Count:  {:>10}".format(len(tek_zip_list)))

    return text_lines


def print_tek_keys_list(tek_zip_list:dict) -> list:
    text_lines = []

    text_lines.append("{0:11}  {1:28} {2:32}".format("#", "Created", "TEK Data"))
    key_cnt = 0
    for item in tek_zip_list:
        zip_content = get_url_content(item["url"])
        key_bin, _ = extract_key_zip(zip_content)
        tek_bin = TemporaryExposureKeyExport()
        tek_bin.ParseFromString(key_bin)
        for k in tek_bin.keys:
            key_cnt += 1
            text_lines.append("{0:4}:{1:<6}  [{2:%Y-%m-%d %H:%M:%S%z}]   [{3:32}]".format(item["no"]+ 1, key_cnt, item["created"], k.key_data.hex()))
    text_lines.append("ZIP Count:  {:>10}".format(len(tek_zip_list)))
    text_lines.append("Keys Count: {:>10}".format(key_cnt))

    return text_lines


def print_tek_bin_detail(tek_bin) -> str:
    text_lines = []

    text_lines.append("start_timestamp: [{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(tek_bin.start_timestamp).astimezone()))
    text_lines.append("end_timestamp:   [{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(tek_bin.end_timestamp).astimezone()))
    text_lines.append("region:          [{:}]".format(tek_bin.region))
    text_lines.append("batch_num:       [{:}]".format(tek_bin.batch_num))
    text_lines.append("batch_size:      [{:}]".format(tek_bin.batch_size))
    text_lines.append("signature_infos:")
    text_lines.append("    verification_key_version:      [{:}]".format(tek_bin.signature_infos[0].verification_key_version))
    text_lines.append("    verification_key_id:           [{:}]".format(tek_bin.signature_infos[0].verification_key_id))
    text_lines.append("    signature_algorithm:           [{:}]".format(tek_bin.signature_infos[0].signature_algorithm))
    text_lines.append("Keys:  (Count: [{:}])".format(len(tek_bin.keys)))
    for i, k in enumerate(tek_bin.keys):
        text_lines.append("    [{:03d}]:[{:}]".format(i+1, k.key_data.hex()))
        text_lines.append("       [{:30}]:[{:}]".format("transmission_risk_level", str(k.transmission_risk_level)))
        text_lines.append("       [{:30}]:[{:}]".format("rolling_start_interval_number", str(k.rolling_start_interval_number)))
        text_lines.append("       [{:30}]:[{:}]".format("rolling_period", str(k.rolling_period)))

    return text_lines


def main() -> None:
    parser = argparse.ArgumentParser(description='Probe TemporaryExposureKeys and Files of Exposure Notifications System in Japan a.k.a. "COCOA".', prefix_chars='-')
    parser.add_argument("-z", "--zip-url", default=None, dest="zip_url", help="print TEK ZIP Detail. If not set, print TEK distribution list")
    parser.add_argument("-ekc", "--each-keys-count", action='store_true', dest="ekc", help="Print keys count each ZIP with TEK distribution list. Only available when printing TEK distribution list.")
    parser.add_argument("-akl", "--all-keys-list", action='store_true', dest="akl", help="Print a list of all keys for each ZIP. Other options are ignored.")
    parser.add_argument("-dl", "--dl-zip", default=None, dest="dl_dir", help="Specified directory for downloading all TEK ZIP and list JSON from TEK distribution list. Other options are ignored.")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(sys.argv[1:])

    if args.dl_dir is not None:
        try:
            download_zips(_tek_distribution_url, args.dl_dir)
            print("Download done.")
        except Exception as e:
            print("Error happens, when downloading TEK ZIP and distribution list.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    elif args.akl:
        try:
            df = normalize_dataframe(json.loads(get_url_content(_tek_distribution_url).decode('utf-8')))
            tek_zip_list = df.to_dict(orient="records")
            text_lines = print_tek_keys_list(tek_zip_list)
            print(os.linesep.join(text_lines))
        except Exception as e:
            print("Error happens, when getting all keys of ZIP.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    elif args.zip_url is None:
        try:
            df = normalize_dataframe(json.loads(get_url_content(_tek_distribution_url).decode('utf-8')))
            tek_zip_list = df.to_dict(orient="records")
            text_lines = print_tek_zip_list(tek_zip_list, args.ekc)
            print(os.linesep.join(text_lines))
        except Exception as e:
            print("Error happens, when getting TEK distribution list.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    elif _isURL(args.zip_url):
        try:
            zip_content = get_url_content(args.zip_url)
            key_bin, _ = extract_key_zip(zip_content)
            tek_bin = TemporaryExposureKeyExport()
            tek_bin.ParseFromString(key_bin)
            text_lines = print_tek_bin_detail(tek_bin)
            print(os.linesep.join(text_lines))
        except Exception as e:
            print("Error happens, when getting TEK ZIP detail.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    else:
        print("Argument other error happens.")
        return 1

    return 0
