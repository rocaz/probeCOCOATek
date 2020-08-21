#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytest
import sys
import os

from probeCOCOATek.probeCOCOATek import probeCOCOATek, AugumentError, ParamError, DataError


class TestClassProbeCOCOATek(object):
    def setup_method(self, method):
        pass
    def teardown_method(self, method):
        pass

    def test_constractclass_withoption_normal(self, normal_distribution_url, tmpdir):
        set_dir = tmpdir
        #assert not os.path.isdir(set_dir)
        pCT = probeCOCOATek(normal_distribution_url, cache_dir=set_dir)
        assert type(pCT) == probeCOCOATek
        assert pCT.tek_distribution_url == normal_distribution_url
        assert pCT.cache_dir == set_dir
        assert os.path.isdir(pCT.cache_dir)
    def test_constractclass_default_normal(self):
        assert not os.path.isdir(os.path.join(os.path.expanduser("~"), ".probecocoatek" + os.sep + "cache"))
        pCT = probeCOCOATek()
        assert type(pCT) == probeCOCOATek
        assert pCT.tek_distribution_url == "https://covid19radar-jpn-prod.azureedge.net/c19r/440/list.json"
        assert pCT.cache_dir == os.path.join(os.path.expanduser("~"), ".probecocoatek" + os.sep + "cache")
        assert os.path.isdir(pCT.cache_dir)
        print(pCT.cache_dir)
    def test_constractclass_no_tek_distribution_url_error(self):
        with pytest.raises(ParamError) as e:
            pCT = probeCOCOATek("")
    def test_constractclass_invalid_cachedir_error(self, tmpdir):
        t = tmpdir.join("dummy.txt")
        t.write("dummy")
        with pytest.raises(ParamError) as e:
            pCT = probeCOCOATek(cache_dir=t)