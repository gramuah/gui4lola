# GUI FOR LOLA PLATFORM
import tkinter as tk
from utilities import ImageLabel
import vlc
from tkvlc import Player
# Main dialog (root window)
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Bienvenidos a LOLA')

        # Create background image
        lbl = ImageLabel(self)
        lbl.pack()
        lbl.load('data/robot.gif')

        # place a button on the root window for action analysis window
        tk.Button(self,
                  text='Comenzar',
                  command=self.open_action_analysis).pack()

    # function to create Dialog for action analysis window
    def open_action_analysis(self):
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

    def on_activity(self):
        """Creates a frame to display VLC Media player
        """
        # VLC player object
        # TODO: select from the dataset of activities
        video_name = "data/video_baby_shark.mp4"
        self.player = Player(self.window_oaa, title='LOLA - Monitorizacion de acciones',  video=video_name)
        self.window_oaa.protocol(("WM_DELETE_WINDOW", self.player.OnClose))




    def on_monitorization(self):
        print('patata')


if __name__ == "__main__":
    # Run main dialog
    app = App()
    app.mainloop()
