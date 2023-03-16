import os
from termcolor import colored
from PyPDF2 import PdfFileMerger

def warningPrint(msg):
    print(colored(msg, "red", attrs=["bold"]))

reports = ["./Reports/1_report_cloud.pdf", "./Reports/2_report_scripts.pdf", "./Reports/3_report_php.pdf"]

def merge_pdfs(input_dir, output_path):
    # Create an empty PDF merger object
    pdf_merger = PdfFileMerger()

    # Loop through all the PDF files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.pdf'):
            # Open the PDF file
            pdf_file = open(os.path.join(input_dir, filename), 'rb')

            # Add the PDF file to the merger object
            pdf_merger.append(pdf_file)

            pdf_file.close()

    # Write the output PDF file
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)

def merge_reports(output_path):

    pdf_merger = PdfFileMerger()

    # Loop through reports array and merge
    for report in reports:
        if os.path.exists(report):
            with open(report, 'rb') as pdf:
                pdf_merger.append(pdf)
                pdf.close()
        else:
            warningPrint(f"Generate Report: {report.split('/')[2].split('_')[2].split('.')[0]} report missing!")

    with open(output_path, 'wb') as mergedpdf:
        pdf_merger.write(mergedpdf)

def remove_pre_pdf():
    for report in reports:
        if os.path.exists(report):
            os.remove(report)
        else:
            warningPrint(f"Generate Report: {report.split('/')[2].split('_')[2].split('.')[0]} report missing!") 

