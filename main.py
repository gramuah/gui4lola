# GUI FOR LOLA PLATFORM
import json
import os
import random
import tkinter as tk
import tkinter.font as font
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
        self.attributes("-fullscreen", True)
        self.path = "config/config.json"
        self.config_data = None

        self.default_font = font.Font(name='Helvetica', size=30)
        # Create background image
        lbl = ImageLabel(self)
        lbl.place(x=270, y=35)
        lbl.load('data/Gif/robot.gif')

        # place a button on the root window for action analysis window
        tk.Button(self,
                  text='Comenzar',
                  command=self.open_action_analysis, font=self.default_font,  width="10", height="2").place(x=25, y=460)
        tk.Button(self,
                  text='Configuración',
                  command=self.open_configuration, font=self.default_font,  width="12", height="2").place(x=350, y=460)
        tk.Button(self,
                  text="Salir", font=self.default_font,  width="10", height="2",
                  command=lambda: self.destroy()).place(x=720, y=460)

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
        self.window_oaa.attributes("-fullscreen", True)
        self.window_oaa.title('LOLA - Monitorizacion de acciones')
        # Prepare buttons for the dialog
        # Button to start activity (with video visualization)
        tk.Button(self.window_oaa,
                  text='Comenzar Actividad', font=("Helvetica", 25),
                  command=self.on_activity, width="25", height="3").place(x=260, y=100)

        # Button to start monitorization
        tk.Button(self.window_oaa,
                  text='Comenzar Monitorización', font=("Helvetica", 25),
                  command=self.on_monitorization, width="25", height="3").place(x=260, y=250)

        # Button to exit
        tk.Button(self.window_oaa,
                  text="Salir", font=("Helvetica", 25),
                  command=lambda: self.window_oaa.destroy(), width="25", height="3").place(x=260, y=400)
        self.window_oaa.mainloop()

    def open_configuration(self):
        # Open file
        
        self.config_data = self.__open_file(self.path)

        """
        function to create Dialog for action analysis window
        """
        window_config = tk.Toplevel(self.master)
        window_config.grab_set()
        window_config.attributes("-fullscreen", True)
        window_config.title('LOLA - Configuración del dispositivo')

        # Prepare buttons for the dialog
        conf_label = tk.Label(window_config, text="Configuración", font=("Helvetica", 30)).place(x=390, y=30)
        dni_label = tk.Label(window_config, text="Usuario", font=("Helvetica", 20)).place(x=22, y=95)
        action_label = tk.Label(window_config, text="Acciones",font=("Helvetica", 20)).place(x=675, y=95)
        oad_label = tk.Label(window_config, text="Activar detección de acciones en tiempo real",font=("Helvetica", 20)).place(x=250, y=230)
        atp_label = tk.Label(window_config, text="Activar analisis de la postura corporal", font=("Helvetica", 20)).place(x=300, y=330)
        rg_label = tk.Label(window_config, text="Generar informe", font=("Helvetica", 20)).place(x=425, y=430)

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

        id = tk.OptionMenu(window_config, self.last_id, *options1, command=self.__save_data_option,)
        id.config(width="25", height="2", font=("Helvetica", 15))
        menu1= window_config.nametowidget(id.menuname)
        menu1.config(font=("Helvetica", 15))
        id.place(x=22, y=130)

        action = tk.OptionMenu(window_config, self.last_action, *options, command=self.__save_data_option)
        action.config(width="25", height="2", font=("Helvetica", 15))
        menu2= window_config.nametowidget(action.menuname)
        menu2.config(font=("Helvetica", 15))
        action.place(x=675, y=130)

        button_oaa = tk.Checkbutton(window_config,
                                    text='SI', font=("Helvetica", 12),
                                    variable=self.last_online_action_detection,
                                    onvalue=True,
                                    offvalue=False,
                                    command=self.__save_data_check, width="10", height="3").place(x=470, y=270)
        button_pe = tk.Checkbutton(window_config,
                                   text='SI', font=("Helvetica", 12),
                                   variable=self.last_pose_estimation,
                                   onvalue=True,
                                   offvalue=False,
                                   command=self.__save_data_check, width="10", height="3").place(x=470, y=370)
        button_rg = tk.Checkbutton(window_config,
                                   text='SI', font=("Helvetica", 12),
                                   variable=self.last_report_generation,
                                   onvalue=True,
                                   offvalue=False,
                                   command=self.__save_data_check, width="10", height="3").place(x=470, y=470)

        submit_btn = tk.Button(window_config, text="Guardar", font=("Helvetica", 20), command=self.__close_file, width="15", height="2").place(
            x=50, y=500)

        exit_button = tk.Button(window_config, text="Salir", font=("Helvetica", 20), command=lambda: window_config.destroy(), width="15", height="2").place(x=725, y=500)

        window_config.mainloop()

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
        print(video_path)
        # VLC player object
        self.player = Player(self.window_oaa, title='LOLA - Monitorizacion de acciones', video=video_path)
        self.window_oaa.protocol(("WM_DELETE_WINDOW", self.player.OnClose))

    def on_monitorization(self):

        self.config_data = self.__open_file(self.path)
        last_id = self.config_data['last_id']
        User_ID = str(last_id)
        last_action = (self.config_data['users_info'][last_id]['last_action'])
        last_act = str(last_action)
        Req_act = last_act.replace(' ' , '_')
        act = str(User_ID + ',' + Req_act)

        os.system('~/miniconda3/envs/torch55/bin/python ~/gui4lola/OAD/action-recognition/source/action_recognition_Log_Thread.py  --info_id_act '  + act)

        #except:

            #os.system('~/miniconda3/envs/torch55/bin/python ~/gui4lola/OAD/action-recognition/source/action_recognition_without_report.py')

 

if __name__ == "__main__":
    # Create main dialog
    app = App()
    # Run app
    app.mainloop()

