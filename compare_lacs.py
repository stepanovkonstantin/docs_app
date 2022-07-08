
def read_csv_file(file):
    csv_input = open(file, 'r+')
    locations_list = {}
    for line in csv_input.readlines():
        linenoend = line.replace('\n', '')
        line_split = list(linenoend.split(';'))
        locations_list[line_split[0]] = line_split[1:]
    csv_input.close()
    return locations_list

def save_to_files(loc_list, file):
    file_out = open(file, "w")
    for area_code, area_values in loc_list.items():
        line_str = ''
        for area_value in area_values:
            line_str = line_str + ";" + area_value
        wline = area_code + line_str + "\n"
        file_out.write(wline)
    file_out.close()
    return

def add_sdp_location_params(loc_list,mcc,loc_type):
    for area_code, area_params in loc_list.items():
        get_select = get_location_sdp(area_code,mcc,loc_type)
        for row in get_select:
            region_id = row[2]
            macroregion_id = row[1]
            region_name = row[0]
        loc_list[area_code].append(macroregion_id)
        loc_list[area_code].append(region_id)
        loc_list[area_code].append(region_name)
    return loc_list

def add_sdp_location_all(loc_list):
    for area_code, area_params in loc_list.items():
        get_select = get_location_sdp_all(area_code)
        for row in get_select:
            mcc = row[3]
            mnc = row[4]
            area_type = row[7]
            region_id = row[2]
            macroregion_id = row[1]
            region_name = row[0]
            area_start = row[9]
            area_end = row[12]
            append_str = str(mcc) + ',' + str(mnc) + ',' + str(area_type) + ',' + str(area_start) + ',' + str(area_end) + ',' + str(region_id) + ',' + str(region_name)
            loc_list[area_code].append(append_str)
    return loc_list


def search_location(loc_list, area):
    if area not in loc_list.keys():
        print('LAC не найден!')
    else:
        print(f'LAC: {area}\nMSC: {loc_list[area][0]}\nNETWORK OPERATOR CODE: {loc_list[area][1]}\nNETWORK OPERATOR NAME: {loc_list[area][2]}\n ')
    return

def list_raw_data(loc_list,area):
    if area in loc_list:
        print('\n', loc_list[area])
    else:
        print('LAC не найден!')
    return

def get_location_sdp(area,mcc,loc_type):
    import sqlite3
    conn = sqlite3.connect('./db/locations.db')
    c = conn.cursor()
    get_select = c.execute('SELECT * FROM LAC_SDP WHERE "DEC(AREA_CODE_START)" < ? AND "DEC(AREA_CODE_END)" > ? AND "HEX(GEO_UNIT.MCC)" = ? AND DATA_LABEL = ?', (area, area, mcc, loc_type))
    return get_select

def get_location_sdp_all(area):
    import sqlite3
    conn = sqlite3.connect('./db/locations.db')
    c = conn.cursor()
    get_select = c.execute('SELECT * FROM LAC_SDP WHERE "DEC(AREA_CODE_START)" < ? AND "DEC(AREA_CODE_END)" > ? AND MACRO_REGION_NAME NOT LIKE "SGSN"', (area, area))
    return get_select

def main(lac_ri_file=None, lac_ri_sdp_file=None):
    help = {
      'l': ['list', 'Вывод raw-data в памяти'],
      'v': ['view', 'Искать LAC'],
      'c': ['compare', 'Добавить все данные из SDP в данные RI'],
      's': ['save', 'Сохранить файл'],
      'g': ['get', 'Найти принадлежность в данных SDP и RI'],
      'a': ['all', 'Найти данные по LAC в справочнике SDP'],
      'h': ['help', 'Вывод справки по командам'],
      'e': ['exit', 'Выход из программы']
    }
    print('------------LOCATIONS READER--v1.0---------------')
    print('-------------------------------------------------')
    print('Для просмотра списка команд введите - h')
    if lac_ri_file == None:
        lac_ri_file = './saved/LAC_RI.csv'
    locations_list = read_csv_file(lac_ri_file)
    if lac_ri_sdp_file == None:
        lac_ri_sdp_file = './saved/LAC_RI_out.csv'

    user_choise = 'h'
    while user_choise != 'e':
        user_choise = input('\nВведите команду > ')
        if user_choise == 'l':
            lac = input('Введите LAC > ')
            list_raw_data(locations_list,lac)
        elif user_choise == 'v':
            lac = input('Введите LAC > ')
            search_location(locations_list,lac)
        elif user_choise == "s":
            save_to_files(locations_list, lac_ri_sdp_file)
        elif user_choise == 'c':
            add_sdp_location_all(locations_list)
        elif user_choise == 'a':
            lac = input('\nВведите LAC > ')
            get_select = get_location_sdp_all(lac)
            for row in get_select:
                print(row)
        elif user_choise == 'g':
            lac = input('\nВведите LAC > ')
            mcc = input('\nВведите MCC > ')
            loc_type = "LAC+CI"
            get_select = get_location_sdp(lac,mcc,loc_type)
            for row in get_select:
                print(row)
            search_location(locations_list,lac)
        elif user_choise == 'h':
            for cmd, cmd_desc in help.items():
                print(f'{cmd} \t- {cmd_desc[1]}')

main()