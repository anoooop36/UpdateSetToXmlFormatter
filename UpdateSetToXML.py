import os
import xml.dom.minidom
import xml.etree.ElementTree as ET
import xml.etree as etree
import glob

def replace_tags(xml_str):
    result = []
    dictionary = {
                    '<sys_created_by>demo_csc</sys_created_by>':'<sys_created_by>now.csc</sys_created_by>',
                    '<sys_updated_by>demo_csc</sys_updated_by>':'<sys_updated_by>now.csc</sys_updated_by>',
                    '<sys_created_by>anoop.chaudhary@snc</sys_created_by>':'<sys_created_by>now.csc</sys_created_by>',
                    '<sys_updated_by>anoop.chaudhary@snc</sys_updated_by>':'<sys_updated_by>now.csc</sys_updated_by>',
                    '<sys_created_by>admin</sys_created_by>':'<sys_created_by>now.csc</sys_created_by>',
                    '<sys_updated_by>admin</sys_updated_by>':'<sys_updated_by>now.csc</sys_updated_by>',
                    'CscUtil':'GuidedSetupUtilCSC',
                    'ECCO':'CSC'
                 }
                
    for key in dictionary:
        xml_str = xml_str.replace(key,dictionary[key])

    return xml_str



files = glob.glob('./generated/*')
for f in files:
    os.remove(f)

# specify the directory path
directory = "./"

# specify the file extension you want to find
extension = ".xml"

# use os.listdir() to get a list of files in the directory
files = os.listdir(directory)

# use a list comprehension to get only the files with the specified extension
filtered_files = [file for file in files if file.endswith(extension)]

for f in filtered_files:
    tree = ET.parse(f)
    root = tree.getroot()
    updateXmls = root.findall('sys_update_xml')
    for child in updateXmls:
        name = child.find('name').text
        action = child.find('action').text
        payload = child.find('payload').text
        payload = payload.replace('anoop.chaudhary@snc','admin');
        payload = payload.replace('maint','admin');
        if('INSERT_OR_UPDATE' == action):
            print('Writing '+ name + '.xml file')
            with open('./generated/'+name+'.xml', "wb") as f:
                f.write(payload.encode('utf-8'))
                print('Done Writing '+ name + '.xml file')


files = glob.glob('./out/*')
for f in files:
    os.remove(f)

# folder containing the XML files
folder_path = "./generated"

# iterate over all files in the folder
for filename in os.listdir(folder_path):
    # check if file is XML
    if filename.endswith(".xml"):
        # read the file contents
        xml_file_path = os.path.join(folder_path, filename)

        # parse the XML file using minidom parser
        dom = xml.dom.minidom.parse(xml_file_path)

        # pretty print the XML file
        xml_str = dom.toprettyxml(indent="  ")

        xml_str = replace_tags(xml_str)

        # remove extra whitespace between tags
        xml_lines = [line for line in xml_str.split("\n") if line.strip()]

        xml_out_file_path = os.path.join("./", os.path.join('out', filename))

        # write formatted XML to file
        with open(xml_out_file_path, "w") as f:
            f.write("\n".join(xml_lines))


