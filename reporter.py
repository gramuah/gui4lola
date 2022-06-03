from fpdf import FPDF
import pandas as pd

# Variables
input_csv_path = '~/Downloads/log_nadia.csv'
input_images_prefix_path = '~/imagenes'


# Functions
def format_card(row):
    """
    Format a row from the csv to print it in the pdf like a card
    @param row: row taken from the csv containing all the info for the card
    """
    table_cell_width = 40
    table_cell_height = 6
    requested_action = str(getattr(row, 'Requested_Action'))
    pdf.cell(table_cell_width, table_cell_height, 'Acción Pedida', align='C', border=1)
    pdf.cell(table_cell_width, table_cell_height, requested_action, align='C', border=1)
    path = str(getattr(row, 'Path'))
    pdf.image('data/Image/robot.jpg', w=20, h=10, x=120)
    pdf.ln(10)
    predicted_action = str(getattr(row, 'Predicted_Action'))
    pdf.cell(table_cell_width, table_cell_height, 'Acción Realizada', align='C', border=1)
    pdf.cell(table_cell_width, table_cell_height, predicted_action, align='C', border=1)
    pdf.ln(10)
    init_date = str(getattr(row, 'T_Start'))
    pdf.cell(table_cell_width, table_cell_height, 'Fecha de inicio', align='C', border=1)
    pdf.cell(table_cell_width, table_cell_height, init_date, align='C', border=1)
    pdf.ln(10)
    init_date = str(getattr(row, 'T_End'))
    pdf.cell(table_cell_width, table_cell_height, 'Fecha de finalizacion', align='C', border=1)
    pdf.cell(table_cell_width, table_cell_height, init_date, align='C', border=1)
    pdf.ln(30)


# 1. Set up the PDF doc basics
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

# 2. Layout the PDF doc contents

# Title
# Get user name
user_name = input_csv_path.split('_')[-1].split('.')[0]
pdf.cell(40, 10, 'Report de {}'.format(user_name))

# Line breaks
pdf.ln(20)

# Image
# Ajustamos los parámetros para colocar los logos del proyecto
pdf.image('data/Image/robot.jpg', x=100, y=20, w=20, h=10, link='https://google.com')
pdf.image('data/Image/robot.jpg', x=80, y=20, w=20, h=10, link='https://gram.web.uah.es')

# Line breaks
pdf.ln(20)

# Load csv
data = pd.read_csv('~/Downloads/log_nadia.csv')

pdf.ln(20)
pdf.set_font('Arial', '', 10)
# Create a loop to print the rows of the document
for row in data.itertuples():
    format_card(row)


def output_df_to_pdf(pdf, df):
    # A cell is a rectangular area, possibly framed, which contains some text
    # Set the width and height of cell
    table_cell_width = 32
    table_cell_height = 6
    # Select a font as Arial, bold, 8
    pdf.set_font('Arial', 'B', 8)

    # Loop over to print column names
    cols = df.columns
    for col in cols:
        pdf.cell(table_cell_width, table_cell_height, col, align='C', border=1)
    # Line break
    pdf.ln(table_cell_height)
    # Select a font as Arial, regular, 10
    pdf.set_font('Arial', '', 10)
    # Loop over to print each data in the table
    for row in df.itertuples():
        for col in cols:
            value = str(getattr(row, col))
            pdf.cell(table_cell_width, table_cell_height, value, align='C', border=1)
        pdf.ln(table_cell_height)


# Use the function defined earlier to print the DataFrame as a table on the PDF
# output_df_to_pdf(pdf, data)

# Line breaks
pdf.ln(20)

# 3. Output the PDF file
pdf.output('fpdf_pdf_report.pdf', 'F')
