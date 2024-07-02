# Nmap - Merging and conversion

Script is used to merge multiple nmap scan results. These combined xml-files can be used to either search for exploits with searchsploit or convert to xls.

## Installation

```bash
pip install -r requirements.txt
```

## Usage
1. Place all xml-files in the folder "xml-files"
2. Run the scripts accordingly:

### NMAP -> XLS
```bash
# Merge files
python3 combiner.py

# Convert results.xml to XLS
python3 xml2xls.py
```

### NMAP -> SEARCHSPLOIT
``` bash
# Merge files into raw xml
python3 combiner.py --raw

# Search for exploit with searchsploit
searchsploit --nmap raw_output.xml
```
