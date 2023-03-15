import re
import json
import os
import csv
import requests
import time

from reportlab.lib.pagesizes import A1, landscape
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from bs4 import BeautifulSoup
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Terraform/scripts')

def mysqlSecureCheck(command,mysqlSecureCommands):
	root_pass_pattern = r'mysql\s-e\s"UPDATE\smysql.user\sSET\sPassword(\s)?=(\s)?PASSWORD\(\'[\S]+.\)\sWHERE\sUser(\s)?=(\s)?\'root\''
	drop_anonyUser_pattern =r'mysql -e "DROP\sUSER\s\'\'\@\'\$\([\S]+.\)\'"'
	drop_test_table=r'mysql -e "DROP DATABASE test"'
	flush_pattern=r'mysql -e "FLUSH PRIVILEGES"'
	if re.search(root_pass_pattern,command) and len(mysqlSecureCommands) != 0:
		for i in range(len(mysqlSecureCommands)):
			if re.search(root_pass_pattern,mysqlSecureCommands[i]):
				mysqlSecureCommands.pop(i)
				break
	if re.search(drop_test_table,command) and len(mysqlSecureCommands) != 0:
		for i in range(len(mysqlSecureCommands)):
			if re.search(drop_test_table,mysqlSecureCommands[i]):
				mysqlSecureCommands.pop(i)
				break
	if re.search(drop_anonyUser_pattern,command) and len(mysqlSecureCommands) != 0:
		for i in range(len(mysqlSecureCommands)):
			if re.search(drop_anonyUser_pattern,mysqlSecureCommands[i]):
				mysqlSecureCommands.pop(i)
				break
	if len(mysqlSecureCommands)==0:
		match = re.search(flush_pattern,command)
		if match:
			return True
	return False

def extract_package_info(command):
	pattern = r"install\s(.+)=([\d.]+)"
	match = re.search(pattern, command)
	if match:
		package_name = match.group(1)
		package_version = match.group(2)
		return package_name, package_version
	else:
		return None

def has_version_number(command):
	pattern = r"=([\d.]+)(\s-y)?$"
	match = re.search(pattern, command)
	return bool(match)

def has_mql_installation(command):
	pattern = r"apt(-get)? install\s(.+)(=([\d.]+)?)(\s-y)?"
	match = re.search(pattern, command)
	if match:
		db = ['mysql','mariadb']
		return match.group(2) in db	
	return False

def getFileContent(filename):
	lines=[]
	with open(filename, "r") as file:
		for line in file:
			lines.append(line.strip())
	return lines

def checkAptUpdate(command):
	pattern = r"apt(-get)? install\s(.+)(=([\d.]+)?)"
	match = re.search(pattern, command)
	if match:
		package_name = match.group(1)
		package_version = match.group(2)
		return package_name, package_version
	else:
		return None

def CVE_number(pkg_name, pkg_version):
	link="https://www.cybersecurity-help.cz/vdb/list.php?search_line=Y&filter%5B%25SEARCH%5D={}+{}".format(pkg_name,pkg_version)
	# print("Querying Vulnerabilities Database on: {} {}".format(pkg_name,pkg_version))
	source_code = requests.get(link)  # do a get request for html source code
	plain_text = source_code.text  # convert to plain text
	soup = BeautifulSoup(plain_text, 'html.parser')  # using bs4 soup to process
	result = soup.find('div', {'class': 'col-xs-10 col-xs-offset-05'}).get_text(" ", strip=True)
	if result == 'No vulnerabilities found using your search criteria':
		return None
	else:
		result_list = soup.find_all("div", {"class": "cvp_short"})
		return result_list


def get_all_files():
	lemp_files_dir = TPL_FOLDER # Specify directory with php file TODO: Get vuln php codes
	lemp_files_arr = []
	get_tpl_files(lemp_files_dir, lemp_files_arr)
	return lemp_files_arr

# Function to get list of php files
def get_tpl_files(dir, result):
    # Loop through directory 
    for file in os.listdir(dir):
        # File uri
        file_path = os.path.join(dir, file)
        # Check if isfile and with .php extension
        if os.path.isfile(file_path):
            if file.endswith('.tpl'):
                result.append(file)

def generate_script_report():
	apt_update_checked = False
	validated = False
	mysqlSecureChecked = False

	mysqlSecureCommands = ["sudo mysql -e \"UPDATE mysql.user SET Password = PASSWORD(\'$database_pwd\') WHERE User = \'root\'\"",
	'sudo mysql -e \"DROP USER \'\'@\'$(hostname)\'\"',
	'sudo mysql -e "DROP DATABASE test"']

	apt_update_pattern = r"apt(-get)? update(\s-y)?"
	apt_install_pattern = r"apt(-get)? install(=[\d.]+)?(\s-y)?"

	lemp_report = SimpleDocTemplate("./report/2_report_scripts.pdf", pagesize=landscape(A1))
	styles = getSampleStyleSheet()
	report_info = []
	lemp_files = get_all_files()

	for file in lemp_files:
		package_flagged = {}
		file_content_list = getFileContent(TPL_FOLDER+'/'+file)
		section_style = styles["Heading1"]
		section_style.alignment = 0
		section = f"<u>Validations on file: {file}</u>"
		section_data = Paragraph(section, section_style)
		report_info.append(section_data)
		report_info_len = len(report_info)
		sql_flag = False
		for i in file_content_list:
			if not sql_flag:
				sql_flag = has_mql_installation(i)
			# Check Apt update
			if not validated:
				if not apt_update_checked:
					apt_install_match = re.search(apt_install_pattern,i)
					if apt_install_match:
						section_style = styles["Heading2"]
						section_style.alignment = 0
						section = "<u>[WARNING!] apt update is not performed before installtions of package</u>"
						section_data = Paragraph(section, section_style)
						report_info.append(section_data)
						pkgname_style = styles["Heading3"]
						pkgname_style.alignment = 0
						pkgname_style.textColor = colors.red
						pkgname = f"Please run the following command before any package installtions using apt!"
						pkgname_data = Paragraph(pkgname, pkgname_style)
						report_info.append(pkgname_data)
						formatLine = f"|:|<b>sudo apt update </b>\n<br/>{'-' * 180}"
						line_style = styles["Code"]
						line_style.fontSize = 14
						line_style.leading = 14 * 1.2
						line_style.underline = 1
						line_style.alignment = 0
						line_data = Paragraph(formatLine, line_style)
						report_info.append(line_data)	
						# print("[!]************** Warning! apt update is not run before installtions from apt.")
						validated = True
					if not validated:
						apt_update_match = re.search(apt_update_pattern,i)
						if apt_update_match:
							apt_update_check = True
							validated = True
			# Check specificed package vulnerabilities
			if has_version_number(i):
				package_name, package_version = extract_package_info(i)
				query = CVE_number(package_name, package_version)
				if query:
					package_details = []
					# print("\n[!]*************Package: "+package_name+"\tVersion: "+package_version+" Vulnerabilities found!\n")
					for x in query:
						package_details.append(x.get_text(" ", strip=True))
					package_flagged[package_name+' '+package_version] = package_details
				else:
					print("No vulnerabilities found for "+package_name+":"+package_version)
			if sql_flag:
				if not mysqlSecureChecked:
					mysqlSecureChecked=mysqlSecureCheck(i,mysqlSecureCommands)

		if len(package_flagged)>1:
			section_style = styles["Heading2"]
			section_style.alignment = 0
			section = f"<u>Vulnerable Packages found: </u>"
			section_data = Paragraph(section, section_style)
			report_info.append(section_data)

			for key, value in package_flagged.items():
				# print("*"*50)
				# print(f"Potential vulnerability package found in: [{key}]")

				pkgname_style = styles["Heading3"]
				pkgname_style.alignment = 0
				pkgname_style.textColor = colors.red
				pkgname = f"Potential vulnerability found in: [{key}]"
				pkgname_data = Paragraph(pkgname, pkgname_style)
				report_info.append(pkgname_data)

				for line in value:
					formatLine = f"|:|<b>{line}</b>\n<br/>{'-' * 180}"
					line_style = styles["Code"]
					line_style.fontSize = 14
					line_style.leading = 14 * 1.2
					line_style.underline = 1
					line_style.alignment = 0
					line_data = Paragraph(formatLine, line_style)
					report_info.append(line_data)
		if len(report_info)==report_info_len:
			pkgname_style = styles["Heading2"]
			pkgname_style.alignment = 0
			pkgname_style.textColor = colors.green
			pkgname = f"No vulnerability found in: [{file}]"
			pkgname_data = Paragraph(pkgname, pkgname_style)
			report_info.append(pkgname_data)
		if sql_flag:
			# Display check result of mysql_secure_installation
			if mysqlSecureChecked is False:
				section_style = styles["Heading2"]
				section_style.alignment = 0
				section_style.textColor = colors.black
				section = f"<u>Mysql-secure-installation is not performed properly on file: {file}</u>"
				section_data = Paragraph(section, section_style)
				report_info.append(section_data)

				if len(mysqlSecureCommands)>0:
					# print("[!] ************************************* Following command Not performed!")
					# print("\n["+" || 	".join(mysqlSecureCommands)+"]")

					pkgname_style = styles["Heading3"]
					pkgname_style.alignment = 0
					pkgname_style.textColor = colors.red
					pkgname = f"Following command Not performed!"
					pkgname_data = Paragraph(pkgname, pkgname_style)
					report_info.append(pkgname_data)
					for xx in mysqlSecureCommands:
						formatLine = f"|:|<b>{xx}</b>\n<br/>{'-' * 180}"
						line_style = styles["Code"]
						line_style.fontSize = 14
						line_style.leading = 14 * 1.2
						line_style.underline = 1
						line_style.alignment = 0
						line_data = Paragraph(formatLine, line_style)
						report_info.append(line_data)
				else:
					# print("[!] ************************************* \"FLUSH PRIVILEGES\" Not performed!")
					pkgname_style = styles["Heading3"]
					pkgname_style.alignment = 0
					pkgname_style.textColor = colors.red
					pkgname = f"FLUSH PRIVILEGES command Not performed properly!"
					pkgname_data = Paragraph(pkgname, pkgname_style)
					report_info.append(pkgname_data)
					formatLine = f"|:|<b>sudo mysql -e \"FLUSH PRIVILEGES\"</b>\n<br/>{'-' * 180}"
					line_style = styles["Code"]
					line_style.fontSize = 14
					line_style.leading = 14 * 1.2
					line_style.underline = 1
					line_style.alignment = 0
					line_data = Paragraph(formatLine, line_style)
					report_info.append(line_data)
	
	lemp_report.build(report_info)
