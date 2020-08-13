#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import argparse
from urllib.parse import urlparse

from probeCOCOATek import __version__
from probeCOCOATek.probeCOCOATek import probeCOCOATek

_tek_distribution_url = "https://covid19radar-jpn-prod.azureedge.net/c19r/440/list.json"

def _isURL(url:str) -> bool:
    try:
        u = urlparse(url)
    except:
        return False
    return True

def main() -> int:
    pCT = probeCOCOATek(_tek_distribution_url)

    parser = argparse.ArgumentParser(description='Probe TemporaryExposureKeys and Files of Exposure Notifications System in Japan a.k.a. "COCOA".', prefix_chars='-')
    parser.add_argument("-z", "--zip-url", default=None, dest="zip_url", help="print TEK ZIP Detail. If not set, print TEK distribution list")
    parser.add_argument("-ekc", "--each-keys-count", action='store_true', dest="ekc", help="Print keys count each ZIP with TEK distribution list. Only available when printing TEK distribution list.")
    parser.add_argument("-akl", "--all-keys-list", action='store_true', dest="akl", help="Print a list of all keys for each ZIP. Other options are ignored.")
    parser.add_argument("-dl", "--dl-zip", default=None, dest="dl_dir", help="Specified directory for downloading all TEK ZIP and list JSON from TEK distribution list. Other options are ignored.")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(sys.argv[1:])

    if args.dl_dir is not None:
        try:
            pCT.download_zips(_tek_distribution_url, args.dl_dir)
            print("Download done.")
        except Exception as e:
            print("Error happens, when downloading TEK ZIP and distribution list.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    elif args.akl:
        try:
            df = pCT.normalize_dataframe(json.loads(pCT.get_url_content(_tek_distribution_url).decode('utf-8')))
            tek_zip_list = df.to_dict(orient="records")
            text_lines = pCT.print_tek_keys_list(tek_zip_list)
            print(os.linesep.join(text_lines))
        except Exception as e:
            print("Error happens, when getting all keys of ZIP.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    elif args.zip_url is None:
        try:
            df = pCT.normalize_dataframe(json.loads(pCT.get_url_content(_tek_distribution_url).decode('utf-8')))
            tek_zip_list = df.to_dict(orient="records")
            text_lines = pCT.print_tek_zip_list(tek_zip_list, args.ekc)
            print(os.linesep.join(text_lines))
        except Exception as e:
            print("Error happens, when getting TEK distribution list.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    elif _isURL(args.zip_url):
        try:
            zip_content = pCT.get_url_content(args.zip_url)
            key_bin, _ = pCT.extract_key_zip(zip_content)
            tek_bin = pCT.parse_export_bin(key_bin)
            text_lines = pCT.print_tek_bin_detail(tek_bin)
            print(os.linesep.join(text_lines))
        except Exception as e:
            print("Error happens, when getting TEK ZIP detail.")
            tb = sys.exc_info()[2]
            print(e.with_traceback(tb))
            return 1
    else:
        print("Argument other error happens.")
        return 1

    return 0


    if __name__ == "__main__":
        sys.exit(main())