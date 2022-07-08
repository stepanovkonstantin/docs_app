def read_csv_file(file):
    csv_input = open(file, 'r+')
    locations_dict = {}
    for line in csv_input.readlines():
        linenoend = line.replace('\n', '')
        line_split = list(linenoend.split(';'))
        locations_dict[line_split[0]] = line_split[2:]
    csv_input.close()
    return locations_dict

def save_csv_file(locations_dict,file):
    file_out = open(file, "w")
    for area_name, area_codes in locations_dict.items():
        for area_code in area_codes:
            wline = str(area_name) + ';' + str(area_code) +'\n'
            file_out.write(wline)
    file_out.close()
    return


def main():
    locations_dict = read_csv_file('./saved/ST-092-5_MOCN.csv')
    #print(locations_dict)
    save_csv_file(locations_dict,'./saved/ST-092-5_MOCN_parsed.csv')

main()
