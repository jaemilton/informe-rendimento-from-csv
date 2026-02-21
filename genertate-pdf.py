#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import pdfkit
import unidecode
from datetime import datetime
import csv
from tqdm import tqdm
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Define paths (adjust for your installation and file locations)
PATH_WKHTMLTOPDF = r'.\\wkhtmltox\\bin\\wkhtmltopdf.exe' # Use a raw string for path

# Create a configuration object pointing to the wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)


# --- PDF generation options (explicitly set encoding) ---
options = {
    'encoding': 'UTF-8',
    'enable-local-file-access': True # Needed for local CSS/images if using from_string or from_file
}



# #read informe-model.html content with utf-8 encoding
file = open('informe-model-from-image.html', 'r', encoding='utf-8')
html_content_template = file.read()
file.close()

html_content_template = html_content_template.replace('{{DATA}}', os.getenv('DATA_INFOME'))
html_content_template = html_content_template.replace('{{CNPJ_FONTE_PAGADORA}}', os.getenv('CNPJ_FONTE_PAGADORA'))
html_content_template = html_content_template.replace('{{NOME_FONTE_PAGADORA}}', os.getenv('NOME_FONTE_PAGADORA'))
html_content_template = html_content_template.replace('{{NOME_RESPOSAVEL_INFORMACOES}}', os.getenv('NOME_RESPOSAVEL_INFORMACOES'))
html_content_template = html_content_template.replace('{{ANO_EXERCICIO}}', os.getenv('ANO_EXERCICIO'))
html_content_template = html_content_template.replace('{{ANO_CALENDARIO}}', os.getenv('ANO_CALENDARIO'))

# read csv file with utf-8 encoding
with open('dados.csv', 'r', encoding='utf-8') as csvfile:
    csv_data = list(csv.DictReader(csvfile, delimiter=';'))
    total_rows = len(csv_data)
    
for row in tqdm(csv_data, desc='Processing CSV records', unit='record'):
        nome = row['nome']
        #get nome and format it as uppercase
        nome = nome.upper()
        #remove accents from nome
        nome_without_accents = unidecode.unidecode(nome)
        
        #get cpf and format it as 000.000.000-00
        cpf = row['cpf']
        formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        valor = row['valor']
        valor = valor.lstrip().replace(".", "").replace(",", ".") # Replace comma with dot for float conversion
        #get valor and format it as R$ 0.000,00
        valor = f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                

        # Replace placeholders in the HTML template with actual values
        html_content = html_content_template.replace('{{NOME}}', nome)
        html_content = html_content.replace('{{CPF}}', formatted_cpf)
        html_content = html_content.replace('{{VALOR}}', valor)
        # Convert from an HTML file
        # pdfkit.from_file('index.html', 'output_file.pdf')
        pdfkit.from_string(html_content, f'./pdfs/{nome_without_accents}.pdf', configuration=config, options=options)