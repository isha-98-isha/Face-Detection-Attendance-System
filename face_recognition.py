import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import threading
import mysql.connector
import pymysql
pymysql.install_as_MySQLdb()
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
from db_config import DB_CONFIG
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")
class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Pannel")
        
        # Register window close event handler for the main window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Image and background setup
        img = Image.open(os.path.join(IMAGE_DIR, "banner.jpg"))
        img = img.resize((1366, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = tk.Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=130)

        bg1 = Image.open(os.path.join(IMAGE_DIR, "bg3.jpg"))
        bg1 = bg1.resize((1366, 768), Image.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = tk.Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Title section
        title_lb1 = tk.Label(bg_img, text="Welcome to Face Recognition Pannel", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Face Detector Button
        std_img_btn = Image.open(os.path.join(IMAGE_DIR, "f_det.jpg"))
        std_img_btn = std_img_btn.resize((180, 180), Image.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = tk.Button(bg_img, command=self.start_face_recognition, image=self.std_img1, cursor="hand2")
        std_b1.place(x=600, y=180, width=150, height=180)

        std_b1_1 = tk.Button(bg_img, command=self.start_face_recognition, text="Face Detector", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=600, y=330, width=150, height=45)

        # Button to stop face recognition
        stop_btn = tk.Button(bg_img, command=self.stop_face_recognition, text="Stop Recognition", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        stop_btn.place(x=590, y=390, width=180, height=45)
        
        # Flag to control recognition thread
        self.recognition_running = False
        self.recognition_thread = None
        self.videoCap = None
        
        # Variable to track if windows were created
        self.windows_created = False

    def on_closing(self):
        """Handle main window closing event"""
        self.stop_face_recognition()
        self.root.destroy()

    def mark_attendance(self, i, r, n):
        try:
            # Create the file if it doesn't exist
            if not os.path.exists("attendance.csv"):
                with open("attendance.csv", "w", newline="\n") as f:
                    f.write("ID,Roll,Name,Time,Date,Attendance\n")
                    print("Created new attendance.csv file")
                    
            # First, check if the person is already in the attendance list
            with open("attendance.csv", "r", newline="\n") as f:
                myDatalist = f.readlines()
                name_list = []
                for line in myDatalist:
                    entry = line.split(",")
                    if len(entry) > 0:
                        name_list.append(entry[0])
            
            # If not in list, then add the attendance record
            if i not in name_list:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                # Open the file in append mode
                with open("attendance.csv", "a", newline="\n") as f:
                    f.write(f"{i},{r},{n},{dtString},{d1},Present\n")
                    print(f"Attendance marked for {n}")
        except Exception as e:
            print(f"Error marking attendance: {e}")
            # Create an error log for debugging
            with open("attendance_error_log.txt", "a") as log:
                log.write(f"{datetime.now()}: Error marking attendance for {n}: {e}\n")

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        coord = []
        
        for (x,y,w,h) in features:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 3)
            
            try:
                id, predict = clf.predict(gray_image[y:y+h, x:x+w])
                confidence = int((100 * (1 - predict/300)))

                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                # Fetch student details
                cursor.execute("SELECT Name FROM student WHERE Student_ID = %s", (str(id),))
                n = cursor.fetchone()
                n = "+".join([str(item) for item in n]) if n else "Unknown"

                cursor.execute("SELECT Roll_No FROM student WHERE Student_ID = %s", (str(id),))
                r = cursor.fetchone()
                r = "+".join([str(item) for item in r]) if r else "Unknown"

                cursor.execute("SELECT Student_ID FROM student WHERE Student_ID = %s", (str(id),))
                i = cursor.fetchone()
                i = "+".join([str(item) for item in i]) if i else "Unknown"

                cursor.close()
                conn.close()

                # Add confidence display
                if confidence > 80:

                    cv2.putText(img, f"Student_ID:{i}", (x,y-80), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64,15,223), 2)
                    cv2.putText(img, f"Name:{n}", (x,y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64,15,223), 2)
                    cv2.putText(img, f"Roll-No:{r}", (x,y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64,15,223), 2)
                    cv2.putText(img, f"Confidence:{confidence}%", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (64,15,223), 2)
                    self.mark_attendance(i, r, n)
                else:
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 3)
                    cv2.putText(img, f"Unknown Face ({confidence}%)", (x,y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255,255,0), 3)    

                coord = [x,y,w,y]
            except Exception as e:
                print(f"Error in face recognition: {e}")
        
        return coord
    
    def check_database():
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            
            # Check if there are any students
            cursor.execute("SELECT COUNT(*) FROM student")
            count = cursor.fetchone()[0]
            print(f"Number of students in database: {count}")
            
            if count > 0:
                # Get details of first 5 students
                cursor.execute("SELECT Student_ID, Name, Roll_No FROM student LIMIT 5")
                students = cursor.fetchall()
                print("Sample student records:")
                for student in students:
                    print(f"ID: {student[0]}, Name: {student[1]}, Roll: {student[2]}")
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")

    if __name__ == "__main__":
        check_database()
        
    def test_recognition(self):
    #""Test the face recognition with a single image"""
        try:
            # Load test image
            test_img_path = "test_face.jpg"  # Replace with path to a test image
            if not os.path.exists(test_img_path):
                messagebox.showerror("Error", f"Test image {test_img_path} not found")
                return
                
            test_img = cv2.imread(test_img_path)
            gray = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
            
            # Load face detector
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                messagebox.showinfo("Info", "No face detected in test image")
                return
                
            # Load classifier
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("clf.xml")
            
            # Process each face
            for (x,y,w,h) in faces:
                face_img = gray[y:y+h, x:x+w]
                id, confidence = recognizer.predict(face_img)
                confidence_percent = int((100 * (1 - confidence/300)))
                
                # Display result
                messagebox.showinfo("Test Result", f"Detected ID: {id}\nConfidence: {confidence_percent}%")
                
                # Try database lookup
                try:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT Name, Roll_No FROM student WHERE Student_ID = %s", (str(id),))
                    result = cursor.fetchone()
                    
                    if result:
                        name, roll = result
                        messagebox.showinfo("Student Info", f"ID: {id}\nName: {name}\nRoll: {roll}")
                    else:
                        messagebox.showinfo("Student Info", f"No student found with ID {id}")
                        
                    cursor.close()
                    conn.close()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))
                    
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def recognize(self, img, clf, faceCascade):
        coord = self.draw_boundary(img, faceCascade, 1.1, 10, (255,25,255), "Face", clf)
        return img

    def face_recognition_thread(self):
        try:
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("clf.xml")

            self.videoCap = cv2.VideoCapture(0)
            
            # Add window close event handler using named window
            cv2.namedWindow("Face Detector")
            
            # Mark that window was created
            self.windows_created = True

            while self.recognition_running:
                ret, img = self.videoCap.read()
                if not ret:
                    break

                img = self.recognize(img, clf, faceCascade)
                cv2.imshow("Face Detector", img)

                # Add a small delay to reduce CPU usage
                key = cv2.waitKey(1) & 0xFF
                if key == 13 or key == 27:  # Enter or ESC key
                    self.stop_face_recognition()
                    break
        except Exception as e:
            print(f"Error in face recognition thread: {e}")
        finally:
            # Clean up resources
            self.clean_up_resources()

    def clean_up_resources(self):
        """Clean up video capture and windows"""
        if self.videoCap is not None:
            self.videoCap.release()
            self.videoCap = None
            
        if self.windows_created:
            cv2.destroyAllWindows()
            self.windows_created = False
            
        self.recognition_running = False

    def stop_face_recognition(self):
        #"""Stop the face recognition thread safely"""
        if self.recognition_running:
            print("Stopping face recognition...")
            self.recognition_running = False
            
            # Wait for thread to finish
            if self.recognition_thread and self.recognition_thread.is_alive():
                self.recognition_thread.join(timeout=1.0)
                
            # Ensure resources are cleaned up
            self.clean_up_resources()

    def start_face_recognition(self):
        if not self.recognition_running:
            self.recognition_running = True
            # Use threading to prevent GUI freezing
            self.recognition_thread = threading.Thread(target=self.face_recognition_thread)
            self.recognition_thread.daemon = True  # Make thread daemon so it exits when main program exits
            self.recognition_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    obj = Face_Recognition(root)
    root.mainloop()