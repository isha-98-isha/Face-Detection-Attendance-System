from tkinter import* 
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
from register import Register
import mysql.connector
import pymysql
import re  # Import regex module for email validation
pymysql.install_as_MySQLdb()
# --------------------------
from train import Train
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from helpsupport import Helpsupport
from db_config import DB_CONFIG
from main import Face_Recognition_System
import os
import json
from Session_utils import save_session, load_session, clear_session
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")

class Login:
    def __init__(self, root):
        self.root = root

        # -------------------- Remember-me auto login --------------------
        # If a valid remembered session exists, skip the login form entirely
        # and go straight to the dashboard on this same root window.
        if self.try_auto_login():
            return

        self.root.title("Login • Face Recognition Attendance System")
        self.root.minsize(920, 620)
        self.set_auth_window_state()
        self.root.configure(bg="#F7F9FC")

        # -------------------- Variables --------------------
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()
        self.var_remember = BooleanVar(value=False)

        # -------------------- Theme --------------------
        WHITE = "#FFFFFF"
        BG = "#F7F9FC"
        BLUE = "#2563EB"
        BLUE_DARK = "#172554"
        BLUE_SOFT = "#EFF6FF"
        PINK = "#EC4899"
        PINK_SOFT = "#FDF2F8"
        TEXT = "#1E293B"
        MUTED = "#64748B"
        BORDER = "#E2E8F0"

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Auth.TEntry",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=(12, 10),
            font=("Segoe UI", 11),
        )
        style.map(
            "Auth.TEntry",
            bordercolor=[("focus", BLUE)],
            lightcolor=[("focus", BLUE)],
            darkcolor=[("focus", BLUE)],
        )

        style.configure(
            "Auth.Primary.TButton",
            background=BLUE,
            foreground=WHITE,
            relief="flat",
            borderwidth=0,
            padding=(14, 11),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Auth.Primary.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
        )

        style.configure(
            "Auth.Secondary.TButton",
            background=WHITE,
            foreground=BLUE,
            relief="flat",
            borderwidth=1,
            bordercolor=BORDER,
            padding=(14, 10),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Auth.Secondary.TButton",
            background=[("active", BLUE_SOFT), ("pressed", "#DBEAFE")],
            bordercolor=[("focus", BLUE)],
        )

        style.configure(
            "Auth.TCheckbutton",
            background=WHITE,
            foreground=TEXT,
            font=("Segoe UI", 9),
        )
        style.map(
            "Auth.TCheckbutton",
            background=[("active", WHITE)],
        )

        # -------------------- Responsive root --------------------
        # Clear the dashboard's two-column grid before rebuilding login in
        # the same root window after logout.
        for column in range(2):
            self.root.grid_columnconfigure(column, weight=0)
        for row in range(2):
            self.root.grid_rowconfigure(row, weight=0)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        shell = Frame(self.root, bg=BG)
        shell.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        shell.grid_rowconfigure(0, weight=1)
        shell.grid_columnconfigure(0, weight=11)
        shell.grid_columnconfigure(1, weight=9)

        # -------------------- Brand / visual panel --------------------
        visual = Frame(shell, bg=BLUE_DARK)
        visual.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # Decorative pink / blue blocks
        Frame(visual, bg=PINK, width=190, height=190).place(
            relx=0.88, rely=-0.08, anchor="ne"
        )
        Frame(visual, bg=BLUE, width=150, height=150).place(
            relx=-0.05, rely=0.88, anchor="sw"
        )
        Frame(visual, bg="#60A5FA", width=90, height=90).place(
            relx=0.12, rely=0.10
        )
        Frame(visual, bg="#F9A8D4", width=70, height=70).place(
            relx=0.78, rely=0.78
        )

        visual_content = Frame(visual, bg=BLUE_DARK)
        visual_content.place(relx=0.11, rely=0.16, relwidth=0.78, relheight=0.68)

        Label(
            visual_content,
            text="FACE RECOGNITION",
            bg=BLUE_DARK,
            fg="#BFDBFE",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        Label(
            visual_content,
            text="Attendance\nSystem",
            bg=BLUE_DARK,
            fg=WHITE,
            font=("Segoe UI", 34, "bold"),
            justify="left",
        ).pack(anchor="w", pady=(10, 8))

        Label(
            visual_content,
            text="Smart student management,\nface recognition and attendance tracking.",
            bg=BLUE_DARK,
            fg="#CBD5E1",
            font=("Segoe UI", 12),
            justify="left",
        ).pack(anchor="w")

        feature = Frame(visual_content, bg="#1E3A8A")
        feature.pack(fill="x", pady=(40, 0))

        Label(
            feature,
            text="SECURE  •  SIMPLE  •  CONNECTED",
            bg="#1E3A8A",
            fg="#DBEAFE",
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=12,
        ).pack(anchor="w")

        Label(
            visual_content,
            text="Face Recognition Attendance System",
            bg=BLUE_DARK,
            fg="#93C5FD",
            font=("Segoe UI", 9),
        ).pack(anchor="w", side="bottom", pady=(18, 0))

        # -------------------- Login card --------------------
        card_wrap = Frame(shell, bg=BG)
        card_wrap.grid(row=0, column=1, sticky="nsew")
        card_wrap.grid_rowconfigure(0, weight=1)
        card_wrap.grid_columnconfigure(0, weight=1)

        card = Frame(
            card_wrap,
            bg=WHITE,
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        card.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=30)
        card.grid_columnconfigure(0, weight=1)

        # Pink accent
        Frame(card, bg=PINK, height=5).grid(
            row=0, column=0, sticky="ew"
        )

        content = Frame(card, bg=WHITE)
        content.grid(row=1, column=0, sticky="nsew", padx=54, pady=48)
        content.grid_columnconfigure(0, weight=1)

        Label(
            content,
            text="Welcome back",
            bg=WHITE,
            fg=BLUE_DARK,
            font=("Segoe UI", 28, "bold"),
        ).grid(row=0, column=0, sticky="w")

        Label(
            content,
            text="Sign in to continue to the attendance system",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, sticky="w", pady=(6, 34))

        Label(
            content,
            text="EMAIL",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=2, column=0, sticky="w", pady=(0, 6))

        self.txtuser = ttk.Entry(content, style="Auth.TEntry")
        self.txtuser.grid(row=3, column=0, sticky="ew")

        self.email_status = Label(
            content,
            text="",
            font=("Segoe UI", 9),
            fg=PINK,
            bg=WHITE,
        )
        self.email_status.grid(row=4, column=0, sticky="w", pady=(5, 16))

        Label(
            content,
            text="PASSWORD",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=5, column=0, sticky="w", pady=(0, 6))

        self.txtpwd = ttk.Entry(content, style="Auth.TEntry", show="*")
        self.txtpwd.grid(row=6, column=0, sticky="ew")

        self.pwd_status = Label(
            content,
            text="",
            font=("Segoe UI", 9),
            fg=PINK,
            bg=WHITE,
        )
        self.pwd_status.grid(row=7, column=0, sticky="w", pady=(5, 14))

        ttk.Checkbutton(
            content,
            text="Keep me signed in",
            variable=self.var_remember,
            style="Auth.TCheckbutton",
        ).grid(row=8, column=0, sticky="w", pady=(0, 12))

        ttk.Button(
            content,
            text="Sign In",
            command=self.login,
            style="Auth.Primary.TButton",
        ).grid(row=9, column=0, sticky="ew", pady=(6, 10))

        actions = Frame(content, bg=WHITE)
        actions.grid(row=10, column=0, sticky="ew", pady=(8, 0))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        ttk.Button(
            actions,
            text="Create account",
            command=self.reg,
            style="Auth.Secondary.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ttk.Button(
            actions,
            text="Forgot password?",
            command=self.forget_pwd,
            style="Auth.Secondary.TButton",
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))

        Label(
            content,
            text="Your account credentials are used only for this application.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8),
            wraplength=420,
            justify="left",
        ).grid(row=11, column=0, sticky="w", pady=(24, 0))

        # Preserve existing validation callbacks.
        self.txtuser.bind("<FocusOut>", self.validate_email)
        self.txtpwd.bind("<FocusOut>", self.validate_password)

    def set_auth_window_state(self):
        self.root.update_idletasks()
        try:
            self.root.state("normal")
            self.root.state("zoomed")
        except Exception:
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
            self.root.geometry(f"{screen_w}x{screen_h}+0+0")

    # Validate email format
    def validate_email(self, event=None):
        email = self.txtuser.get()
        # Regular expression pattern for email validation
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if email == "":
            self.email_status.config(text="")
            return False
        
        if re.match(pattern, email):
            self.email_status.config(text="Valid email format", fg="green")
            return True
        else:
            self.email_status.config(text="Invalid email format", fg="red")
            return False
            
    # Validate password strength
    def validate_password(self, event=None):
        password = self.txtpwd.get()
        
        if password == "":
            self.pwd_status.config(text="")
            return False
        
        # Check password length
        if len(password) < 8:
            self.pwd_status.config(text="Password too short (min 8 chars)", fg="red")
            return False
        
        # Check for password strength (optional - can be modified)
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_special = any(not char.isalnum() for char in password)
        
        if has_digit and has_upper and has_lower and has_special:
            self.pwd_status.config(text="Strong password", fg="green")
            return True
        elif (has_digit and has_upper) or (has_lower and has_special) or (has_upper and has_special):
            self.pwd_status.config(text="Moderate password", fg="yellow")
            return True
        else:
            self.pwd_status.config(text="Weak password", fg="orange")
            return True  # Still allow login with weak password
    
    #  THis function is for open register window
    def reg(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)


    def login(self):
        # First validate input fields
        is_valid_email = self.validate_email()
        is_valid_pwd = self.validate_password()
        
        if not is_valid_email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
            
        if not is_valid_pwd:
            messagebox.showerror("Error", "Please enter a valid password!")
            return
            
        if (self.txtuser.get()=="" or self.txtpwd.get()==""):
            messagebox.showerror("Error","All Fields Required!")
        elif(self.txtuser.get()=="admin" and self.txtpwd.get()=="admin"):
            messagebox.showinfo("Successfully","Welcome to Attendance Management System Using Facial Recognition")
            if self.var_remember.get():
                save_session(self.txtuser.get())
            else:
                clear_session()
            self.open_dashboard("admin", "Admin")
        else:
            # messagebox.showerror("Error","Please Check Username or Password !")
            conn = mysql.connector.connect(**DB_CONFIG)
            mycursor = conn.cursor()
            mycursor.execute("select * from regteach where BINARY email = BINARY %s and BINARY pwd = BINARY %s",(
                self.txtuser.get(),
                self.txtpwd.get()
            ))
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username and Password!")
            else:
                open_min=messagebox.askyesno("YesNo","Access only Admin")
                if open_min>0:
                    if self.var_remember.get():
                        save_session(self.txtuser.get())
                    else:
                        clear_session()
                    self.open_dashboard(
                        self.txtuser.get(),
                        f"{row[0]} {row[1]}".strip(),
                    )
                else:
                    if not open_min:
                        return
                conn.commit()
                conn.close()

    # -------------------- Remember-me helpers --------------------
    def open_dashboard(self, user_email, user_name):
        """Swap this window's content from the login form to the
        dashboard, reusing the same window (mirrors main.py's logout)."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.app = Face_Recognition_System(
            self.root,
            authenticated=True,
            user_email=user_email,
            user_name=user_name,
        )

    def try_auto_login(self):
        """If a remembered session exists and is still valid, open the
        dashboard directly on this root window and return True."""
        email = load_session()
        if not email:
            return False
        try:
            if email == "admin":
                self.app = Face_Recognition_System(
                    self.root, authenticated=True,
                    user_email="admin", user_name="Admin")
                return True

            conn = mysql.connector.connect(**DB_CONFIG)
            mycursor = conn.cursor()
            mycursor.execute("select * from regteach where BINARY email = BINARY %s", (email,))
            row = mycursor.fetchone()
            conn.close()

            if row is None:
                clear_session()
                return False

            self.app = Face_Recognition_System(
                self.root,
                authenticated=True,
                user_email=email,
                user_name=f"{row[0]} {row[1]}".strip(),
            )
            return True
        except Exception:
            clear_session()
            return False
#=======================Reset Password Function=============================
    def reset_pass(self):
        # Validate new password
        password = self.var_pwd.get()
        if len(password) < 8:
            messagebox.showerror("Error","Password must be at least 8 characters long!",parent=self.root2)
            return
            
        # Check for password strength (can be modified based on requirements)
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_special = any(not char.isalnum() for char in password)
        
        if not (has_digit and has_upper and has_lower and has_special):
            messagebox.showwarning("Warning","Password should include uppercase, lowercase, digits and special characters!",parent=self.root2)
            # Continue anyway - just a warning
        
        if self.var_ssq.get()=="Select":
            messagebox.showerror("Error","Select the Security Question!",parent=self.root2)
        elif(self.var_sa.get()==""):
            messagebox.showerror("Error","Please Enter the Answer!",parent=self.root2)
        elif(self.var_pwd.get()==""):
            messagebox.showerror("Error","Please Enter the New Password!",parent=self.root2)
        else:
            conn = mysql.connector.connect(**DB_CONFIG)
            mycursor = conn.cursor()
            query=("select * from regteach where BINARY email = BINARY %s and BINARY ss_que = BINARY %s and BINARY s_ans = BINARY %s")
            value=(self.txtuser.get(),self.var_ssq.get(),self.var_sa.get())
            mycursor.execute(query,value)
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please Enter the Correct Answer!",parent=self.root2)
            else:
                query=("update regteach set pwd=%s where BINARY email = BINARY %s")
                value=(self.var_pwd.get(),self.txtuser.get())
                mycursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Successfully Your password has been reset, Please login with new Password!",parent=self.root2)
                



# =====================Forget window=========================================
    def forget_pwd(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please Enter the Email ID to reset Password!")
        elif not self.validate_email():
            messagebox.showerror("Error","Please Enter a Valid Email Address!")
        else:
            conn = mysql.connector.connect(**DB_CONFIG)
            mycursor = conn.cursor()
            query=("select * from regteach where BINARY email = BINARY %s")
            value=(self.txtuser.get(),)
            mycursor.execute(query,value)
            row=mycursor.fetchone()
# print(row)

        if row==None:
            messagebox.showerror("Error","Please Enter the Valid Email ID!")
        else:
            conn.close()
            self.root2 = Toplevel(self.root)
            self.root2.title("Forgot Password • Face Recognition Attendance System")
            self.root2.minsize(920, 620)
            self.root2.configure(bg="#F7F9FC")
            self.root2.grid_rowconfigure(0, weight=1)
            self.root2.grid_columnconfigure(0, weight=11)
            self.root2.grid_columnconfigure(1, weight=9)

            WHITE = "#FFFFFF"
            BG = "#F7F9FC"
            BLUE = "#2563EB"
            BLUE_DARK = "#172554"
            BLUE_SOFT = "#EFF6FF"
            PINK = "#EC4899"
            TEXT = "#1E293B"
            MUTED = "#64748B"
            BORDER = "#E2E8F0"

            visual = Frame(self.root2, bg=BLUE_DARK)
            visual.grid(row=0, column=0, sticky="nsew", padx=(24, 12), pady=24)
            Frame(visual, bg=PINK, width=190, height=190).place(relx=0.88, rely=-0.08, anchor="ne")
            Frame(visual, bg=BLUE, width=150, height=150).place(relx=-0.05, rely=0.88, anchor="sw")
            Frame(visual, bg="#60A5FA", width=90, height=90).place(relx=0.12, rely=0.10)
            Frame(visual, bg="#F9A8D4", width=70, height=70).place(relx=0.78, rely=0.78)

            visual_content = Frame(visual, bg=BLUE_DARK)
            visual_content.place(relx=0.11, rely=0.16, relwidth=0.78, relheight=0.68)
            Label(visual_content, text="FACE RECOGNITION", bg=BLUE_DARK, fg="#BFDBFE",
                font=("Segoe UI", 11, "bold")).pack(anchor="w")
            Label(visual_content, text="Attendance\nSystem", bg=BLUE_DARK, fg=WHITE,
                font=("Segoe UI", 34, "bold"), justify="left").pack(anchor="w", pady=(10, 8))
            Label(visual_content,
                text="Smart student management,\nface recognition and attendance tracking.",
                bg=BLUE_DARK, fg="#CBD5E1", font=("Segoe UI", 12),
                justify="left").pack(anchor="w")
            feature = Frame(visual_content, bg="#1E3A8A")
            feature.pack(fill="x", pady=(40, 0))
            Label(feature, text="SECURE  •  SIMPLE  •  CONNECTED", bg="#1E3A8A",
                fg="#DBEAFE", font=("Segoe UI", 9, "bold"), padx=16, pady=12).pack(anchor="w")
            Label(visual_content, text="Face Recognition Attendance System", bg=BLUE_DARK,
                fg="#93C5FD", font=("Segoe UI", 9)).pack(anchor="w", side="bottom", pady=(18, 0))

            card = Frame(self.root2, bg=WHITE, highlightthickness=1, highlightbackground=BORDER)
            card.grid(row=0, column=1, sticky="nsew", padx=(12, 24), pady=24)
            card.grid_columnconfigure(0, weight=1)
            Frame(card, bg=PINK, height=5).grid(row=0, column=0, sticky="ew")

            content = Frame(card, bg=WHITE)
            content.grid(row=1, column=0, sticky="nsew", padx=54, pady=48)
            content.grid_columnconfigure(0, weight=1)
            Label(content, text="Reset your password", bg=WHITE, fg=BLUE_DARK,
                font=("Segoe UI", 28, "bold")).grid(row=0, column=0, sticky="w")
            Label(content, text="Verify your account and create a new password",
                bg=WHITE, fg=MUTED, font=("Segoe UI", 10)).grid(row=1, column=0,
                sticky="w", pady=(6, 34))

            Label(content, text="SECURITY QUESTION", bg=WHITE, fg=TEXT,
                font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 6))
            self.combo_security = ttk.Combobox(
                content, textvariable=self.var_ssq,
                values=("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book"),
                state="readonly", style="Auth.TEntry")
            self.combo_security.grid(row=3, column=0, sticky="ew")
            self.combo_security.current(0)

            Label(content, text="SECURITY ANSWER", bg=WHITE, fg=TEXT,
                font=("Segoe UI", 9, "bold")).grid(row=4, column=0, sticky="w", pady=(18, 6))
            self.reset_answer_entry = ttk.Entry(content, textvariable=self.var_sa, style="Auth.TEntry")
            self.reset_answer_entry.grid(row=5, column=0, sticky="ew")

            Label(content, text="NEW PASSWORD", bg=WHITE, fg=TEXT,
                font=("Segoe UI", 9, "bold")).grid(row=6, column=0, sticky="w", pady=(18, 6))
            self.new_pwd = ttk.Entry(content, textvariable=self.var_pwd, style="Auth.TEntry", show="*")
            self.new_pwd.grid(row=7, column=0, sticky="ew")
            self.pwd_indicator = Label(content, text="", font=("Segoe UI", 9),
                               fg=MUTED, bg=WHITE)
            self.pwd_indicator.grid(row=8, column=0, sticky="w", pady=(5, 14))
            self.new_pwd.bind("<KeyRelease>", self.check_password_strength)

            ttk.Button(content, command=self.reset_pass, text="Reset Password",
                     style="Auth.Primary.TButton").grid(row=9, column=0, sticky="ew", pady=(6, 10))
            ttk.Button(content, command=self.back_to_login, text="Back to login",
                     style="Auth.Secondary.TButton").grid(row=10, column=0, sticky="ew")
            self.root2.transient(self.root)
            self.root2.grab_set()
            self.root2.update_idletasks()
            try:
                self.root2.state("normal")
                self.root2.state("zoomed")
            except Exception:
                self.root2.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}+0+0")

    def back_to_login(self):
        if hasattr(self, "root2") and self.root2.winfo_exists():
            self.root2.grab_release()
            self.root2.destroy()
        self.root.deiconify()
        self.root.focus_force()

    # Check password strength for the reset password window
    def check_password_strength(self, event=None):
        password = self.var_pwd.get()
        
        if password == "":
            self.pwd_indicator.config(text="")
            return
            
        # Check password length
        if len(password) < 8:
            self.pwd_indicator.config(text="Password too short (min 8 chars)", fg="red")
            return
            
        # Check for password strength
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_special = any(not char.isalnum() for char in password)
        
        strength = 0
        criteria = [has_digit, has_upper, has_lower, has_special]
        for criteria_met in criteria:
            if criteria_met:
                strength += 1
                
        if strength == 4:
            self.pwd_indicator.config(text="Strong password", fg="green")
        elif strength == 3:
            self.pwd_indicator.config(text="Moderate password", fg="blue")
        elif strength == 2:
            self.pwd_indicator.config(text="Fair password", fg="orange")
        else:
            self.pwd_indicator.config(text="Weak password", fg="red")


if __name__ == "__main__":
    root=Tk()
    app=Login(root)
    root.mainloop()