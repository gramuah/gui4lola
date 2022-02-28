import cv2
import numpy as np
from clip_classification import C3DClipClassification

K = None

def Mouse_click(event, x, y, flags, param):
    global K
    #Stop video on left mouse click
    if event == cv2.EVENT_LBUTTONDOWN:
        K = 27
    return K

def center_crop(frame):

    frame = frame[8:120, 30:142, :]

    return np.array(frame).astype(np.float64)


def main():

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

            clip.pop(0)

        cv2.namedWindow('result', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('result', frame)
        cv2.waitKey(100)
        # if cv2.getWindowProperty('result', cv2.WND_PROP_VISIBLE) < 1:
        #   break
        if K == 27 or cv2.setMouseCallback('result', Mouse_click) or cv2.getWindowProperty('result', cv2.WND_PROP_VISIBLE) < 1:
            retaining = not retaining
        #out.write(frame)

    cap.release()
    #out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

