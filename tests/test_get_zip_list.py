#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import requests
import requests_mock
import sys
import os

from probeCOCOATek.probeCOCOATek import probeCOCOATek, AugumentError, ParamError, DataError


class TestGetZipList(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    def test_list_normal(self, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            tek_zip_list = pCT.get_zip_list()
            print(tek_zip_list)
            for t in tek_zip_list:
                assert t["keys"]["count"] == len(zip_data[t["url"]]["keys"])
                assert set(t["keys"]["key_data"]) == set([z["key_data"] for z in zip_data[t["url"]]["keys"]])
                assert os.path.isfile(os.path.join(pCT.cache_dir, os.path.basename(t["url"])))

    def test_list_url_notfound_error(self, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, text='Not Found', status_code=404)
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            with pytest.raises(requests.exceptions.HTTPError) as e:
                tek_zip_list = pCT.get_zip_list()

    def test_list_url_invalid_json_error(self, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content='invalid_json'.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            with pytest.raises(DataError) as e:
                tek_zip_list = pCT.get_zip_list()

    def test_list_url_others_error(self, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, text='server error', status_code=500)
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            with pytest.raises(requests.exceptions.HTTPError) as e:
                tek_zip_list = pCT.get_zip_list()

    def test_list_zip_url_notfound_error(self, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]), status_code=404)
            with pytest.raises(requests.exceptions.HTTPError) as e:
                tek_zip_list = pCT.get_zip_list()

    def test_list_zip_invalid_data_error(self, normal_distribution_url, normal_distribution_json, zip_data, invalid_zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(invalid_zip_data))
            with pytest.raises(DataError) as e:
                tek_zip_list = pCT.get_zip_list()

    def test_list_zip_url_server_error(self, normal_distribution_url, normal_distribution_json, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]), status_code=500)
            with pytest.raises(requests.exceptions.HTTPError) as e:
                tek_zip_list = pCT.get_zip_list()

                
