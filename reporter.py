from fpdf import FPDF
import pandas as pd
import os

# Variables
input_csv_path = '~/Downloads/log_nadia.csv'
input_images_prefix_path = '~/imagenes'


# Functions
def format_card(row, temp):
    """
    Format a row from the csv to print it in the pdf like a card
    @param row: row taken from the csv containing all the info for the card
    """
    init_pos_y = 98
    table_cell_width = 94
    table_cell_height = 7
    requested_action = str(getattr(row, 'Requested_Action'))
    pdf.cell(table_cell_width, table_cell_height, 'Acción Pedida', align='C', border=1)
    pdf.cell(table_cell_width, table_cell_height, requested_action, align='C', border=1)
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
    pdf.ln(60)
    path = str(getattr(row, 'Path'))
    dir_list = 'data/Image/'
    paths = os.listdir(dir_list)
    offset = 0
    for path in paths:
        extended_path = os.path.join(dir_list, path)
        pdf.image(extended_path, x=(30 + offset), y=init_pos_y + temp, w=30, h=30)
        offset += 60
    # 'data/Image/robot.jpg'



# 1. Set up the PDF doc basics
pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 30)

# 2. Layout the PDF doc contents

# Title
# Get user name
user_name = input_csv_path.split('_')[-1].split('.')[0]
pdf.cell(80, 17, 'Report de {}'.format(user_name), align='C')

# Line breaks
pdf.ln(20)
pdf.set_font('Arial', 'B', 16)
# Image
# Ajustamos los parámetros para colocar los logos del proyecto
pdf.image('data/Image/uah.jpg', x=175, y=10, w=27, h=17, link='https://www.uah.es')
pdf.image('data/Image/logo_air4dp.png', x=140, y=10, w=27, h=17, link='')

# Load csv
data = pd.read_csv('~/Downloads/log_nadia.csv')

pdf.ln(20)
pdf.set_font('Arial', '', 10)
# Create a loop to print the rows of the document
temp = 0
for i, row in enumerate(data.itertuples()):
    format_card(row, temp)
    if i % 2 == 0 and i != 0:
        pdf.add_page()
    temp += 90



# Use the function defined earlier to print the DataFrame as a table on the PDF
# output_df_to_pdf(pdf, data)

# Line breaks
pdf.ln(20)

# 3. Output the PDF file
pdf.output('Report.pdf', 'F')
