import os
from ui.theme import COLORS, apply_theme, FONTS
from ui.components import *
from ui.icons import ICONS
from ui.assets import get_image_path, load_image, BASE_DIR
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
import re  # Adding regex for validation
from db_config import DB_CONFIG
pymysql.install_as_MySQLdb()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register • Face Recognition Attendance System")
        self.root.geometry("1260x820")
        self.root.minsize(1000, 700)
        try:
            self.root.state("zoomed")
        except Exception:
            pass
        self.root.configure(bg="#F7F9FC")

        # -------------------- Variables --------------------
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_cnum = StringVar()
        self.var_email = StringVar()
        self.var_ssq = StringVar()
        self.var_sa = StringVar()
        self.var_pwd = StringVar()
        self.var_cpwd = StringVar()
        self.var_check = IntVar()
        self.var_showpwd = IntVar()

        # -------------------- Theme --------------------
        WHITE = COLORS["white"]
        BG = COLORS["bg_main"]
        BLUE = COLORS["primary"]
        BLUE_DARK = COLORS["secondary"]
        BLUE_SOFT = "#EFF6FF"
        PINK = COLORS["accent_pink"]
        PINK_SOFT = "#FDF2F8"
        TEXT = COLORS["text_main"]
        MUTED = COLORS["text_muted"]
        BORDER = COLORS["border"]

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Reg.TEntry",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=(11, 9),
            font=("Segoe UI", 10),
        )
        style.map(
            "Reg.TEntry",
            bordercolor=[("focus", BLUE)],
            lightcolor=[("focus", BLUE)],
            darkcolor=[("focus", BLUE)],
        )

        style.configure(
            "Reg.TCombobox",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            arrowcolor=BLUE,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=(9, 9),
            font=("Segoe UI", 10),
        )
        style.map(
            "Reg.TCombobox",
            fieldbackground=[("readonly", WHITE)],
            bordercolor=[("focus", BLUE)],
            lightcolor=[("focus", BLUE)],
            darkcolor=[("focus", BLUE)],
        )

        style.configure(
            "Reg.Primary.TButton",
            background=BLUE,
            foreground=WHITE,
            relief="flat",
            borderwidth=0,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Reg.Primary.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
        )

        style.configure(
            "Reg.Secondary.TButton",
            background=WHITE,
            foreground=BLUE,
            relief="flat",
            borderwidth=1,
            bordercolor=BORDER,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Reg.Secondary.TButton",
            background=[("active", BLUE_SOFT), ("pressed", "#DBEAFE")],
            bordercolor=[("focus", BLUE)],
        )

        # -------------------- Responsive split layout --------------------
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=11)
        self.root.grid_columnconfigure(1, weight=9)

        visual = Frame(self.root, bg=BLUE_DARK)
        visual.grid(row=0, column=0, sticky="nsew", padx=(20, 8), pady=20)

        form_area = Frame(self.root, bg=BG)
        form_area.grid(row=0, column=1, sticky="nsew", padx=(8, 20), pady=20)
        form_area.grid_rowconfigure(0, weight=1)
        form_area.grid_columnconfigure(0, weight=1)

        # -------------------- Left branding panel: same language as Login --------------------
        Frame(visual, bg=PINK, width=175, height=175).place(
            relx=0.90, rely=-0.08, anchor="ne"
        )
        Frame(visual, bg=BLUE, width=135, height=135).place(
            relx=-0.05, rely=0.90, anchor="sw"
        )
        Frame(visual, bg="#60A5FA", width=76, height=76).place(
            relx=0.12, rely=0.10
        )
        Frame(visual, bg="#F9A8D4", width=60, height=60).place(
            relx=0.80, rely=0.80
        )

        visual_content = Frame(visual, bg=BLUE_DARK)
        visual_content.place(relx=0.12, rely=0.16, relwidth=0.76, relheight=0.70)

        Label(
            visual_content,
            text="FACE RECOGNITION",
            bg=BLUE_DARK,
            fg="#BFDBFE",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        Label(
            visual_content,
            text="Attendance\nSystem",
            bg=BLUE_DARK,
            fg=WHITE,
            font=("Segoe UI", 32, "bold"),
            justify="left",
        ).pack(anchor="w", pady=(10, 8))

        Label(
            visual_content,
            text="Smart student management,\nface recognition and attendance tracking.",
            bg=BLUE_DARK,
            fg="#CBD5E1",
            font=("Segoe UI", 11),
            justify="left",
        ).pack(anchor="w")

        feature = Frame(visual_content, bg="#1E3A8A")
        feature.pack(fill="x", pady=(38, 0))

        Label(
            feature,
            text="SECURE  •  SIMPLE  •  CONNECTED",
            bg="#1E3A8A",
            fg="#DBEAFE",
            font=("Segoe UI", 8, "bold"),
            padx=14,
            pady=11,
        ).pack(anchor="w")

        Label(
            visual_content,
            text="Face Recognition Attendance System",
            bg=BLUE_DARK,
            fg="#93C5FD",
            font=("Segoe UI", 8),
        ).pack(anchor="w", side="bottom", pady=(18, 0))

        # -------------------- Full-width register form --------------------
        card = Frame(
            form_area,
            bg=WHITE,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        card.grid(row=0, column=0, sticky="nsew", pady=18)
        card.grid_columnconfigure(0, weight=1)

        Frame(card, bg=PINK, height=5).grid(
            row=0, column=0, sticky="ew"
        )

        inner = Frame(card, bg=WHITE)
        inner.grid(row=1, column=0, sticky="nsew", padx=30, pady=26)
        inner.grid_rowconfigure(2, weight=1)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=1)

        Label(
            inner,
            text="Create your account",
            bg=WHITE,
            fg=BLUE_DARK,
            font=("Segoe UI", 22, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        Label(
            inner,
            text="Register an account to access the attendance system.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 17))

        left = Frame(inner, bg=WHITE)
        left.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
        right = Frame(inner, bg=WHITE)
        right.grid(row=2, column=1, sticky="nsew", padx=(8, 0))

        left.grid_columnconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        def field_label(parent, text, row):
            Label(
                parent,
                text=text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 8, "bold"),
            ).grid(row=row, column=0, sticky="w", pady=(0, 4))

        field_label(left, "FIRST NAME", 0)
        ttk.Entry(left, textvariable=self.var_fname, style="Reg.TEntry").grid(
            row=1, column=0, sticky="ew", pady=(0, 9)
        )

        field_label(left, "LAST NAME", 2)
        ttk.Entry(left, textvariable=self.var_lname, style="Reg.TEntry").grid(
            row=3, column=0, sticky="ew", pady=(0, 9)
        )

        field_label(left, "CONTACT NUMBER", 4)
        ttk.Entry(left, textvariable=self.var_cnum, style="Reg.TEntry").grid(
            row=5, column=0, sticky="ew", pady=(0, 9)
        )

        field_label(left, "EMAIL ADDRESS", 6)
        self.txtemail = ttk.Entry(
            left, textvariable=self.var_email, style="Reg.TEntry"
        )
        self.txtemail.grid(row=7, column=0, sticky="ew", pady=(0, 9))
        self.var_email.set("example@gmail.com")
        self.txtemail.bind("<FocusIn>", self.on_email_focus_in)
        self.txtemail.bind("<FocusOut>", self.on_email_focus_out)

        field_label(left, "SECURITY QUESTION", 8)
        self.combo_security = ttk.Combobox(
            left,
            textvariable=self.var_ssq,
            values=("Select", "Your Date of Birth", "Your Nick Name", "Your Favorite Book"),
            state="readonly",
            style="Reg.TCombobox",
        )
        self.combo_security.grid(row=9, column=0, sticky="ew", pady=(0, 9))
        self.combo_security.current(0)

        field_label(left, "SECURITY ANSWER", 10)
        ttk.Entry(left, textvariable=self.var_sa, style="Reg.TEntry").grid(
            row=11, column=0, sticky="ew"
        )

        field_label(right, "PASSWORD", 0)
        self.txtpwd = ttk.Entry(
            right, textvariable=self.var_pwd, style="Reg.TEntry", show="*"
        )
        self.txtpwd.grid(row=1, column=0, sticky="ew", pady=(0, 4))

        Label(
            right,
            text="Minimum 8 characters, including a number and a symbol.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8),
        ).grid(row=2, column=0, sticky="w", pady=(0, 10))

        field_label(right, "CONFIRM PASSWORD", 3)
        self.txtcpwd = ttk.Entry(
            right, textvariable=self.var_cpwd, style="Reg.TEntry", show="*"
        )
        self.txtcpwd.grid(row=4, column=0, sticky="ew", pady=(0, 8))

        Checkbutton(
            right,
            variable=self.var_showpwd,
            text="Show password",
            font=("Segoe UI", 8),
            fg=TEXT,
            bg=WHITE,
            activebackground=WHITE,
            selectcolor=WHITE,
            command=self.toggle_password,
        ).grid(row=5, column=0, sticky="w", pady=(0, 14))

        Label(
            right,
            text="ACCOUNT AGREEMENT",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 8, "bold"),
        ).grid(row=6, column=0, sticky="w", pady=(0, 7))

        Checkbutton(
            right,
            variable=self.var_check,
            text="I agree to the Terms & Conditions",
            font=("Segoe UI", 8),
            fg=TEXT,
            bg=WHITE,
            activebackground=WHITE,
            selectcolor=WHITE,
        ).grid(row=7, column=0, sticky="w")

        ttk.Button(
            right,
            text="Register",
            command=self.reg,
            style="Reg.Primary.TButton",
        ).grid(row=8, column=0, sticky="ew", pady=(18, 7))

        ttk.Button(
            right,
            text="Back to Login",
            command=self.open_login,
            style="Reg.Secondary.TButton",
        ).grid(row=9, column=0, sticky="ew")

        Label(
            card,
            text="Your registration details are stored in the application's database.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8),
        ).grid(row=2, column=0, sticky="w", padx=34, pady=(0, 16))

    def on_email_focus_in(self, event):
        """Clear placeholder text when entry gets focus"""
        if self.var_email.get() == "example@gmail.com":
            self.var_email.set("")

    def on_email_focus_out(self, event):
        """Restore placeholder text if field is empty"""
        if self.var_email.get() == "":
            self.var_email.set("example@gmail.com")

    def toggle_password(self):
        """Toggle between showing and hiding passwords"""
        if self.var_showpwd.get():
            self.txtpwd.config(show="")
            self.txtcpwd.config(show="")
        else:
            self.txtpwd.config(show="*")
            self.txtcpwd.config(show="*")

    def validate_email(self, email):
        """Validate email format and check for @gmail.com"""
        # Check if email ends with @gmail.com
        if not email.endswith("@gmail.com"):
            return False

        # Check for basic email format using regex
        pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
        if not re.match(pattern, email):
            return False

        return True

    def validate_password(self, password):
        """Validate password strength"""
        # Check length
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        # Check for at least one digit
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one number"

        # Check for at least one special character
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in password):
            return False, "Password must contain at least one special character"

        return True, "Password is valid"

    def open_login(self):
        # Close the current Register window
        self.root.destroy()

        # Import Login class from login.py
        from login import Login

        # Create new Login window
        root=Tk()
        app=Login(root)
        root.mainloop()

    def reg(self):
        # Get values and strip whitespace
        fname = self.var_fname.get().strip()
        lname = self.var_lname.get().strip()
        cnum = self.var_cnum.get().strip()
        email = self.var_email.get().strip()
        ssq = self.var_ssq.get()
        sa = self.var_sa.get().strip()
        pwd = self.var_pwd.get()
        cpwd = self.var_cpwd.get()

        # 1. First Name
        if fname == "":
            messagebox.showerror("Error", "First Name is required.\nPlease enter your first name.", parent=self.root)
            return

        # 2. Last Name
        if lname == "":
            messagebox.showerror("Error", "Last Name is required.\nPlease enter your last name.", parent=self.root)
            return

        # 3. Contact Number
        if cnum == "":
            messagebox.showerror("Error", "Contact Number is required.\nPlease enter a valid contact number.", parent=self.root)
            return
        if not cnum.isdigit() or len(cnum) < 10:
            messagebox.showerror("Error", "Invalid Contact Number.\nPlease enter digits only and use a valid phone number.", parent=self.root)
            return

        # 4. Email
        if email == "" or email == "example@gmail.com":
            messagebox.showerror("Error", "Email Address is required.\nPlease enter your Gmail address.", parent=self.root)
            self.txtemail.focus_set()
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid Email Address.\nPlease enter a valid Gmail address in this format:\nexample@gmail.com", parent=self.root)
            self.txtemail.focus_set()
            return

        # 5. Security Question
        if ssq == "Select":
            messagebox.showerror("Error", "Security Question is required.\nPlease select a security question.", parent=self.root)
            self.combo_security.focus_set()
            return

        # 6. Security Answer
        if sa == "":
            messagebox.showerror("Error", "Security Answer is required.\nPlease enter an answer.", parent=self.root)
            return

        # 7. Password
        if pwd == "":
            messagebox.showerror("Error", "Password is required.\nPlease enter a password.", parent=self.root)
            self.txtpwd.focus_set()
            return

        if len(pwd) < 8:
            messagebox.showerror("Error", "Password is too short.\nIt must contain at least 8 characters.", parent=self.root)
            self.txtpwd.focus_set()
            return

        if not any(char.isdigit() for char in pwd):
            messagebox.showerror("Error", "Password is invalid.\nIt must contain at least one number.", parent=self.root)
            self.txtpwd.focus_set()
            return

        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in pwd):
            messagebox.showerror("Error", "Password is invalid.\nIt must contain at least one special character.", parent=self.root)
            self.txtpwd.focus_set()
            return

        # 8. Confirm Password
        if cpwd == "":
            messagebox.showerror("Error", "Confirm Password is required.\nPlease re-enter your password.", parent=self.root)
            self.txtcpwd.focus_set()
            return

        if pwd != cpwd:
            messagebox.showerror("Error", "Passwords do not match.\nConfirm Password must exactly match Password.", parent=self.root)
            self.txtcpwd.focus_set()
            return

        # 9. Terms & Conditions
        if self.var_check.get() == 0:
            messagebox.showerror("Error", "Terms & Conditions are required.\nPlease check the agreement before registering.", parent=self.root)
            return

        # Database operations
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            mycursor = conn.cursor()

            # 10. Database duplicate-email check
            query=("select * from regteach where BINARY email = BINARY %s")
            value=(email,)
            mycursor.execute(query,value)
            row=mycursor.fetchone()

            if row!=None:
                messagebox.showerror("Error","This email is already registered.\nPlease use a different email address or return to Login.", parent=self.root)
                self.txtemail.focus_set()
            else:
                # 11. Database insertion
                mycursor.execute("insert into regteach values(%s,%s,%s,%s,%s,%s,%s)",(
                fname,
                lname,
                cnum,
                email,
                ssq,
                sa,
                pwd
                ))

                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Registration Successful!\nYour account has been created. You can now log in.", parent=self.root)

                # Navigate to login
                self.open_login()

        except Exception as es:
            messagebox.showerror("Error",f"Registration could not be completed.\nPlease check the database connection and try again.\n\nDetails: {str(es)}", parent=self.root)

if __name__ == "__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()