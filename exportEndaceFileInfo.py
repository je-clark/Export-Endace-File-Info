import textfsm
import csv
import EndaceDevices
from netmiko import ConnectHandler


def print_output_to_csv(output, filename, templateFilename):
    with open(templateFilename, "r") as template:
        re_table = textfsm.TextFSM(template)
    data = re_table.ParseText(output)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)
        csvfile.close()
    return


def getFileSystemInfo(connection):
    connection.enable()
    output = connection.find_prompt()
    output += "\n"
    output += connection.send_command("show files system")
    return output


def getRotFileInfo(connection):
    connection.enable()
    output = connection.find_prompt()
    output += "\n"
    output += connection.send_command("show erfstream rotation-file")
    return output


fscsvName = 'fileSystems.csv'
rotcsvName = 'rotFiles.csv'
fsTemplate = 'TextFSMTemplates/filesSystemTemplate.txt'
rotTemplate = 'TextFSMTemplates/rotTemplate.txt'
with open(fscsvName, "w", newline='') as fscsv:
    writer = csv.writer(fscsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Device', 'Total Space (GB)', 'Used Space (GB)'
                    , 'Usable Space (GB)', 'Free Space (GB)'])
    fscsv.close()
with open(rotcsvName, "w", newline='') as rotcsv:
    writer = csv.writer(rotcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Device', 'Rot File Name', 'User Size Limit (GB)'
                    , 'Actual Size Limit (GB)', 'Disk Usage (GB)'
                    , 'Vision Retention Time', 'Vision Size (GB)'
                    , 'Current Size (GB)', 'Source'])
    rotcsv.close()
for device in EndaceDevices.prod_probes:
    connection = ConnectHandler(**device)
    fsInfo = getFileSystemInfo(connection)
    rotInfo = getRotFileInfo(connection)
    connection.disconnect()
    print_output_to_csv(fsInfo, fscsvName, fsTemplate)
    print_output_to_csv(rotInfo, rotcsvName, rotTemplate)
