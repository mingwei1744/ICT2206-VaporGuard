import os
import textwrap
import re
from hcl import *
import requests.exceptions
from checkov.runner_filter import RunnerFilter
from checkov.terraform.runner import Runner
import json
from reportlab.lib.pagesizes import A1, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import openai
import time

#global request time
last_request_time = 0
min_time_between_requests = 1.0  # minimum time in seconds between requests
def generate_report(json_file_path, report_file_path):
    # Read in the JSON report file
    with open(json_file_path, 'r') as f:
        report_data = json.load(f)
        # Get guideline URLs
        url = "https://www.bridgecrew.cloud/api/v2/guidelines"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            #get guidelines based on check_id
            guidelines = response_data.get("guidelines", {})
        else:
            guidelines = {}

        # Create report table data
        data = [['Check ID', 'File', 'Resource', 'Check Name', 'Line', 'Potential CVE/CWE', 'Guideline URL', 'Status']]
        for check in report_data['results']['failed_checks']:
            cwe_cve = ''
            guideline_url = guidelines.get(check['check_id'], '')
            if guideline_url:
                response = chatgpt_request("Based on " + check['check_name'] + " and "+ check['resource']+ " given, what are 1-3 possible cve/cwe if this is not ensured, shorten and return CVE/CWE results in 1. CVE/CWE 2. CVE/CWE 3. CVE/CWE with short description")
                cwe_cve = re.sub(r"\ format", "", ("\n".join(textwrap.wrap(response.replace(", ", "\n"), width=100))))
                cwe_cve = re.sub(r'(?<!\n)\s*\n\s*', ' ', cwe_cve)  # remove line breaks that are not at the start of a line
                cwe_cve = re.sub(r'\n\s*', r'\n', cwe_cve)  # remove whitespace characters after newlines
                cwe_cve = re.sub(r'\n+', r'\n', cwe_cve).strip()  # remove duplicate newlines
                cwe_cve = re.sub(r'^\n', '', cwe_cve).strip()  # remove leading newline if present
                cwe_cve = re.sub(r'(\d+\.)\s*', r'\1 ', cwe_cve).strip()  # insert a space after the numbers
                cwe_cve = re.sub(r'(\d+\.)', r'\n\1', cwe_cve).strip()  # insert newlines before the numbers

            data.append([check['check_id'], check['file_path'], check['resource'], check['check_name'], '-'.join(str(x) for x in check['file_line_range']),
                         cwe_cve, guideline_url, 'FAILED'])

        for check in report_data['results']['passed_checks']:
            cwe_cve = ''
            guideline_url = guidelines.get(check['check_id'], '')
            data.append([check['check_id'], check['file_path'], check['resource'], check['check_name'], '-'.join(str(x) for x in check['file_line_range']),
                         cwe_cve, guideline_url, 'PASSED'])
        for check in report_data['results']['skipped_checks']:
            cwe_cve = ''
            guideline_url = guidelines.get(check['check_id'], '')
            data.append([check['check_id'], check['file_path'], check['resource'], check['check_name'], '-'.join(str(x) for x in check['file_line_range']),
                         cwe_cve, guideline_url, 'SKIPPED'])

    # Create PDF report
    doc = SimpleDocTemplate(report_file_path, pagesize=landscape(A1))

    # Set the table style
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    table = Table(data)
    # Change the font color of the "Status" column based on row value
    for i in range(1, len(data)):
        if data[i][-1] == 'PASSED':
            status_color = colors.green
        elif data[i][-1] == 'FAILED':
            status_color = colors.red
        else:
            status_color = colors.black
        table_style.append(('TEXTCOLOR', (-1, i), (-1, i), status_color))

    table.setStyle(TableStyle(table_style))

    # Create a custom style for the section header
    styles = getSampleStyleSheet()
    section_header_style = styles['Heading1']
    section_header_style.fontSize = 24
    section_header_style.leading = 30
    section_header_style.alignment = 1  # Center alignment

    # Create the section header Paragraph object
    section_header = Paragraph("Terraform Scan Results", section_header_style)

    # Add the section header and table to the PDF
    doc.build([section_header, Spacer(1, 20), table])


def read_config_file(config_file_path):
    with open(config_file_path, 'r') as f:
        return load(f)

def chatgpt_request(prompt):

    global last_request_time
    global min_time_between_requests
    # Wait until enough time has elapsed since the last request
    elapsed_time = time.time() - last_request_time
    if elapsed_time < min_time_between_requests:
        time.sleep(min_time_between_requests - elapsed_time)
    # Make the API request
    openai.api_key = "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"
    model = "text-davinci-003"
    #When the temperature is set to a low value, the model will tend to produce more conservative or predictable responses
    temperature = 0.2
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=500,  temperature=temperature)
    generated_text = response.choices[0].text
    # Update the last request time
    last_request_time = time.time()
    #print(generated_text)
    return generated_text

def generate_cloud_report(external_checks_dir, json_file_path, report_file_path):

    # Initialize a runner filter, to do a scan on config based on terraform framework
    runner_filter = RunnerFilter(framework=["terraform"], include_all_checkov_policies=True)
    # Initialize a runner
    runner = Runner()
    # Load external checks from current directory, includes main.tf,outputs,providers and etc

    external_checks = [f"{external_checks_dir}/{f}" for f in os.listdir(external_checks_dir) if f.endswith(".tf")]
    runner.load_external_checks(external_checks)
    # Scan folders & sub folders recursively for .tf files and get the results - checkov
    report = runner.run(root_folder=external_checks_dir, runner_filter=runner_filter)
    # location of report.json and pdf would be created

    # Write the results to a JSON file for data processing/used for other modules
    with open(json_file_path, "w") as f:
        json.dump(report.get_dict(), f, indent=4)

    #generate report function using reportlab lib, by reading json
    generate_report(json_file_path, report_file_path)

    # Loop through the list of file paths and process each file manually
    for file_path in external_checks:
        if os.path.basename(file_path) == "main.tf":
            # Read in the configuration file in hcl format
            config = read_config_file(file_path)
            #if .tf has no key pair
            if not bool(config):
                continue
    #Do something to the particular .tf file


# if __name__ == "__main__":
#     # code for the main program here
#     external_checks_dir = "../Terraform"
#     json_file_path = "./report.json"
#     report_file_path = "../report/report.pdf"
#     main()
# else:
#     external_checks_dir = "./Terraform"
#     json_file_path = "./Configpackage/report.json"
#     report_file_path = "./report/report.pdf"
#     main()