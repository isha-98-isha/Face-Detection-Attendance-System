import re
from sys import path
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
import mysql.connector
import pymysql
pymysql.install_as_MySQLdb()
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
import calendar
import csv
from tkinter import filedialog
from db_config import DB_CONFIG

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")

# Global variable for importCsv Function
mydata = []


class Attendance:
    def __init__(self, root, authenticated=False, owner_email=None):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.owner_email = owner_email
        self.root.title("Attendance Management • Face Recognition Attendance System")
        self.root.geometry("1280x780")
        self.root.minsize(1050, 680)
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # -------------------- Design system --------------------
        BG = "#F7F9FC"
        WHITE = "#FFFFFF"
        BLUE = "#2563EB"
        DARK_BLUE = "#172554"
        PINK = "#EC4899"
        TEXT = "#1E293B"
        MUTED = "#64748B"
        BORDER = "#E2E8F0"
        SOFT_BLUE = "#EFF6FF"
        SOFT_PINK = "#FDF2F8"
        DANGER = "#DC2626"

        self.root.configure(bg=BG)

        # -------------------- Variables --------------------
        self.var_id = StringVar()
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_dep = StringVar()
        self.var_time = StringVar()
        self.var_date = StringVar()
        self.var_attend = StringVar(value="Status")
        self.var_search_type = StringVar(value="Select field")
        self.var_search_value = StringVar()
        self.selected_record = None

        # -------------------- ttk styles --------------------
        style = ttk.Style(self.root)
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
            darkcolor=[("focus", BLUE)],
        )

        style.configure(
            "Modern.TCombobox",
            fieldbackground=WHITE,
            background=WHITE,
            foreground=TEXT,
            arrowcolor=BLUE,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=(8, 7),
            font=("Segoe UI", 10),
        )
        style.map(
            "Modern.TCombobox",
            fieldbackground=[("readonly", WHITE)],
            bordercolor=[("focus", BLUE)],
            lightcolor=[("focus", BLUE)],
            darkcolor=[("focus", BLUE)],
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

        style.configure(
            "Modern.Horizontal.TScrollbar",
            troughcolor="#EEF2F7",
            background="#CBD5E1",
            bordercolor="#EEF2F7",
            arrowcolor=DARK_BLUE,
        )
        style.configure(
            "Modern.Vertical.TScrollbar",
            troughcolor="#EEF2F7",
            background="#CBD5E1",
            bordercolor="#EEF2F7",
            arrowcolor=DARK_BLUE,
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
            text="Attendance management",
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

        # -------------------- Main content --------------------
        content = Frame(self.root, bg=BG)
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=18)
        content.grid_rowconfigure(0, weight=0)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1, uniform="content")
        content.grid_columnconfigure(1, weight=1, uniform="content")

        # Intro
        intro_left = Frame(content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        intro_left.grid(row=0, column=0, sticky="ew", padx=(0, 7), pady=(0, 14))
        intro_left.grid_columnconfigure(0, weight=1)

        Label(
            intro_left,
            text="Attendance records",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(13, 0))

        Label(
            intro_left,
            text="Review, update, import and export attendance records.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", padx=18, pady=(1, 13))

        intro_right = Frame(content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        intro_right.grid(row=0, column=1, sticky="ew", padx=(7, 0), pady=(0, 14))

        Label(
            intro_right,
            text="DATABASE ATTENDANCE",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=18, pady=(14, 3))

        Label(
            intro_right,
            text="Select a record to manage it from the form.",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=18, pady=(0, 13))

        search_panel = Frame(intro_right, bg=WHITE)
        search_panel.pack(fill=X, padx=18, pady=(0, 13))
        search_panel.grid_columnconfigure(1, weight=1)
        self.search_type_combo = ttk.Combobox(
            search_panel,
            textvariable=self.var_search_type,
            values=("Select field", "Date", "Student Name", "Roll No", "Student ID"),
            state="readonly",
            width=16,
            style="Modern.TCombobox",
        )
        self.search_type_combo.grid(row=0, column=0, padx=(0, 6))
        self.search_type_combo.bind("<<ComboboxSelected>>", self.update_search_controls)
        ttk.Entry(search_panel, textvariable=self.var_search_value,
                  style="Modern.TEntry").grid(row=0, column=1, sticky="ew")
        self.search_calendar_button = ttk.Button(
            search_panel, text="\U0001F4C5", command=self.choose_search_date,
            style="Secondary.TButton")
        self.search_calendar_button.grid(row=0, column=2, padx=(6, 0))
        self.search_calendar_button.grid_remove()
        ttk.Button(search_panel, text="Search", command=self.search_records,
                   style="Primary.TButton").grid(row=0, column=3, padx=(6, 0))
        ttk.Button(search_panel, text="All", command=self.clear_search,
                   style="Secondary.TButton").grid(row=0, column=4, padx=(6, 0))

        # -------------------- Two-column workspace --------------------
        left_panel = Frame(content, bg=BG)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 7))
        right_panel = Frame(content, bg=BG)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(7, 0))

        left_panel.grid_rowconfigure(0, weight=0)
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=0)
        right_panel.grid_rowconfigure(2, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # -------------------- CSV / entry form card --------------------
        details_card = Frame(left_panel, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        details_card.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        details_card.grid_columnconfigure(0, weight=1)

        Label(
            details_card,
            text="ATTENDANCE DETAILS",
            bg=WHITE,
            fg=BLUE,
            font=("Segoe UI", 9, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(15, 10))

        form = Frame(details_card, bg=WHITE)
        form.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 16))
        for col in range(4):
            form.grid_columnconfigure(col, weight=1, uniform="attendance_form")

        def add_entry(label_text, variable, row, col, combo_values=None):
            block = Frame(form, bg=WHITE)
            block.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=(0, 8 if col == 0 else 0),
                pady=(0, 9),
            )
            block.grid_columnconfigure(0, weight=1)

            Label(
                block,
                text=label_text,
                bg=WHITE,
                fg=TEXT,
                font=("Segoe UI", 9, "bold"),
            ).grid(row=0, column=0, sticky="w", pady=(0, 4))

            if combo_values:
                widget = ttk.Combobox(
                    block,
                    textvariable=variable,
                    values=combo_values,
                    state="readonly",
                    style="Modern.TCombobox",
                )
                widget.current(0)
            elif variable == self.var_date:
                field = Frame(block, bg=WHITE)
                field.grid(row=1, column=0, sticky="ew")
                field.grid_columnconfigure(0, weight=1)
                widget = ttk.Entry(field, textvariable=variable, style="Modern.TEntry")
                widget.grid(row=0, column=0, sticky="ew")
                ttk.Button(field, text="\U0001F4C5", command=self.choose_date,
                           style="Secondary.TButton").grid(row=0, column=1, padx=(5, 0))
                return widget
            elif variable == self.var_time:
                field = Frame(block, bg=WHITE)
                field.grid(row=1, column=0, sticky="ew")
                field.grid_columnconfigure(0, weight=1)
                widget = ttk.Entry(field, textvariable=variable, style="Modern.TEntry")
                widget.grid(row=0, column=0, sticky="ew")
                ttk.Button(field, text="\U0001F552", command=self.choose_time,
                           style="Secondary.TButton").grid(row=0, column=1, padx=(5, 0))
                return widget
            else:
                widget = ttk.Entry(block, textvariable=variable, style="Modern.TEntry")

            widget.grid(row=1, column=0, sticky="ew")
            return widget

        add_entry("Student ID", self.var_id, 0, 0)
        add_entry("Roll No", self.var_roll, 0, 2)
        add_entry("Student Name", self.var_name, 1, 0)
        add_entry("Time", self.var_time, 1, 2)
        add_entry("Date", self.var_date, 2, 0)
        add_entry("Attendance Status", self.var_attend, 2, 2, ("Status", "Present", "Absent"))

        # Actions
        actions = Frame(details_card, bg=WHITE)
        actions.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 16))
        for col in range(4):
            actions.grid_columnconfigure(col, weight=1, uniform="att_action")

        ttk.Button(
            actions,
            text="Save",
            command=self.action,
            style="Accent.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

        ttk.Button(
            actions,
            text="Reset",
            command=self.reset_data,
            style="Secondary.TButton",
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # -------------------- Student list --------------------
        student_card = Frame(left_panel, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        student_card.grid(row=1, column=0, sticky="nsew")
        student_card.grid_rowconfigure(1, weight=1)
        student_card.grid_columnconfigure(0, weight=1)
        Label(student_card, text="STUDENTS", bg=WHITE, fg=TEXT,
              font=("Segoe UI", 11, "bold")).grid(
                  row=0, column=0, sticky="w", padx=18, pady=(14, 9))
        student_wrap = Frame(student_card, bg=WHITE)
        student_wrap.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        student_wrap.grid_rowconfigure(0, weight=1)
        student_wrap.grid_columnconfigure(0, weight=1)
        student_scroll = ttk.Scrollbar(student_wrap, orient=VERTICAL)
        self.student_list = ttk.Treeview(
            student_wrap, columns=("ID", "Roll", "Name"), show="headings",
            yscrollcommand=student_scroll.set, style="Modern.Treeview")
        for column, heading, width in (("ID", "Student ID", 100), ("Roll", "Roll No", 100), ("Name", "Student Name", 180)):
            self.student_list.heading(column, text=heading, anchor="center")
            self.student_list.column(column, width=width, anchor="center", stretch=True)
        self.student_list.grid(row=0, column=0, sticky="nsew")
        student_scroll.grid(row=0, column=1, sticky="ns")
        student_scroll.config(command=self.student_list.yview)
        self.student_list.bind("<<TreeviewSelect>>", self.select_student)

        # -------------------- Imported CSV card --------------------
        csv_card = Frame(right_panel, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        csv_card.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
        csv_card.grid_rowconfigure(1, weight=1)
        csv_card.grid_columnconfigure(0, weight=1)

        csv_title = Frame(csv_card, bg=WHITE)
        csv_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 9))
        csv_title.grid_columnconfigure(0, weight=1)

        Label(
            csv_title,
            text="IMPORTED CSV PREVIEW",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, sticky="w")

        Label(
            csv_title,
            text="Data loaded from CSV before database import",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=0, column=1, sticky="e")

        csv_table_wrap = Frame(csv_card, bg=WHITE)
        csv_table_wrap.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        csv_table_wrap.grid_rowconfigure(0, weight=1)
        csv_table_wrap.grid_columnconfigure(0, weight=1)

        scroll_x_left = ttk.Scrollbar(
            csv_table_wrap,
            orient=HORIZONTAL,
            style="Modern.Horizontal.TScrollbar",
        )
        scroll_y_left = ttk.Scrollbar(
            csv_table_wrap,
            orient=VERTICAL,
            style="Modern.Vertical.TScrollbar",
        )

        cols = ("ID", "Roll_No", "Name", "Time", "Date", "Attend")

        self.attendanceReport_left = ttk.Treeview(
            csv_table_wrap,
            columns=cols,
            show="headings",
            xscrollcommand=scroll_x_left.set,
            yscrollcommand=scroll_y_left.set,
            style="Modern.Treeview",
        )
        self.attendanceReport_left.grid(row=0, column=0, sticky="nsew")
        scroll_y_left.grid(row=0, column=1, sticky="ns")
        scroll_x_left.grid(row=1, column=0, sticky="ew")

        scroll_x_left.config(command=self.attendanceReport_left.xview)
        scroll_y_left.config(command=self.attendanceReport_left.yview)

        headings = {
            "ID": "Student ID",
            "Roll_No": "Roll No",
            "Name": "Student Name",
            "Time": "Time",
            "Date": "Date",
            "Attend": "Status",
        }
        widths = {
            "ID": 105,
            "Roll_No": 105,
            "Name": 160,
            "Time": 110,
            "Date": 110,
            "Attend": 110,
        }

        for col in cols:
            self.attendanceReport_left.heading(col, text=headings[col], anchor="center")
            self.attendanceReport_left.column(
                col, width=widths[col], minwidth=90, stretch=False, anchor="center",
            )

        self.attendanceReport_left.bind("<ButtonRelease>", self.get_cursor_left)

        # -------------------- Database records card --------------------
        db_card = Frame(right_panel, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        db_card.grid(row=0, column=0, sticky="nsew")
        db_card.grid_rowconfigure(1, weight=1)
        db_card.grid_columnconfigure(0, weight=1)

        db_title = Frame(db_card, bg=WHITE)
        db_title.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 9))
        db_title.grid_columnconfigure(0, weight=1)

        Label(
            db_title,
            text="DATABASE RECORDS",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=0, sticky="w")

        Label(
            db_title,
            text="Select a record to load its details",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=0, column=1, sticky="e")

        db_table_wrap = Frame(db_card, bg=WHITE)
        db_table_wrap.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        db_table_wrap.grid_rowconfigure(0, weight=1)
        db_table_wrap.grid_columnconfigure(0, weight=1)

        scroll_x_right = ttk.Scrollbar(
            db_table_wrap,
            orient=HORIZONTAL,
            style="Modern.Horizontal.TScrollbar",
        )
        scroll_y_right = ttk.Scrollbar(
            db_table_wrap,
            orient=VERTICAL,
            style="Modern.Vertical.TScrollbar",
        )

        self.attendanceReport = ttk.Treeview(
            db_table_wrap,
            columns=cols,
            show="headings",
            selectmode="extended",
            xscrollcommand=scroll_x_right.set,
            yscrollcommand=scroll_y_right.set,
            style="Modern.Treeview",
        )
        self.attendanceReport.grid(row=0, column=0, sticky="nsew")
        scroll_y_right.grid(row=0, column=1, sticky="ns")
        scroll_x_right.grid(row=1, column=0, sticky="ew")

        scroll_x_right.config(command=self.attendanceReport.xview)
        scroll_y_right.config(command=self.attendanceReport.yview)

        for col in cols:
            self.attendanceReport.heading(col, text=headings[col], anchor="center")
            self.attendanceReport.column(
                col, width=widths[col], minwidth=90, stretch=False, anchor="center",
            )

        self.attendanceReport.bind("<ButtonRelease>", self.get_cursor_right)

        # -------------------- Database actions --------------------
        db_actions = Frame(right_panel, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        db_actions.grid(row=1, column=0, sticky="ew", pady=(12, 0))

        for column in range(4):
            db_actions.grid_columnconfigure(column, weight=1)

        ttk.Button(
            db_actions,
            text="Update Record",
            command=self.update_data,
            style="Primary.TButton",
        ).grid(row=0, column=0, sticky="ew", padx=(18, 6), pady=14)

        ttk.Button(
            db_actions,
            text="Delete Record",
            command=self.delete_data,
            style="Danger.TButton",
        ).grid(row=0, column=1, sticky="ew", padx=6, pady=14)

        ttk.Button(db_actions, text="Import CSV", command=self.importCsv,
               style="Secondary.TButton").grid(row=0, column=2, sticky="ew", padx=6, pady=14)
        ttk.Button(db_actions, text="Export CSV", command=self.exportCsv,
               style="Secondary.TButton").grid(row=0, column=3, sticky="ew", padx=(6, 18), pady=14)

        # Load current database records exactly as before.
        self.fetch_data()
        self.fetch_students()

    def go_back(self):
        self.root.destroy()

    def fetch_students(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT Student_ID, Roll_No, Name FROM student WHERE Owner_Email=%s ORDER BY Name",
                (self.owner_email,),
            )
            self.student_list.delete(*self.student_list.get_children())
            for row in cursor.fetchall():
                self.student_list.insert("", END, values=row)
        finally:
            cursor.close()
            conn.close()

    def select_student(self, event=None):
        selected = self.student_list.selection()
        if not selected:
            return
        values = self.student_list.item(selected[0], "values")
        self.var_id.set(values[0])
        self.var_roll.set(values[1])
        self.var_name.set(values[2])
        if not self.var_date.get():
            self.set_today()
        if not self.var_time.get():
            self.set_now()

    def set_today(self):
        self.var_date.set(datetime.now().strftime("%d-%m-%Y"))

    def set_now(self):
        self.var_time.set(datetime.now().strftime("%H:%M"))

    def choose_search_date(self):
        self.var_search_type.set("Date")
        self.choose_date(target=self.var_search_value)

    def update_search_controls(self, event=None):
        if self.var_search_type.get() == "Date":
            self.search_calendar_button.grid()
        else:
            self.search_calendar_button.grid_remove()

    def clear_search(self):
        self.var_search_type.set("Select field")
        self.var_search_value.set("")
        self.search_calendar_button.grid_remove()
        self.fetch_data()

    def choose_time(self):
        picker = Toplevel(self.root)
        picker.title("Select time")
        picker.transient(self.root)
        picker.grab_set()
        now = datetime.now()
        hour = StringVar(value=now.strftime("%H"))
        minute = StringVar(value=now.strftime("%M"))
        Label(picker, text="Hour").grid(row=0, column=0, padx=8, pady=(12, 4))
        Label(picker, text="Minute").grid(row=0, column=1, padx=8, pady=(12, 4))
        Spinbox(picker, from_=0, to=23, width=4, textvariable=hour).grid(row=1, column=0, padx=8)
        Spinbox(picker, from_=0, to=59, width=4, textvariable=minute).grid(row=1, column=1, padx=8)

        def apply_time():
            self.var_time.set(f"{int(hour.get()):02d}:{int(minute.get()):02d}")
            picker.destroy()

        ttk.Button(picker, text="Use time", command=apply_time,
                   style="Primary.TButton").grid(row=2, column=0, columnspan=2, padx=8, pady=12)

    def choose_date(self, target=None):
        target = target or self.var_date
        picker = Toplevel(self.root)
        picker.title("Select date")
        picker.transient(self.root)
        picker.grab_set()
        now = datetime.now()
        month = IntVar(value=now.month)
        year = IntVar(value=now.year)

        def render():
            for child in calendar_body.winfo_children():
                child.destroy()
            Label(calendar_body, text=f"{calendar.month_name[month.get()]} {year.get()}",
                  font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=7, pady=8)
            for column, name in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
                Label(calendar_body, text=name, width=4, fg="#64748B").grid(row=1, column=column)
            for index, day in enumerate(calendar.monthcalendar(year.get(), month.get())):
                for column, value in enumerate(day):
                    if value:
                        Button(calendar_body, text=str(value), width=3, relief="flat",
                               command=lambda value=value: select_day(value)).grid(
                                   row=2 + index, column=column, padx=1, pady=1)

        def select_day(day):
            target.set(f"{day:02d}-{month.get():02d}-{year.get()}")
            picker.destroy()

        controls = Frame(picker)
        controls.pack(fill=X, padx=8, pady=(8, 0))
        Button(controls, text="<", command=lambda: change_month(-1)).pack(side=LEFT)
        Button(controls, text=">", command=lambda: change_month(1)).pack(side=RIGHT)
        calendar_body = Frame(picker)
        calendar_body.pack(padx=8, pady=8)

        def change_month(offset):
            value = month.get() + offset
            if value < 1:
                month.set(12)
                year.set(year.get() - 1)
            elif value > 12:
                month.set(1)
                year.set(year.get() + 1)
            else:
                month.set(value)
            render()

        render()

    # ===============================update function for mysql database=================
    def update_data(self):
        if self.selected_record is None:
            messagebox.showerror("Error", "Select a database record to update.", parent=self.root)
            return
        if self.var_id.get()=="" or self.var_roll.get()=="" or self.var_name.get()=="" or self.var_time.get()=="" or self.var_date.get()=="" or self.var_attend.get()=="Status":
            messagebox.showerror("Error","Please Fill All Fields are Required!",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to Update this Student Attendance!",parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(**DB_CONFIG)
                    mycursor = conn.cursor()
                    mycursor.execute("update stdattendance set std_id=%s,std_roll_no=%s,std_name=%s,std_time=%s,std_date=%s,std_attendance=%s where std_id=%s and Owner_Email=%s and std_roll_no=%s and std_name=%s and std_time=%s and std_date=%s and std_attendance=%s LIMIT 1",(
                    self.var_id.get(),
                    self.var_roll.get(),
                    self.var_name.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                    self.var_attend.get(),
                    self.var_id.get(),
                    self.owner_email,
                    self.selected_record[1],
                    self.selected_record[2],
                    self.selected_record[3],
                    self.selected_record[4],
                    self.selected_record[5],
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Successfully Updated!",parent=self.root)
                conn.commit()
                self.fetch_data()
                self.selected_record = None
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    # =============================Delete Attendance form my sql============================
    def delete_data(self):
        selected = self.attendanceReport.selection()
        delete_all = not selected
        if delete_all:
            question = "No rows are selected. Delete all of your attendance records?"
        else:
            question = f"Delete {len(selected)} selected attendance record(s)?"
        if messagebox.askyesno("Delete", question, parent=self.root):
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                mycursor = conn.cursor()
                if delete_all:
                    mycursor.execute("DELETE FROM stdattendance WHERE Owner_Email=%s", (self.owner_email,))
                else:
                    for item in selected:
                        values = self.attendanceReport.item(item, "values")
                        mycursor.execute(
                            "DELETE FROM stdattendance WHERE std_id=%s AND std_roll_no=%s AND std_name=%s AND std_time=%s AND std_date=%s AND std_attendance=%s AND Owner_Email=%s LIMIT 1",
                            (*values, self.owner_email),
                        )
                conn.commit()
                self.fetch_data()
                conn.close()
                self.reset_data()
                messagebox.showinfo("Delete", "Selected records deleted.", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)  
    # ===========================fatch data form mysql attendance===========

    def fetch_data(self):
        conn = mysql.connector.connect(**DB_CONFIG)
        mycursor = conn.cursor()

        mycursor.execute(
            "UPDATE stdattendance a JOIN student s "
            "ON a.std_id=s.Student_ID AND a.Owner_Email=s.Owner_Email "
            "SET a.std_roll_no=s.Roll_No, a.std_name=s.Name "
            "WHERE a.Owner_Email=%s",
            (self.owner_email,),
        )
        conn.commit()
        mycursor.execute("select std_id,std_roll_no,std_name,std_time,std_date,std_attendance from stdattendance where Owner_Email=%s", (self.owner_email,))
        data=mycursor.fetchall()

        if len(data)!= 0:
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            for i in data:
                self.attendanceReport.insert("",END,values=i)
            conn.commit()
        conn.close()

    def search_records(self):
        search_type = self.var_search_type.get()
        search_value = self.var_search_value.get().strip()
        if search_type == "Select field" or not search_value:
            messagebox.showerror(
                "Search required",
                "Select a field and enter a value to search.",
                parent=self.root,
            )
            return

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        try:
            search_columns = {
                "Date": "std_date",
                "Student Name": "std_name",
                "Roll No": "std_roll_no",
                "Student ID": "std_id",
            }
            column = search_columns[search_type]
            if search_type == "Date":
                values = (self.owner_email, search_value, search_value.replace("-", "/"))
                query = (
                    "SELECT std_id,std_roll_no,std_name,std_time,std_date,std_attendance "
                    "FROM stdattendance WHERE Owner_Email=%s AND std_date IN (%s, %s)"
                )
            else:
                values = (self.owner_email, search_value)
                query = (
                    f"SELECT std_id,std_roll_no,std_name,std_time,std_date,std_attendance "
                    f"FROM stdattendance WHERE Owner_Email=%s AND {column}=%s"
                )
            cursor.execute(query, values)
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            for row in cursor.fetchall():
                self.attendanceReport.insert("", END, values=row)
        finally:
            cursor.close()
            conn.close()

    #============================Reset Data======================
    def reset_data(self):
        self.var_id.set("")
        self.var_roll.set("")
        self.var_name.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Status")
        self.selected_record = None

    # =========================Fetch Data Import data ===============

    def fetchData(self,rows):
        global mydata
        mydata = rows
        self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
        for i in rows:
            self.attendanceReport_left.insert("",END,values=i)
            print(i)
        

    def importCsv(self):
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
        if not fln:
            return
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
        self.fetchData(mydata)
            

    #==================Experot CSV=============
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("Error","No Data Found!",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Successfuly","Export Data Successfully!",parent=self.root)
        except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)    

    #=============Cursur Function for CSV========================

    def get_cursor_left(self,event=""):
        cursor_focus = self.attendanceReport_left.focus()
        content = self.attendanceReport_left.item(cursor_focus)
        data = content["values"]

        if len(data) < 6:
            return

        self.var_id.set(data[0]),
        self.var_roll.set(data[1]),
        self.var_name.set(data[2]),
        self.var_time.set(data[3]),
        self.var_date.set(data[4]),
        self.var_attend.set(data[5])  

     #=============Cursur Function for mysql========================

    def get_cursor_right(self,event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content["values"]

        if len(data) < 6:
            return

        self.var_id.set(data[0]),
        self.var_roll.set(data[1]),
        self.var_name.set(data[2]),
        self.var_time.set(data[3]),
        self.var_date.set(data[4]),
        self.var_attend.set(data[5])    
        self.selected_record = tuple(data)
    #=========================================Update CSV============================

    # export upadte
    def action(self):
        if self.var_id.get()=="" or self.var_roll.get=="" or self.var_name.get()=="" or self.var_time.get()=="" or self.var_date.get()=="" or self.var_attend.get()=="Status":
            messagebox.showerror("Error","Please Fill All Fields are Required!",parent=self.root)
            return
        else:
            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                mycursor = conn.cursor()
                mycursor.execute(
                    "SELECT COUNT(*) FROM stdattendance WHERE std_id=%s AND Owner_Email=%s AND std_date=%s",
                    (self.var_id.get(), self.owner_email, self.var_date.get()),
                )
                if mycursor.fetchone()[0] > 0:
                    conn.close()
                    messagebox.showwarning(
                        "Already recorded",
                        "This student already has attendance for this date.",
                        parent=self.root,
                    )
                    return
                mycursor.execute("insert into stdattendance (std_id,std_roll_no,std_name,std_time,std_date,std_attendance,Owner_Email) values(%s,%s,%s,%s,%s,%s,%s)",(
                self.var_id.get(),
                self.var_roll.get(),
                self.var_name.get(),
                self.var_time.get(),
                self.var_date.get(),
                self.var_attend.get(),
                self.owner_email,
                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","All Records are Saved in Database!",parent=self.root)
                return
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
                return



        conn = mysql.connector.connect(**DB_CONFIG)
        mycursor = conn.cursor()
        if messagebox.askyesno("Confirmation","Do you want to save attendance on database?",parent=self.root):
            for i in mydata:
                uid = i[0]
                uroll = i[1]
                uname = i[2]
                utime = i[3]
                udate = i[4]
                uattend = i[5]
                qury = "INSERT INTO stdattendance(std_id, std_roll_no, std_name, std_time, std_date, std_attendance, Owner_Email) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                mycursor.execute(qury,(uid,uroll,uname,utime,udate,uattend,self.owner_email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Successfully Updated!",parent=self.root)
        else:
            return False


if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()