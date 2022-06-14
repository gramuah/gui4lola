import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import customtkinter
from reporter_datapane import generate_report


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# create the root window
root = customtkinter.CTk()
root.title('Generador de informes')
root.resizable()
root.geometry('500x200')


def select_file():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='~/',
        filetypes=filetypes)

    generate_report(filename)

    showinfo(
        title='Informe generado',
        message=filename
    )



# open button
open_button = customtkinter.CTkButton(
    root,
    text='Generar informe',
    command=select_file,
)

open_button.pack(expand=True)


# run the application
root.mainloop()
