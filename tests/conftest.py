import pytest
import os
from probeCOCOATek.probeCOCOATek import probeCOCOATek

@pytest.fixture(scope='function', autouse=True)
def monkeypatch_expanduser(monkeypatch, tmpdir):
    # TODO: Why don't work?
    #with monkeypatch.context() as m:
    #    m.setattr('os.path.expanduser', lambda x: tmpdir)
    #    m.setattr(probeCOCOATek.probeCOCOATek.probeCOCOATek, 'interval_sec_in_japan', 0)
    monkeypatch.setattr('os.path.expanduser', lambda x: tmpdir)
    monkeypatch.setattr(probeCOCOATek, 'interval_sec_in_japan', 0)

@pytest.fixture(scope='module')
def normal_distribution_url():
    return "https://example.com/test/list.json"

@pytest.fixture(scope='module')
def normal_distribution_json():
    return                        '[{"region":"440","url":"https://example.com/test/366.zip","created":1597676424614},\
                                    {"region":"440","url":"https://example.com/test/774.zip","created":1597676424873},\
                                    {"region":"440","url":"https://example.com/test/812.zip","created":1597676425134}]'

@pytest.fixture(scope='module')
def zip_data():
    return {
                'https://example.com/test/366.zip':{
                    'start_timestamp':'2020-07-24 09:00:00+0900', 'end_timestamp':'2020-07-25 09:00:00+0900',
                    'region':'440','batch_num':1,'batch_size':1,
                    'signature_infos':{
                        'verification_key_version':'v1','verification_key_id':'440','signature_algorithm':'1.2.840.10045.4.3.2',
                    },
                    'keys':[
                        {'key_data':'40ea03a8cb3ad80df3b330b6493c69da','transmission_risk_level':0,'rolling_start_interval_number':2659248,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0}
                    ],
                    'raw_data':
                    '504b03041400000008000410f95020233547870000009b0000000a0000006578706f72742e62696e72f55670ad28c82f2a512833540002ce0615a978'\
                    '0620106428930633a4984d4c0c141835188d02b8c4b30af4d2f3f5723372caf592f3cb32530c2d8b1253128b847049483195192a810cd01236d433d2'\
                    'b33031d03334303031d533d133d633b292e1127078c5bce2b4d50ddecf9b0db679da64de126090d8b07c11a3c2044600000000ffff0300504b030414'\
                    '00000008000410f950e5688af698000000a20000000a0000006578706f72742e736967e29acfc815c0259e55a0979eaf979b9153ae979c5f96996268'\
                    '599498925824844b428aa9cc5089d9c4c4404bd850cf48cfc2c440cfd0c0c0c454cf44cf58cf4880518251c9ddc09549c1e85fce5bf5770ed66b9d59'\
                    '17298a6c5fad315bf8f3d9a5ff799f1a55ed38a8d81ccda4c8f0bf71a3d9ac5715ca699743d33c37e62829ae3a68d572d12486ffd877919e9f771901'\
                    '000000ffff0300504b010214001400000008000410f95020233547870000009b0000000a00000000000000000000000000000000006578706f72742e'\
                    '62696e504b010214001400000008000410f950e5688af698000000a20000000a00000000000000000000000000af0000006578706f72742e73696750'\
                    '4b05060000000002000200700000006f0100000000'},
                'https://example.com/test/774.zip':{
                    'start_timestamp':'2020-08-02 09:00:00+0900', 'end_timestamp':'2020-08-03 09:00:00+0900',
                    'region':'440','batch_num':1,'batch_size':1,
                    'signature_infos':{
                        'verification_key_version':'v1','verification_key_id':'440','signature_algorithm':'1.2.840.10045.4.3.2',
                    },
                    'keys':[
                        {'key_data':'5ced4b2dec081fcea50a42255338eff5','transmission_risk_level':0,'rolling_start_interval_number':2660544,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'b38c0d52d91e3a943855629a8be913af','transmission_risk_level':0,'rolling_start_interval_number':2660544,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'5f6b493f4490910cb143e249eb32d2cb','transmission_risk_level':0,'rolling_start_interval_number':2660544,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'92cb692ae1359da107319ce5310b6add','transmission_risk_level':0,'rolling_start_interval_number':2660544,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'7be2506466fc8b95d843f382880be0d9','transmission_risk_level':0,'rolling_start_interval_number':2660544,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0}
                    ],
                    'raw_data':
                    '504b030414000000080003780f51c342d271d4000000130100000a0000006578706f72742e62696e72f55670ad28c82f2a5128335400024e0626b578'\
                    '0620106c08560733a4984d4c0c141835188d02b8c4b30af4d2f3f5723372caf592f3cb32530c2d8b1253128b847049483195192a810cd01236d433d2'\
                    'b33031d03334303031d533d133d633b292e1128879ebadfb8643fedc522e27d5608bf75f0518240e6c5cc4a830811124bbb98737e8a69cd5148bd0a4'\
                    '59dd2f85d7a3cac6677bdabb4c98c8b3d1f991e76ba34ba75165279dced47a683a7721bbe19ca786dc59775165ab1f05a4a4fde99e7ac3f9735307f7'\
                    '839b085900000000ffff0300504b030414000000080003780f515ec19c7196000000a10000000a0000006578706f72742e736967e29ac7c815c0259e'\
                    '55a0979eaf979b9153ae979c5f96996268599498925824844b428aa9cc5089d9c4c4404bd850cf48cfc2c440cfd0c0c0c454cf44cf58cf4880518251'\
                    'c9cdc0854981c778fe2c1719f52f51cb942e09c4d4c534729c9e6c927db1362425aaf0d2aaab214c0ad9a7d6156999c86a5576553777cfe1e198f860'\
                    '4e59f22cc51eaf89f79d269e7a9706000000ffff0300504b0102140014000000080003780f51c342d271d4000000130100000a000000000000000000'\
                    '00000000000000006578706f72742e62696e504b0102140014000000080003780f515ec19c7196000000a10000000a00000000000000000000000000'\
                    'fc0000006578706f72742e736967504b0506000000000200020070000000ba0100000000'},
                'https://example.com/test/812.zip':{
                    'start_timestamp':'2020-08-16 09:00:00+0900', 'end_timestamp':'2020-08-17 09:00:00+0900',
                    'region':'440','batch_num':1,'batch_size':1,
                    'signature_infos':{
                        'verification_key_version':'v1','verification_key_id':'440','signature_algorithm':'1.2.840.10045.4.3.2',
                    },
                    'keys':[
                        {'key_data':'85ca24b815863adfa8555e4124e3421e','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'51af14515309f878d8d66897776ee012','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'c9f2a35c558e5e45c06abbbeab5bd657','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'722c706dc0c8dfa30691942e3bb4b2ca','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'bb98d27dd685131df8f1d173c78d8fe4','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'1b74130f39c3ac9a5a707646bdbdc6e3','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'4b79b4384b483c18a57e60b09415ab9a','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'fb72d04dbff16b81684578b0ba29326d','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'32fc05108893d671a13532becbfbb2a8','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'e13c1214971a381b2a42404ad3f84619','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'98e859e1af50e8cec820c63a9646a34d','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'256ce9e6f47870b083c42b45378153ff','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'2a5744b3e5d0e03926d02a68fd557989','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'03f3486f99e1943327fcda772bffc4c1','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'79ef78edbeeeaf3f2f7a591a72b15b70','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'730b19585edd0d61e7e5611aa81e062b','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'217d8b034354cd4e72c7f864e5d06241','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'e250f3c4aeaab88f0cdb9e35d330c564','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'ce462fed29dcbe3534e342766bf98e07','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'130a379c5642e9b007c5ec428450be70','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'2057e4ad10799ac4b8a3e1d615562c68','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'4b735e60f6a8f4fead475369d82a8e3e','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'1c879d376dd151d364648569c6ec9ee9','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'70c00386f07c7398b7eb1b5d8cde17fd','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'9b2a346f1e2bd2e12699625a58067349','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'57c85e9394e34fb41fa3f6cd6007e36f','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'68ab04d7187cffde41d4115992729bbb','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'c00f19f46381cb98799e99e9243cf056','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'ff53ed3d71a2c24ccfc8f323e1c023d0','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'81122959f8738766fcf89da1f5ec5242','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'95a063d51ab208934b687d91a3179bc5','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                        {'key_data':'fcdd23cbe642b5ea9a3555ca94d6ba45','transmission_risk_level':0,'rolling_start_interval_number':2662560,'rolling_period':144,'report_type':0, 'days_since_onset_of_symptoms':0},
                    ],
                    'raw_data':
                    '504b03041400000008000c78115147709fb2d10200003d0400000a0000006578706f72742e62696e72f55670ad28c82f2a5128335400024e86728b78'\
                    '0620106c3861096648319b981828306a301a0570896715e8a5e7ebe566e494eb25e79765a6185a1625a6241609e19290622a33540219a0256ca867a4'\
                    '676162a06768606062aa67a267ac676425c325d07a4a6587689bd5fd15a1718e2a8f9de4041824161c5cc4a8308111241bb85e243098f347c58d6b19'\
                    'd3cbf31e08a1ca9efcb43826b42fcef540d6ee7daba3af85a3ca16e914e41e38717f31dbc4297ad65b369d4295dd3de352edb55661d91f1f2f161fef'\
                    'ed7f822a2b5d22cc6f7978cdaca88232b7bd7b8f3d4695f5aedc62e1ed6123b1b42e61c314d1d5b350657f175df0ddff31bb31c3b562c32e4da35c54'\
                    '59a33fac021d93af152e3435da77faf7a615a8b20f6d8444a64b59486b3939785dfee126892a3be345e4c3f5012fce9d50386635cd6db12faaac6ace'\
                    'cb675f2a0a36341fd176356f0cfe8f2aab15eeb2f9e98507966a17b432fe865676a2ca327ff6c89ff9708ab1fa9f5be5daff8f1c4495ad7c5ff176df'\
                    'bbf5f6fa559152451ba30b50658bb92523e2eef2263e7f9a28b5428e4d1b5556b1b69bd939e4ac5fd1f11f294f2f2439a2ca3e0af87c64ddaa1dfd3c'\
                    'b7e7995e36389a822a7bce4dffade69d7da6268f9dcab27ff6b1a3ca0a7399cf09737ab981fde81ba796807d68ae52087fb256a072d6911d8b1f5e13'\
                    '0dd3c9408bc1e2b8846f2bbefc5beb1e9c7943abcf0e5556a67dae79eec5c0cb2929ad99c7decc7b892a5b7080b9ed434df18cedafa5637bee89ff45'\
                    '959dad65922fa77de9a1dacca4a808b6624f54d9f0137193a73cf6df22bff8dbd904f6c7f9a8b219ab59ae4bd4fcbfe77845307252d1ecdda8b207f8'\
                    '25bf24379e9e51396fe64b159b0f61a8b2ff83dfda162e3ae473fec467e58707942fa0ca360a6946fe286e4ffbf363eec2af6f829c5065a72e48be2a'\
                    'b58963b27746edc4c5e2b38fa2cafeb9ab7cfa99d3d657b34c434f4db9b6cb15210b000000ffff0300504b03041400000008000c781151f7ea1c8198'\
                    '000000a20000000a0000006578706f72742e736967e29acfc815c0259e55a0979eaf979b9153ae979c5f96996268599498925824844b428aa9cc5089'\
                    'd9c4c4404bd850cf48cfc2c440cfd0c0c0c454cf44cf58cf4880518251c9ddc09549817fb690e4f61faf2a16f9fe3edddedd64b2c0677dfb9269bc1b'\
                    '7543dfdd989d31b39b4991e1ff31dbf6593cc1f38c7f9bf5cf083399be606ba704db2bc5f36e2a319af5e727b803000000ffff0300504b0102140014'\
                    '00000008000c78115147709fb2d10200003d0400000a00000000000000000000000000000000006578706f72742e62696e504b010214001400000008'\
                    '000c781151f7ea1c8198000000a20000000a00000000000000000000000000f90200006578706f72742e736967504b05060000000002000200700000'\
                    '00b90300000000'}
        }

@pytest.fixture(scope='module')
def invalid_zip_data():
    return          '00'


