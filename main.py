from tkinter import *
from tkinter import ttk
from train import Train
from PIL import Image, ImageTk
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
import os
from helpsupport import Helpsupport
import mysql.connector
import pymysql

pymysql.install_as_MySQLdb()


# ============================================================
# Project paths
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")


class Face_Recognition_System:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face_Recogonition_System")

        # ====================================================
        # Header image
        # ====================================================

        img = Image.open(os.path.join(IMAGE_DIR, "banner.jpg"))
        img = img.resize((1366, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lb1 = Label(self.root, image=self.photoimg)
        f_lb1.place(x=0, y=0, width=1366, height=100)

        # ====================================================
        # Background image
        # ====================================================

        bg1 = Image.open(os.path.join(IMAGE_DIR, "bg3.jpg"))
        bg1 = bg1.resize((1366, 768), Image.LANCZOS)
        self.photobg1 = ImageTk.PhotoImage(bg1)

        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=100, width=1366, height=768)

        # ====================================================
        # Title
        # ====================================================

        title_lb1 = Label(
            bg_img,
            text="Face Recognition Attendance System      ",
            font=("verdana", 30, "bold"),
            bg="white",
            fg="navyblue"
        )
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # ====================================================
        # Student button
        # ====================================================

        std_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "std1.jpg")
        )
        std_img_btn = std_img_btn.resize((180, 180), Image.LANCZOS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(
            bg_img,
            command=self.student_pannels,
            image=self.std_img1,
            cursor="hand2"
        )
        std_b1.place(x=250, y=100, width=160, height=150)

        std_b1_1 = Button(
            bg_img,
            command=self.student_pannels,
            text="Student Pannel",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        std_b1_1.place(x=250, y=250, width=160, height=35)

        # ====================================================
        # Face Detector button
        # ====================================================

        det_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "det1.jpg")
        )
        det_img_btn = det_img_btn.resize((180, 180), Image.LANCZOS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(
            bg_img,
            command=self.face_rec,
            image=self.det_img1,
            cursor="hand2"
        )
        det_b1.place(x=480, y=100, width=160, height=150)

        det_b1_1 = Button(
            bg_img,
            command=self.face_rec,
            text="Face Detector",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        det_b1_1.place(x=480, y=250, width=160, height=35)

        # ====================================================
        # Attendance button
        # ====================================================

        att_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "att.jpg")
        )
        att_img_btn = att_img_btn.resize((180, 180), Image.LANCZOS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(
            bg_img,
            command=self.attendance_pannel,
            image=self.att_img1,
            cursor="hand2"
        )
        att_b1.place(x=710, y=100, width=160, height=150)

        att_b1_1 = Button(
            bg_img,
            command=self.attendance_pannel,
            text="Attendance",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        att_b1_1.place(x=710, y=250, width=160, height=35)

        # ====================================================
        # Help Support button
        # ====================================================

        hlp_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "hlp.jpg")
        )
        hlp_img_btn = hlp_img_btn.resize((180, 180), Image.LANCZOS)
        self.hlp_img1 = ImageTk.PhotoImage(hlp_img_btn)

        hlp_b1 = Button(
            bg_img,
            command=self.helpSupport,
            image=self.hlp_img1,
            cursor="hand2"
        )
        hlp_b1.place(x=940, y=100, width=160, height=150)

        hlp_b1_1 = Button(
            bg_img,
            command=self.helpSupport,
            text="Help Support",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        hlp_b1_1.place(x=940, y=250, width=160, height=35)

        # ====================================================
        # Data Train button
        # ====================================================

        tra_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "tra1.jpg")
        )
        tra_img_btn = tra_img_btn.resize((180, 180), Image.LANCZOS)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(
            bg_img,
            command=self.train_pannels,
            image=self.tra_img1,
            cursor="hand2"
        )
        tra_b1.place(x=250, y=330, width=160, height=150)

        tra_b1_1 = Button(
            bg_img,
            command=self.train_pannels,
            text="Data Train",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        tra_b1_1.place(x=250, y=480, width=160, height=35)

        # ====================================================
        # Developers button
        # ====================================================

        dev_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "dev.jpg")
        )
        dev_img_btn = dev_img_btn.resize((180, 180), Image.LANCZOS)
        self.dev_img1 = ImageTk.PhotoImage(dev_img_btn)

        dev_b1 = Button(
            bg_img,
            command=self.developr,
            image=self.dev_img1,
            cursor="hand2"
        )
        dev_b1.place(x=480, y=330, width=160, height=150)

        dev_b1_1 = Button(
            bg_img,
            command=self.developr,
            text="Developers",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        dev_b1_1.place(x=480, y=480, width=160, height=35)

        # ====================================================
        # Exit button
        # ====================================================

        # OIP.jpg is not present in the recovered Images_GUI.
        # Use the available exit image instead.
        exi_img_btn = Image.open(
            os.path.join(IMAGE_DIR, "exi.jpg")
        )
        exi_img_btn = exi_img_btn.resize((180, 180), Image.LANCZOS)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(
            bg_img,
            command=self.Close,
            image=self.exi_img1,
            cursor="hand2"
        )
        exi_b1.place(x=710, y=330, width=160, height=150)

        exi_b1_1 = Button(
            bg_img,
            command=self.Close,
            text="Exit",
            cursor="hand2",
            font=("tahoma", 15, "bold"),
            bg="white",
            fg="navyblue"
        )
        exi_b1_1.place(x=710, y=480, width=160, height=35)

    # ========================================================
    # Function for opening image folder
    # ========================================================

    def open_img(self):
        dataset_path = os.path.join(BASE_DIR, "dataset")

        if os.path.exists(dataset_path):
            os.startfile(dataset_path)
        else:
            messagebox.showerror(
                "Error",
                "Dataset folder not found."
            )

    # ========================================================
    # Button functions
    # ========================================================

    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_rec(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def developr(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window)

    def helpSupport(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(self.new_window)

    def Close(self):
        self.root.destroy()


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()