import sqlite3
import csv

def get_string_ri(index, c):
    get_select = c.execute('SELECT id, LOCATION_AREA_CODE, NETWORK_OPERATOR_CODE, HOST_CODE FROM DB_LAC_RI WHERE id = ?', [index])
    return get_select

def get_location_info(lac, c):
    get_select = c.execute('SELECT * FROM DB_LAC_ST0925 WHERE (LAC_Start <= ? AND Lac_End >= ?)', (lac, lac))
    return get_select

def put_location_list(location_file, location_data):
    with open(location_file, 'a') as f:
        write = csv.writer(f, delimiter=';', lineterminator="\n")
        write.writerow(location_data)
    return

def main_cycle(count_i, c, out_file):
    with open(out_file, "w") as f:
        write = csv.writer(f, delimiter=';', lineterminator="\n")
        write.writerow(["LAC", "NETWORK_OPERATOR_CODE", "HOST_ID", "STATUS", "REF_NETWORK_OPERATOR_CODE", "REGION_NAME", "LAC_START", "LAC_END", "ZONE_CODE_TYPE"])
    count_i = count_i + 1
    for index in range(1, count_i):
        get_select_ri = get_string_ri(str(index), c)
        for row in get_select_ri:
            location_data_out = [row[1], row[3], row[2]]
        loc_info = get_location_info(location_data_out[0], c)
        for row in loc_info:
            if row[0] == None:
                location_data_out.append("non-existent")
            if str(location_data_out[2]) == str(row[1]):
                location_data_out.append("ok")
                location_data_out.append(row[1])
                location_data_out.append(row[0])
                location_data_out.append(row[3])
                location_data_out.append(row[4])
                location_data_out.append(row[2])
            else:
                location_data_out.append("delete")
                location_data_out.append(row[1])
                location_data_out.append(row[0])
                location_data_out.append(row[3])
                location_data_out.append(row[4])
                location_data_out.append(row[2])
        put_location_list(out_file, location_data_out)

def main(db, out_file):
    global count_i
    global c
    conn = sqlite3.connect(db)
    c = conn.cursor()
    count_strngs = c.execute('SELECT COUNT(*) FROM DB_LAC_RI')
    for row in count_strngs:
        count_i = int(row[0])
    main_cycle(count_i, c, out_file)


main('./db/locations.db', './saved/locations_ri_analyze.csv')
