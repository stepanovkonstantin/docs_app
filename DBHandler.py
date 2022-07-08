import json
from datetime import datetime
ltimestamp = datetime.now()

session_data = {
    'last_uniq_id': 1,
    'last_user_authorized': 'none',
    'last_user_action': 'none',
    'last_user_action_ts': str(ltimestamp),
    'last_db_saved_ts': '2021-10-15 02:14:11.298713'
}

docs_type = {
    0: ['Unspecified type', ['']],
    11: ['passport', ['birth date', 'birth place', 'issuing authority', 'authority code', 'registration address', 'registration date']],
    12: ['international passport', ['gender', 'birth date',  'issuing authority']],
    13: ['drivers license', ['birth date', 'allowed categories', 'special notes']],
    19: ['vehicle registration certificate',
         ['reg number', 'vehicle passport id', 'VIN', 'manufacture brand', 'vehicle body type', 'engine hps', 'engine volume', 'vehicle weigth', 'vehicle color']
         ],
    22: ['taxpayer ID', ['issuing authority']],
    23: ['civil insurance ID', []],
    24: ['medical insurance ID', []],
    25: ['military ID', ['birth date', 'retirement date', 'initial category', 'eventual actegory']],
    31: ['birth certificate', ['issuing authority', 'birth date', 'gender', 'place of birth']],
    32: ['marriage certificate', ['issuing authority', 'marriage date', 'spouses gender', 'spouses first name', 'spouses last name']],
    33: ['death certificate', ['issuing authority', 'date of death', 'death reason']],
    34: ['credentials change certificate', ['issuing authority', 'old first name', 'old last name']],
    35: ['divorce certificate', ['issuing authority', 'date of divorce', 'spouses gender', 'spouses first name', 'spouses last name']],
    40: ['ownership certificate (unspecified)', ['issuing authority', 'property', 'date of ownership', 'property registration place']],
    41: ['vehicle passport',
         ['vehicle owner name', 'date of ownership', 'VIN', 'manufacture', 'vehicle type', 'engine hps', 'engine volume', 'vehicle weigth', 'vehicle color']
         ],
    43: ['realty ownership certificate', ['issuing authority', 'date of ownership']],
    51: ['bank account', ['account id']]
}
#
# doc1 = {
#     'id': 1,
#     'dir': 2,
#     'type': 11,
#     'ts': '2021-10-15 02:14:11.298713',
#     'data': {
#         'document id': {'serial': '4123', 'number': '123450'},
#         'owners name': {'first name': 'Konstantin', 'last name': 'Stepanov', 'patronymic': 'Evgenevich'},
#         'date of issue': '02-06-2021',
#         'type_specific': {
#             'birth date': '21-09-1988',
#             'birth place': 'Moscow',
#             'issuing authority': 'GU MVD RUSSIAN FEDERATION',
#             'authority code': '770-121',
#             'registration address': 'Moscow, Feodosiyskaya st., 7-5-5',
#             'registration date': '18-09-2019'
#         }
#     }
# }
#
# doc2 = {
#     'id': 2,
#     'dir': 2,
#     'type': 13,
#     'ts': '2021-10-15 02:14:11.298713',
#     'data': {
#         'document id': {'serial': '9909', 'number': '270379'},
#         'owners name': {'first name': 'Konstantin', 'last name': 'Stepanov', 'patronymic': 'Evgenevich'},
#         'date of issue': '14-06-2018',
#         'type_specific': {
#             'birth date': '21-09-1988',
#             'allowed categories': 'B,C',
#             'special notes': 'n/a'
#         }
#     }
# }

doc3 = {
    'id': new_uniq_id(),
    'dir': 2,
    'type': 13,
    'ts': '2021-10-15 02:14:11.298713',
    'data': {
        'document id': {'serial': '9909', 'number': '270379'},
        'owners name': {'first name': 'Konstantin', 'last name': 'Stepanov', 'patronymic': 'Evgenevich'},
        'date of issue': '14-06-2018',
        'type_specific': {
            'birth date': '21-09-1988',
            'allowed categories': 'B,C',
            'special notes': 'n/a'
        }
    }
}
# json.dump(session_data, docsdb_input, sort_keys=False, indent=4)
# docsdb_input.write(',')

docsdb_input = open('docsdb.json', 'w')
json.dump(doc3, docsdb_input, sort_keys=False, indent=4)
docsdb_input.close()
# print(json.dumps(session_data, sort_keys=False, indent=4))
# print(json.dumps(doc_str1, sort_keys=False, indent=4))