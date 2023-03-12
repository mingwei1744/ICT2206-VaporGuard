import json
import math
import re
import os
from reportlab.lib.pagesizes import A1, landscape
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

# PHP rules stated in json format
with open('php_rules.json') as f:
    data = json.load(f)

# Function to get specific key-value from all rules
def get_rule_values(key, result):
    for value in data['phpVulnerabilities']:
        result.append(value[key])

# Function to get specific rule information
def get_rule_infos(vuln_id):
    for vulnerability in data["phpVulnerabilities"]:
        if vulnerability["id"] == vuln_id:
            message = (vulnerability["message"])
            severity = (vulnerability["severity"])
            owasp = (vulnerability["owasp"])
            cwe = (vulnerability["cwe"])
            fix = (vulnerability["fix"])

            if severity == "Low":
                col = "green"
            elif severity == "Medium":
                col = "orange"
            elif severity == "High":
                col = "red"

            setValFont = f"<font color='green'><b>"
            setSeverityFont = f"<font color='{col}'><b>"
            setValFonte = "</b></font><br/>"

            infos = f"<br/><br/>\
            \n>>> Vulnerability ID: {setValFont}{vuln_id}{setValFonte}\
            \n>>> Details: {setValFont}{message}{setValFonte}\
            \n>>> Severity: {setSeverityFont}{severity}{setValFonte}\
            \n>>> OWASP: {setValFont}{owasp}{setValFonte}\
            \n>>> CWE: {setValFont}{cwe}{setValFonte}\
            \n>>> Recommendation: {setValFont}{fix}{setValFonte}\
            \n{'<' * 180}<br/>\n"

    return infos

# Function to get list of php files
def get_php_files(dir, result):
    # Loop through directory 
    for file in os.listdir(dir):
        # File uri
        file_path = os.path.join(dir, file)
        # Check if isfile and with .php extension
        if os.path.isfile(file_path):
            if file.endswith('.php'):
                result.append(file)
        
# Function to store results vulnerabilities result into a dictionary of file:vulns
def store_results(file, vulns, result_dict):
    if file in result_dict:
        # Append the vulns value only if it's not empty
        if len(vulns) !=0:
            result_dict[file].append(vulns)
    else:
        if len(vulns) !=0:
            result_dict[file] = [vulns]
    return result_dict

# Php vulnerability checker with 1 iteration
def php_vuln_checker1(filename, vuln_id):
    iter1_results = checker_iter1(filename, vuln_id)

    return iter1_results

# Php vulnerability checker with 2 iterations
def php_vuln_checker2(filename, vuln_id):
    iter1_results = checker_iter1(filename, vuln_id)
    iter2_results = checker_iter2(iter1_results, vuln_id)

    return iter2_results

# First iteration of vulnerability check in code
def checker_iter1(filename, vuln_id):
    # Array for matches
    matches = []
    pattern = ""

    for vulnerability in data["phpVulnerabilities"]:
        if vulnerability["id"] == vuln_id:
            pattern = (vulnerability["pattern-match"])

    with open(filename, "r") as f:
        for line_num, line in enumerate(f, start=1):
            match = re.search(pattern, line)
            # If a match is found, append the line to the matches array with the corresponding line number
            if match:
                matches.append(f"vulnID:[{vuln_id}] | line:|{line_num}| " + line.strip())

    return matches

# Second iteration of vulnerability check in code
def checker_iter2(iter1, vuln_id):
    pat_include = ""
    pat_exclude = ""
    results = []

    for vulnerability in data["phpVulnerabilities"]:
        if vulnerability["id"] == vuln_id:
            pat_include = (vulnerability["pattern-include"])
            pat_exclude = (vulnerability["pattern-exclude"])

    for x in range(len(iter1)):
        match_include = re.search(pat_include, iter1[x])
        match_exclude = re.search(pat_exclude, iter1[x])

        if match_include and not match_exclude:
            #print(iter1[x])
            results.append(iter1[x])

    return results

#TODO: Analyse High Entropy Strings and add potential vulns to report
# Function for shannon entropy of each php file
def shannon_entropy(data, iter):
    if not data:
        return 0
    entropy = 0
    for x in iter:
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy

#TODO: Checker Functions for SQLINJECT, XSS, SESSIONS and high false positive rules in php_rules.json

# Generate presentable values from the result dictionary
def generate_php_report(result_dict):
    php_report = SimpleDocTemplate("php_report.pdf", pagesize=landscape(A1))
    styles = getSampleStyleSheet()
    report_info = []

    section_style = styles["Heading1"]
    section_style.alignment = 0
    section = "<u>PHP Vulnerability Report</u>"
    section_data = Paragraph(section, section_style)
    report_info.append(section_data)

    # For each file, and vulnerable codeLines
    for file, codeLines in result_dict.items():
        print("*"*50)
        print(f"Potential vulnerability found in: [{file.strip(php_files_dir)}]")

        filename_style = styles["Heading2"]
        filename_style.alignment = 0
        filename_style.textColor = colors.red
        filename = f"Potential vulnerability found in: [{file.strip(php_files_dir)}]"
        filename_data = Paragraph(filename, filename_style)
        report_info.append(filename_data)

        # Separated list of vulnerabilities based on vulnerability ID
        for codeLine in codeLines:
            # Extracted from individual list
            for line in codeLine:

                # Get unique vulnerablity ID to retrieve relevant information and display info on respective file check
                value_split1 = line.split("|")[0].strip("vulnID:")
                value_split2 = value_split1.strip("[ ]")

                # Vulnerable code line
                # Syntax: vulnID:[AXX.X] | line:[X] $xmlfile = file_get_contents($_POST['data']);
                # print(line)

                formatLine = f"|:|<b>{line}</b>\n<br/>{'-' * 180}"

                line_style = styles["Code"]
                line_style.fontSize = 14
                line_style.leading = 14 * 1.2
                line_style.underline = 1
                line_style.alignment = 0
                line_data = Paragraph(formatLine, line_style)
                report_info.append(line_data)
            
            # Vulnerable code information
            if get_rule_infos(value_split2) is not None:
                #print(get_rule_infos(value_split2))

                info = get_rule_infos(value_split2) # CHANGE TO SINGLE STRING FORMAT
                print(info)
                info_style = styles["Normal"]
                info_style.fontSize = 14
                info_style.leading = 14 * 1.2
                info_style.textColor = colors.blue
                info_style.alignment = 0
                info_data = Paragraph(info, info_style)
                report_info.append(info_data)

    php_report.build(report_info)

# TODO: Change to argpaser for main python file to call
if __name__ == "__main__":
    # Get all vulnerabilities IDs
    vuln_ids_arr = []
    get_rule_values("id", vuln_ids_arr)

    # Get all php files
    php_files_dir = "./vulns/" # Specify directory with php file TODO: Get vuln php codes
    php_files_arr = []
    get_php_files(php_files_dir, php_files_arr)

    # Store results into a dictionary
    vuln_results_consolidated = {}
    for phpfiles in php_files_arr:
        phpfile = php_files_dir + phpfiles
        for vuln_id in vuln_ids_arr:
            # Generate results with phpfile, checker(), store_in_dict
            store_results(phpfile, php_vuln_checker2(phpfile, vuln_id), vuln_results_consolidated)

    generate_php_report(vuln_results_consolidated)