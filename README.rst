probeCOCOATek
=============

Probe TemporaryExposureKeys and Files of Exposure Notifications System
in Japan a.k.a. “COCOA”.

|Python: 3.6+| |PyPI|

|License: MIT|

|GitHub Actions| |codecov|

CAUTION
-------

**In Japan, the interval to access the server MUST BE AT LEAST 1 SEC to
avoid being arrested by the Okazaki Police Department or the Kanagawa
Prefectural Police, Therefore, some options are very slow.**

`Librahack Incident
(Japanese) <https://ja.wikipedia.org/wiki/%E5%B2%A1%E5%B4%8E%E5%B8%82%E7%AB%8B%E4%B8%AD%E5%A4%AE%E5%9B%B3%E6%9B%B8%E9%A4%A8%E4%BA%8B%E4%BB%B6,>`__

Requirement
-----------

-  Python 3.6+
-  pandas 1.1.0+

Install
-------

::

   pip install pandas
   pip install probeCOCOATek

Usage
-----

probeCOCOATek [-h] [-nk] [-nc] [-f {text,json}] [-v]
COMMAND{list,zip,dl} [PARAM]

COMMAND{list,zip,dl}:

Command. ‘list’: Getting ZIP and TEK list with TEK distribution list.
‘zip’: Taking the ZIP’s TEK details. ‘dl’: Downloading all TEK ZIP and
list JSON from TEK distribution list to the specified directory.

PARAM:

Parameter per Command. With ‘zip’, specified ZIP url or filename. With
‘dl’, Specified directory for downloading.

-nk, –no-keys: Without key information when printing ZIP and TEK list
with TEK distribution list. Available with ‘list’ command.

-nc, –no-cache: \*\* Not work yet \*\* Do not use cache.

-f {text,json}, –format {text,json}: Output format type, default is
‘text’.

-h, –help: show this help message and exit

-v, –version: show program’s version number and exit

Exsamples
---------

1. TEK Distribution List

``$ probeCOCOATek list``

::

   #     Created                      ZIP URL / Key Data                                                 KeyCount
      1  [2020-08-03 16:23:04+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/609.zip]     [  10]
       1                              [caab200e81f6f0e208d385771c7a844c]
       2                              [270b8c5c3f9ec1c28cb2bb94468d78ab]
       3                              [db0aca0fe8afdd86eb46c03ba9a2579d]
       4                              [d4a1664a7335e28e997864702e4f2537]
       5                              [c3f85d781f070df6781a90eaf726637a]
       6                              [1c1a00dae53dbe92c54ff03f1086ea5e]
       7                              [33ea25d015aae4f683875a0ea5998f35]
       8                              [0b8fc787cc4adda36a3bb539e7486980]
       9                              [5c34250f7f2986b43e94d09ae295e44a]
      10                              [76fed3b413d6f4c3bf14e1d092598727]
      2  [2020-08-04 00:00:22+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/630.zip]     [   5]
       1                              [26d1dd4b972bdbdcdcdaa6706b3f3bee]
       2                              [50bf85a6b53d41b830b718c3298f301b]
       3                              [3b50fd16f9bf68c319a758c473ea9842]
       4                              [4d445838c792716b7e40b1dc8d23b386]
       5                              [6a9b318bbc0efafbed7e4938f2d6d2ce]
       :
      29                              [ff53ed3d71a2c24ccfc8f323e1c023d0]
      30                              [81122959f8738766fcf89da1f5ec5242]
      31                              [95a063d51ab208934b687d91a3179bc5]
      32                              [fcdd23cbe642b5ea9a3555ca94d6ba45]
   ZIP Count:               118
   Keys Total Count:       1985

2. TEK Distribution List without keys

``$ probeCOCOATek list -nk``

::

   #     Created                      ZIP URL                                                            KeyCount
      1  [2020-08-03 16:23:04+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/609.zip]     [  10]
      2  [2020-08-04 00:00:22+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/630.zip]     [   5]
      3  [2020-08-05 00:00:09+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/631.zip]     [  20]
      4  [2020-08-05 00:00:11+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/632.zip]     [  19]
      5  [2020-08-06 00:00:26+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/651.zip]     [  27]
      6  [2020-08-06 00:00:27+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/652.zip]     [  28]
      7  [2020-08-06 00:00:27+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/653.zip]     [  29]
      8  [2020-08-07 00:00:07+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/657.zip]     [  16]
      9  [2020-08-07 00:00:09+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/658.zip]     [  17]
     10  [2020-08-07 00:00:15+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/665.zip]     [  17]
      :
    115  [2020-08-18 00:00:24+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/809.zip]     [  28]
    116  [2020-08-18 00:00:25+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/810.zip]     [  30]
    117  [2020-08-18 00:00:25+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/811.zip]     [  30]
    118  [2020-08-18 00:00:25+0900]   [https://covid19radar-jpn-prod.azureedge.net/c19r/440/812.zip]     [  32]
   ZIP Count:               118

3. TEK Zip Detail

``$ probeCOCOATek zip https://covid19radar-jpn-prod.azureedge.net/c19r/440/638.zip``

or

``$ probeCOCOATek zip /foo/bar/638.zip``

::

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

4. Download all TEK ZIP

``$ probeCOCOATek dl tek_dir``

::

   Download done.

License
-------

MIT

Copyright (c) 2020 rocaz.net

See Also
--------

https://developers.google.com/android/exposure-notifications/exposure-notifications-api

https://developer.apple.com/documentation/exposurenotification

.. |Python: 3.6+| image:: https://img.shields.io/badge/Python-3.6+-4584b6.svg?style=popout&logo=python
   :target: https://www.python.org/
.. |PyPI| image:: https://img.shields.io/pypi/v/probeCOCOATek
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |GitHub Actions| image:: https://github.com/rocaz/probeCOCOATek/workflows/GitHub%20Actions/badge.svg
.. |codecov| image:: https://codecov.io/gh/rocaz/probeCOCOATek/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/rocaz/probeCOCOATek
