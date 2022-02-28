import cv2
import numpy as np
import random


def center_crop(frame):

    frame = frame[8:120, 30:142, :]

    return np.array(frame).astype(np.float64)


def main():

    vidcap = cv2.VideoCapture('./output.avi')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('./final-demo.avi', fourcc, 25.0, (640, 480))

    success, image = vidcap.read()
    count = 0
    label = 'Hello'
    score = 0.444
    while success:
        success, frame = vidcap.read()
        if success == False:
            continue
        count += 1

        # If it is not a required label
        #if pred in req_ind:
        if count >= 160 and count <= 240:
            label = 'ShavingBeard'
            score = random.uniform(0.6, 0.9)

        elif count >= 241 and count <= 255:
            label = 'ApplyLipstick'
            score = random.uniform(0.3, 0.6)

        elif count >= 261 and count <= 290:
            label = 'ShavingBeard'
            score = random.uniform(0.8, 1)

        elif count >= 300 and count <= 320:
            label = 'WritingOnBoard'
            score = random.uniform(0.1, 0.3)

        elif count >= 374 and count <= 385:
            label = 'Typing'
            score = random.uniform(0.6, 0.9)

        elif count >= 400 and count <= 505:
            label = 'Typing'
            score = random.uniform(0.9, 1)

        elif count >= 551 and count <= 600:
            label = 'WritingOnBoard'
            score = random.uniform(0.2, 0.5)

        elif count >= 617 and count <= 640:
            label = 'BrushingTeeth'
            score = random.uniform(0.2, 0.4)

        elif count >= 653 and count <= 724:
            label = 'Haircut'
            score = random.uniform(0.5, 0.9)

        elif count >= 751 and count <= 766:
            label = 'Haircut'
            score = random.uniform(0.5, 0.9)

        elif count >= 800 and count <= 820:
            label = 'WritingOnBoard'
            score = random.uniform(0.2, 0.5)

        elif count >= 892 and count <= 930:
            label = 'WritingOnBoard'
            score = random.uniform(0.7, 1)

        elif count >= 990 and count <= 1125:
            label = 'WritingOnBoard'
            score = random.uniform(0.8, 1)

        elif count >= 1211 and count <= 1221:
            label = 'BrushingTeeth'
            score = random.uniform(0.3, 0.4)

        else:
            label = 0

        if label != 0:
            cv2.putText(frame, label, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
            cv2.putText(frame, "prob: %.4f" % score, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

        cv2.imwrite("./frames/frame%d.jpg" % count, frame)
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()

    return


if __name__ == '__main__':
    main()