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
import google.protobuf.message as pbm

from probeCOCOATek import __version__
from probeCOCOATek.TemporaryExposureKey.TemporaryExposureKey_pb2 import TemporaryExposureKeyExport

class Error(Exception):
  pass
class AugumentError(Error):
  def __init__(self, message):
        self.message = message
class ParamError(Error):
  def __init__(self, message):
        self.message = message
class DataError(Error):
  def __init__(self, message):
        self.message = message


class probeCOCOATek():
    version = __version__

    __tek_key_name = "export.bin"
    __tek_sig_name = "export.sig"
    
    tek_distribution_url = "https://covid19radar-jpn-prod.azureedge.net/c19r/440/list.json"
    cache_dir = None
    interval_sec_in_japan = 1
    tek_distribution_content = None
    tek_zip_list = None


    def __init__(self, tek_distribution_url:str=None, cache_dir:str=None):
        self.tek_distribution_url = "https://covid19radar-jpn-prod.azureedge.net/c19r/440/list.json"
        self.cache_dir = None

        if tek_distribution_url is not None:
            if not (tek_distribution_url.startswith("http://") or tek_distribution_url.startswith("https://")):
                raise ParamError("tek_distribution_url is invalid.")
            self.tek_distribution_url = tek_distribution_url

        if cache_dir is None:
            self.cache_dir = os.path.join(os.path.expanduser("~"), ".probecocoatek" + os.sep + "cache")
        else:
            self.cache_dir = cache_dir
        if not os.path.isdir(self.cache_dir):
            try:
                os.makedirs(self.cache_dir)
            except Exception as e:
                raise ParamError("cache_dir is invalid.")


    def _get_distribution_url(self) -> bytes:
        time.sleep(self.interval_sec_in_japan)
        r = requests.get(self.tek_distribution_url, stream=True)
        r.raise_for_status()
        self.tek_distribution_content = r.content
        return self.tek_distribution_content


    def _get_zip_content(self, url_or_fname:str) -> bytes:
        if os.path.isfile(url_or_fname):
            zip_content = self._get_zip_file(url_or_fname)
        elif os.path.isfile(os.path.join(self.cache_dir, url_or_fname)):
            zip_content = self._get_zip_file(os.path.join(self.cache_dir, url_or_fname))
        elif url_or_fname.startswith("http://") or url_or_fname.startswith("https://"):
            if os.path.isfile(os.path.join(self.cache_dir, os.path.basename(url_or_fname))):
                zip_content = self._get_zip_file(os.path.join(self.cache_dir, os.path.basename(url_or_fname)))
            else:
                zip_content = self._get_zip_url(url_or_fname)
            with open(os.path.join(self.cache_dir, os.path.basename(url_or_fname)), 'wb') as f:
                f.write(zip_content)
        else:
            raise ParamError("TEK ZIP url or filename is invalid.")
        return zip_content


    def _get_zip_url(self, url:str) -> bytes:
        time.sleep(self.interval_sec_in_japan)
        r = requests.get(url, stream=True)
        r.raise_for_status()
        return r.content


    def _get_zip_file(self, filename:str) -> bytes:
        with open(filename, 'rb') as f:
            zip_content = f.read()
        return zip_content


    def _extract_key_zip(self, zip_content:bytes) -> (bytes, bytes):
        try:
            z = zipfile.ZipFile(io.BytesIO(zip_content))
        except zipfile.BadZipFile as e:
            raise DataError("TEK ZIP is invalid.")
        return z.read(self.__tek_key_name).strip("{:16}".format("EK Export v1").encode('utf-8')), z.read(self.__tek_sig_name)


    def _parse_export_key(self, pb_bin:bytes) -> TemporaryExposureKeyExport:
        tek_bin = TemporaryExposureKeyExport()
        try:
            tek_bin.ParseFromString(pb_bin)
        except pbm.DecodeError as e:
            #print('DecodeError: {}'.format(e))
            pass
        except Exception as e:
            print('Error: {}'.format(e))
        return tek_bin


    def _normalize_zip_list(self, tek_list:dict) -> dict:
        df = pd.DataFrame(tek_list)
        df.index.name = "no"
        df.reset_index(inplace=True)
        df.set_index("created", inplace=True)
        df.index = pd.to_datetime(df.index)
        df.reset_index(inplace=True)
        return df.to_dict(orient="records")
    

    def _date_handler(self, obj):
        return obj.isoformat() if hasattr(obj, 'isoformat') else obj


    def get_zip_list(self) -> dict:
        js = self._get_distribution_url().decode('utf-8')
        try:
            distribution_list = json.loads(js)
        except json.decoder.JSONDecodeError as e:
            raise DataError("distribution list is not JSON.")
        tek_list = []
        for item in distribution_list:
            tek = {"created":datetime.fromtimestamp(round(item["created"] / 1000)).astimezone(), "url": item["url"]}
            tek_bin = self.get_tek_content(item["url"])
            tek["keys"] = {}
            tek["keys"]["count"] = len(tek_bin.keys)
            key_data = []
            for k in tek_bin.keys:
                key_data.append(k.key_data.hex())
            tek["keys"]["key_data"] = key_data
            tek_list.append(tek)
        tek_zip_list = self._normalize_zip_list(tek_list)
        self.tek_zip_list = tek_zip_list
        return tek_zip_list


    def zip_list_toText(self, nokeys:bool) -> list:
        if self.tek_zip_list is None or type(self.tek_zip_list) != list or len(self.tek_zip_list) == 0:
            raise DataError("ZIP list is invalid.")
        text_lines = []
        key_cnt = 0
        coltitle = "ZIP URL / Key Data" if not nokeys else "ZIP URL"
        text_lines.append("{0:4}  {1:28} {2:64}   {3:}".format("#", "Created", coltitle, "KeyCount"))
        for item in self.tek_zip_list:
            text_lines.append("{0:4}  [{1:%Y-%m-%d %H:%M:%S%z}]   {2:66} [{3:4d}]".format(item["no"] + 1, item["created"], "[" + item["url"] + "]", item["keys"]["count"]))
            if not nokeys:
                for i, key_data in enumerate(item["keys"]["key_data"]):
                    key_cnt += 1
                    text_lines.append(" {0:4}{1:30}[{2:32}]".format(i+1, " ", key_data))
        text_lines.append("ZIP Count:        {:>10}".format(len(self.tek_zip_list)))
        if not nokeys:
            text_lines.append("Keys Total Count: {:>10}".format(key_cnt))
        return text_lines


    def zip_list_toJson(self, nokeys:bool) -> str:
        if self.tek_zip_list is None or type(self.tek_zip_list) != list or len(self.tek_zip_list) == 0:
            raise DataError("ZIP list is invalid.")
        if nokeys:
            jd = []
            for item in self.tek_zip_list:
                del item["keys"]
                jd.append(item)
        else:
            jd = self.tek_zip_list
        return json.dumps(jd, default=self._date_handler)


    def get_tek_content(self, url_or_fname:str) -> bytes:
        zip_content = self._get_zip_content(url_or_fname)
        tek_key, tek_sig = self._extract_key_zip(zip_content)
        tek_bin = self._parse_export_key(tek_key)
        return tek_bin


    def tek_toText(self, tek_bin:TemporaryExposureKeyExport) -> str:
        if tek_bin is None or type(tek_bin) != TemporaryExposureKeyExport:
            raise DataError("TEK is invalid.")
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
            text_lines.append("       [{:30}]:[{:}]".format("report_type", str(k.report_type)))
            text_lines.append("       [{:30}]:[{:}]".format("days_since_onset_of_symptoms", str(k.days_since_onset_of_symptoms)))
        return text_lines


    def tek_toJson(self, tek_bin:TemporaryExposureKeyExport) -> str:
        if tek_bin is None or type(tek_bin) != TemporaryExposureKeyExport:
            raise DataError("TEK is invalid.")
        jd = {}
        jd["start_timestamp"] = datetime.fromtimestamp(tek_bin.start_timestamp).astimezone().isoformat()
        jd["end_timestamp"] = datetime.fromtimestamp(tek_bin.end_timestamp).astimezone().isoformat()
        jd["region"] = tek_bin.region
        jd["batch_num"] = tek_bin.batch_num
        jd["batch_size"] = tek_bin.batch_size
        jd["signature_infos"] = {}
        jd["signature_infos"]["verification_key_version"] = tek_bin.signature_infos[0].verification_key_version
        jd["signature_infos"]["verification_key_id"] = tek_bin.signature_infos[0].verification_key_id
        jd["signature_infos"]["signature_algorithm"] = tek_bin.signature_infos[0].signature_algorithm
        jd["keys"] = []
        for i, k in enumerate(tek_bin.keys):
            kd = {}
            kd["key_data"] = k.key_data.hex()
            kd["transmission_risk_level"] = k.transmission_risk_level
            kd["rolling_start_interval_number"] = k.rolling_start_interval_number
            kd["rolling_period"] = k.rolling_period
            kd["report_type"] = k.report_type
            kd["days_since_onset_of_symptoms"] = k.days_since_onset_of_symptoms
            jd["keys"].append(kd)
        return json.dumps(jd)


    def download_zips(self, dir_base:str) -> None:
        dir_name = os.path.abspath(dir_base)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        dtname = "{:%Y%m%d_%H%M%S}".format(datetime.now())
        tek_zip_list = self.get_zip_list()
        text_lines = self.zip_list_toText(False)

        with open(os.path.join(dir_name, dtname+".json"), 'w') as f:
            f.write(self.tek_distribution_content.decode('utf-8'))

        with open(os.path.join(dir_name, dtname+".txt"), 'w') as f:
            f.write(os.linesep.join(text_lines))
        
        for item in tek_zip_list:
            if not os.path.exists(os.path.join(dir_name, os.path.basename(item["url"]))):
                z = self._get_zip_content(item["url"])
                with open(os.path.join(dir_name, os.path.basename(item["url"])), 'wb') as f:
                    f.write(z)


    
