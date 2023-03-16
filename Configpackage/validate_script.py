import re
import os
import requests

from reportlab.lib.pagesizes import A1, landscape
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from bs4 import BeautifulSoup
from datetime import datetime

#Global variable for path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_FOLDER = os.path.join(PROJECT_ROOT,'Terraform/scripts')

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
		unparse_package_name = match.group(1)
		parse_pattern = r"(.+)-(.+)"
		parse_match = re.search(parse_pattern, unparse_package_name)
		if parse_match:
			package_name = parse_match.group(1)
		else:
			package_name = unparse_package_name
		package_version = match.group(2)
		return package_name, package_version
	else:
		return None

def has_version_number(command):
	pattern = r"apt(-get)? install\s(.+)(=([\d.]+)?)(\s-y)?$"
	match = re.search(pattern, command)
	return bool(match)

def has_mql_installation(command):
	db = ['mysql','mariadb']
	pattern = r"apt(-get)? install\s(.+)=([\d.]+)?(\s-y)?"
	match = re.search(pattern, command)
	if match:
		unparse_package_name = match.group(2)
		parse_pattern = r"(.+)-(.+)"
		parse_match = re.search(parse_pattern, unparse_package_name)
		if parse_match:
			unparse_package_name = parse_match.group(1)
		return unparse_package_name in db	
	return False

def getFileContent(filename):
	lines=[]
	with open(filename, "r") as file:
		for line in file:
			lines.append(line.strip())
	return lines

def CVE_number(pkg_name, pkg_version):
	link="https://www.cybersecurity-help.cz/vdb/list.php?search_line=Y&filter%5B%25SEARCH%5D={}+{}".format(pkg_name,pkg_version)
	source_code = requests.get(link)  # do a get request for html source code
	plain_text = source_code.text  # convert to plain text
	soup = BeautifulSoup(plain_text, 'html.parser')  # using bs4 soup to process
	result = soup.find('div', {'class': 'col-xs-10 col-xs-offset-05'}).get_text(" ", strip=True)
	if result == 'No vulnerabilities found using your search criteria':
		return None
	else:
		result_list = soup.find_all("div", {"class": "cvp_short"})
		return result_list, link


def get_all_lemp_files():
	lemp_files_dir = TPL_FOLDER # Specify directory with php file
	lemp_files_arr = []
	get_tpl_files(lemp_files_dir, lemp_files_arr)
	return lemp_files_arr

# Function to get list of tpl files
def get_tpl_files(dir, result):
    # Loop through directory 
    for file in os.listdir(dir):
        # File uri
        file_path = os.path.join(dir, file)
        # Check if isfile and with .tpl extension
        if os.path.isfile(file_path):
            if file.endswith('.tpl'):
                result.append(file)
def cast_severity(result_str):
	col = "black"
	if result_str == "Low":
		col = "green"
	elif result_str == "Medium":
		col = "orange"
	elif result_str == "High":
		col = "red"
	return f"|:|Severity:<font color='{col}'>"+result_str+"</font>"

def cast_verify(result_str):
	col = "orange"
	if result_str == "Yes":
		col = "green"
	return f"|:|Verified:<font color='{col}'>"+result_str+"</font>"

# Functions to scan and generate tpl validation report
def generate_script_report():
	mysqlSecureChecked = False
	clickable = "Click here for more detail!"
	mysqlSecureCommands = [	
	"sudo mysql -e \"UPDATE mysql.user SET Password = PASSWORD(\'$database_pwd\') WHERE User = \'root\'\"",
	'sudo mysql -e \"DROP USER \'\'@\'$(hostname)\'\"',
	'sudo mysql -e "DROP DATABASE test"']

	apt_update_pattern = r"apt(-get)? update(\s-y)?"
	apt_install_pattern = r"apt(-get)? install(=[\d.]+)?(\s-y)?"

	lemp_report = SimpleDocTemplate("./Reports/2_report_scripts.pdf", pagesize=landscape(A1))
	styles = getSampleStyleSheet()
	report_info = []
	lemp_files = get_all_lemp_files()

	title_style = styles["Title"]
	title_style.fontSize = 40
	title_style.leading = 40 * 2
	title = f"<u>Configuration Scripts Scan Results</u>"
	title_data = Paragraph(title, title_style)
	report_info.append(title_data)

	for file in lemp_files:
		file_content_list = getFileContent(TPL_FOLDER+'/'+file)
		file_section_style = styles["Heading1"]
		file_section_style.fontSize = 24
		file_section_style.leading = 24 * 1.2
		file_section_style.alignment = 0
		file_section = f"<u>File:\t{file}</u>"
		file_section_data = Paragraph(file_section, file_section_style)
		report_info.append(file_section_data)

		package_flagged = {}
		sql_flag = False
		apt_update_checked = False
		validated = False
		report_info_len = len(report_info)
		for i in file_content_list:
			if not sql_flag:
				sql_flag = has_mql_installation(i)
			# Verify Apt update
			if not validated:
				# If Apt update not checked, check every line for installing command
				if not apt_update_checked:
					apt_install_match = re.search(apt_install_pattern,i)
					# If found, prompt warning
					if apt_install_match:
						apt_style = styles["Heading3"]
						apt_style.fontSize = 18
						apt_style.leading = 18 * 1.2
						apt_style.alignment = 0
						apt_style.textColor = colors.red
						apt = "WARNING! apt update is not perform before installtions of package"
						apt_data = Paragraph(apt, apt_style)
						report_info.append(apt_data)

						formatLine = f"|:|<b>sudo apt update </b>\n<br/>{'-' * 180}"
						line_style = styles["Code"]
						line_style.fontSize = 14
						line_style.leading = 14 * 1.2
						line_style.underline = 1
						line_style.alignment = 0
						line_data = Paragraph(formatLine, line_style)
						report_info.append(line_data)

						pkgname_style = styles["Normal"]
						pkgname_style.alignment = 0
						pkgname_style.fontSize = 12
						pkgname_style.leading = 12 * 1.2
						pkgname_style.textColor = colors.blue
						pkgname = f"Before installing any packages using apt, it is advisable to run the above command.<br></br>"
						pkgname_data = Paragraph(pkgname, pkgname_style)
						report_info.append(pkgname_data)	

						validated = True
					# If not found, check apt update command
					if not validated:
						apt_update_match = re.search(apt_update_pattern,i)
						if apt_update_match:
							apt_update_check = True
							validated = True

			# Check specificed package vulnerabilities
			if has_version_number(i):
				package_name, package_version = extract_package_info(i)
				query , url= CVE_number(package_name, package_version)
				if query:
					package_details = []
					for x in query:
						rs = x.get_text(" ", strip=True)
						rs = rs.split()
						last2 = rs[-2:]
						last2[0] = cast_severity(last2[0])
						last2[1] = cast_verify(last2[1])
						last2 = [f"\t{p}" for p in last2]
						rs = ' '.join(rs[:-3])+"\t["+rs[-3]+"]"+' '.join(last2)
						package_details.append(rs)
					package_details.append(url)
					package_flagged[package_name+' '+package_version] = package_details

			# If particular file has install mysql or mariadb thn validate secure installation
			if sql_flag:
				if not mysqlSecureChecked:
					mysqlSecureChecked=mysqlSecureCheck(i,mysqlSecureCommands)
		# If result found for package x, print findings
		if len(package_flagged)>1:
			for key, value in package_flagged.items():
				pkgname_style = styles["Heading3"]
				pkgname_style.fontSize = 18
				pkgname_style.leading = 18 * 1.2
				pkgname_style.alignment = 0
				pkgname_style.textColor = colors.red
				pkgname = f"Potential vulnerability found in: [{key}]"
				pkgname_data = Paragraph(pkgname, pkgname_style)
				report_info.append(pkgname_data)
				pkg_link = value.pop()
				for line in value:
					formatLine = f"|:|<b>{line}</b>\n<br/>{'-' * 180}"
					line_style = styles["Code"]
					line_style.fontSize = 14
					line_style.leading = 14 * 1.2
					line_style.underline = 1
					line_style.alignment = 0
					line_data = Paragraph(formatLine, line_style)
					report_info.append(line_data)

				link_style = styles["Normal"]
				link_style.fontSize = 12
				link_style.leading = 12 * 1.2
				link_style.textColor = colors.blue
				link_style.alignment = 0
				link_data = Paragraph('<u><link href="' + pkg_link + '">' + clickable + '</link></u><br></br>', link_style)
				report_info.append(link_data)
		# If report_info_len didnt change, conclude no vul found!
		if len(report_info)==report_info_len:
			pkgname_style = styles["Heading2"]
			pkgname_style.alignment = 0
			pkgname_style.textColor = colors.green
			pkgname = f"No vulnerability found in: [{file}]"
			pkgname_data = Paragraph(pkgname, pkgname_style)
			report_info.append(pkgname_data)
		# If file flagged mysql/mariadb installed
		if sql_flag:
			# Display check result of mysql_secure_installation
			if mysqlSecureChecked is False:
				mysql_style = styles["Heading3"]
				mysql_style.fontSize = 18
				mysql_style.leading = 18 * 1.2
				mysql_style.alignment = 0
				mysql_style.textColor = colors.red
				mysql = f"Mysql-secure-installation is not performed properly! The following command was not executed."
				mysql_data = Paragraph(mysql, mysql_style)
				report_info.append(mysql_data)

				if len(mysqlSecureCommands)>0:
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
					formatLine = f"|:|<b>sudo mysql -e \"FLUSH PRIVILEGES\"</b>\n<br/>{'-' * 180}"
					line_style = styles["Code"]
					line_style.fontSize = 14
					line_style.leading = 14 * 1.2
					line_style.underline = 1
					line_style.alignment = 0
					line_data = Paragraph(formatLine, line_style)
					report_info.append(line_data)

				sqlReco_style = styles["Normal"]
				sqlReco_link = "https://bertvv.github.io/notes-to-self/2015/11/16/automating-mysql_secure_installation/"
				sqlReco_style.alignment = 0
				sqlReco_style.fontSize = 12
				sqlReco_style.leading = 12 * 1.2
				sqlReco_style.textColor = colors.blue
				sqlReco_data = Paragraph('<u><link href="' + sqlReco_link + '">' + clickable + '</link></u><br></br>', sqlReco_style)
				report_info.append(sqlReco_data)
	# build report
	lemp_report.build(report_info)