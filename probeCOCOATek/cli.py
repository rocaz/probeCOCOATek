#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import json
import argparse
from urllib.parse import urlparse

from probeCOCOATek import __version__
from probeCOCOATek.probeCOCOATek import probeCOCOATek, AugumentError, ParamError


def main() -> int:
    parser = argparse.ArgumentParser(prog='probeCOCOATek', description='Probe TemporaryExposureKeys and Files of Exposure Notifications System in Japan a.k.a. "COCOA".', prefix_chars='-')
    parser.add_argument("command", nargs=1, default="list", metavar="COMMAND{list,zip,dl}", help="Command. 'list': Getting ZIP and TEK list with TEK distribution list. 'zip': Taking the ZIP's TEK details. 'dl': Downloading all TEK ZIP and list JSON from TEK distribution list to the specified directory.")
    parser.add_argument("param", nargs="?", default=None, metavar="COMMAND_PARAM", help="Parameter per Command. With 'list', It means aggregate unit, Either the date('date') or the date and key('key'). With 'zip', specified ZIP url. With 'dl', Specified directory for downloading.")
    parser.add_argument("-nk", "--no-keys", action='store_true', dest="no_keys", help="Without key information when printing ZIP and TEK list with TEK distribution list. Available with 'list' command.")
    parser.add_argument("-nc", "--no-cache", action='store_true', dest="no_cache", help="** Not work yet ** Do not use cache.")
    parser.add_argument("-f", "--format", choices=("text","json"), default="text", dest="format_type", help="Output format type, default is 'text'. ")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args(sys.argv[1:])

    pCT = probeCOCOATek()

    if args.command is None or args.command == "":
        command = "list"
    else:
        command = args.command[0]
    if args.param is None or args.param == "":
        if command == "list":
            command_param = 'date'
        else:
            print("Error happens, command-param is invalid.")
            return 1
    else:
        command_param = str(args.param)
    
    try:
        if command == "list":
            try:
                tek_zip_list = pCT.get_zip_list()
                if args.format_type == "text":
                    text_lines = pCT.zip_list_toText(args.no_keys)
                    print(os.linesep.join(text_lines))
                elif args.format_type == "json":
                    print(pCT.zip_list_toJson(args.no_keys))
                else:
                    print("Format type error.")
                    return 1
            except Exception as e:
                print("Error happens, when getting TEK distribution list.")
                raise e
        elif command == "zip":
            try:
                tek_bin = pCT.get_tek_content(command_param)
                if args.format_type == "text":
                    text_lines = pCT.tek_toText(tek_bin)
                    print(os.linesep.join(text_lines))
                elif args.format_type == "json":
                    print(pCT.tek_toJson(tek_bin))
                else:
                    print("Format type error.")
                    return 1
            except Exception as e:
                print("Error happens, when getting TEK ZIP detail.")
                raise e
        elif command == "dl":
            try:
                pCT.download_zips(command_param)
                print("Download done.")
            except Exception as e:
                print("Error happens, when downloading TEK ZIP and distribution list.")
                raise e
        else:
            print("Argument other error happens.")
            return 1
    except Exception as e:
        tb = sys.exc_info()[2]
        print(e.with_traceback(tb))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())