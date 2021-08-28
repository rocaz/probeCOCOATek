#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import requests
import requests_mock
import json
import sys
import os
from datetime import datetime

from probeCOCOATek.probeCOCOATek import probeCOCOATek, AugumentError, ParamError, DataError


class TestTEKToJSON(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    @pytest.mark.parametrize("nocache", [True, False])
    def test_tekjson_normal(self, nocache, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        if not nocache:
            for k,v in zip_data.items():
                with open(os.path.join(pCT.cache_dir, os.path.basename(k)), 'wb') as f:
                    f.write(bytes.fromhex(v["raw_data"]))
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for k,v in zip_data.items():
                m.get(k, content=bytes.fromhex(zip_data[k]["raw_data"]))
                tek_bin = pCT.get_tek_content(k)
                js_str = pCT.tek_toJson(tek_bin)
                js = json.loads(js_str)
                assert js["start_timestamp"] == datetime.fromtimestamp(tek_bin.start_timestamp).astimezone().isoformat()
                assert js["end_timestamp"] == datetime.fromtimestamp(tek_bin.end_timestamp).astimezone().isoformat()
                assert js["region"] == tek_bin.region
                assert js["batch_num"] == tek_bin.batch_num
                assert js["batch_size"] == tek_bin.batch_size
                assert js["signature_infos"]["verification_key_version"] == tek_bin.signature_infos[0].verification_key_version
                assert js["signature_infos"]["verification_key_id"] == tek_bin.signature_infos[0].verification_key_id
                assert js["signature_infos"]["signature_algorithm"] == tek_bin.signature_infos[0].signature_algorithm
                assert len(js["keys"]) == len(tek_bin.keys)
                for k in js["keys"]:
                    assert k["key_data"] in [tk.key_data.hex() for tk in tek_bin.keys if k["key_data"] == tk.key_data.hex()]
                    assert k["transmission_risk_level"] in [tk.transmission_risk_level for tk in tek_bin.keys if k["key_data"] == tk.key_data.hex()]
                    assert k["rolling_start_interval_number"] in [tk.rolling_start_interval_number for tk in tek_bin.keys if k["key_data"] == tk.key_data.hex()]
                    assert k["rolling_period"] in [tk.rolling_period for tk in tek_bin.keys if k["key_data"] == tk.key_data.hex()]
                    assert k["report_type"] in [tk.report_type for tk in tek_bin.keys if k["key_data"] == tk.key_data.hex()]
                    assert k["days_since_onset_of_symptoms"] in [tk.days_since_onset_of_symptoms for tk in tek_bin.keys if k["key_data"] == tk.key_data.hex()]


    @pytest.mark.parametrize("nocache", [True, False])
    def test_tekjson_invalid_data_error(self, nocache, normal_distribution_url, normal_distribution_json, zip_data, invalid_zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        if not nocache:
            for k,v in zip_data.items():
                with open(os.path.join(pCT.cache_dir, os.path.basename(k)), 'wb') as f:
                    f.write(bytes.fromhex(v["raw_data"]))
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for k,v in zip_data.items():
                m.get(k, content=bytes.fromhex(zip_data[k]["raw_data"]))
                tek_bin = pCT.get_tek_content(k)
                with pytest.raises(DataError) as e:
                    js_str = pCT.tek_toJson(bytes.fromhex(invalid_zip_data))