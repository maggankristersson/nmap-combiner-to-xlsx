import os
import subprocess
from datetime import datetime

# Define the folder for output
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to run nmap scan
def run_nmap(scan_name, flags):
    output_file = os.path.join(output_dir, f"{scan_name}")
    command = ["nmap", "--unprivileged", "-iL", "targets.txt", "--unique", "-oA", output_file] + flags
    subprocess.run(command)

# Read targets file
targets_file = "targets.txt"
if not os.path.exists(targets_file):
    print(f"Error: {targets_file} does not exist.")
    exit(1)

# Base nmap scan
base_scan_name = "base_scan"
print("Starting base nmap scan...")
run_nmap(base_scan_name, [])

# Enhanced scan 1: Aggressive scan
aggressive_scan_name = "aggressive_scan"
print("Starting aggressive nmap scan...")
run_nmap(aggressive_scan_name, ["-A"])

# Enhanced scan 2: Stealth scan to evade detection
stealth_scan_name = "stealth_scan"
print("Starting stealth nmap scan...")
run_nmap(stealth_scan_name, ["-sS"])

# Enhanced scan 3: Scan with version detection and script scanning
version_script_scan_name = "version_script_scan"
print("Starting version detection and script scanning...")
run_nmap(version_script_scan_name, ["-sV", "-sC"])

# Enhanced scan 4: Scan with more timing options to avoid detection
timing_scan_name = "timing_scan"
print("Starting timing nmap scan...")
run_nmap(timing_scan_name, ["-T2"])

print("All scans completed. Check the output directory for results.")
