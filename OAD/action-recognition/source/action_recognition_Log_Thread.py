import cv2
import numpy as np
from clip_classification import C3DClipClassification
import datetime
import csv
import os
import argparse
import threading
import sys
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument('--info_id_act', type=str, help='The info for the current user.')
args = parser.parse_args()
inform = vars(args)['info_id_act']
info = inform.split(',')
name_of_User = info[0]
name_of_action = info[1]

# Load face detection classifier
faceCascade = cv2.CascadeClassifier('./OAD/action-recognition/source/cascades/haarcascade_frontalface_default.xml')

# Global variables for multithreading
global frame16
global clip_ready
global predicted_label
global act_log



# Class for Online Action Detection
class OAD(threading.Thread):
    def __init__(self, action_name):
        threading.Thread.__init__(self)
        self.zoomed_frame = []
        self.action_name = action_name


    def center_crop(self, frame):
        cropped_frame = frame[8:120, 30:142, :]

        return np.array(cropped_frame).astype(np.float64)

    def Face_detection(self, frame):
        discard = True
        ar_wb = (640 / 480)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            x0 = x + int(w / 2)
            y0 = y + int(h / 2)
            ymin = y0 - h
            ymax = y0 + h
            xmin = x0 - int(ar_wb * h)
            xmax = x0 + int(ar_wb * h)
            if (ymin <= 0) or (xmin <= 0) or (ymax >= 480) or (xmax >= 640):  # detect failure
                discard = True
            else:
                self.zoomed_frame = frame[ymin:ymax, xmin:xmax]
                discard = False
        return self.zoomed_frame, discard

    def Upperbody_detection(self, frame):
        discard = True
        ar_wb = (640 / 480)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            x0 = x + int(w / 2)
            y0 = y + int(h / 2)
            ymin = y0 + (2 * h)
            ymax = y0 + (4 * h)
            xmin = x0 - int(ar_wb * h)
            xmax = x0 + int(ar_wb * h)
            if (ymin <= 0) or (xmin <= 0) or (ymax >= 480) or (xmax >= 640):  # detect failure
                discard = True
            else:
                self.zoomed_frame = frame[ymin:ymax, xmin:xmax]
                discard = False
        return self.zoomed_frame, discard

    def run(self):

        # Class labels
        global frame16
        global clip_ready
        global predicted_label
        global act_log
        
        #Initialize last predicted label
        last_predicted_label = 'Wait-Loading app'
        count = 0

        with open('./OAD/action-recognition/source/ucf_labels.txt', 'r') as f:
            class_labels = f.readlines()

        # Required labels
        with open('./OAD/action-recognition/source/ucf_labels_selection.txt') as f:
            req_labels = f.readlines()

        # Keep only label index
        req_ind = list()
        for i, label in enumerate(req_labels):
            req_ind.append(int(label.split(' ')[0]) - 1)

        # Init C3D
        c3d = C3DClipClassification()
        discard_frame = False
        clip = []
        Zlist = []

        # Start the loop in the thread
        while True:
            if clip_ready is False:
                continue

            # Face detection or body detection + cropping
            if str(name_of_action) == 'Cepillarse_los_dientes' or str(name_of_action) == 'Secar_el_pelo':
                for i in frame16:
                    frame_face, discard_frame = self.Face_detection(i)
                    frame_face_array = np.array(frame_face)

                    if frame_face_array.size == 0:
                        discard_frame = True
                        break

                    if discard_frame is False:
                        Zlist.append(frame_face)
                    else:                        
                        break

            elif str(name_of_action) == 'Cortar_en_la_cocina':
                for i in frame16:
                    frame_body, discard_frame = self.Upperbody_detection(i)
                    frame_body_array = np.array(frame_body)

                    if frame_body_array.size == 0:
                        discard_frame = True
                        break
                    
                    if discard_frame is False:
                        Zlist.append(frame_body)
                    else:                        
                        break
            else:
                for i in frame16:
                    Zlist.append(i)

            if discard_frame is True:
                Zlist.clear()
                frame16.clear()
                predicted_label = 'None'
                clip_ready = False
                continue

            if len(Zlist) == 16:
                for Z_frame in Zlist:
                    tmp_ = self.center_crop(cv2.resize(Z_frame, (171, 128)))
                    tmp = tmp_ - np.array([[[90.0, 98.0, 102.0]]])
                    clip.append(tmp)

            if len(clip) == 16:
                inputs = np.array(clip).astype(np.float32)
                inputs = np.expand_dims(inputs, axis=0)
                inputs = np.transpose(inputs, (0, 4, 1, 2, 3))

                prob, pred = c3d.clip_classification(inputs)

                if pred in req_ind:
                    # Update global predicted label
                    predicted_label = (class_labels[pred].split(' ')[-1].strip())
                else:
                    predicted_label = 'None'

                if last_predicted_label != predicted_label:
                    Now = datetime.datetime.now()
                    if count != 0:
                        end = Now.strftime("%H:%M:%S")
                        act_log.write(',' + str(end) + '\n')
                    last_predicted_label = predicted_label
                    act_log.write(str(name_of_action) + ',')
                    translated_label = eng_to_spn(predicted_label)
                    act_log.write(translated_label + ',')
                    day = Now.strftime('%d/%m/%Y')
                    act_log.write(str(day) + ',')
                    hour = Now.strftime('%H:%M:%S')
                    act_log.write(str(hour))
                    count += 1
                    # To save original frame
                    user = os.path.join(path, name_of_User)
                    image_path = (user + str(count) + '_' + str(translated_label) + '.jpg')
                    frame = frame16[-1] #save last frame for the log to generate the report
                    cv2.imwrite(image_path, frame)
                    act_log.write(',' + str(image_path))               


            # Clear variables
            frame16.clear()
            Zlist.clear()
            clip.clear()
            clip_ready = False

    def kill(self):
        sys.exit()
        

# Function for closing the display with left click
def close_Mouse(event, x, y, flags, param):
    global K
    if event == cv2.EVENT_LBUTTONDOWN:
        K = 27
    return K

# Function to create new folder for users to keep reports
def report(id):
    save_path = './OAD/action-recognition/source/fotos/'
    path = os.path.join(save_path, id)
    Now = datetime.datetime.now()
    try:
        os.mkdir(path)
        date = Now.strftime('%d_%m_%Y')
        User_path = os.path.join(path, date)
        os.mkdir(User_path)
    except:
        date = Now.strftime('%d_%m_%Y')
        User_path = os.path.join(path, date)
        time = Now.strftime("%H:%M:%S")
        try:
            User_path = os.path.join(path, date)
            os.mkdir(User_path)
        except:
            User_path = os.path.join(User_path, time)
            os.mkdir(User_path)
    return User_path

# Function to translate labels from english to spanish in reports
def eng_to_spn(label):  
    label = str(label)
    if "Pelo" in label:
        label = 'SecarELPelo'
    elif "Dientes" in label:
        label = 'CepillarLosDientes'
    elif "Cutting" in label:
        label = 'CortarEnLaCocina'
    elif "Fregona" in label:
        label = 'PasarLaFreguna'
    elif "Pizarra" in label:
        label = 'EscribirEnLaPizarra'
    else:
        label = label
    return label


# Function for visualization
def visualization():

    #global variables
    global frame16
    global clip_ready
    global predicted_label    
    global K
    global act_log

    # Open camera device to capture
    cap = cv2.VideoCapture(2)
    cap.set(3, 640)  # set Width
    cap.set(4, 480)  # set Height
    frame16 = [] #start with an empty clip
    clip_ready = False #start with the clip marked as not ready
    predicted_label = 'Wait-Loading app'
   
    retaining = True
    
    K = None


    #Launch thread for OAD + AI
    Action_Detection = OAD(name_of_action)
    Action_Detection.daemon = True
    Action_Detection.start()

    while retaining:
        retaining, frame = cap.read()
        local_frame = deepcopy(frame)      


        if not retaining and frame is None:
            continue

        if clip_ready is False:
            frame16.append(frame)

            if len(frame16) == 16:
                clip_ready = True
                

        cv2.putText(local_frame, predicted_label, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.9,(255, 0, 0), 3)
        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('result',local_frame)
        cv2.waitKey(100)
        if K == 27 or cv2.setMouseCallback('result', close_Mouse) or cv2.getWindowProperty('result',cv2.WND_PROP_VISIBLE) < 1:
            retaining = not retaining

    cap.release()
    cv2.destroyAllWindows()

    # Generate from txt a log.csv
    Now = datetime.datetime.now()
    End = Now.strftime("%H:%M:%S")
    act_log.write(',' + str(End))
    act_log.close()
    User_log = os.path.join(path, 'log_' + name_of_User + '.csv')
    with open('./OAD/action-recognition/source/actions.txt', 'r') as in_file:
         lines = in_file.read().splitlines()
         stripped = [line.replace(" ", "_").replace(",", " ").split() for line in lines]
         grouped = zip(*[stripped] * 1)
         with open(User_log, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('Requested_Action', 'Predicted_Action', 'Date', 'T_Start', 'Path', 'T_End'))
            for group in grouped:
                writer.writerows(group)

    Action_Detection.kill()
    return


global act_log
act_log = open('./OAD/action-recognition/source/actions.txt', 'w')
path = report(name_of_User)

if __name__ == '__main__':
      visualization()




