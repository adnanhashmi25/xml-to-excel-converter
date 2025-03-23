import os
import re
import csv
import tarfile
import re
from datetime import datetime
import zipfile
import sys
# import psutil

print('xml to excel Tool \n \n \n')

def check_folder(folder_path):
    if not folder_path:
        return True
    if not os.path.isdir(folder_path):
        print(f"Folder {folder_path} does not exist")
        input('\n Press any key to continue')
        sys.exit()

current_date = datetime.now().date()
june_30 = datetime(2025, 6, 30).date()
if current_date > june_30:
    print("Tool license expired, please check with admin")
    input('\n Press any key to continue')
    sys.exit()

current_dir = os.getcwd()
input_folder = input('Please enter input folder path or enter for default path:')
f_flag = check_folder(input_folder)
if f_flag:
    input_folder = os.path.join(current_dir,'input')
output_folder = input('Please enter output folder path or enter for default path:')
f_flag = check_folder(output_folder)
if f_flag:
    output_folder = os.path.join(current_dir,'output')
input_conf_folder = input('Please enter input_config folder path or enter for default path:')
f_flag = check_folder(input_conf_folder)
if f_flag:
    input_conf_folder = os.path.join(current_dir,'input_config')
output_zip = input_folder.rstrip('/\\') + '_zip'
if not os.path.exists(output_zip):
    os.makedirs(output_zip)
file_list = os.listdir(input_folder)
data_count = {}

# Initialize psutil process to track memory usage
# process = psutil.Process(os.getpid())


def get_site_list():
    site_list = set()
    site_list_csv = os.path.join(input_conf_folder,'site_list.csv')
    with open(site_list_csv,'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            site_list.add(row[0])
    return site_list

def get_mo_list():
    mo_list = {}
    mo_list_csv = os.path.join(input_conf_folder,'MO_list.csv')
    with open(mo_list_csv,'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            key  = row[1] + '_' + row[0]
            if key not in mo_list:
                mo_list[key] = []
            if row[2]:
                mo_list[key].append(row[2])
    return mo_list

def get_bracket(type):
    csv_path = os.path.join(current_dir, 'config')
    csv_path = os.path.join(csv_path, type + '.csv')
    check = {}
    with open(csv_path,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] not in check:
                check[row[0]] = []
            check[row[0]].append(row[1])
    # for key in check:
    #     for row in check[key]:
    #         if key == 'managed-element/hardware-management/radio-unit/radio-unit-info':
    #             print(row)
    return check

def write_to_excel(data,file_type):
    out_path = os.path.join(output_folder, file_type)
    mo_list = get_mo_list()
    header = []
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for key in data:
        out_name = key.split('/')[-1] + '.csv'
        key_c = key + '_' + file_type
        if mo_list and key_c not in mo_list:
            continue
        if key_c not in data_count:
            data_count[key_c] = [0,out_name]
        if not os.path.exists(os.path.join(out_path, data_count[key_c][1])):
            with open(os.path.join(out_path, data_count[key_c][1]),'a',newline='') as output_file:
                csv_writer = csv.writer(output_file)
                if key_c == 'managed-element/ip-system/cpu/ip-interface/external-interfaces/ipv6-address_DU':
                    header = ['site_name','module','cpu-id','interface-name','ip','prefix-length','ip-get-type','ip-oper','prefix-length-oper','address-state','bearer-link-rate','management','control','bearer','ieee1588']
                    csv_writer.writerow(header)
                else:
                    brac_h = re.findall(r'\[([^\]=]+=[^\]]+)\]', data[key][0][1])
                    h_temp = []
                    for h in brac_h:
                        h_temp.append(h.split('=')[0])
                    header = ['site_name', 'module'] + h_temp
                    prev_val = ''
                    for line in data[key]:
                        if not prev_val:
                            prev_val = line[1]
                        if prev_val != line[1]:
                            break
                        else:
                            if mo_list and mo_list[key_c]:
                                if line[2] in mo_list[key_c]:
                                    header.append(line[2])
                            else:
                                header.append(line[2])
                    csv_writer.writerow(header)
        
        with open(os.path.join(out_path, data_count[key_c][1]),'a',newline='') as output_file:
            csv_writer = csv.writer(output_file)
            curr_hierarchy = ''
            temp = []
            for line in data[key]:
                hierarchy = line[1]
                # print(hierarchy)
                if not curr_hierarchy:
                    curr_hierarchy = hierarchy
                # data_count[key_c][0] += 1
                try:
                    brac = re.findall(r'\[([^\]=]+=[^\]]+)\]', line[1])
                    # print(brac)
                    if not temp:
                        temp.append(line[0])
                        temp.append(key)
                        for b in brac:
                            temp.append(b.split('=')[1])
                    if curr_hierarchy !=  hierarchy:
                        # print(temp)
                        if key_c == 'managed-element/ip-system/cpu/ip-interface/external-interfaces/ipv6-address_DU' and len(temp) == 14:
                            temp = temp[:10] + [''] + temp[10:]
                        data_count[key_c][0] += 1
                        csv_writer.writerow(temp)
                        temp = []
                        curr_hierarchy = hierarchy
                        temp.append(line[0])
                        temp.append(key)
                        for b in brac:
                            temp.append(b.split('=')[1])
                        if mo_list and mo_list[key_c]:
                            if line[2] in mo_list[key_c]:
                                temp.append(line[-1])
                        else:
                            temp.append(line[-1])
                    else:
                        if mo_list and mo_list[key_c]:
                            if line[2] in mo_list[key_c]:
                                temp.append(line[-1])
                        else:
                            temp.append(line[-1])
                    # line = [line[0]] + [key] + temp + line[2:]
                    # csv_writer.writerow(line)
                    if data_count[key_c][0] > 900000:
                        if '_' not in data_count[key_c][1]:
                            out_name = key.split('/')[-1] + '_1' + '.csv'
                            data_count[key_c][1] = out_name
                        else:
                            var = data_count[key_c][1].split('_')[-1].rstrip('.csv')
                            var = int(var) + 1
                            out_name = key.split('/')[-1] + '_' + str(var) + '.csv'
                            data_count[key_c][1] = out_name
                        data_count[key_c][0] = 0
                except IndexError as e:
                    print(e)
            if temp:
                csv_writer.writerow(temp)
                temp = []


def process_xml(content,file_name):
    data={}
    hierarchy = 'managed-element'
    key = 'managed-element'
    file_type = file_name.split('_')[0]
    check = get_bracket(file_type)
    raw_file_data = content.decode('utf-8')
    raw_file_data = re.sub(r'><', r'>\n<', raw_file_data)
    raw_file_data = raw_file_data.split('\n')
    start = [index for index, item in enumerate(raw_file_data) if '<managed-element' in item]
    end = [index for index, item in enumerate(raw_file_data) if '</managed-element>' in item]
    try:
        for a,line in enumerate(raw_file_data[start[0]+1:end[0]]):
            if '<' in line and '</' not in line and '/>' not in line:
                temp = line.lstrip().rstrip('>').lstrip('<')
                hierarchy = hierarchy + '/' + temp
                key = key + '/' + temp
            elif ('</' in line) and (line.count('>') == 2):
                tag = re.search(r'<(.*?)>',line)
                tag = tag.group(1)
                val = re.search(r'>(.*?)<',line)
                val = val.group(1)
                if key in check:
                    if tag in check[key]:
                        if '/' in val:
                            val = val.replace('/', '.')
                        hierarchy = hierarchy + '[' + tag + '=' + val + ']'
                    else:
                        if key not in data:
                            data[key] = []
                        data[key].append([file_name.strip('.xml'),hierarchy,tag,val]) 
                else:
                    if key not in data:
                        data[key] = []
                    data[key].append([file_name.strip('.xml'),hierarchy,tag,val])
            elif ('</' in line) and (line.count('>') == 1):
                temp = line.lstrip().rstrip('>').lstrip('</')
                # hierarchy = hierarchy.split(temp)[0].rstrip('/')
                # key = key.split(temp)[0].rstrip('/')
                hierarchy = hierarchy.split('/')
                hierarchy = '/'.join(hierarchy[:-1])
                key = key.split('/')
                key = '/'.join(key[:-1])
    except IndexError as e:
        print(file_name)
        return

    write_to_excel(data,file_type)

def zip_file():
    output_folder_list = os.listdir(output_folder)
    print('File compression started')
    for output_type_folder in output_folder_list:
        csv_folder_path = os.path.join(output_folder, output_type_folder)
        csv_file_list = os.listdir(csv_folder_path)
        temp_paths = []
        mo = ''
        zip_folder_path = os.path.join(output_zip, output_type_folder)
        if not os.path.exists(zip_folder_path):
            os.makedirs(zip_folder_path)
        for csv_file in csv_file_list:
            csv_file_path = os.path.join(csv_folder_path, csv_file)
            curr_mo = csv_file.split('_')
            curr_mo = curr_mo[0].removesuffix('.csv')
            if not mo:
                mo = curr_mo
                temp_paths.append(csv_file_path)
                continue                
            if curr_mo == mo :
                temp_paths.append(csv_file_path)
            else:
                zip_name = os.path.join(zip_folder_path, mo + '.zip')
                compression = zipfile.ZIP_DEFLATED
                with zipfile.ZipFile(zip_name, 'w', ) as zipf:
                    for file in temp_paths:
                        zipf.write(file, os.path.basename(file),compress_type=compression)
                mo = curr_mo
                temp_paths = []
                temp_paths.append(csv_file_path)
        if temp_paths:
            zip_name = os.path.join(zip_folder_path, mo + '.zip')
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                for file in temp_paths:
                    zipf.write(file, os.path.basename(file))
    print('File compression Done')

    
def main():
    with tarfile.open(os.path.join(input_folder, file_list[0]), 'r:gz') as tar:
        # Iterate through files in the tar.gz archive
        members = tar.getmembers()
        total_members = len(members)
        progress_marker = 10
        processed_files = 0
        current_time = datetime.now()
        site_list = get_site_list()
        print(f'time: {current_time.strftime("%H:%M")}')
        for member in members:

            # list_file = os.path.join(current_dir,  "list_file.txt")
            # f = open(list_file,"a+")
            # f.write(member.name)
            # f.write('\n')
            # continue
            if site_list and member.name.rstrip('.xml') not in site_list:
                continue
            # Check if it's a file (not a directory)
            if member.isfile():
                # Extract the file object into memory
                f = tar.extractfile(member)
                if f is not None:
                    # Read the file content
                    # print(f)
                    content = f.read()
                    process_xml(content, member.name)
                    # break
                    # # Process the content in memory (example: decode and print)
                    # print(content.decode('utf-8'))  # Assuming the file is text-based

            processed_files += 1
            # Calculate the percentage of processed files
            progress = (processed_files / total_members) * 100
            # Print progress when it crosses every 10% mark
            if progress >= progress_marker:
                print(f'{progress_marker}% XML to Excel completed')
                current_time = datetime.now()
                print(f'time: {current_time.strftime("%H:%M")}')
                progress_marker += 10

    # Track peak memory usage after processing
    # peak_memory = process.memory_info().rss / (1024 * 1024)  # Memory in MB
    # print(f"Peak memory usage: {peak_memory:.2f} MB")
    zip_file()


    print('Output Generated \n \n')
    input('\n Press any key to continue')

main()
