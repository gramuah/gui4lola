# GUI FOR LOLA PLATFORM
import json
import os
import random
import tkinter as tk

from tkvlc import Player
from utilities import ImageLabel


class App(tk.Tk):
    """
    Main dialog (root window)
    """

    def __init__(self):
        super().__init__()

        self.title('Bienvenidos a LOLA')
        # self.wm_iconbitmap("/home/ivanf/proyects/gui4lola/data/Image/robot.ico")
        self.path = "config/config.json"
        self.config_data = None

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

    @staticmethod
    def __open_file(path):
        """
        Function to open the file
        :return: serialized data from json
        """

        # Read file
        f = open(path)
        config_data = json.load(f)
        f.close()

        return config_data

    def __close_file(self):
        """
        Function to close the file
        """

        # Serialize json
        json_serialized = json.dumps(self.config_data)

        # Writing to config_new.json
        with open(self.path, "w") as outfile:
            outfile.write(json_serialized)

    def __save_data_option(self, _):
        """
        Function to save option menu the data to a dict
        """
        self.config_data["last_id"] = self.last_id.get()
        self.config_data["users_info"][self.last_id.get()]["last_action"] = self.last_action.get()

    def __save_data_check(self):
        """
        Function to save the check button data to a dict
        """
        self.config_data["users_info"][self.last_id.get()]["last_oaa"] = self.last_online_action_detection.get()
        self.config_data["users_info"][self.last_id.get()]["last_pe"] = self.last_pose_estimation.get()
        self.config_data["users_info"][self.last_id.get()]["last_rg"] = self.last_report_generation.get()

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
        # Open file
        
        self.config_data = self.__open_file(self.path)

        """
        function to create Dialog for action analysis window
        """
        window_config = tk.Toplevel(self.master)
        window_config.grab_set()
        window_config.geometry("500x500")
        window_config.title('LOLA - Configuración del dispositivo')

        # Prepare buttons for the dialog
        conf_label = tk.Label(window_config, text="Configuración").place(x=210, y=30)
        dni_label = tk.Label(window_config, text="Usuario").place(x=22, y=70)
        action_label = tk.Label(window_config, text="Acciones").place(x=22, y=130)
        oad_label = tk.Label(window_config, text="Activar detección de acciones en tiempo real").place(x=90, y=200)
        atp_label = tk.Label(window_config, text="Activar analisis de la postura corporal").place(x=110, y=260)
        rg_label = tk.Label(window_config, text="Generar informe").place(x=190, y=320)

        self.last_id = tk.StringVar()
        self.last_id.set(self.config_data['last_id'])
        options1 = [*self.config_data["users_info"]]

        self.last_action = tk.StringVar()
        self.last_action.set(self.config_data['users_info'][self.last_id.get()]['last_action'])
        options = self.config_data['actions']

        self.last_online_action_detection = tk.BooleanVar()
        self.last_online_action_detection.set(self.config_data['users_info'][self.last_id.get()]['last_oaa'])

        self.last_pose_estimation = tk.BooleanVar()
        self.last_pose_estimation.set(self.config_data['users_info'][self.last_id.get()]['last_pe'])

        self.last_report_generation = tk.BooleanVar()
        self.last_report_generation.set(self.config_data['users_info'][self.last_id.get()]['last_rg'])

        id = tk.OptionMenu(window_config, self.last_id, *options1, command=self.__save_data_option)
        id.config(width="35")
        id.place(x=22, y=90)

        action = tk.OptionMenu(window_config, self.last_action, *options, command=self.__save_data_option)
        action.config(width="40")
        action.place(x=22, y=150)

        button_oaa = tk.Checkbutton(window_config,
                                    text='SI',
                                    variable=self.last_online_action_detection,
                                    onvalue=True,
                                    offvalue=False,
                                    command=self.__save_data_check).place(x=220, y=230)
        button_pe = tk.Checkbutton(window_config,
                                   text='SI',
                                   variable=self.last_pose_estimation,
                                   onvalue=True,
                                   offvalue=False,
                                   command=self.__save_data_check).place(x=220, y=290)
        button_rg = tk.Checkbutton(window_config,
                                   text='SI',
                                   variable=self.last_report_generation,
                                   onvalue=True,
                                   offvalue=False,
                                   command=self.__save_data_check).place(x=220, y=350)

        submit_btn = tk.Button(window_config, text="Guardar", width="25", height="2", command=self.__close_file).place(
            x=150, y=400)

        exit_button = tk.Button(window_config, text="Salir", width="25", height="2", command=lambda: window_config.destroy()).place(
            x=150, y=450)

        window_config.mainloop()

    def open_window_save(self):
        """

        :return:
        """
        window_config_save = tk.Toplevel(self.master)
        window_config_save.grab_set()
        window_config_save.geometry("500x500")
        window_config_save.title('Guardado')

        self.window_config_save.mainloop()

    def on_activity(self):
        """
        Creates a frame to display VLC Media player
        """
        # Load data
        if self.config_data:
            pass
        else:
            self.config_data = self.__open_file(self.path)
        last_id = self.config_data['last_id']
        video_dir = "data/Video/" + self.config_data['users_info'][last_id]['last_action']
        video_name = random.choice(os.listdir(video_dir))
        video_path = os.path.join(video_dir, video_name)
        # VLC player object
        self.player = Player(self.window_oaa, title='LOLA - Monitorizacion de acciones', video=video_path)
        self.window_oaa.protocol(("WM_DELETE_WINDOW", self.player.OnClose))

    def on_monitorization(self):
        """
        Placeholder for the monitorization activity
        :return: NotImplemented
        """
        return NotImplemented

if __name__ == "__main__":
    # Run main dialog
    app = App()
    app.mainloop()
