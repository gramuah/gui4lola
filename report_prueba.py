from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import itertools
from random import randint
from statistics import mean
import pandas as pd
import os

# Variables
input_csv_path = '~/Downloads/log_nadia.csv'
input_images_prefix_path = '~/imagenes'

# Load csv
data = pd.read_csv(input_csv_path)

# Pdf

"""
Title
"""
w, h = A4
c = canvas.Canvas("Reportprueba.pdf", pagesize=A4)
c.setFillColorRGB(0, 0, 0)
c.setFont("Helvetica", 25)
user_name = input_csv_path.split('_')[-1].split('.')[0]
c.drawString(50, h - 65, 'Report de {}'.format(user_name))


"""
Image
"""
c.drawImage("data/Image/uah.jpg", 475, h - 70, width=70, height=50)
c.drawImage("data/Image/logo_air4dp.png", 390, h - 70, width=70, height=50)

"""
Text
"""


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


def export_to_pdf(data):
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 100
    # Space between rows.
    padding = 15

    xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

# PDF Table
# PDF Table - Styles
# [(start_column, start_row), (end_column, end_row)]
all_cells = [(0, 0), (-1, -1)]
header = [(0, 0), (-1, 0)]
column0 = [(0, 0), (0, -1)]
column1 = [(1, 0), (1, -1)]
column2 = [(2, 0), (2, -1)]
column3 = [(3, 0), (3, -1)]
column4 = [(4, 0), (4, -1)]
column5 = [(5, 0), (5, -1)]
column6 = [(6, 0), (6, -1)]
table_style = TableStyle([
    ('VALIGN', all_cells[0], all_cells[1], 'TOP'),
    ('LINEBELOW', header[0], header[1], 1, colors.black),
    ('ALIGN', column0[0], column0[1], 'LEFT'),
    ('ALIGN', column1[0], column1[1], 'LEFT'),
    ('ALIGN', column2[0], column2[1], 'LEFT'),
    ('ALIGN', column3[0], column3[1], 'RIGHT'),
    ('ALIGN', column4[0], column4[1], 'RIGHT'),
    ('ALIGN', column5[0], column5[1], 'LEFT'),
    ('ALIGN', column6[0], column6[1], 'RIGHT'),
])

# PDF Table - Column Widths
colWidths = [
    3.5 * cm,  # Column 0
    3.1 * cm,  # Column 1
    3.7 * cm,  # Column 2
    1.2 * cm,  # Column 3
    2.5 * cm,  # Column 4
    6 * cm,  # Column 5
]

# PDF Table - Strip '[]() and add word wrap to column 5
for index, row in enumerate(data):
    for col, val in enumerate(row):
        if col != 5 or index == 0:
            data[index][col] = val.strip("'[]()")
        else:
            data[index][col] = Paragraph(val)

# Add table to elements
t = Table(data, colWidths=colWidths)
t.setStyle(table_style)
elements.append(t)



c.setFont("Helvetica", 12)
export_to_pdf(data)


# Dibujar una línea horizontal.
x = 50
y = h - 75
c.line(x, y, x + 500, y)
x = 50
y = h - 400
c.line(x, y, x + 500, y)
c.showPage()
c.save()

