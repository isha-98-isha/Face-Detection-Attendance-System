import os
from ui.theme import COLORS, apply_theme, FONTS
from ui.components import *
from ui.icons import ICONS
from ui.assets import get_image_path, load_image, BASE_DIR
import calendar
from datetime import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from db_config import DB_CONFIG, owner_data_dir

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")

class Student:
    def __init__(self, root, authenticated=False, owner_email=None, owner_name=""):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.owner_email = owner_email
        self.owner_name = owner_name
        self.data_dir = owner_data_dir(owner_email)
        self.root.title("Student Management • Face Recognition Attendance System")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 700)
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # Modern light theme
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

        self.root.configure(bg=BG)

        # -------------------- Variables --------------------
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_mob = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_teacher.set(self.owner_name)
        self.var_radio1 = StringVar()
        self.var_searchTX = StringVar(value="Select")
        self.var_search = StringVar()
        self.selected_student_id = None

        # -------------------- ttk styles --------------------
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Modern.TEntry",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=(10, 8),
            font=("Segoe UI", 10),
        )
        style.map(
            "Modern.TEntry",
            bordercolor=[("focus", BLUE)],
            lightcolor=[("focus", BLUE)],
        )

        style.configure(
            "Modern.TCombobox",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=(8, 7),
            font=("Segoe UI", 10),
        )

        style.configure(
            "Primary.TButton",
            background=BLUE,
            foreground=WHITE,
            borderwidth=0,
            focusthickness=0,
            padding=(16, 9),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
            foreground=[("disabled", "#CBD5E1")],
        )

        style.configure(
            "Accent.TButton",
            background=PINK,
            foreground=WHITE,
            borderwidth=0,
            focusthickness=0,
            padding=(16, 9),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", "#DB2777"), ("pressed", "#BE185D")],
        )

        style.configure(
            "Danger.TButton",
            background=DANGER,
            foreground=WHITE,
            borderwidth=0,
            focusthickness=0,
            padding=(16, 9),
            font=("Segoe UI", 10, "bold"),
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

        style.configure(
            "Modern.Treeview",
            background=WHITE,
            foreground=TEXT,
            fieldbackground=WHITE,
            bordercolor=BORDER,
            rowheight=34,
            font=("Segoe UI", 9),
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", DARK_BLUE)],
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=DARK_BLUE,
            foreground=WHITE,
            bordercolor=DARK_BLUE,
            relief="flat",
            padding=(8, 8),
            font=("Segoe UI", 9, "bold"),
        )
        style.map(
            "Modern.Treeview.Heading",
            background=[("active", "#1E3A8A")],
        )

        # -------------------- Root layout --------------------
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # -------------------- Header --------------------
        header = Frame(self.root, bg=WHITE, height=82, bd=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        try:
            _logo = Image.open(os.path.join(IMAGE_DIR, "Face-Recognition-Software.png"))
            _logo = _logo.resize((44, 44), Image.LANCZOS)
            self._hdr_logo = ImageTk.PhotoImage(_logo)
            brand_mark = Label(header, image=self._hdr_logo, bg=WHITE)
            brand_mark.grid(row=0, column=0, padx=(24, 14), pady=17)
        except Exception:
            brand_mark = Frame(
                header,
                bg=BLUE,
                width=48,
                height=48,
                highlightthickness=0,
            )
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
        brand_area.grid(row=0, column=1, sticky="ew", pady=13)
        brand_area.grid_columnconfigure(0, weight=1)

        Label(
            brand_area,
            text="Face Recognition Attendance System",
            bg=WHITE,
            fg=DARK_BLUE,
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        Label(
            brand_area,
            text="Student management",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 10),
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        ttk.Button(header, text="Back to Dashboard", command=self.go_back,
                   style="Secondary.TButton").grid(
                       row=0, column=2, padx=(10, 24), pady=19)

        header_rule = Frame(self.root, bg=BORDER, height=1)
        header_rule.grid(row=0, column=0, sticky="ews")

        # -------------------- Main content --------------------
        content = Frame(self.root, bg=BG)
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=18)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=4, uniform="content")
        content.grid_columnconfigure(1, weight=6, uniform="content")

        # Card helpers
        def create_card(parent, row, column, padx=8, pady=0):
            outer = Frame(parent, bg=BORDER, bd=0, highlightthickness=0)
            outer.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=padx,
                pady=pady,
            )
            inner = Frame(outer, bg=WHITE, bd=0, highlightthickness=0)
            inner.pack(fill=BOTH, expand=True, padx=1, pady=1)
            return inner

        # -------------------- Left side --------------------
        left = Frame(content, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        left.grid_rowconfigure(1, weight=0)
        left.grid_rowconfigure(2, weight=1)
        left.grid_columnconfigure(0, weight=1)

        title_card = create_card(left, 0, 0, padx=0, pady=(0, 12))
        title_card.grid_columnconfigure(0, weight=1)

        title_text = Frame(title_card, bg=WHITE)
        title_text.grid(row=0, column=0, sticky="ew", padx=22, pady=17)
        title_text.grid_columnconfigure(0, weight=1)

        Label(
            title_text,
            text="Student Information",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        Label(
            title_text,
            text="Create and manage student profiles",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
            anchor="w",
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

        # Course card
        course_card = create_card(left, 1, 0, padx=0, pady=(0, 12))
        course_card.grid_columnconfigure(0, weight=1)

        Label(
            course_card,
            text="CURRENT COURSE",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8))

        current_course_frame = Frame(course_card, bg=WHITE)
        current_course_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 16))
        for col in range(4):
            current_course_frame.grid_columnconfigure(col, weight=1, uniform="course")

        course_fields = [
            ("Department", self.var_dep, ("Select Department", "CGPIT", "AMTICS", "SHRIMCA", "SRCP", "BMIIT"), 0),
            ("Course", self.var_course, ("Select Course", "CSE", "ME", "CS", "CE", "IT"), 1),
            ("Year", self.var_year, ("Select Year", "2018-22", "2019-23", "2020-24", "2021-25", "2022-26"), 2),
            ("Semester", self.var_semester, ("Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4", "Semester-5", "Semester-6", "Semester-7", "Semester-8"), 3),
        ]

        for label_text, variable, values, col in course_fields:
            field = Frame(current_course_frame, bg=WHITE)
            field.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 8, 0))
            field.grid_columnconfigure(0, weight=1)

            Label(
                field,
                text=label_text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            ).grid(row=0, column=0, sticky="w", pady=(0, 5))

            combo = ttk.Combobox(
                field,
                textvariable=variable,
                values=values,
                state="readonly",
                style="Modern.TCombobox",
            )
            combo.grid(row=1, column=0, sticky="ew")
            combo.current(0)

        # Details card
        details_card = create_card(left, 2, 0, padx=0, pady=0)
        details_card.grid_rowconfigure(1, weight=1)
        details_card.grid_columnconfigure(0, weight=1)

        Label(
            details_card,
            text="STUDENT DETAILS",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8))

        form = Frame(details_card, bg=WHITE)
        form.grid(row=1, column=0, sticky="nsew", padx=18)
        for col in range(4):
            form.grid_columnconfigure(col, weight=1, uniform="details")

        fields = [
            ("Student ID", self.var_std_id, 0, 0),
            ("Student Name", self.var_std_name, 0, 2),
            ("Roll No", self.var_roll, 1, 0),
            ("Class Division", self.var_div, 1, 2),
            ("Gender", self.var_gender, 2, 0),
            ("Date of Birth", self.var_dob, 2, 2),
            ("Email", self.var_email, 3, 0),
            ("Mobile No", self.var_mob, 3, 2),
            ("Address", self.var_address, 4, 0),
            ("Tutor Name", self.var_teacher, 4, 2),
        ]

        def add_entry(parent, label_text, variable, row, col, combo_values=None):
            block = Frame(parent, bg=WHITE)
            block.grid(row=row, column=col, sticky="ew", padx=(0 if col == 0 else 8, 8), pady=(0, 10))
            block.grid_columnconfigure(0, weight=1)

            Label(
                block,
                text=label_text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            ).grid(row=0, column=0, sticky="w", pady=(0, 5))

            if combo_values is not None:
                widget = ttk.Combobox(
                    block,
                    textvariable=variable,
                    values=combo_values,
                    state="readonly",
                    style="Modern.TCombobox",
                )
                widget.current(0)
            elif label_text == "Date of Birth":
                date_field = Frame(block, bg=WHITE)
                date_field.grid(row=1, column=0, sticky="ew")
                date_field.grid_columnconfigure(0, weight=1)
                widget = ttk.Entry(date_field, textvariable=variable, style="Modern.TEntry")
                widget.grid(row=0, column=0, sticky="ew")
                self.dob_button = ttk.Button(date_field, text="\U0001F4C5", command=self.choose_birth_date,
                           style="Secondary.TButton", width=3)
                self.dob_button.grid(row=0, column=1, padx=(5, 0))
                return widget
            elif label_text == "Tutor Name":
                widget = ttk.Entry(
                    block,
                    textvariable=variable,
                    style="Modern.TEntry",
                    state="readonly",
                )
            else:
                widget = ttk.Entry(block, textvariable=variable, style="Modern.TEntry")

            widget.grid(row=1, column=0, sticky="ew")
            return widget

        for label_text, variable, row, col in fields:
            if label_text == "Class Division":
                add_entry(form, label_text, variable, row, col, ("select", "A", "B", "C"))
            elif label_text == "Gender":
                add_entry(form, label_text, variable, row, col, ("select", "Male", "Female", "Others"))
            else:
                add_entry(form, label_text, variable, row, col)

        # Radio buttons
        photo_row = Frame(form, bg=WHITE)
        photo_row.grid(row=5, column=0, columnspan=4, sticky="w", pady=(1, 8))

        Label(
            photo_row,
            text="Photo Sample",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 9, "bold"),
        ).pack(side=LEFT, padx=(0, 14))

        ttk.Radiobutton(
            photo_row,
            text="Take Photo Sample",
            variable=self.var_radio1,
            value="Yes",
        ).pack(side=LEFT, padx=(0, 14))

        ttk.Radiobutton(
            photo_row,
            text="No Photo Sample",
            variable=self.var_radio1,
            value="No",
        ).pack(side=LEFT)

        # Action buttons
        button_bar = Frame(details_card, bg=WHITE)
        button_bar.grid(row=2, column=0, sticky="ew", padx=18, pady=(8, 18))
        for col in range(3):
            button_bar.grid_columnconfigure(col, weight=1, uniform="actions")

        ttk.Button(
            button_bar,
            text="Save",
            command=self.add_data,
            style="Primary.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ttk.Button(
            button_bar,
            text="Reset",
            command=self.reset_data,
            style="Secondary.TButton",
        ).grid(row=0, column=1, sticky="ew", padx=6)

        ttk.Button(
            button_bar,
            text="Take Photo",
            command=self.generate_dataset,
            style="Accent.TButton",
        ).grid(row=0, column=2, sticky="ew", padx=6)

        # -------------------- Right side --------------------
        right = Frame(content, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        right.grid_rowconfigure(1, weight=1)
        right.grid_rowconfigure(2, weight=0)
        right.grid_columnconfigure(0, weight=1)

        search_card = create_card(right, 0, 0, padx=0, pady=(0, 12))
        search_card.grid_columnconfigure(1, weight=1)

        Label(
            search_card,
            text="SEARCH STUDENTS",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=18, pady=(14, 8))

        search_combo = ttk.Combobox(
            search_card,
            textvariable=self.var_searchTX,
            values=("Select", "Date", "Student ID", "Name", "Roll-No", "Mobile No", "Gender", "Course", "Department"),
            state="readonly",
            style="Modern.TCombobox",
            width=14,
        )
        search_combo.grid(row=1, column=0, padx=(18, 8), pady=(0, 14))
        search_combo.current(0)
        search_combo.bind("<<ComboboxSelected>>", self.update_search_controls)

        search_entry = ttk.Entry(
            search_card,
            textvariable=self.var_search,
            style="Modern.TEntry",
        )
        search_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=(0, 14))

        self.search_date_button = ttk.Button(
            search_card, text="\U0001F4C5", command=self.choose_search_date,
            style="Secondary.TButton")
        self.search_date_button.grid(row=1, column=2, padx=(0, 6), pady=(0, 14))
        self.search_date_button.grid_remove()

        ttk.Button(
            search_card,
            text="Search",
            command=self.search_data,
            style="Primary.TButton",
        ).grid(row=1, column=3, padx=8, pady=(0, 14))

        ttk.Button(
            search_card,
            text="Show All",
            command=self.fetch_data,
            style="Secondary.TButton",
        ).grid(row=1, column=4, padx=(8, 18), pady=(0, 14))

        table_card = create_card(right, 1, 0, padx=0, pady=0)
        table_card.grid_rowconfigure(1, weight=1)
        table_card.grid_columnconfigure(0, weight=1)

        table_title = Frame(table_card, bg=WHITE)
        table_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 10))

        Label(
            table_title,
            text="STUDENT RECORDS",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).pack(side=LEFT)

        Label(
            table_title,
            text="Click a row to load its details",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(side=RIGHT)

        table_area = Frame(table_card, bg=WHITE)
        table_area.grid(row=1, column=0, sticky="nsew", padx=(18, 18), pady=(0, 18))
        table_area.grid_rowconfigure(0, weight=1)
        table_area.grid_columnconfigure(0, weight=1)

        scroll_x = ttk.Scrollbar(table_area, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_area, orient=VERTICAL)

        columns = (
            "ID",
            "Name",
            "Dep",
            "Course",
            "Year",
            "Sem",
            "Div",
            "Gender",
            "DOB",
            "Mob-No",
            "Address",
            "Roll-No",
            "Email",
            "Teacher",
            "Photo",
        )

        self.student_table = ttk.Treeview(
            table_area,
            columns=columns,
            show="headings",
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
            style="Modern.Treeview",
        )
        self.student_table["displaycolumns"] = (
            "ID",
            "Name",
            "Roll-No",
            "Dep",
            "Course",
            "Year",
            "Sem",
            "Div",
            "Gender",
            "DOB",
            "Mob-No",
            "Address",
            "Email",
            "Teacher",
            "Photo",
        )

        scroll_x.grid(row=1, column=0, sticky="ew")
        scroll_y.grid(row=0, column=1, sticky="ns")

        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.grid(row=0, column=0, sticky="nsew")
        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        headings = {
            "ID": "Student ID",
            "Name": "Name",
            "Dep": "Department",
            "Course": "Course",
            "Year": "Year",
            "Sem": "Semester",
            "Div": "Division",
            "Gender": "Gender",
            "DOB": "DOB",
            "Mob-No": "Mobile No",
            "Address": "Address",
            "Roll-No": "Roll No",
            "Email": "Email",
            "Teacher": "Teacher",
            "Photo": "Photo Sample",
        }

        widths = {
            "ID": 100,
            "Name": 140,
            "Dep": 125,
            "Course": 110,
            "Year": 105,
            "Sem": 110,
            "Div": 90,
            "Gender": 95,
            "DOB": 105,
            "Mob-No": 120,
            "Address": 180,
            "Roll-No": 105,
            "Email": 190,
            "Teacher": 140,
            "Photo": 115,
        }

        for column in columns:
            self.student_table.heading(column, text=headings[column])
            anchor_val = "center" if column == "Name" else "w"
            self.student_table.column(column, width=widths[column], minwidth=80, stretch=False, anchor=anchor_val)

        record_actions = Frame(right, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        record_actions.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        record_actions.grid_columnconfigure(0, weight=1)
        record_actions.grid_columnconfigure(1, weight=1)
        ttk.Button(record_actions, text="Update Record", command=self.update_data,
                   style="Primary.TButton").grid(row=0, column=0, sticky="ew", padx=(18, 6), pady=14)
        ttk.Button(record_actions, text="Delete Record", command=self.delete_data,
                   style="Danger.TButton").grid(row=0, column=1, sticky="ew", padx=(6, 18), pady=14)

        # Load existing records exactly as before
        self.fetch_data()

    def go_back(self):
        self.root.destroy()
    def choose_birth_date(self):
        self._choose_date(self.var_dob, "Select date of birth", getattr(self, 'dob_button', None))

    def choose_search_date(self):
        self.var_searchTX.set("Date")
        self.update_search_controls()
        self._choose_date(self.var_search, "Select search date", getattr(self, 'search_date_button', None))

    def update_search_controls(self, event=None):
        if self.var_searchTX.get() == "Date":
            self.search_date_button.grid()
        else:
            self.search_date_button.grid_remove()

    def _choose_date(self, target, title, btn_widget=None):
        from tkcalendar import Calendar
        picker = Toplevel(self.root)
        picker.title(title)
        picker.transient(self.root)
        picker.grab_set()
        
        cal = Calendar(picker, selectmode='day', date_pattern='dd-mm-yyyy')
        cal.pack(padx=2, pady=2, fill="both", expand=True)
        
        def select_day():
            target.set(cal.get_date())
            picker.destroy()
            
        btn_frame = Frame(picker, bg=COLORS["border"])
        btn_frame.pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="Select", command=select_day, style="Primary.TButton").pack(side="left", expand=True, padx=2)
        ttk.Button(btn_frame, text="Cancel", command=picker.destroy, style="Secondary.TButton").pack(side="right", expand=True, padx=2)


# ==================Function Decleration==============================
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_course.get()=="Select Course" or self.var_year.get()=="Select Year" or self.var_semester.get()=="Select Semester" or self.var_std_id.get()=="" or self.var_std_name.get()=="" or self.var_div.get()=="" or self.var_div.get()=="select" or self.var_roll.get()=="" or self.var_gender.get()=="" or self.var_gender.get()=="select" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_mob.get()=="" or self.var_address.get()=="" or self.var_teacher.get()=="":
            messagebox.showerror("Error","Please Fill All Fields are Required!",parent=self.root)
        else:
            try:
                if self.var_radio1.get() == "Yes":
                    self.capture_face_samples(self.var_std_id.get())
                conn = mysql.connector.connect(**DB_CONFIG)
                mycursor = conn.cursor()
                mycursor.execute("insert into student (Student_ID,Name,Department,Course,Year,Semester,Division,Gender,DOB,Mobile_No,Address,Roll_No,Email,Teacher_Name,PhotoSample,Owner_Email) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                self.var_std_id.get(),
                self.var_std_name.get(),
                self.var_dep.get(),
                self.var_course.get(),
                self.var_year.get(),
                self.var_semester.get(),
                self.var_div.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_mob.get(),
                self.var_address.get(),
                self.var_roll.get(),
                self.var_email.get(),
                self.var_teacher.get(),
                self.var_radio1.get(),
                self.owner_email,
                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Record Saved!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)

    # ===========================Fetch data form database to table ================================

    def fetch_data(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        mycursor = conn.cursor()

        mycursor.execute("select Student_ID,Name,Department,Course,Year,Semester,Division,Gender,DOB,Mobile_No,Address,Roll_No,Email,Teacher_Name,PhotoSample from student where Owner_Email=%s", (self.owner_email,))
        data=mycursor.fetchall()

        self.student_table.delete(*self.student_table.get_children())
        for i in data:
            self.student_table.insert("",END,values=i)
        conn.close()

    #================================get cursor function=======================

    def get_cursor(self,event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        if len(data) < 15:
            return

        self.var_std_id.set(data[0]),
        self.var_std_name.set(data[1]),
        self.var_dep.set(data[2]),
        self.var_course.set(data[3]),
        self.var_year.set(data[4]),
        self.var_semester.set(data[5]),
        self.var_div.set(data[6]),
        self.var_gender.set(data[7]),
        self.var_dob.set(data[8]),
        self.var_mob.set(data[9]),
        self.var_address.set(data[10]),
        self.var_roll.set(data[11]),
        self.var_email.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio1.set(data[14])
        self.selected_student_id = data[0]
    # ========================================Update Function==========================
    def update_data(self):
        if self.var_dep.get()=="Select Department" or self.var_course.get()=="Select Course" or self.var_year.get()=="Select Year" or self.var_semester.get()=="Select Semester" or self.var_std_id.get()=="" or self.var_std_name.get()=="" or self.var_div.get()=="" or self.var_div.get()=="select" or self.var_roll.get()=="" or self.var_gender.get()=="" or self.var_gender.get()=="select" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_mob.get()=="" or self.var_address.get()=="" or self.var_teacher.get()=="":
            messagebox.showerror("Error","Please Fill All Fields are Required!",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to Update this Student Details!",parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    mycursor = conn.cursor()
                    mycursor.execute("update student set Name=%s,Department=%s,Course=%s,Year=%s,Semester=%s,Division=%s,Gender=%s,DOB=%s,Mobile_No=%s,Address=%s,Roll_No=%s,Email=%s,Teacher_Name=%s,PhotoSample=%s where Student_ID=%s and Owner_Email=%s",( 
                    self.var_std_name.get(),
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_div.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_mob.get(),
                    self.var_address.get(),
                    self.var_roll.get(),
                    self.var_email.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    self.var_std_id.get(),
                    self.owner_email,
                    ))
                else:
                    if not Update:
                        return
                if self.var_radio1.get() == "Yes":
                    self.capture_face_samples(self.var_std_id.get())
                messagebox.showinfo("Success","Successfully Updated!",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    
    #==============================Delete Function=========================================
    def delete_data(self):
        selected = self.student_table.selection()
        student_id = None
        if selected:
            values = self.student_table.item(selected[0], "values")
            if values:
                student_id = values[0]
        if not student_id:
            student_id = self.selected_student_id or self.var_std_id.get()
        if not student_id:
            messagebox.showerror("Error", "Select a student record first.", parent=self.root)
            return

        if not messagebox.askyesno("Delete", "Do you want to delete this student?", parent=self.root):
            return

        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM student WHERE Student_ID=%s AND Owner_Email=%s",
                (student_id, self.owner_email),
            )
            deleted = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            if deleted == 0:
                messagebox.showwarning(
                    "Not deleted",
                    "The selected student was not found for this account.",
                    parent=self.root,
                )
                return
            self.fetch_data()
            self.reset_data()
            messagebox.showinfo("Delete", "Student deleted successfully.", parent=self.root)
        except Exception as error:
            messagebox.showerror("Error", f"Due to: {error}", parent=self.root)

    # Reset Function 
    def reset_data(self):
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_dep.set("Select Department"),
        self.var_course.set("Select Course"),
        self.var_year.set("Select Year"),
        self.var_semester.set("Select Semester"),
        self.var_div.set("Morning"),
        self.var_gender.set("Male"),
        self.var_dob.set(""),
        self.var_mob.set(""),
        self.var_address.set(""),
        self.var_roll.set(""),
        self.var_email.set(""),
        self.var_teacher.set(self.owner_name),
        self.var_radio1.set("")
    
    # ===========================Search Data===================
    def search_data(self):
        if self.var_search.get()=="" or self.var_searchTX.get()=="Select":
            messagebox.showerror("Error","Select Combo option and enter entry box",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                my_cursor = conn.cursor()
                search_columns = {
                    "Date": "DOB",
                    "Student ID": "Student_ID",
                    "Name": "Name",
                    "Roll-No": "Roll_No",
                    "Mobile No": "Mobile_No",
                    "Gender": "Gender",
                    "Course": "Course",
                    "Department": "Department",
                }
                search_column = search_columns[self.var_searchTX.get()]
                search_value = self.var_search.get().strip()
                if self.var_searchTX.get() == "Date":
                    sql = f"SELECT Student_ID,Name,Department,Course,Year,Semester,Division,Gender,DOB,Mobile_No,Address,Roll_No,Email,Teacher_Name,PhotoSample FROM student WHERE {search_column} IN (%s, %s) AND Owner_Email=%s"
                    my_cursor.execute(sql, (search_value, search_value.replace("-", "/"), self.owner_email))
                else:
                    sql = f"SELECT Student_ID,Name,Department,Course,Year,Semester,Division,Gender,DOB,Mobile_No,Address,Roll_No,Email,Teacher_Name,PhotoSample FROM student WHERE {search_column}=%s AND Owner_Email=%s"
                    my_cursor.execute(sql, (search_value, self.owner_email))
                # my_cursor.execute("select * from student where Roll_No= " +str(self.var_search.get())+" "+str(self.var_searchTX.get())+"")
                rows=my_cursor.fetchall()        
                if len(rows)!=0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in rows:
                        self.student_table.insert("",END,values=i)
                    if rows==None:
                        messagebox.showerror("Error","Data Not Found",parent=self.root)
                        conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To :{str(es)}",parent=self.root)


#=====================This part is related to Opencv Camera part=======================
# ==================================Generate Data set take image=========================
    def generate_dataset(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Select or save a student before taking photos.", parent=self.root)
            return
        try:
            self.capture_face_samples(self.var_std_id.get())
            self.var_radio1.set("Yes")
            messagebox.showinfo("Result", "Face samples captured successfully.", parent=self.root)
        except Exception as error:
            messagebox.showerror("Camera error", str(error), parent=self.root)

    def capture_face_samples(self, student_id):
        detector = cv2.CascadeClassifier(
            os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
        )
        if detector.empty():
            raise RuntimeError("Face detector file could not be loaded.")
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError("Camera could not be opened.")

        image_id = 0
        try:
            while True:
                ok, frame = camera.read()
                if not ok:
                    raise RuntimeError("Camera frame could not be read.")
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                if len(faces):
                    x, y, width, height = faces[0]
                    image_id += 1
                    face = cv2.resize(gray[y:y + height, x:x + width], (200, 200))
                    cv2.imwrite(os.path.join(
                        self.data_dir, f"stdudent.{student_id}.{image_id}.jpg"), face)
                    cv2.putText(face, str(image_id), (50, 50),
                                cv2.FONT_HERSHEY_COMPLEX, 2, 255, 2)
                    cv2.imshow("Capture Images", face)
                if cv2.waitKey(1) == 13 or image_id >= 100:
                    break
        finally:
            camera.release()
            cv2.destroyAllWindows()
        if image_id == 0:
            raise RuntimeError("No face was detected. No samples were captured.")


# main class object

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()
