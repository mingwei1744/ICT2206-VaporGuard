import os
from PyPDF2 import PdfFileMerger

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

            # Close the PDF file
            pdf_file.close()

    # Write the output PDF file
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)


#merge_pdfs('./', './new.pdf')
