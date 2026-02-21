#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# #read informe-model.html content with utf-8 encoding
file = open('informe-model.html', 'r', encoding='utf-8')
html_content_template = file.read()
file.close()

import pdfkit

# Define paths (adjust for your installation and file locations)
PATH_WKHTMLTOPDF = r'.\\wkhtmltox\\bin\\wkhtmltopdf.exe' # Use a raw string for path

# Create a configuration object pointing to the wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)


# --- PDF generation options (explicitly set encoding) ---
options = {
    'encoding': 'UTF-8',
    'enable-local-file-access': None # Needed for local CSS/images if using from_string or from_file
}

#get today data  and format it dd de mmmm de aaaa
from datetime import datetime
data = datetime.today().strftime('%d/%m/%Y')
# Split the date string into day, month, and year components
day, month, year = data.split('/')
# Define a mapping of month numbers to month names in Portuguese
month_names = {
    '01': 'janeiro',
    '02': 'fevereiro',
    '03': 'março',
    '04': 'abril',
    '05': 'maio',
    '06': 'junho',
    '07': 'julho',
    '08': 'agosto',
    '09': 'setembro',
    '10': 'outubro',
    '11': 'novembro',
    '12': 'dezembro'
}
# Get the month name from the mapping
month_name = month_names[month]

# Format the date as "dd de mmmm de aaaa"
formatted_date = f"{day} de {month_name} de {year}"

# read csv file with utf-8 encoding
import csv
with open('dados.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        nome = row['nome']
        #get cpf and format it as 000.000.000-00
        cpf = row['cpf']
        formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        valor = row['valor']
        valor = valor.replace(",", ".") # Replace comma with dot for float conversion
        #get valor and format it as R$ 0.000,00
        valor = f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                

        # Replace placeholders in the HTML template with actual values
        html_content = html_content_template.replace('{{NOME}}', nome)
        html_content = html_content.replace('{{CPF}}', formatted_cpf)
        html_content = html_content.replace('{{VALOR}}', valor)
        html_content = html_content.replace('{{DATA}}', formatted_date)

        # Convert from an HTML file
        # pdfkit.from_file('index.html', 'output_file.pdf')
        pdfkit.from_string(html_content, f'{cpf}.pdf', configuration=config, options=options)