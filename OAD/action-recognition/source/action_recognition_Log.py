import cv2
import numpy as np
from clip_classification import C3DClipClassification
import datetime
import csv
import os
import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--info_id_act', type=str, help='The info for the current user.')
args = parser.parse_args()
inform = vars(args)['info_id_act']
info = inform.split(',')
name_of_User = info[0]
name_of_action = info[1]

K = None

#load face deteciton classifier
faceCascade = cv2.CascadeClassifier('./OAD/action-recognition/source/cascades/haarcascade_frontalface_default.xml')

def Mouse_click(event, x, y, flags, param):
    global K
    #Stop video on left mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        K = 27
    return K

def report (id):
    save_path = './OAD/action-recognition/source/fotos/'
    path = os.path.join(save_path, id)
    Now = datetime.datetime.now()
    try:
        os.mkdir(path)
        bt = Now.strftime('%d_%m_%Y')
        pit = os.path.join(path, bt)
        os.mkdir(pit)
    except:
        bt = Now.strftime('%d_%m_%Y')
        pit = os.path.join(path, bt)
        hora = Now.strftime("%H:%M:%S")
        try:
            pit = os.path.join(path, bt)
            os.mkdir(pit)
        except:
            pit = os.path.join(pit, hora)
            os.mkdir(pit)
    return pit


def center_crop(frame):

    frame = frame[8:120, 30:142, :]

    return np.array(frame).astype(np.float64)

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            #print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports

def Face_detection(frame, discard):
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
            frame = frame[ymin:ymax, xmin:xmax]            
            discard = False        
    return frame,discard

def Upperbody_detection(frame, discard): #Zoom Upperbody part
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
        ymin = y0 + (2*h)
        ymax = y0 + (4*h)
        xmin = x0 - int(ar_wb * h)
        xmax = x0 + int(ar_wb * h)
        if (ymin <= 0) or (xmin <= 0) or (ymax >= 480) or (xmax >= 640):  # detect failure
            discard = True           
        else:
            frame = frame[ymin:ymax, xmin:xmax]            
            discard = False        
    return frame,discard

def eng_to_spn(lable): #translate classes from english to spanish
    lable = str(lable)
    if "Teeth" in lable:
        lable ='CepillarLosDientes'
    elif "Writing" in lable:
        lable = 'EscribirEnLaPizarra'
    elif "Cutting" in lable:
        lable ='CortarEnLaCocina'
    elif "Mopping" in lable:
        lable ='PasarLaMopa'
    elif "Hair" in lable:
        lable = 'SecarElPelo'
    else:
        lable = lable
    return lable

def main():
     
    tarea = ('none')
    count = 0

    # Class labels
    with open('./OAD/action-recognition/source/ucf_labels.txt', 'r') as f:
        class_labels = f.readlines()

    # Required labels
    with open('./OAD/action-recognition/source/ucf_labels_selection.txt') as f:
        req_labels = f.readlines()


    # Keep only label index
    req_ind = list()
    for i, label in enumerate(req_labels):
        req_ind.append(int(label.split(' ')[0]) - 1)

    #list_ports()    

    # Open camera device to capture
    cap = cv2.VideoCapture(2)
    cap.set(3,640)
    cap.set (4,480)
    retaining = True
    discard_frame = False

    # Init C3D
    c3d = C3DClipClassification()

    clip = []
    frame16 = []
    Zlist= []
    while retaining:
        retaining, frame = cap.read()
        frame16.append(frame)
        if len(frame16) == 16:
            if str(name_of_action) == 'Cepillarse_los_dientes' or str(name_of_action) == 'Secar_el_pelo':
                #print ('ACT = AB')
                for i in frame16:
                    frame, discard_frame = Face_detection(i, discard_frame)
                    if frame.size == 0:
                        discard_frame = True
                    elif discard_frame is True:
                        discard_frame = True
                    else:
                        Zlist.append(frame)

                frame16.clear()
                #print ('Clear AB')
            elif str(name_of_action) == 'Cortar_en_la_cocina':
                #print ('ACT = CD')
                for i in frame16:
                    frame, discard_frame = Upperbody_detection(i, discard_frame)
                    if frame.size == 0:
                        discard_frame = True
                    elif discard_frame is True:
                        discard_frame = True
                    else:
                        Zlist.append(frame)

                frame16.clear()
                #print ('Clear CD')

            else:
                for i in frame16:
                   Zlist.append(i)

                frame16.clear()
                #print ('Clear Else')

        
        if not retaining and frame is None:
            continue
        if frame.size == 0:
            #print('00000')
            Zlist.clear()
            continue
        if discard_frame is True:
            #print('True')
            Zlist.clear()
            discard_frame = False
            continue

        for frame in Zlist:
            tmp_ = center_crop(cv2.resize(frame, (171, 128)))
            tmp = tmp_ - np.array([[[90.0, 98.0, 102.0]]])
            clip.append(tmp)
        if len(clip) == 16:
            #print('Created Clip')
            inputs = np.array(clip).astype(np.float32)
            inputs = np.expand_dims(inputs, axis=0)
            inputs = np.transpose(inputs, (0, 4, 1, 2, 3))

            prob, pred = c3d.clip_classification(inputs)


            # If it is not a required label
            if pred in req_ind:
                cv2.putText(frame, class_labels[pred].split(' ')[-1].strip(), (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.9, (255, 0, 0), 3)

                # Print the predicted actions in a file
                tar = (class_labels[pred].split(' ')[-1].strip())

                # Save date, time_start, image_path, time_end and translate the classes in spanish
                if tarea != tar:
                        Now = datetime.datetime.now()
                        if count != 0:
                             end = Now.strftime("%H:%M:%S")
                             act.write(',' + str(end) + '\n')
                        tarea = tar
                        act.write(str(name_of_action) + ',')
                        tar = eng_to_spn(tar)
                        act.write(tar + ',')
                        ct = Now.strftime('%d/%m/%Y')
                        act.write(str(ct) + ',')
                        nt = Now.strftime('%H:%M:%S')
                        act.write(str(nt))
                        count +=1
                        #Save original frame
                        _, framee = cap.read()
                        user = os.path.join(pathh, name_of_User)
                        path = (user +'_'+ str(count)+ '_' +str(tar)+'.jpg')
                        cv2.imwrite(path, framee)
                        act.write(',' + str(path))
                        
                else:
                    pass                    


        #cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        #cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('result', frame)
        cv2.waitKey(100)
        clip.clear()
        Zlist.clear()
        if K == 27 or cv2.setMouseCallback('result', Mouse_click) or cv2.getWindowProperty('result', cv2.WND_PROP_VISIBLE) < 1:
            retaining = not retaining


    cap.release()
    cv2.destroyAllWindows()
    return

act = open('./OAD/action-recognition/source/actions.txt', 'w')
pathh = report(name_of_User)

if __name__ == '__main__':
    #try:
        main()

''''
    except:
        Now = datetime.datetime.now()
        End = Now.strftime("%H:%M:%S")
        act.write(',' + str(End))
        act.close()
        print ('Problem in main')
'''

# Generate from txt a log.csv
Now = datetime.datetime.now()
End = Now.strftime("%H:%M:%S")
act.write(',' + str(End))
act.close()
bit = os.path.join(pathh, 'log_' + name_of_User +'.csv')
with open('./OAD/action-recognition/source/actions.txt', 'r') as in_file:
    lines = in_file.read().splitlines()
    stripped = [line.replace(" ","_").replace(","," ").split() for line in lines]
    grouped = zip(*[stripped] * 1)
    with open(bit, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Requested_action', 'Predicted_action', 'Date', 'T_Start', 'Path', 'T_End'))
        for group in grouped:
            writer.writerows(group)
