# probeCOCOATek
Probe TemporaryExposureKeys and Files of Exposure Notifications System in Japan a.k.a. "COCOA".

[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-4584b6.svg?style=popout&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Requirement

- Python 3.7+

## Usage

probeCOCOATek.py [-h] [-v] [TEK]

TEK:            TEK Zip URL. if not set, print TEK distrubuted list.

-h, --help:     show this help message and exit

-v, --version:  show program's version number and exit

## Exsamples

1. TEK Distributed List

```$ python probeCOCOATek/probeCOCOATek.py```

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
Total:       149
```

2. TEK Zip Detail

```$ python probeCOCOATek/probeCOCOATek.py https://covid19radar-jpn-prod.azureedge.net/c19r/440/638.zip```

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
keys:  (Total:      [17])
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

## License

MIT
