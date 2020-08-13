# probeCOCOATek
Probe TemporaryExposureKeys and Files of Exposure Notifications System in Japan a.k.a. "COCOA".

[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-4584b6.svg?style=popout&logo=python)](https://www.python.org/) ![PyPI](https://img.shields.io/pypi/v/probeCOCOATek)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Requirement

- Python 3.7+

## Install

```
pip install probeCOCOATek
```

## Usage

probeCOCOATek [-h] [-z ZIP_URL] [-ekc] [-akl] [-dl DL_DIR] [-v]

-z ZIP_URL, --zip-url ZIP_URL:  TEK Zip URL. if not set, print TEK distrubuted list.

-ekc, --each-keys-count:        Print keys count each zip with TEK distribution list. Only available when printing TEK distribution list.

-akl, --all-keys-list:          Print a list of all keys for each ZIP, instead of TEK distribution list. Other options are ignored.

-dl, --dl-zip:                  Specified directory for downloading all TEK ZIP and list JSON from TEK distribution list. Other options are ignored.

-h, --help:                     show this help message and exit

-v, --version:                  show program's version number and exit

## Exsamples

1. TEK Distribution List

```$ probeCOCOATek```

```
#     Created                      TEK URL
   0  [2020-07-25 11:00:09+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/366.zip]
   1  [2020-07-25 16:00:18+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/389.zip]
   2  [2020-07-25 17:00:15+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/402.zip]
   3  [2020-07-25 18:00:11+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/415.zip]
   4  [2020-07-25 21:00:08+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/416.zip]
   :
 146  [2020-08-09 00:00:06+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/693.zip]
 147  [2020-08-09 00:00:06+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/694.zip]
 148  [2020-08-09 00:00:06+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/695.zip]
ZIP Count:         149
```

2. TEK Zip Detail

```$ probeCOCOATek -z https://covid19radar-jpn-prod.azureedge.net/c19r/440/638.zip```

```
start_timestamp: [2020-07-27 09:00:00+0900]
end_timestamp:   [2020-07-28 09:00:00+0900]
region:          [440]
batch_num:       [1]
batch_size:      [1]
signature_infos:
    verification_key_version:      [v1]
    verification_key_id:           [440]
    signature_algorithm:           [1.2.840.10045.4.3.2]
Keys:  (Count: [17])
    [001]:[12e603645fd3475c4c74ee8bdebcb5af]
       [transmission_risk_level       ]:[0]
       [rolling_start_interval_number ]:[2659680]
       [rolling_period                ]:[144]
    [002]:[8a0fe13019472a31f3426a1c94c3eb1b]
       [transmission_risk_level       ]:[0]
       [rolling_start_interval_number ]:[2659680]
       [rolling_period                ]:[144]
    :
```

3. TEK Keys List

```$ probeCOCOATek -akl```

```
#            Created                      TEK Data
   1:1       [2020-07-25 11:00:09+0900]   [40ea03a8cb3ad80df3b330b6493c69da]
   2:2       [2020-07-25 16:00:18+0900]   [8ea050eea9f05f46630a178f6fcd0f74]
   3:3       [2020-07-25 17:00:15+0900]   [3bd0b1143dae2661b1272a189a6ad463]
   4:4       [2020-07-25 18:00:11+0900]   [985e35726ff00045d8d107fd129d2528]
   5:5       [2020-07-25 21:00:08+0900]   [3fad7513f520e9ba6c9a4c3692137c79]
   6:6       [2020-07-25 22:00:10+0900]   [d59e8078beb674868c0d55cd4da6f134]
   7:7       [2020-07-26 13:00:08+0900]   [52a6cc952a072fa958619312e9b86701]
   8:8       [2020-07-26 13:00:08+0900]   [80ab4fd273709052fe1b1b1717b45fe2]
   9:9       [2020-07-26 16:00:14+0900]   [2363bbf84bc65aae0acb7477aedfe0da]
  10:10      [2020-07-26 16:00:17+0900]   [a44834b836c2302bf4031e36088f4f8a]
  11:11      [2020-07-26 17:00:06+0900]   [14bb779490ee2d38bbc199f8a35b98e8]
  11:12      [2020-07-26 17:00:06+0900]   [2d5bb13d05598f72af48cdd3c9db7223]
  12:13      [2020-07-26 17:00:08+0900]   [522a23219d005dab77e0efca677c48c3]
  12:14      [2020-07-26 17:00:08+0900]   [2e91f101edfaca20cd264182cabb2917]
  13:15      [2020-07-27 12:00:23+0900]   [5e3ee001bc705e596c0eb1f97fe131fc]
  14:16      [2020-07-27 12:00:24+0900]   [1714b924e7da1438172f03d264456c92]
  15:17      [2020-07-27 12:00:24+0900]   [246bbb6325c48829d44f00dfb373a9e3]
  16:18      [2020-07-27 14:00:12+0900]   [57103c17ce1fa8c74d52763cd75efe63]
  :
 149:1783    [2020-08-09 00:00:06+0900]   [e6fb3c70e5b931a53273061cab111851]
 149:1784    [2020-08-09 00:00:06+0900]   [58164ebfbf9a62c73e032014b69991fd]
 149:1785    [2020-08-09 00:00:06+0900]   [251ba0a4da50d516161d64ca0100c495]
ZIP Count:         149
Keys Count:       1785
```

4. Download all TEK ZIP

```$ probeCOCOATek -dl tek_dir```

```
Download done.
```

## CAUTION

**In Japan, the interval to access the server MUST BE AT LEAST 1 SEC to avoid being arrested by the Okazaki Police Department or the Kanagawa Prefectural Police, Therefore, some options are very slow.**

[Librahack Incident (Japanese)](https://ja.wikipedia.org/wiki/%E5%B2%A1%E5%B4%8E%E5%B8%82%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%9B%B3%E6%9B%B8%E9%A4%A8%E4%BA%8B%E4%BB%B6, "Librahack Incident (Japanese)")

## License

MIT

Copyright (c) 2020 rocaz.net

## See Also

https://developers.google.com/android/exposure-notifications/exposure-notifications-api

https://developer.apple.com/documentation/exposurenotification
