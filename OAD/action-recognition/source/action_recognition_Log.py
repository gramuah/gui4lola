import cv2
import numpy as np
from clip_classification import C3DClipClassification
import datetime
import csv
import os
import glob
import argparse

'''
# Delete all image from the directory of fotos
removing_files = glob.glob('./fotos/*.jpg')
for i in removing_files:
    os.remove(i)
'''
parser = argparse.ArgumentParser()
parser.add_argument('--user-id', type=str, help='The id for the current user.')
args = parser.parse_args()
name_of_User = vars(args)['user_id']

K = None

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
            print("Port %s is not working." %dev_port)
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

    list_ports()    

    # Open camera device to capture
    cap = cv2.VideoCapture(2)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('./output.avi', fourcc, 25.0, (640, 480))
    retaining = True

    # Init C3D
    c3d = C3DClipClassification()

    clip = []
    while retaining:
        retaining, frame = cap.read()
        if not retaining and frame is None:
            continue
        tmp_ = center_crop(cv2.resize(frame, (171, 128)))
        tmp = tmp_ - np.array([[[90.0, 98.0, 102.0]]])
        clip.append(tmp)
        if len(clip) == 16:
            inputs = np.array(clip).astype(np.float32)
            inputs = np.expand_dims(inputs, axis=0)
            inputs = np.transpose(inputs, (0, 4, 1, 2, 3))

            prob, pred = c3d.clip_classification(inputs)


            # If it is not a required label
            if pred in req_ind:
                cv2.putText(frame, class_labels[pred].split(' ')[-1].strip(), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
                
                cv2.putText(frame, "prob: %.4f" % prob[0][pred], (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

                # Print the predicted actions in a file
                tar = (class_labels[pred].split(' ')[-1].strip())

                # Save date, time_start, image_path, time_end and translate the classes in spanish
                if tarea != tar:
                        Now = datetime.datetime.now()
                        if count != 0:
                             end = Now.strftime("%H:%M:%S")
                             act.write(',')
                             act.write(str(end))
                             act.write('\n')
                        tarea = tar
                        if "Teeth" in tar:
                            act.write('CepillarLosDientes')
                        if "Writing" in tar:
                            act.write('EscribirEnLaPizarra')
                        if "Typing" in tar:
                            act.write('Teclear')
                        if "Cutting" in tar:
                            act.write('CortarEnLaCocina')
                        if "Mixing" in tar:
                            act.write('Mezclar')
                        if "Mopping" in tar:
                            act.write('PasarLaMopa')
                        if "Hair" in tar:
                            act.write('Peinarse')
                        else:
                            #act.write(tar)
                            pass
                        act.write(',')
                        ct = Now.strftime('%d/%m/%Y %H:%M:%S')
                        act.write(str(ct))
                        count +=1
                        _, frame = cap.read()
                        user = os.path.join(pathh, name_of_User)
                        path = (user +'_'+ str(count)+ '_' +str(tar)+'.jpg')
                        cv2.imwrite(path, frame)
                        act.write(',')
                        act.write(str(path))
                        
                else:
                    pass
                    

            clip.pop(0)

        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('result', frame)
        cv2.waitKey(100)
        # if cv2.getWindowProperty('result', cv2.WND_PROP_VISIBLE) < 1:
        #   break
        if K == 27 or cv2.setMouseCallback('result', Mouse_click) or cv2.getWindowProperty('result', cv2.WND_PROP_VISIBLE) < 1:
            # print('khoond injaro')
            retaining = not retaining
        #out.write(frame)

    cap.release()
    #out.release()
    cv2.destroyAllWindows()
    return

act = open('./OAD/action-recognition/source/actions.txt', 'w')
pathh = report(name_of_User)

if __name__ == '__main__':
    try:
        main()
    except:
        Now = datetime.datetime.now()
        End = Now.strftime("%H:%M:%S")
        act.write(',')
        act.write(str(End))
        act.close()

# Generate from txt a log.csv
Now = datetime.datetime.now()
End = Now.strftime("%H:%M:%S")
act.write(',')
act.write(str(End))
act.close()
bit = os.path.join(pathh, 'log_' + name_of_User +'.csv')
with open('./OAD/action-recognition/source/actions.txt', 'r') as in_file:
    lines = in_file.read().splitlines()
    stripped = [line.replace(","," ").split() for line in lines]
    grouped = zip(*[stripped] * 1)
    with open(bit, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('Action', 'Date', 'T_Start', 'Path', 'T_End'))
        for group in grouped:
            writer.writerows(group)
