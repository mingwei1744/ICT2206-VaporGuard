import hcl
import requests.exceptions

# Define the path to the configuration file, to be moved to variables.tf later
# config_file = sys.argv[1]
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

# Loop through the configuration file to find relevant information
for resource_type, resources in config["resource"].items():
    for resource_name, resource in resources.items():
        # Check if the resource is a virtual machine
        if resource_type == "azurerm_linux_virtual_machine" or resource_type == "azurerm_windows_virtual_machine":
            try:
                # Make the API call
                response = requests.get(f"{base_url}?keywordSearch={search_params}")
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
                print(f"An error occurred: {e}")


# Print and write the CVE results
if cve_results:
    with open(report_file, 'a') as report:
        report.write(f"Found {len(cve_results)} CVEs:\n")
        for result in cve_results:
            report.write(f"CVE ID: {result['id']}\n")
            report.write(f"Description: {result['description']}\n")
            report.write(f"Base Score: {result['base_score']}\n\n")
            report.write(f"references: {result['references']}\n\n")
            print(f"CVE ID: {result['id']}")
            print(f"Description: {result['description']}")
            print(f"Base Score: {result['base_score']}")
            print(f"references: {result['references']}")
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
