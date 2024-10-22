import xml.etree.ElementTree as ET
import glob
import os
import argparse
from xml.dom import minidom

def parse_nmap_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def extract_host_info(nmap_root):
    hosts = []
    if nmap_root is None:
        return hosts

    for host in nmap_root.findall('host'):
        host_info = {}
        address = host.find('address[@addrtype="ipv4"]')
        hostname = host.find('hostnames/hostname')
        mac_address_elem = host.find('address[@addrtype="mac"]')
        ports = host.find('ports')

        host_info['address'] = address.attrib['addr'] if address is not None else 'N/A'
        host_info['hostname'] = hostname.attrib['name'] if hostname is not None else 'N/A'
        host_info['mac_address'] = mac_address_elem.attrib['addr'] if mac_address_elem is not None else 'N/A'
        host_info['vendor'] = mac_address_elem.attrib.get('vendor', 'N/A') if mac_address_elem is not None else 'N/A'
        host_info['ports'] = []

        if ports is not None:
            for port in ports.findall('port'):
                service = port.find('service')
                port_info = {
                    'portid': port.attrib['portid'],
                    'protocol': port.attrib['protocol'],
                    'state': port.find('state').attrib['state'],
                    'service': {
                        'name': service.attrib.get('name', ' ') if service is not None else ' ',
                        'product': service.attrib.get('product', ' ') if service is not None else ' ',
                        'version': service.attrib.get('version', ' ') if service is not None else ' ',
                        'extrainfo': service.attrib.get('extrainfo', ' ') if service is not None else ' '
                    }
                }
                host_info['ports'].append(port_info)

        hosts.append(host_info)
    return hosts

def combine_hosts_info(hosts_info_list):
    combined_hosts = []
    for hosts_info in hosts_info_list:
        combined_hosts.extend(hosts_info)
    return combined_hosts

def create_combined_xml(hosts_info, output_file):
    root = ET.Element("output")

    for host_info in hosts_info:
        host_elem = ET.SubElement(root, "host")

        address_elem = ET.SubElement(host_elem, "address")
        address_elem.text = host_info['address']

        hostname_elem = ET.SubElement(host_elem, "hostname")
        hostname_elem.text = host_info['hostname']

        mac_elem = ET.SubElement(host_elem, "mac_address")
        mac_elem.text = host_info['mac_address']

        vendor_elem = ET.SubElement(host_elem, "vendor")
        vendor_elem.text = host_info['vendor']

        ports_elem = ET.SubElement(host_elem, "ports")
        for port in host_info['ports']:
            port_elem = ET.SubElement(ports_elem, "port", portid=port['portid'], protocol=port['protocol'])
            
            state_elem = ET.SubElement(port_elem, "state")
            state_elem.text = port['state']

            service_elem = ET.SubElement(port_elem, "service")

            name_elem = ET.SubElement(service_elem, "name")
            name_elem.text = port['service']['name']

            product_elem = ET.SubElement(service_elem, "product")
            product_elem.text = port['service']['product']

            version_elem = ET.SubElement(service_elem, "version")
            version_elem.text = port['service']['version']

            extrainfo_elem = ET.SubElement(service_elem, "extrainfo")
            extrainfo_elem.text = port['service']['extrainfo']

    # Convert to a string and pretty print
    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_as_str = parsed_xml.toprettyxml(indent="    ")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_str)

def create_raw_combined_xml(nmap_files, output_file):
    root = ET.Element("nmaprun")

    for file in nmap_files:
        nmap_root = parse_nmap_xml(file)
        if nmap_root is not None:
            for host in nmap_root.findall('host'):
                root.append(host)

    # Convert to a string and pretty print
    xml_str = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml_as_str = parsed_xml.toprettyxml(indent="    ")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_str)

def main():
    parser = argparse.ArgumentParser(description="Combine Nmap XML files.")
    parser.add_argument('-r', '--raw', action='store_true', help="Perform a raw merge of the XML files.")
    args = parser.parse_args()

    nmap_files = glob.glob('xml-files/*.xml')
    if not nmap_files:
        print("No XML files found in the specified directory.")
        return

    if args.raw:
        create_raw_combined_xml(nmap_files, 'raw_output.xml')
        print("Raw combined XML file 'raw_output.xml' created successfully.")
    else:
        all_hosts_info = []

        for file in nmap_files:
            print(f"Processing file: {file}")
            nmap_root = parse_nmap_xml(file)
            hosts_info = extract_host_info(nmap_root)
            all_hosts_info.append(hosts_info)

        combined_hosts_info = combine_hosts_info(all_hosts_info)
        create_combined_xml(combined_hosts_info, 'output.xml')
        print("Combined XML file 'output.xml' created successfully.")

if __name__ == "__main__":
    main()
