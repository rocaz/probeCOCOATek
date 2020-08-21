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


class TestZipListToText(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listtext_normal(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            text_lines = pCT.zip_list_toText(nokey)
            zip_list = json.loads(normal_distribution_json)
            key_cnt = 0
            for i,z in enumerate(zip_list):
                assert True in [(str(i) in l) and (z["url"] in l) and ("[{:%Y-%m-%d %H:%M:%S%z}]".format(datetime.fromtimestamp(round(z["created"] / 1000)).astimezone()) in l) and (str(len(zip_data[z["url"]]["keys"])) in l) for l in text_lines]
                for i,v in enumerate(zip_data[z["url"]]["keys"]):
                    assert (True in [(v["key_data"] in l) for l in text_lines]) != nokey
                    key_cnt += 1
            assert True in [("ZIP Count" in l) and (str(len(zip_list)) in l) for l in text_lines]
            assert (True in [("Keys Total Count" in l) and (str(key_cnt) in l) for l in text_lines]) != nokey

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listtext_invalid_data_error(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            pCT.tek_zip_list = "invalid_data"
            with pytest.raises(DataError) as e:
                text_lines = pCT.zip_list_toText(nokey)

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listtext_none_data_error(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            pCT.tek_zip_list = None
            with pytest.raises(DataError) as e:
                text_lines = pCT.zip_list_toText(nokey)

    @pytest.mark.parametrize("nokey", [True, False])
    def test_listtext_no_data_error(self, nokey, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            pCT.tek_zip_list = []
            with pytest.raises(DataError) as e:
                text_lines = pCT.zip_list_toText(nokey)

