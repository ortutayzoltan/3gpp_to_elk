#!/usr/bin/python3
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from collections import defaultdict

def generate_3gpp_filename(vendor_name, timestamp, file_type="HardwareUtilization", sequence_number="0001"):
    """
    Generate a file name following the 3GPP TS 32.432 standard format.
    """
    # Convert timestamp to the desired format (YYYYMMDD_HHMMSS)
    timestamp_str = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y%m%d_%H%M%S')

    filename = f"{vendor_name}_{timestamp_str}_{file_type}_{sequence_number}.xml"
    return filename

def prettify_xml(elem):
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_xml_for_timestamp(data, timestamp, output_directory='.'):
    # Generate the output file name based on 3GPP TS 32.432, using the timestamp from the CSV
    output_xml_file = generate_3gpp_filename("NebulaTek", timestamp)

    # Create the root element
    measData = ET.Element('measData', xmlns="http://www.3gpp.org/ftp/specs/latest/Rel-15/32_series/32432-790.xml", 
                          attrib={"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance", 
                                  "xsi:schemaLocation": "http://www.3gpp.org/ftp/specs/latest/Rel-15/32_series/32432-790.xml MeasData.xsd"})

    # Add file header
    fileHeader = ET.SubElement(measData, 'fileHeader')
    ET.SubElement(fileHeader, 'fileFormatVersion').text = "32.432 V15.0"
    ET.SubElement(fileHeader, 'vendorName').text = "NebulaTek"
    ET.SubElement(fileHeader, 'dnPrefix').text = "test/data"

    # Add measurement information
    measInfo = ET.SubElement(measData, 'measInfo')
    ET.SubElement(measInfo, 'measInfoId').text = "HardwareUtilization"
    ET.SubElement(measInfo, 'granPeriod', duration="PT15M")

    # Define measurement types
    measTypes = ET.SubElement(measInfo, 'measTypes')
    ET.SubElement(measTypes, 'measType', p="1").text = "CPU_Utilization"
    ET.SubElement(measTypes, 'measType', p="2").text = "Memory_Utilization"
    ET.SubElement(measTypes, 'measType', p="3").text = "Disk_Utilization"

    # Add measurement values for the specific timestamp
    for row in data:
        measValue = ET.SubElement(measInfo, 'measValue', measObjLdn=f"TEST/DATA/{row['machine_id']}")
        ET.SubElement(measValue, 'r', p="1").text = row['cpu_utilization']
        ET.SubElement(measValue, 'r', p="2").text = row['memory_utilization']
        ET.SubElement(measValue, 'r', p="3").text = row['disk_utilization']

    # Add file footer
    fileFooter = ET.SubElement(measData, 'fileFooter')
    ET.SubElement(fileFooter, 'measDataCollection', duration="PT15M")
    ET.SubElement(fileFooter, 'measDataCollectionEndTime').text = timestamp

    # Pretty-print the XML content
    pretty_xml_str = prettify_xml(measData)

    # Write the pretty-printed XML to a file
    with open(f"{output_directory}/{output_xml_file}", 'w', encoding='utf-8') as f:
        f.write(pretty_xml_str)

    print(f"File generated: {output_directory}/{output_xml_file}")

def create_xmls_from_csv(csv_file, output_directory='.'):
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Group data by timestamp
        data_by_timestamp = defaultdict(list)
        for row in reader:
            data_by_timestamp[row['timestamp']].append(row)

    # Create an XML file for each unique timestamp
    for timestamp, data in data_by_timestamp.items():
        create_xml_for_timestamp(data, timestamp, output_directory)

# Example usage
create_xmls_from_csv('hardware_utilization.csv', output_directory='results')
