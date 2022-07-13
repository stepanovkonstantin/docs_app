import sqlite3
import csv

def get_string_ri(index, c):
    data_out = {}
    get_select = c.execute('SELECT id, LOCATION_AREA_CODE, NETWORK_OPERATOR_CODE, HOST_CODE FROM DB_LAC_RI WHERE id = ?', [index])
    for row in get_select:
        data_out = {'lac': row[1], 'netopcode': row[2], 'host_code': row[3]}
        print(data_out['netopcode'])
    return data_out

def get_location_info(lac, c):
    data_out = {}
    get_select = c.execute('select * FROM db_st0925 ds where (zone_code_start <= ? AND zone_code_end >= ?)', (lac, lac))
    for row in get_select:
        data_out = {'region_name' : row[0], 'zone_type' : row[1], 'zone_start' : row[2], 'zone_end' : row[3]}
    return data_out

def get_zone_info(zone_name, c):
    zone_info = {}
    opcode = ''
    get_select_opcode = c.execute('select network_operator from regions2netopcode where region_name like ?', [zone_name])
    for row in get_select_opcode:
        opcode = str(row[0])
        print(opcode)
    get_select_zone_info = c.execute('select * from rus_regions where provider like ?', [opcode])
    for row in get_select_zone_info:
        zone_info = {'provider': row[0], 'sdp_zone': row[2], 'sdp_region_name': row[1], 'macroregion': row[4]}
    return zone_info, opcode

def put_location_list(location_file, location_data):
    with open(location_file, 'a', newline='') as f:
        write = csv.writer(f, delimiter=';', lineterminator="\n")
        write.writerows(location_data)
    return

def main_cycle(count_i, c, out_file):
    location_info_out = []
    with open(out_file, "w") as f:
        write = csv.writer(f, delimiter=';', lineterminator="\n")
        write.writerow(["RI_LAC", "RI_NETWORK_OPERATOR_CODE", "RI_HOST_CODE", "STATUS", "REGION_NAME", "ZONE_CODE_TYPE", "LAC_START", "LAC_END", "SDP_PROVIDER", "SDP_REGION", "SDP_REGION_NAME", "SDP_MACROREGION"])
    count_i = count_i + 1
    for index in range(1, count_i):
        select_zone_info = {}
        select_ri = get_string_ri(str(index), c)
        select_locinfo = get_location_info(select_ri['lac'], c)
        if 'region_name' in select_locinfo.keys():
            select_zone_info, select_opcode = get_zone_info(select_locinfo['region_name'], c)
            if str(select_ri['netopcode']).lower() == select_opcode.lower():
                select_ri['status'] = "ok"
            else:
                select_ri['status'] = "delete"
        else:
            select_ri['status'] = "non-existent"
            select_locinfo = {'region_name' : 'n/a', 'zone_type' : 'n/a', 'zone_start' : 'n/a', 'zone_end' : 'n/a'}
            select_zone_info = {'provider': 'n/a', 'sdp_zone': 'n/a', 'sdp_region_name': 'n/a', 'macroregion': 'n/a'}

        location_info_str = [
            select_ri['lac'],
            select_ri['netopcode'],
            select_ri['host_code'],
            select_ri['status'],
            select_locinfo.get('region_name'),
            select_locinfo.get('zone_type'),
            select_locinfo.get('zone_start'),
            select_locinfo.get('zone_end'),
            select_zone_info.get('provider'),
            select_zone_info.get('sdp_zone'),
            select_zone_info.get('sdp_region_name'),
            select_zone_info.get('macroregion')
        ]

        location_info_out.append(location_info_str)
    return location_info_out

def main(db, out_file):
    global count_i
    global c
    conn = sqlite3.connect(db)
    c = conn.cursor()
    count_strngs = c.execute('SELECT COUNT(*) FROM DB_LAC_RI')
    for row in count_strngs:
        count_i = int(row[0])
    location_info_out = main_cycle(count_i, c, out_file)
    put_location_list(out_file, location_info_out)


main('./db/locations.db', './saved/locations_ri_analyze.csv')
