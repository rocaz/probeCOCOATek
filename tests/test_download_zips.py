#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import requests
import requests_mock
import sys
import os

from probeCOCOATek.probeCOCOATek import probeCOCOATek, AugumentError, ParamError, DataError


class TestDownloadZips(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    @pytest.mark.parametrize("nocache", [True, False])
    def test_dl_normal(self, nocache, normal_distribution_url, normal_distribution_json, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        if not nocache:
            for k,v in zip_data.items():
                with open(os.path.join(pCT.cache_dir, os.path.basename(k)), 'wb') as f:
                    f.write(bytes.fromhex(v["raw_data"]))
        for k,v in zip_data.items():
            assert not os.path.exists(os.path.join(tmpdir, os.path.basename(k)))
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            pCT.download_zips(tmpdir)
            for k,v in zip_data.items():
                assert os.path.exists(os.path.join(tmpdir, os.path.basename(k)))
                with open(os.path.join(tmpdir, os.path.basename(k)), 'rb') as f:
                    assert v["raw_data"] == f.read().hex()
    
    def test_dl_noexist_dir_normal(self, normal_distribution_url, normal_distribution_json, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        for k,v in zip_data.items():
            assert not os.path.exists(os.path.join(tmpdir, os.path.basename(k)))
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            target_dir = os.path.join(tmpdir,"test")
            assert not os.path.exists(target_dir)
            pCT.download_zips(target_dir)
            for k,v in zip_data.items():
                assert os.path.exists(target_dir)
                with open(os.path.join(target_dir, os.path.basename(k)), 'rb') as f:
                    assert v["raw_data"] == f.read().hex()
    
    def test_dl_list_url_notfound_error(self, normal_distribution_url, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, text='Not Found', status_code=404)
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            with pytest.raises(requests.exceptions.HTTPError) as e:
                pCT.download_zips(tmpdir)

    def test_dl_list_url_invalid_json_error(self, normal_distribution_url, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content='invalid_json'.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            with pytest.raises(DataError) as e:
                pCT.download_zips(tmpdir)

    def test_dl_list_url_others_error(self, normal_distribution_url, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, text='server error', status_code=500)
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
            with pytest.raises(requests.exceptions.HTTPError) as e:
                pCT.download_zips(tmpdir)

    def test_dl_zip_url_notfound_error(self, normal_distribution_url, normal_distribution_json, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]), status_code=404)
            with pytest.raises(requests.exceptions.HTTPError) as e:
                pCT.download_zips(tmpdir)

    def test_dl_zip_invalid_data_error(self, normal_distribution_url, normal_distribution_json, zip_data, tmpdir, invalid_zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(invalid_zip_data))
            with pytest.raises(DataError) as e:
                pCT.download_zips(tmpdir)

    def test_dl_zip_url_server_error(self, normal_distribution_url, normal_distribution_json, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            m.get(normal_distribution_url, content=normal_distribution_json.encode('utf-8'))
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]), status_code=500)
            with pytest.raises(requests.exceptions.HTTPError) as e:
                pCT.download_zips(tmpdir)
