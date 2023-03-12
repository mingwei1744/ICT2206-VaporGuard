import re
import json
import os
import csv
import requests
import time

from bs4 import BeautifulSoup
from googletrans import Translator
from datetime import datetime

apt_update_checked = False
validated = False
mysqlSecureChecked = False

mysqlSecureCommands = ["sudo mysql -e \"UPDATE mysql.user SET Password = PASSWORD(\'$database_pwd\') WHERE User = \'root\'\"",
'sudo mysql -e \"DROP USER \'\'@\'$(hostname)\'\"',
'sudo mysql -e "DROP DATABASE test"']

def mysqlSecureCheck(command):
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
	print("Querying Vulnerabilities Database on: {} {}".format(pkg_name,pkg_version))
	source_code = requests.get(link)  # do a get request for html source code
	plain_text = source_code.text  # convert to plain text
	soup = BeautifulSoup(plain_text, 'html.parser')  # using bs4 soup to process
	result = soup.find('div', {'class': 'col-xs-10 col-xs-offset-05'}).get_text(" ", strip=True)
	if result == 'No vulnerabilities found using your search criteria':
		return None
	else:
		result_list = soup.find_all("div", {"class": "cvp_short"})
		return result_list

file_content_list = getFileContent("config_lemp.tpl")
apt_update_pattern = r"apt(-get)? update(\s-y)?"
apt_install_pattern = r"apt(-get)? install(=[\d.]+)?(\s-y)?"

for i in file_content_list:
	# Check Apt update
	if not validated:
		if not apt_update_checked:
			apt_install_match = re.search(apt_install_pattern,i)
			if apt_install_match:
				print("[!]************** Warning! apt update is not run before installtions from apt.")
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
			print("\n[!]*************Package: "+package_name+"\tVersion: "+package_version+" Vulnerabilities found!\n")
			for x in query:
				print(x.get_text(" ", strip=True))
		else:
			print("No vulnerabilities found for "+package_name+":"+package_version)

	# Check mysql_secure_installation
	if not mysqlSecureChecked:
		mysqlSecureChecked=mysqlSecureCheck(i)

# Display check result of mysql_secure_installation
if mysqlSecureChecked is False:
	print("[!] ************************************* mysql-secure-installation is not performed!")
	if len(mysqlSecureCommands)>0:
		print("[!] ************************************* Following command Not performed!")
		print("\n["+" || 	".join(mysqlSecureCommands)+"]")
	else:
		print("[!] ************************************* \"FLUSH PRIVILEGES\" Not performed!")	