import face_recognition
import cv2
import xlwt
import os
import time
import numpy as np
from tkinter import *
from datetime import datetime

from pymongo import MongoClient
from arctic import Arctic

client = MongoClient('localhost', 27017)
db = client.attendancedb

harcascadePath = "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(harcascadePath)

root_main = Tk()
root_main.configure(background="#80D8FF")

student_rollno = []
student_names = []
student_encodings = []

DATA = [["RollNumber", "Name", "STATUS"]]
for i in range(0, 100):
    DATA.append([])



no_of_stds = 0

image = []
encoding = []
face_locations = []
face_encodings = []
face_names = []
frame_number = 0
saved_for_exel = []


def function1():  # Function to update database
    root_1 = Tk()
    root_1.title("ENTER DETAILS")
    root_1.configure(bg="white")
    camera = cv2.VideoCapture(0)

    def enter_the_value():
        global no_of_stds, DATA
        usn = int(e2_1.get())   
        std_name = e1_1.get()
        print("Taking image...")
        _, camera_capture = camera.read()
        time.sleep(2)
        # if usn != 0:
        print("image received")
        faces = detector.detectMultiScale(camera_capture, 1.3, 5)
        if len(faces) == 1:
            (x, y, w, h) = faces[0]
            final_capture = camera_capture[y:y+h, x:x+w]
            cv2.imwrite("database/" + str(std_name) + str(usn) + ".jpeg", final_capture)  # check face
            print("image saved")
            encoding = face_recognition.face_encodings(final_capture)[0]
            # encoding = encoding.tolist()
            # import pdb;pdb.set_trace()
            data = {'roll_no': str(usn),'name': str(std_name), 'attendance': 'absent', 'encoding': encoding.tobytes().hex() }
            inserted_id = db.students.insert_one(data)
            print("INSERTED")
            if inserted_id == None:
                print("Mongo Error")
            no_of_stds = no_of_stds + 1
            # DATA[usn].append(str(usn))
            # DATA[usn].append(str(std_name))
            # DATA[usn].append("Absent")
            print("image captured, resized and renamed successfully")
        # print(DATA)
        # img = cv2.imread("/database/image"+str(usn)+".png")
        # cv2.imshow('user_image',img)
        camera.release()
        cv2.destroyAllWindows()
        root_1.destroy()
        # os.system("python3 photo.py")
    Label(root_1, text="ENROLLMENT OF A NEW STUDENT", font=("helvatica", 30), bg="#F44336", fg="#0a0800").grid(rowspan=2,
                                                                                                         columnspan=2,
                                                                                                         sticky=N + E + W + S,
                                                                                                         padx=5, pady=5)

    Label(root_1, text="Enter Student's name: ", fg="black", font=("chiller", 16)).grid(row=3, padx=5,
                                                                                                      pady=5, sticky=E)
    Label(root_1, text="Enter Roll No.: ", fg="black", font=("chiller", 16)).grid(row=5, padx=5, pady=5,
                                                                                                  sticky=E)
    Label(root_1, text="(ENTER DETAILS AND PRESS 'SUBMIT' TO CAPTURE IMAGE)", fg="black",
          font=("chiller", 10)).grid(rowspan=2, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

    e1_1 = Entry(root_1)
    e1_1.grid(row=3, rowspan=2, column=1)
    e2_1 = Entry(root_1)
    e2_1.grid(row=5, rowspan=2, column=1)

    Button(root_1, text="CLEAR", bg="blue", fg="white", font=("times new roman", 25), command=root_1.quit).grid(row=8,
                                                                                                       columnspan=2,
                                                                                                       stick=E + W + N + S,
                                                                                                       pady=4)
    Button(root_1, text="SUBMIT", bg="blue", fg="white", font=("times new roman", 25), command=enter_the_value).grid(row=9,
                                                                                                            columnspan=2,
                                                                                                            stick=W + E + N + S,
                                                                                                            pady=4)

    root_1.mainloop()


def start_attendance():  # Function to mark attendance in the list
    video_capture = cv2.VideoCapture(0)
    global no_of_stds, frame_number
    global saved_for_exel
    dummy_append_data = []
    global atten
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame_number += 1
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = "Unknown"
            match = list(face_recognition.face_distance(student_encodings, face_encoding))
            min_face_distance = min(match)
            print(min_face_distance)
            atten = 'absent'
            if min_face_distance <= 0.5:
                student_name_mark = student_rollno[match.index(min_face_distance)]
                name_for_atten = db.students.find_one_and_update({'roll_no':student_name_mark}, {'$set':{'attendance': 'present'}})
                atten = 'present'
                if name_for_atten:
                    print("marked", student_name_mark)
                name = student_names[match.index(min_face_distance)]
                
                dummy_append_data = [student_name_mark, name]
        try:
            dummy_append_data.append(atten)
        
            # print("no face found")
            # saved_for_exel.append(dummy_append_data)
                
                # for i in range(0, no_of_stds):
                #     if match[i]:
                #         name = DATA[i + 1][1] #+ "_" + str(i)
                #         DATA[i + 1][2] = "present"
            face_names.append(name)
        except:
            print("no face found")

        # Label the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()




def function2():  # Function to mark attendance in the spreadsheet
    root_2 = Tk()
    root_2.title("ENTER DETAILS")
    root_2.configure(bg="white")

    global student_rollno
    global student_names
    global student_encodings
    global saved_for_exel

    for student in db.students.find():
        student_rollno.append(student['roll_no'])
        student_names.append(student['name'])
        student_encodings.append(np.frombuffer(bytes.fromhex(student['encoding'])))

    def save_attendance():
        wb = xlwt.Workbook()
        ws = wb.add_sheet("My Sheet")
        final_exel=[]
        for stu in db.students.find():
            print(stu,end="########################")
            final_exel.append([stu['roll_no'], stu['name'], stu['attendance']])
            
        # for x in saved_for_exel:
        #     if x not in final_exel:
        #         final_exel.append(x)s
        for i, row in enumerate(final_exel):
            for j, col in enumerate(row):
                ws.write(i, j, col)
        wb.save(e2_2.get() + "_" + str(datetime.now().date()) + ".xls")

        clear_all()
    
    def clear_all():
        db.students.update_many({}, {'$set':{'attendance': 'absent'}})

    Label(root_2, text="Enter details for the lecture", font=("helvatica", 30), fg="black").grid(rowspan=2,
                                                                                                         columnspan=2,
                                                                                                         sticky=N + E + W + S,
                                                                                                         padx=5, pady=5)

    # Label(root_2, text="Enter date and time: ", fg="#42A5F5", bg="#795548", font=("chiller", 16)).grid(row=3, padx=5,pady=5, sticky=E)
    Label(root_2, text="Enter subject name: ", fg="black", font=("chiller", 16)).grid(row=5, padx=5, pady=5,
                                                                                                 sticky=E)
    Label(root_2, text="(Press Q to Stop the camera, Attendance will automatically take date)", fg="black", font=("chiller", 10)).grid(
        rowspan=2, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)
    # e1_2 = Entry(root_2)
    # e1_2.grid(row=3, rowspan=2, column=1)
    e2_2 = Entry(root_2)
    e2_2.grid(row=5, rowspan=2, column=1)

    Button(root_2, text="CLEAR", bg="#00695C", font=("times new roman", 25), command=root_2.quit).grid(row=8,
                                                                                                       columnspan=2,
                                                                                                       stick=E + W + N + S,
                                                                                                       pady=4)
    Button(root_2, text="START ATTENDANCE", bg="#00695C", font=("times new roman", 25), command=start_attendance).grid(
        row=9, columnspan=2, stick=W + E + N + S, pady=4)
    Button(root_2, text="SUBMIT", bg="#00695C", font=("times new roman", 25), command=save_attendance).grid(row=10,
                                                                                                            columnspan=2,
                                                                                                            stick=W + E + N + S,
                                                                                                            pady=4)

    root_2.mainloop()

def function3():
    print("Student is successfully added")
root_main.title("Real-Time Smart Attendance System using Face Recognition")
# root_main.geometry("600x500")
Label(root_main, text="Real-Time Smart Attendance System using Face Recognition", font=("helvatica", 30), fg="white", bg="black", height=3).grid(row=0,
                                                                                                             rowspan=2,
                                                                                                             columnspan=2,
                                                                                                             sticky=N + E + W + S,
                                                                                                             padx=5,
                                                                                                             pady=5)
Label(root_main, text="Please select the process", font=("helvatica", 30), fg="white", bg="#00BFA5", height=2).grid(row=1,
                                                                                                             rowspan=2,
                                                                                                             columnspan=2,
                                                                                                             sticky=N + E + W + S,
                                                                                                             padx=5,
                                                                                                             pady=5)

Button(root_main, text="Enroll New Student", font=("times new roman", 30), bg="#3F51B5", fg='white',
       command=function1).grid(row=4, columnspan=2, sticky=W + E + N + S, padx=5, pady=5)

Button(root_main, text="Mark Attendance", font=("times new roman", 30), bg="#3F51B5", fg='white',command=function2).grid(row=6, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)
Button(root_main, text="Get All Attendance", font=("times new roman", 30), bg="#3F51B5", fg='white',command=function3).grid(row=5, columnspan=2, sticky=N + E + W + S, padx=5, pady=5)

root_main.mainloop()