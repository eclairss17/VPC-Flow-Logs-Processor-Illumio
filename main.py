import csv

def load_lookup_table(lookup_file):
    """
    Loads a lookup table from a CSV file.

    Args:
        lookup_file: The path to the CSV file containing the lookup table data.

    Returns:
        A dictionary where the keys are colon separated destination port and protocol, and the values are tags.
    """

    lookup = {}
    with open(lookup_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dstport = row['dstport'].strip()
            protocol = row['protocol'].strip().lower()
            key = f"{dstport}:{protocol}"
            lookup[key] = row['tag'].strip().lower()
    return lookup

def get_tag_from_lookup(lookup_table, dstport, protocol):
    """
    Retrieves the tag associated with a given destination port and protocol from the lookup table.

    Args:
        lookup_table: A dictionary containing the lookup table data.
        dstport: The destination port number.
        protocol: The protocol name, case insensitive

    Returns:
        The tag associated with the specified destination port and protocol, or None if not found.
    """
    
    key = f"{dstport}:{protocol.lower()}"
    return lookup_table.get(key) or "Untagged"

def load_protocols_from_csv(file_path):
    """
    Creates a dictionary of protocol numbers to corresponding protocol names from a CSV file. 
    This code supports all identified protocols.
    csv downloaded from https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        dict: A dictionary where the keys are protocol numbers and the values are the protocol names.
    """
    protocols = {}
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            decimal = row['Decimal']
            keyword = row['Keyword']
            protocols[decimal] = keyword

    return protocols

def get_protcol_from_protocol_number(protocol_number, protocols):
    """
    Retrieves the protocol name associated with a given protocol number.

    Args:
        protocol_number (int): The protocol number.
        protocols (dict): A dictionary mapping protocol numbers to their names.

    Returns:
        str: The keyword associated with the given protocol number, or "Unassigned" if not found.
    """
    return protocols.get(protocol_number, "Unassigned")


def extract_dstport_protocol(row):
    """
    Extracts the dstport and protocol numbers from a valid row.

    Args:
        row: a row of flow_logs.txt or can be a csv file 

    Returns:
        A tuple containing the dstport and protocol numbers, Assuming the fields cannot be null
    """
    fields = row
    if not isinstance(row, list):
        fields = row.split()
    dstport = fields[5].strip()
    protocol = fields[7].strip()
    if not dstport or not protocol:
        return None
    return dstport, protocol

def process_flow_log_file(filename):
    """
    Processes a text or CSV file containing flow log data, extracting destination port, protocol numbers, and associated tags.

    Args:
        filename (str): The path to the text or CSV file.

    Returns:
        tuple: A tuple containing two dictionaries:
            - tag_counts: A dictionary mapping tags to their respective counts.
            - port_protocol_counts: A dictionary mapping port-protocol pairs to their counts.
    """

    tag_counts = {}
    port_protocol_counts = {}

    if filename.endswith('.csv'):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 14:
                    continue
                process_row(row, tag_counts, port_protocol_counts)
    else:
        with open(filename, 'r') as file:
            for row in file:
                row = row.strip()
                if not row or len(row.split()) != 14:
                    continue
                process_row(row, tag_counts, port_protocol_counts)

    return tag_counts, port_protocol_counts

def process_row(row, tag_counts, port_protocol_counts):
    dstport, protocol_number = extract_dstport_protocol(row)
    if dstport and protocol_number:
        protocol_name = get_protcol_from_protocol_number(protocol_number, protocols)
        tag = get_tag_from_lookup(lookup_table, dstport, protocol_name)
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
        port_protocol_identifier = (dstport, protocol_name.lower())
        port_protocol_counts[port_protocol_identifier] = port_protocol_counts.get(port_protocol_identifier, 0) + 1

def write_tag_counts_to_csv(tag_counts, filename='tag_counts.csv'):
    """
    Writes tag counts to a CSV file.

    Args:
        tag_counts: A dictionary containing tag counts.
        filename: The name of the output CSV file- 'tag_counts.csv'.
    """

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tag', 'Count'])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])

def write_port_protocol_counts_to_csv(port_protocol_counts, filename='port_protocol_counts.csv'):
    """
    Writes port/protocol unique combination counts to a CSV file.

    Args:
        port_protocol_counts: A dictionary containing port/protocol combination counts.
        filename: The name of the output CSV file- 'port_protocol_counts.csv'.
    """

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Port', 'Protocol', 'Count'])
        for (dstport_number, protocol_name), count in port_protocol_counts.items():
            writer.writerow([dstport_number, protocol_name, count])

protocols = load_protocols_from_csv('protocol_numbers.csv')
lookup_table = load_lookup_table('lookup_table.csv')

if __name__ == "__main__":
    tag_counts, port_protocol_counts = process_flow_log_file('flow_logs.txt')

    write_tag_counts_to_csv(tag_counts)
    write_port_protocol_counts_to_csv(port_protocol_counts)
