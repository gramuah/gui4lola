# GUI FOR LOLA PLATFORM
import tkinter as tk
from utilities import ImageLabel
import vlc
from tkvlc import Player
import json

class App(tk.Tk):
    """
    Main dialog (root window)
    """
    def __init__(self):
        super().__init__()

        self.title('Bienvenidos a LOLA')

        # Create background image
        lbl = ImageLabel(self)
        lbl.pack()
        lbl.load('data/Gift/robot.gif')

        # place a button on the root window for action analysis window
        tk.Button(self,
                  text='Comenzar',
                  command=self.open_action_analysis).pack()
        tk.Button(self,
                  text='Configuración',
                  command=self.open_configuration).pack()

    def open_action_analysis(self):
        """
        function to create Dialog for action analysis window
        """
        self.window_oaa = tk.Toplevel(self.master)
        self.window_oaa.grab_set()
        self.window_oaa.title('LOLA - Monitorizacion de acciones')
        # Prepare buttons for the dialog
        # Button to start activity (with video visualization)
        tk.Button(self.window_oaa,
                  text='Comenzar Actividad',
                  command=self.on_activity).pack()

        # Button to start monitorization
        tk.Button(self.window_oaa,
                  text='Comenzar Monitorización',
                  command=self.on_monitorization).pack()
        self.window_oaa.mainloop()

    def open_configuration(self):
        x = 'json'
        y = json.loads(x)
        """
        function to create Dialog for action analysis window
        """
        self.window_config = tk.Toplevel(self.master)
        self.window_config.grab_set()
        self.window_config.geometry("500x500")
        self.window_config.title('LOLA - Configuración del dispositivo')

        # Prepare buttons for the dialog
        conf_label = tk.Label(self.window_config, text="Configuración").place(x=210, y=30)
        dni_label = tk.Label(self.window_config, text="Usuario")
        dni_label.place(x=22, y=70)
        action_label = tk.Label(self.window_config, text="Acciones")
        action_label.place(x=22, y=130)
        oad_label = tk.Label(self.window_config, text="Activar detección de acciones en tiempo real")
        oad_label.place(x=90, y=220)
        atp_label = tk.Label(self.window_config, text="Activar analisis de la postura corporal")
        atp_label.place(x=140, y=260)
        rg_label = tk.Label(self.window_config, text="Generar informe")
        rg_label.place(x=190, y=320)


        options = tk.StringVar()
        self.var = tk.StringVar()
        self.var.set('Caminar')
        options = ['Secarse el pelo', 'Lavarse los dientes', 'Teclear', 'Pasear con el perro', 'Mezclar',
                 'Escribir en la pizarra', 'Gatear', 'Nadar', 'Soplar las velas', 'Saltar en trampolín',
                 'Montar en bicicleta', 'Caminar']

        options1 = tk.StringVar()
        self.users = tk.StringVar()
        self.users.set('UDC_0036')
        options1 = ['UDC_0036', 'UDC_6523', 'UDC_6569', 'UDC_6263']

        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()

        self.users = tk.OptionMenu(self.window_config, self.users, *options1)
        self.users.config(width="35")
        self.users.place(x=22, y=220)

        self.action = tk.OptionMenu(self.window_config, self.var, *options)
        self.action.config(width="40")
        self.action.place(x=22, y=190)


        c1 = tk.Checkbutton(self.window_config, text='SI', variable=self.var1, onvalue=1, offvalue=0).place(x=220, y=290)
        c2 = tk.Checkbutton(self.window_config, text='SI', variable=self.var2, onvalue=1, offvalue=0).place(x=220, y=350)
        c3 = tk.Checkbutton(self.window_config, text='SI', variable=self.var3, onvalue=1, offvalue=0).place(x=220, y=370)

        if self.var1==1:
            print("Hello world")
        else:
            print("Do nothing")

        if self.var2==1:
            print("Hello world")
        else:
            print("Do nothing")

        if self.var3==1:
            print("Hello world")
        else:
            print("Do nothing")

        submit_btn = tk.Button(self.window_config, text="Guardar", command=json.dumps(json), width="25", height="2")
        submit_btn.place(x=150, y=400)

        self.window_config.mainloop()

    def on_activity(self):
        """
        Creates a frame to display VLC Media player
        """
        # VLC player object
        # TODO: select from the dataset of activities
        video_name = "data/Video/Lavarlosdientes.mp4"
        self.player = Player(self.window_oaa, title='LOLA - Monitorizacion de acciones', video=video_name)
        self.window_oaa.protocol(("WM_DELETE_WINDOW", self.player.OnClose))

    def on_monitorization(self):
        print('patata')


    def send_data(self):
        dni_data = self.dni.get()
        username_data = self.username.get()
        newfile = open("registration.txt", "a")
        newfile.write(dni_data)
        newfile.write("\t")
        newfile.write(username_data)
        newfile.write("\t")
        newfile.write("\n")
        newfile.close()

        self.dni_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)


if __name__ == "__main__":
    # Run main dialog
    app = App()
    app.mainloop()
