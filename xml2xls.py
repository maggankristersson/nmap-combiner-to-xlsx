import xml.etree.ElementTree as ET
import pandas as pd

def parse_results_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def extract_data_from_xml(xml_root):
    data = []

    if xml_root is None:
        return data

    for host in xml_root.findall('host'):
        address = host.find('address').text if host.find('address') is not None else 'N/A'
        hostname = host.find('hostname').text if host.find('hostname') is not None else 'N/A'
        mac_address = host.find('mac_address').text if host.find('mac_address') is not None else 'N/A'
        vendor = host.find('vendor').text if host.find('vendor') is not None else 'N/A'
        ports = host.find('ports')

        port_info_list = []
        if ports is not None:
            for port in ports.findall('port'):
                portid = port.attrib['portid']
                protocol = port.attrib['protocol']
                state = port.find('state').text if port.find('state') is not None else 'N/A'
                service = port.find('service')

                service_name = service.find('name').text if service.find('name') is not None else 'N/A'
                service_product = service.find('product').text if service.find('product') is not None else 'N/A'
                service_version = service.find('version').text if service.find('version') is not None else 'N/A'
                service_extrainfo = service.find('extrainfo').text if service.find('extrainfo') is not None else 'N/A'

                port_info = f"{portid}/{protocol} {service_name} {service_product} {service_version} {service_extrainfo}"
                port_info_list.append(port_info)

        data.append({
            'IP-address': address,
            'hostname': hostname,
            'MAC-address': mac_address,
            'vendor': vendor,
            'ports': '\n'.join(port_info_list)
        })
    
    return data

def create_excel_file(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

def main():
    xml_file = 'output.xml'
    output_file = 'output.xlsx'

    xml_root = parse_results_xml(xml_file)
    data = extract_data_from_xml(xml_root)
    create_excel_file(data, output_file)

    print(f"Excel file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()
