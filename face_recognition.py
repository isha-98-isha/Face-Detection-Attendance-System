import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from ui.theme import COLORS, apply_theme, FONTS
from ui.components import *
from ui.icons import ICONS
from ui.assets import get_image_path, load_image, BASE_DIR
import threading
import mysql.connector
import pymysql
pymysql.install_as_MySQLdb()
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
from db_config import DB_CONFIG, owner_attendance_path, owner_model_path
from camera_config import get_camera_source, get_settings, save_settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")
class Face_Recognition:
    def __init__(self, root, authenticated=False, owner_email=None):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.owner_email = owner_email
        self.model_path = owner_model_path(owner_email)
        self.attendance_path = owner_attendance_path(owner_email)
        self.root.title("Face Recognition • Face Recognition Attendance System")
        self.root.geometry("1280x780")
        self.root.minsize(1050, 680)
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # Register window close event handler for the main window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # -------------------- Design system --------------------
        BG = COLORS["bg_main"]
        WHITE = COLORS["white"]
        BLUE = COLORS["primary"]
        DARK_BLUE = COLORS["secondary"]
        PINK = COLORS["accent_pink"]
        TEXT = COLORS["text_main"]
        MUTED = COLORS["text_muted"]
        BORDER = COLORS["border"]
        SOFT_BLUE = COLORS["primary_light"]
        SOFT_PINK = COLORS["accent_pink_soft"]
        DANGER = COLORS["danger"]
        SOFT_DANGER = "#FEF2F2"

        self.root.configure(bg=BG)

        # -------------------- ttk styles --------------------
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Primary.TButton",
            background=BLUE,
            foreground=WHITE,
            borderwidth=0,
            focusthickness=0,
            padding=(18, 11),
            font=("Segoe UI", 11, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
        )

        style.configure(
            "Danger.TButton",
            background=DANGER,
            foreground=WHITE,
            borderwidth=0,
            focusthickness=0,
            padding=(18, 11),
            font=("Segoe UI", 11, "bold"),
        )
        style.map(
            "Danger.TButton",
            background=[("active", "#B91C1C"), ("pressed", "#991B1B")],
        )

        style.configure(
            "Secondary.TButton",
            background=WHITE,
            foreground=TEXT,
            borderwidth=1,
            bordercolor=BORDER,
            focusthickness=0,
            padding=(16, 9),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#F8FAFC"), ("pressed", "#F1F5F9")],
            bordercolor=[("focus", BLUE)],
        )

        # -------------------- Root layout --------------------
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # -------------------- Header --------------------
        header = Frame(self.root, bg=WHITE, height=82)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        try:
            _logo = Image.open(os.path.join(IMAGE_DIR, "Face-Recognition-Software.png"))
            _logo = _logo.resize((44, 44), Image.LANCZOS)
            self._hdr_logo = ImageTk.PhotoImage(_logo)
            brand_mark = Label(header, image=self._hdr_logo, bg=WHITE)
            brand_mark.grid(row=0, column=0, padx=(24, 14), pady=17)
        except Exception:
            brand_mark = Frame(header, bg=BLUE, width=48, height=48)
            brand_mark.grid(row=0, column=0, padx=(24, 14), pady=17)
            brand_mark.grid_propagate(False)
            Label(
                brand_mark,
                text="FR",
                bg=BLUE,
                fg=WHITE,
                font=("Segoe UI", 14, "bold"),
            ).place(relx=0.5, rely=0.5, anchor="center")

        brand_area = Frame(header, bg=WHITE)
        brand_area.grid(row=0, column=1, sticky="nsw", pady=13)

        Label(
            brand_area,
            text="Face Recognition Attendance System",
            bg=WHITE,
            fg=DARK_BLUE,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        Label(
            brand_area,
            text="Face recognition management",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(2, 0))

        ttk.Button(header, text="Back to Dashboard", command=self.go_back,
                   style="Secondary.TButton").grid(
                       row=0, column=2, padx=(10, 24), pady=19)

        Frame(header, bg=BORDER, height=1).place(
            relx=0, rely=1.0, relwidth=1.0, anchor="sw"
        )

        # -------------------- Body --------------------
        body = Frame(self.root, bg=BG)
        body.grid(row=1, column=0, sticky="nsew", padx=24, pady=22)
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        # Intro
        intro = Frame(body, bg=BG)
        intro.grid(row=0, column=0, sticky="ew", pady=(0, 18))

        Label(
            intro,
            text="Face Recognition",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 22, "bold"),
        ).pack(anchor="w")

        Label(
            intro,
            text="Detect registered students through your camera and mark attendance automatically.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        # Main panel
        panel_wrap = Frame(body, bg=BG)
        panel_wrap.grid(row=1, column=0, sticky="nsew")
        panel_wrap.grid_columnconfigure(0, weight=1)
        panel_wrap.grid_rowconfigure(0, weight=1)

        panel = Frame(panel_wrap, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        panel.grid(row=0, column=0, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        center = Frame(panel, bg=WHITE)
        center.grid(row=0, column=0)

        icon_box = Frame(center, bg=SOFT_PINK, width=110, height=110)
        icon_box.pack(pady=(0, 22))
        icon_box.pack_propagate(False)

        Label(
            icon_box,
            text="\U0001F4F7",
            bg=SOFT_PINK,
            fg=PINK,
            font=("Segoe UI", 40),
        ).pack(expand=True)

        Label(
            center,
            text="Face Detector",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 18, "bold"),
        ).pack()

        Label(
            center,
            text="Start the camera to recognize registered students and mark their attendance.\nPress Enter or Esc in the camera window, or click Stop, to end the session.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10),
            justify="center",
        ).pack(pady=(10, 26))

        btn_row = Frame(center, bg=WHITE)
        btn_row.pack()

        ttk.Button(
            btn_row,
            text="\u25B6  Start Recognition",
            command=self.start_face_recognition,
            style="Primary.TButton",
            cursor="hand2",
        ).grid(row=0, column=0, padx=(0, 12))

        ttk.Button(
            btn_row,
            text="\u25A0  Stop Recognition",
            command=self.stop_face_recognition,
            style="Danger.TButton",
            cursor="hand2",
        ).grid(row=0, column=1)

        # ---- Camera Settings panel (below main panel) ----
        cam_panel = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        cam_panel.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        cam_panel.grid_columnconfigure(1, weight=1)

        Label(
            cam_panel, text="CAMERA SOURCE",
            bg=WHITE, fg=BLUE, font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=18, pady=(12, 6))

        self._cam_type = tk.StringVar()
        saved = get_settings()
        self._cam_type.set(saved.get("source_type", "local"))

        ttk.Radiobutton(
            cam_panel, text="Local webcam (index)",
            variable=self._cam_type, value="local",
            command=self._on_cam_type_change
        ).grid(row=1, column=0, padx=(18, 12), pady=(0, 10))

        ttk.Radiobutton(
            cam_panel, text="IP Webcam / Phone camera (URL)",
            variable=self._cam_type, value="ip_webcam",
            command=self._on_cam_type_change
        ).grid(row=1, column=1, padx=(0, 12), pady=(0, 10), sticky="w")

        self._ip_url_var = tk.StringVar(value=saved.get("ip_url", ""))
        self._ip_entry = ttk.Entry(
            cam_panel, textvariable=self._ip_url_var,
            font=("Segoe UI", 10), width=38
        )
        self._ip_entry.grid(row=1, column=2, padx=(0, 8), pady=(0, 10), sticky="ew")

        Label(
            cam_panel,
            text="e.g.  http://192.168.1.5:8080/video",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 8)
        ).grid(row=2, column=2, sticky="w", padx=(0, 8), pady=(0, 8))

        ttk.Button(
            cam_panel, text="Save", style="Secondary.TButton",
            command=self._save_cam_settings
        ).grid(row=1, column=3, padx=(0, 18), pady=(0, 10))

        Label(
            cam_panel,
            text="\u2139  Install \"IP Webcam\" from Play Store on Android. Start server → paste the URL above.",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 8)
        ).grid(row=3, column=0, columnspan=4, sticky="w", padx=18, pady=(0, 10))

        self._on_cam_type_change()   # set initial entry state

        self.recognition_running = False
        self.recognition_thread = None
        self.videoCap = None

        # Variable to track if windows were created
        self.windows_created = False

    # ---- Camera settings helpers ----
    def _on_cam_type_change(self):
        if self._cam_type.get() == "ip_webcam":
            self._ip_entry.configure(state="normal")
        else:
            self._ip_entry.configure(state="disabled")

    def _save_cam_settings(self):
        save_settings(
            source_type=self._cam_type.get(),
            ip_url=self._ip_url_var.get()
        )
        messagebox.showinfo(
            "Camera settings saved",
            "Camera source updated. Changes take effect on next \"Start Recognition\".",
            parent=self.root
        )

    def on_closing(self):
        """Handle main window closing event"""
        self.stop_face_recognition()
        self.root.destroy()

    def go_back(self):
        self.on_closing()

    def mark_attendance(self, i, r, n):
        try:
            # Create the file if it doesn't exist
            if not os.path.exists(self.attendance_path):
                with open(self.attendance_path, "w", newline="\n") as f:
                    f.write("ID,Roll,Name,Time,Date,Attendance\n")
                    print("Created new attendance.csv file")
                    
            # First, check if the person is already in the attendance list
            with open(self.attendance_path, "r", newline="\n") as f:
                myDatalist = f.readlines()
                name_list = []
                for line in myDatalist:
                    entry = line.split(",")
                    if len(entry) > 0:
                        name_list.append(entry[0])
            
            now = datetime.now()
            d1 = now.strftime("%d/%m/%Y")
            already_recorded_today = any(
                line.split(",")[0] == i and len(line.split(",")) > 4
                and line.split(",")[4] == d1
                for line in myDatalist
            )

            # Store one recognition record per student per day.
            if not already_recorded_today:
                dtString = now.strftime("%H:%M:%S")
                # Open the file in append mode
                with open(self.attendance_path, "a", newline="\n") as f:
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
                cursor.execute("SELECT Name FROM student WHERE Student_ID = %s AND Owner_Email = %s", (str(id), self.owner_email))
                n = cursor.fetchone()
                n = "+".join([str(item) for item in n]) if n else "Unknown"

                cursor.execute("SELECT Roll_No FROM student WHERE Student_ID = %s AND Owner_Email = %s", (str(id), self.owner_email))
                r = cursor.fetchone()
                r = "+".join([str(item) for item in r]) if r else "Unknown"

                cursor.execute("SELECT Student_ID FROM student WHERE Student_ID = %s AND Owner_Email = %s", (str(id), self.owner_email))
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
            recognizer.read(self.model_path)
            
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
                    
                    cursor.execute("SELECT Name, Roll_No FROM student WHERE Student_ID = %s AND Owner_Email = %s", (str(id), self.owner_email))
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
            cascade_path = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
            faceCascade = cv2.CascadeClassifier(cascade_path)
            if faceCascade.empty():
                raise RuntimeError(
                    f"Could not load face detector file:\n{cascade_path}"
                )

            clf = cv2.face.LBPHFaceRecognizer_create()
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(
                    "Trained model not found. Please go to Data Train and click \"Train Dataset\" first."
                )
            clf.read(self.model_path)

            cam_source = get_camera_source()   # int index or URL string
            self.videoCap = cv2.VideoCapture(cam_source)
            if not self.videoCap.isOpened():
                source_label = cam_source if isinstance(cam_source, str) else f"camera index {cam_source}"
                raise RuntimeError(
                    f"Could not open camera ({source_label}).\n"
                    "• For local webcam: make sure it is connected and not in use.\n"
                    "• For IP Webcam: make sure the phone app is running and the URL is correct."
                )

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
            # Show error in GUI — no more silent failures
            self.root.after(0, lambda err=str(e): messagebox.showerror(
                "Face Recognition Error", err, parent=self.root
            ))
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