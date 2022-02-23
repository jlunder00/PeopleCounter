from dbaccessor import DBAccessor
import config
from recorder import Recorder
import numpy as np
import cv2
from datetime import datetime
import random

class Detector():

    def __init__(self, accessor):
        self.database_access = accessor
        self.rec = Recorder(accessor)
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        cv2.startWindowThread()
        self.cap = cv2.VideoCapture(0)
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'),15.,(640,480))
        self.X_size = 640
        self.Y_size = 480
        self.current_boxes_per_frame = []
        self.frames_before_reset = 15
        self.frames_after_detection = 0
        self.in_detection = False

        self.people_inside = []

    def read_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, frame = cv2.threshold(frame, 80, 255, cv2.THRESH_BINARY)
        cv2.imshow('frame', frame)
        return frame, ret

    def reset_detection(self):
        self.frames_after_detection = 0
        self.in_detection = False
        self.current_boxes_per_frame = []

    def box_large_enough(self, w, h):
        # print((w*h)/(self.X_size*self.Y_size), w, h)
        return (w*h)/(self.X_size*self.Y_size) >= 0.07

    def detect(self, frame):
        boxes, weights = self.hog.detectMultiScale(frame, winStride=(8, 8))
        boxes = np.array([[x, y, x+w, y+h] for (x, y, w, h) in boxes if self.box_large_enough(w, h)])
        if len(boxes) > 0:
            if not self.in_detection:
                self.in_detection = True
            self.current_boxes_per_frame.append(boxes)
        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        if self.in_detection:
            if self.frames_after_detection < self.frames_before_reset:
                self.frames_after_detection += 1
            else:
                result = self.analyze_detections()
                if result is not None:
                    dt = datetime.now()
                    time = dt.strftime('%H:%M:%S')
                    date = dt.strftime('%m-%d-%Y')
                    height = 0.0
                    #need additional tool (maybe ir camera, hypersonic sensor) to detect height
                    
                    if result == 1:
                        self.add_person_inside(height, dt)
                        self.rec.record_walk_in(height, time, date)
                    elif result == -1:
                        if len(self.people_inside) > 0:
                            indt = self.find_person_inside(height)
                            if indt is not None:
                                in_time = indt.strftime('%H:%M:%S')
                                in_date = indt.strftime('%m-%d-%Y')
                                self.rec.add_walk_in_time_out(height, in_time, in_date, time, date)
                self.reset_detection()
        return frame

    def add_person_inside(self, height, datetime):
        self.people_inside.append((height, datetime))

    def find_person_inside(self, height):
        person = ()
        height_inc_percent = 0.05
        height_inc = height*height_inc_percent
        upper_height = height + height_inc
        lower_height = height - height_inc
        possible_people = [(h, dt) for (h, dt) in self.people_inside if h <= upper_height and h >= lower_height]
        if len(possible_people) > 0:
            if len(possible_people) > 1:
                min_dt = min([dt for (h,dt) in possible_people])
                possible_people = [(h, dt) for (h, dt) in possible_people if dt == min_dt]
                if len(possible_people) > 1:
                    person = random.choice(possible_people)
                else:
                    person = possible_people[0]
            else:
                person = possible_people[0]
        else:
            return None
        return person[1]
            

    def analyze_detections(self):
        '''
            detect directionality in movement of boxes to determine if person moving in or out 
        '''
        midpoints_per_frame = [[self.find_midpoint(xA, yA, xB, yB) for (xA, yA, xB, yB) in boxes] for boxes in self.current_boxes_per_frame]
        if len(midpoints_per_frame) > 1:
            sl = False
            el = False
            sr = False
            er = False
            if midpoints_per_frame[0][0][0] < self.X_size//4:
                print('start left?', midpoints_per_frame[0][0][0])
                sl = True
            # if midpoints_per_frame[0][0][1] < self.Y_size//4:
            #     print('start top?', midpoints_per_frame[0][0][1])
            if midpoints_per_frame[0][0][0] > self.X_size - self.X_size//4:
                sr = True
                print('start right?', midpoints_per_frame[0][0][0])
            # if midpoints_per_frame[0][0][1] > self.Y_size - self.Y_size//4:
                # print('start bottom?', midpoints_per_frame[0][0][1])
            if midpoints_per_frame[-1][0][0] < self.X_size//4:
                el = True
                print('end left?', midpoints_per_frame[-1][0][0])
            # if midpoints_per_frame[-1][0][1] < self.Y_size//4:
                # print('end top?', midpoints_per_frame[-1][0][1])
            if midpoints_per_frame[-1][0][0] > self.X_size - self.X_size//4:
                er = True
                print('end right?', midpoints_per_frame[-1][0][0])
            # if midpoints_per_frame[-1][0][1] > self.Y_size - self.Y_size//4:
                # print('end bottom?', midpoints_per_frame[-1][0][1])
            if sl and el:
                return None
            elif sr and er:
                return None
            elif sl and er:
                return 1
            elif sr and el:
                return -1
        else:
            return None

                
    def find_midpoint(self, xA, yA, xB, yB):
        return (xB+xA)//2, (yB-yA)//2

    def write_ouput(self, frame):
        self.out.write(frame.astype('uint8'))
        cv2.imshow('frame', frame)

    def end(self):
        self.cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)


    def run(self):
        while(True):
            frame, ret = self.read_frame()
            frame = self.detect(frame)
            self.write_ouput(frame)
            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
        self.end()

def main():
    usr = config.mysql['user']
    pwd = config.mysql['password']
    hst = config.mysql['host']
    db = usr+'_DB'

    access = DBAccessor(usr, pwd, hst, db)
    det = Detector(access)
    det.run()
main()
