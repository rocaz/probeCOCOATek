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


class TestTEKToText(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    @pytest.mark.parametrize("nocache", [True, False])
    def test_tektext_normal(self, nocache, normal_distribution_url, normal_distribution_json, zip_data):
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
                text_lines = pCT.tek_toText(tek_bin)
                assert True in [("start_timestamp" in l) and ("{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(tek_bin.start_timestamp).astimezone()) in l) for l in text_lines]
                assert True in [("end_timestamp" in l) and ("{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(tek_bin.end_timestamp).astimezone()) in l) for l in text_lines]
                assert True in [("region" in l) and (str(tek_bin.region) in l) for l in text_lines]
                assert True in [("batch_num" in l) and (str(tek_bin.batch_num) in l) for l in text_lines]
                assert True in [("batch_size" in l) and (str(tek_bin.batch_size) in l) for l in text_lines]
                assert True in [("verification_key_version" in l) and (tek_bin.signature_infos[0].verification_key_version in l) for l in text_lines]
                assert True in [("verification_key_id" in l) and (tek_bin.signature_infos[0].verification_key_id in l) for l in text_lines]
                assert True in [("signature_algorithm" in l) and (tek_bin.signature_infos[0].signature_algorithm in l) for l in text_lines]
                assert True in [("Keys" in l) and ("Count" in l) and ("[{:}]".format(len(tek_bin.keys)) in l) for l in text_lines]
                for i, k in enumerate(tek_bin.keys):
                    assert True in [("[{:03d}]".format(i+1) in l) and ("[{:}]".format(k.key_data.hex()) in l) for l in text_lines]
                    assert True in [("transmission_risk_level" in l) and ("[{:}]".format(k.transmission_risk_level) in l) for l in text_lines]
                    assert True in [("rolling_start_interval_number" in l) and ("[{:}]".format(k.rolling_start_interval_number) in l) for l in text_lines]
                    assert True in [("rolling_period" in l) and ("[{:}]".format(k.rolling_period) in l) for l in text_lines]
                    assert True in [("report_type" in l) and ("[{:}]".format(k.report_type) in l) for l in text_lines]
                    assert True in [("days_since_onset_of_symptoms" in l) and ("[{:}]".format(k.days_since_onset_of_symptoms) in l) for l in text_lines]

    @pytest.mark.parametrize("nocache", [True, False])
    def test_tektext_invalid_data_error(self, nocache, normal_distribution_url, normal_distribution_json, zip_data, invalid_zip_data):
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
                    text_lines = pCT.tek_toText(bytes.fromhex(invalid_zip_data))

