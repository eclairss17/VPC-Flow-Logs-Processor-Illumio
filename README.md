# VPC-Flow-Logs-Processor-Illumio

**Project Overview**

This script processes flow log data (assumed to be in a text file format) and generates two CSV files for further analysis:

* **tag_counts.csv:** Contains the count of occurrences for each unique tag extracted from the flow logs.
* **port_protocol_counts.csv:** Contains the count of occurrences for each unique combination of destination port and protocol name found in the flow logs.

**Requirements**

* Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/)), locally used python 3.9.6.
* Standard library `csv` module, no dependencies are required to be installed in order to run the project.


**Assumptions**

* The flow log data resides in a text file named flow_logs.txt within the same directory as this script.
* The lookup table (mapping dstport-protocol combinations to tags) exists as a CSV file named lookup_table.csv in the same directory.
* The flow log data is clean and consistent, adhering to AWS VPC log requirements. **This source code supports all the protocol types listed under AWS VPC logs** ([here.](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml))
* dstport (destination port) and protocol_name (derived from protocol number) form a unique key in the lookup table. Multiple unique keys can share the same associated tag.
* Case-sensitivity for dstport and protocol_name is irrelevant due to stripping leading/trailing spaces before processing and converting protocol names to lowercase for tag lookups.

**Testing**
* For the purpose of self testing, the function has been modified to accept `flow_logs` files both as a `txt` flow log file as well as a `csv`. As for the purpose of testing on large data, I tested the source code on a `csv` flow log data file, sized (5MB and 10MB). This large log file has also been committed and is present in the project directory as `vpc_logs_5mb.csv`.


**Run the script**
1. Save the script as `main.py` in a directory containing `flow_logs.txt` and `lookup_table.csv`.

2. Clone the repository, open a terminal or command prompt and navigate to the directory containing these files.

   ```bash
   python main.py

**Input and Output Files**

Input:

1: `flow_logs.txt`: Text file containing flow log data.

2: `lookup_table.csv`: CSV file mapping dstport-protocol combinations to tags.

3: `protocol_numbers.csv`: Downloaded all accepted protocol types in a csv from ([source.](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml.))

Output:

1: `tag_counts.csv`: CSV file containing a header row (Tag, Count) followed by rows listing unique tags and their respective counts.

2: `port_protocol_counts.csv`: CSV file containing a header row (Port, Protocol, Count) followed by rows listing unique port-protocol combinations and their counts.

**Global Variables (Optimization Strategy)**

* The script leverages global variables `protocols` (mapping protocol numbers to names) and `lookup_table` (mapping dstport-protocol combinations to tags) to potentially save space during execution. However, we can consider passing these objects as function arguments when the script complexity increases or readability becomes a concern.
* Large data files are usually taken as a `csv`, this questions provides the `flow_logs` as a `txt` but we modified it to support both formats as a optimal coding strategy.

**Code Structure**

The script is organized into several functions, with docstring to explain the operation of each function:

* `load_protocols_from_csv(file_path)`: Loads protocol mappings from a CSV file.
* `get_protocol_from_protocol_number(protocol_number, protocols)`: Retrieves the protocol name based on its protocol number from the `protocol_numbers` csv.
* `process_flow_log_file(filename)`: Processes the flow log data, calculating tag and port-protocol combination counts.
* `write_tag_counts_to_csv(tag_counts, filename='tag_counts.csv')`: Writes tag counts to a CSV file.
* `write_port_protocol_counts_to_csv(port_protocol_counts, filename='port_protocol_counts.csv')`: Writes port-protocol combination counts to a CSV file.
