def read_csv_file(file):
    csv_input = open(file, 'r+')
    locations_dict = {}
    for line in csv_input.readlines():
        linenoend = line.replace('\n', '')
        line_split = list(linenoend.split(';'))
        locations_list = []
        for i in range(0,10):
            locations_list.append(str(line_split[i+2]))
        locations_dict[line_split[0]] = locations_list
    csv_input.close()
    return locations_dict

def parse_locations(locations_dict):
    locations_out = {}
    for area_name, area_list in locations_dict.items():

        locations_out[str(area_name) + ';LAC_2G/3G'] = (area_list[0],area_list[1])
        locations_out[str(area_name) + ';Femto_LAC'] = (area_list[2], area_list[3])
        locations_out[str(area_name) + ';Super_Femto_LAC'] = (area_list[4], area_list[5])
        locations_out[str(area_name) + ';CFSB_LAC'] = (area_list[6], area_list[7])
        locations_out[str(area_name) + ';TAC'] = (area_list[8], area_list[9])
    return locations_out

def save_to_files(locations_out, file):
    file_out = open(file, "w")
    for area_code, area_values in locations_out.items():
        line_str = ''
        for area_value in area_values:
            line_str = line_str + ";" + area_value
        wline = area_code + line_str + "\n"
        file_out.write(wline)
    file_out.close()
    return

def main():
    locations_dict = read_csv_file('./saved/ST-092-5_LAC_TAC.csv')
    #print(locations_dict)
    locations_out = parse_locations(locations_dict)
    #print(locations_out)
    save_to_files(locations_out,'./saved/ST-092-5_LAC_TAC_parsed.csv')

main()