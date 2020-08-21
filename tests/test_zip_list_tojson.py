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


class TestZipListToJSON(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listjson_normal(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            js_str = pCT.zip_list_toJson(nokey)
            js = json.loads(js_str)
            for i,z in enumerate(js):
                assert z["no"] == i
                assert z["url"] in [j["url"] for j in json.loads(normal_distribution_json)]
                assert z["created"] == datetime.fromtimestamp(round([j["created"] for j in json.loads(normal_distribution_json) if z["url"] == j["url"]][0] / 1000)).astimezone().isoformat()
                if "keys" in z:
                    assert z["keys"]["count"] == len(zip_data[z["url"]]["keys"])

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listjson_invalid_data_error(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            pCT.tek_zip_list = "invalid_data"
            with pytest.raises(DataError) as e:
                js_str = pCT.zip_list_toJson(nokey)

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listjson_none_data_error(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            pCT.tek_zip_list = None
            with pytest.raises(DataError) as e:
                js_str = pCT.zip_list_toJson(nokey)

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listjson_no_data_error(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            pCT.tek_zip_list = []
            with pytest.raises(DataError) as e:
                js_str = pCT.zip_list_toJson(nokey)

    