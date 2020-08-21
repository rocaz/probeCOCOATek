#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import requests
import requests_mock
import sys
import os
from datetime import datetime

from probeCOCOATek.probeCOCOATek import probeCOCOATek, AugumentError, ParamError, DataError


class TestGetTEKContent(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    @pytest.mark.parametrize("nocache", [True, False])
    def test_zip_from_url_nocache_normal(self, nocache, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        if not nocache:
            for k,v in zip_data.items():
                with open(os.path.join(pCT.cache_dir, os.path.basename(k)), 'wb') as f:
                    f.write(bytes.fromhex(v["raw_data"]))
        with requests_mock.Mocker() as m:
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]))
                tek_bin = pCT.get_tek_content(url)
                assert "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.fromtimestamp(tek_bin.start_timestamp).astimezone()) == "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.strptime(zip_data[url]["start_timestamp"], "%Y-%m-%d %H:%M:%S%z").astimezone())
                assert "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.fromtimestamp(tek_bin.end_timestamp).astimezone()) == "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.strptime(zip_data[url]["end_timestamp"], "%Y-%m-%d %H:%M:%S%z").astimezone())
                assert tek_bin.region == zip_data[url]["region"]
                assert tek_bin.batch_num == zip_data[url]["batch_num"]
                assert tek_bin.batch_size == zip_data[url]["batch_size"]
                assert tek_bin.signature_infos[0].verification_key_version == zip_data[url]["signature_infos"]["verification_key_version"]
                assert tek_bin.signature_infos[0].verification_key_id == zip_data[url]["signature_infos"]["verification_key_id"]
                assert tek_bin.signature_infos[0].signature_algorithm == zip_data[url]["signature_infos"]["signature_algorithm"]
                assert set([k.key_data.hex() for k in tek_bin.keys]) == set([z["key_data"] for z in zip_data[url]["keys"]])
                assert set([k.transmission_risk_level for k in tek_bin.keys]) == set([z["transmission_risk_level"] for z in zip_data[url]["keys"]])
                assert set([k.rolling_start_interval_number for k in tek_bin.keys]) == set([z["rolling_start_interval_number"] for z in zip_data[url]["keys"]])
                assert set([k.rolling_period for k in tek_bin.keys]) == set([z["rolling_period"] for z in zip_data[url]["keys"]])
    
    def test_zip_by_absfile_normal(self, normal_distribution_url, zip_data, tmpdir):
        for k,v in zip_data.items():
            with open(os.path.join(tmpdir, os.path.basename(k)), 'wb') as f:
                f.write(bytes.fromhex(v["raw_data"]))
        pCT = probeCOCOATek(normal_distribution_url)
        for k1,v1 in zip_data.items():
            tek_bin = pCT.get_tek_content(os.path.join(tmpdir, os.path.basename(k1)))
            assert "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.fromtimestamp(tek_bin.start_timestamp).astimezone()) == "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.strptime(v1["start_timestamp"], "%Y-%m-%d %H:%M:%S%z").astimezone())
            assert "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.fromtimestamp(tek_bin.end_timestamp).astimezone()) == "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.strptime(v1["end_timestamp"], "%Y-%m-%d %H:%M:%S%z").astimezone())
            assert tek_bin.region == v1["region"]
            assert tek_bin.batch_num == v1["batch_num"]
            assert tek_bin.batch_size == v1["batch_size"]
            assert tek_bin.signature_infos[0].verification_key_version == v1["signature_infos"]["verification_key_version"]
            assert tek_bin.signature_infos[0].verification_key_id == v1["signature_infos"]["verification_key_id"]
            assert tek_bin.signature_infos[0].signature_algorithm == v1["signature_infos"]["signature_algorithm"]
            assert set([k.key_data.hex() for k in tek_bin.keys]) == set([z["key_data"] for z in v1["keys"]])
            assert set([k.transmission_risk_level for k in tek_bin.keys]) == set([z["transmission_risk_level"] for z in v1["keys"]])
            assert set([k.rolling_start_interval_number for k in tek_bin.keys]) == set([z["rolling_start_interval_number"] for z in v1["keys"]])
            assert set([k.rolling_period for k in tek_bin.keys]) == set([z["rolling_period"] for z in v1["keys"]])

    def test_zip_by_relfile_withcache_normal(self, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        for k,v in zip_data.items():
            with open(os.path.join(pCT.cache_dir, os.path.basename(k)), 'wb') as f:
                f.write(bytes.fromhex(v["raw_data"]))
        for k1,v1 in zip_data.items():
            tek_bin = pCT.get_tek_content(os.path.basename(k1))
            assert "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.fromtimestamp(tek_bin.start_timestamp).astimezone()) == "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.strptime(v1["start_timestamp"], "%Y-%m-%d %H:%M:%S%z").astimezone())
            assert "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.fromtimestamp(tek_bin.end_timestamp).astimezone()) == "{:%Y-%m-%d %H:%M:%S%z}".format(datetime.strptime(v1["end_timestamp"], "%Y-%m-%d %H:%M:%S%z").astimezone())
            assert tek_bin.region == v1["region"]
            assert tek_bin.batch_num == v1["batch_num"]
            assert tek_bin.batch_size == v1["batch_size"]
            assert tek_bin.signature_infos[0].verification_key_version == v1["signature_infos"]["verification_key_version"]
            assert tek_bin.signature_infos[0].verification_key_id == v1["signature_infos"]["verification_key_id"]
            assert tek_bin.signature_infos[0].signature_algorithm == v1["signature_infos"]["signature_algorithm"]
            assert set([k.key_data.hex() for k in tek_bin.keys]) == set([z["key_data"] for z in v1["keys"]])
            assert set([k.transmission_risk_level for k in tek_bin.keys]) == set([z["transmission_risk_level"] for z in v1["keys"]])
            assert set([k.rolling_start_interval_number for k in tek_bin.keys]) == set([z["rolling_start_interval_number"] for z in v1["keys"]])
            assert set([k.rolling_period for k in tek_bin.keys]) == set([z["rolling_period"] for z in v1["keys"]])

    def test_zip_not_found_error(self, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]), status_code=404)
                with pytest.raises(requests.exceptions.HTTPError) as e:
                    tek_bin = pCT.get_tek_content(url)

    def test_zip_server_error(self, normal_distribution_url, zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(zip_data[url]["raw_data"]), status_code=500)
                with pytest.raises(requests.exceptions.HTTPError) as e:
                    tek_bin = pCT.get_tek_content(url)

    def test_zip_no_file_error(self, normal_distribution_url, zip_data, tmpdir):
        pCT = probeCOCOATek(normal_distribution_url)
        for k1,v1 in zip_data.items():
            with pytest.raises(ParamError) as e:
                tek_bin = pCT.get_tek_content(os.path.join(tmpdir, os.path.basename(k1)))

    def test_zip_invalid_data_error(self, normal_distribution_url, zip_data, invalid_zip_data):
        pCT = probeCOCOATek(normal_distribution_url)
        with requests_mock.Mocker() as m:
            for url in zip_data.keys():
                m.get(url, content=bytes.fromhex(invalid_zip_data))
                with pytest.raises(DataError) as e:
                    tek_bin = pCT.get_tek_content(url)

