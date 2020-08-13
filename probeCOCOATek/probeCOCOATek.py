#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import io
import time
from datetime import datetime
from pytz import timezone
import json
import requests
import zipfile
import pandas as pd

from probeCOCOATek import __version__
from probeCOCOATek.TemporaryExposureKey.TemporaryExposureKey_pb2 import TemporaryExposureKeyExport


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

class probeCOCOATek():
    tek_key_name = "export.bin"
    tek_sig_name = "export.sig"

    def __init__(self, tek_distribution_url):
        self.tek_distribution_url = tek_distribution_url

        self.interval_sec_in_japan = 1

        self.version = __version__

    def get_url_content(self, url:str) -> bytes:
        time.sleep(self.interval_sec_in_japan)
        return requests.get(url, stream=True).content


    def extract_key_zip(self, zip_content:bytes) -> (bytes, bytes):
        z = zipfile.ZipFile(io.BytesIO(zip_content))
        return z.read(self.tek_key_name).strip("{:16}".format("EK Export v1").encode('utf-8')), z.read(self.tek_sig_name)

    def parse_export_bin(self, pb_bin:bytes) -> TemporaryExposureKeyExport:
        tek_bin = TemporaryExposureKeyExport()
        tek_bin.ParseFromString(pb_bin)
        return tek_bin


    def normalize_dataframe(self, js_content:dict) -> pd.DataFrame:
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


    def download_zips(self, tek_distribution_url:str, dir_base:str) -> None:
        dir_name = os.path.abspath(dir_base)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        dtname = "{:%Y%m%d_%H%M%S}".format(datetime.now())
        js = self.get_url_content(tek_distribution_url).decode('utf-8')

        with open(os.path.join(dir_name, dtname+".json"), 'w') as f:
            f.write(js)

        df = self.normalize_dataframe(json.loads(js))
        tek_zip_list = df.to_dict(orient="records")
        text_lines = self.print_tek_zip_list(tek_zip_list, True)

        with open(os.path.join(dir_name, dtname+".txt"), 'w') as f:
            f.write(os.linesep.join(text_lines))
        
        for item in tek_zip_list:
            if not os.path.exists(os.path.join(dir_name, os.path.basename(item["url"]))):
                z = self.get_url_content(item["url"])
                with open(os.path.join(dir_name, os.path.basename(item["url"])), 'wb') as f:
                    f.write(z)


    def print_tek_zip_list(self, tek_zip_list:dict, ekc:bool) -> list:
        text_lines = []

        if ekc:
            text_lines.append("{0:4}  {1:28} {2:64}   {3:}".format("#", "Created", "ZIP URL", "Keys Count"))
        else:
            text_lines.append("{0:4}  {1:28} {2:64}".format("#", "Created", "ZIP URL"))
        for item in tek_zip_list:
            if ekc:
                zip_content = self.get_url_content(item["url"])
                key_bin, _ = self.extract_key_zip(zip_content)
                tek_bin = self.parse_export_bin(key_bin)
                cnt = len(tek_bin.keys)
                text_lines.append("{0:4}  [{1:%Y-%m-%d %H:%M:%S%z}]   [{2:64}] [{3:4d}]".format(item["no"] + 1, item["created"], item["url"], cnt))
            else:
                text_lines.append("{0:4}  [{1:%Y-%m-%d %H:%M:%S%z}]   [{2:64}]".format(item["no"] + 1, item["created"], item["url"]))
        text_lines.append("ZIP Count:  {:>10}".format(len(tek_zip_list)))

        return text_lines


    def print_tek_keys_list(self, tek_zip_list:dict) -> list:
        text_lines = []

        text_lines.append("{0:11}  {1:28} {2:32}".format("#", "Created", "TEK Data"))
        key_cnt = 0
        for item in tek_zip_list:
            zip_content = self.get_url_content(item["url"])
            key_bin, _ = self.extract_key_zip(zip_content)
            tek_bin = self.parse_export_bin(key_bin)
            for k in tek_bin.keys:
                key_cnt += 1
                text_lines.append("{0:4}:{1:<6}  [{2:%Y-%m-%d %H:%M:%S%z}]   [{3:32}]".format(item["no"]+ 1, key_cnt, item["created"], k.key_data.hex()))
        text_lines.append("ZIP Count:  {:>10}".format(len(tek_zip_list)))
        text_lines.append("Keys Count: {:>10}".format(key_cnt))

        return text_lines


    def print_tek_bin_detail(self, tek_bin:TemporaryExposureKeyExport) -> str:
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
