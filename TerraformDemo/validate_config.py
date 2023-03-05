import os
import hcl
import requests.exceptions
import re
import time
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape

def generate_report(json_file_path, report_file_path):
    # Read in the JSON report file
    with open(json_file_path, 'r') as f:
        report_data = json.load(f)

        # Create report table data
        data = [['Check ID', 'File', 'Resource', 'Check Name', 'Guideline', 'Status']]
        for check in report_data['results']['failed_checks']:
            data.append([check['check_id'], check['file_path'], check['resource'], check['check_name'],
                         check.get('guideline', ''), 'FAILED'])
        for check in report_data['results']['passed_checks']:
            data.append([check['check_id'], check['file_path'], check['resource'], check['check_name'],
                         check.get('guideline', ''), 'PASSED'])
        for check in report_data['results']['skipped_checks']:
            data.append([check['check_id'], check['file_path'], check['resource'], check['check_name'],
                         check.get('guideline', ''), 'SKIPPED'])

        # Create PDF report
        doc = SimpleDocTemplate(report_file_path, pagesize=landscape(A3))
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        doc.build([table])

# Define the path to the configuration file, to be moved to variables.tf later
config_file = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/main.tf"
report_file = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/report.txt"

# Read in the configuration file
with open(config_file, 'r') as f:
    config = hcl.load(f)

# Define the base URL for the NVD API
base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
baseurlcwe = "https://services.nvd.nist.gov/rest/json/cves/2.0?cweId=<cwe_id>"
# Define the search parameters
search_params = 'azure virtual machine'

# Initialize an empty list to store the CVE results
cve_results = []
# Set the delay in seconds
delay = 1

# Set the path to your Terraform file
file_path = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/main.tf"

# Initialize a runner filter
runner_filter = RunnerFilter(framework=["terraform"], include_all_checkov_policies=True)

# Initialize a runner
runner = Runner()

# Load external checks from current directory
external_checks_dir = "."
external_checks = [f"{external_checks_dir}/{f}" for f in os.listdir(external_checks_dir) if f.endswith(".tf")]
runner.load_external_checks(external_checks)

# Scan the file and get the results
report = runner.run(root_folder="A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo", runner_filter=runner_filter)

json_file_path = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/report.json"
report_file_path = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/report.pdf"
# Write the results to a JSON file
with open(json_file_path, "w") as f:
    json.dump(report.get_dict(), f, indent=4)
generate_report(json_file_path, report_file_path)

# # Print the results for passed checks
# print("Passed checks:")
# for result in results["passed_checks"]:
#     print(f"Resource: {result['resource']}")
#     print(f"Check: {result['check_id']}")
#     print(f"Result: {result['check_result']['result']}")
#     print()
#
# # Print the results for failed checks
# print("Failed checks:")
# for result in results["failed_checks"]:
#     print(f"Resource: {result['resource']}")
#     print(f"Check: {result['check_id']}")
#     print(f"Result: {result['check_result']['result']}")
#     print()

# Loop through the configuration file to find relevant information
for resource_type, resources in config["resource"].items():
    for resource_name, resource in resources.items():
        # Check if the resource is a virtual machine, can later change to resource type as search params
        if resource_type == "azurerm_linux_virtual_machine" or resource_type == "azurerm_windows_virtual_machine":
        #     resource_type.strip()
        #     resource_type = re.sub(r"_", " ", resource_type)
        #     search_params = resource_type
            try:
                # Make the API call
                response = requests.get(f"{base_url}?keywordSearch={search_params}")
                time.sleep(delay)
                # Parse the JSON response
                data = response.json()
                # Check if any results were found
                # Process the data as needed and append it to cve_results
                if data["totalResults"] > 0:
                    for cve_item in data["vulnerabilities"]:
                        cve = cve_item["cve"]
                        cve_id = cve["id"]
                        cve_description = ""

                        for description in cve["descriptions"]:
                            if description["lang"] == "en":
                                cve_description = description["value"]
                                break
                        cve_base_score = ""
                        references = cve['references']
                        url = references[0]['url']
                        if "cvssMetricV2" in cve["metrics"]:
                            cve_base_score = cve["metrics"]["cvssMetricV2"][0]["cvssData"]["baseScore"]
                        elif "cvssMetricV31" in cve["metrics"]:
                            cve_base_score = cve["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
                        cve_results.append({"id": cve_id, "description": cve_description, "base_score": cve_base_score, "references": url})
                else:
                    print("No results found.")
            except requests.exceptions.Timeout:
                # Handle the timeout exception here
                print("The request timed out.")
            except requests.exceptions.HTTPError as e:
                # Handle HTTP errors here
                print(f"HTTP error occurred: {e}")
            except requests.exceptions.RequestException as e:
                # Handle other exceptions here
                print(f"Too many request error occurred: {e}")

# Print and write the CVE results
if cve_results:
    with open(report_file, 'a') as report:
        report.write(f"Found {len(cve_results)} CVEs:\n")
        for result in cve_results:
            report.write(f"CVE ID: {result['id']}\n")
            report.write(f"Description: {result['description']}\n")
            report.write(f"Base Score: {result['base_score']}\n")
            report.write(f"References: {result['references']}\n")
            print(f"CVE ID: {result['id']}")
            print(f"Description: {result['description']}")
            print(f"Base Score: {result['base_score']}")
            print(f"References: {result['references']}")
else:
    print("No CVEs found.")

# Check for CWEs
# Loop through the security rules and correct the SSH port
with open(report_file, 'a') as report:
    if 'security_rule' in config['resource']['azurerm_network_security_group']['sg-automate-test']:
        for rule in config['resource']['azurerm_network_security_group']['sg-automate-test']['security_rule']:
            if rule['name'] == 'sshd' and rule['destination_port_range'] == '22':
                report.write(f"WARNING: Security rule {rule['name']} is using default SSH port\n")
            if 'source_address_prefix' not in rule:
                report.write(f"WARNING: Security rule {rule['name']} allows traffic from all sources\n")
            if 'destination_address_prefix' not in rule:
                report.write(f"WARNING: Security rule {rule['name']} allows traffic to all destinations\n")

# # Write out the modified configuration file
# new_config_file = "A:/Users/JJ/Documents/GitHub/ICT2206-VapourGuard/TerraformDemo/main_modified.tf"
# with open(new_config_file, 'w') as f:
#     f.write(hcl.dumps(config, indent=2))

