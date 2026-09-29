from tkinter import *
from tkinter import ttk, messagebox
from train import Train
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from helpsupport import Helpsupport
from db_config import ensure_owner_columns, DB_CONFIG
import os
from datetime import datetime
from ui.theme import COLORS, apply_theme, FONTS
from ui.components import *
from ui.icons import ICONS
from ui.assets import get_image_path, load_image, BASE_DIR
import mysql.connector
import pymysql
from user_profile import Profile

pymysql.install_as_MySQLdb()

# ============================================================
# Project paths
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")


class Face_Recognition_System:

    def __init__(self, root, authenticated=False, user_email=None, user_name="Admin"):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.user_email = user_email
        self.user_name = user_name
        ensure_owner_columns()
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1400x850")
        self.root.minsize(1150, 720)

        try:
            self.root.state("zoomed")
        except Exception:
            pass

        # ====================================================
        # Design system
        # ====================================================
        NAVY = COLORS["secondary"]
        NAVY_SOFT = COLORS["secondary"]
        NAVY_ACTIVE = COLORS["primary_dark"]
        BG = COLORS["bg_main"]
        WHITE = COLORS["white"]
        BLUE = COLORS["primary"]
        BLUE_DARK = COLORS["secondary"]
        BLUE_SOFT = COLORS["primary_light"]
        PINK = COLORS["accent_pink"]
        PINK_SOFT = COLORS["accent_pink_soft"]
        PURPLE = COLORS["accent_purple"]
        PURPLE_SOFT = COLORS["accent_pink_soft"]
        ORANGE = COLORS["accent_orange"]
        ORANGE_SOFT = COLORS["accent_pink_soft"]
        TEAL = COLORS["accent_teal"]
        TEAL_SOFT = COLORS["accent_teal"]
        GREEN = COLORS["success"]
        TEXT = COLORS["text_main"]
        MUTED = COLORS["text_muted"]
        BORDER = COLORS["border"]
        RED = COLORS["danger"]
        RED_SOFT = COLORS["accent_pink_soft"]

        self.C_BG = BG
        self.C_WHITE = WHITE
        self.C_TEXT = TEXT
        self.C_MUTED = MUTED
        self.C_BORDER = BORDER
        self.C_NAVY = NAVY
        self.C_NAVY_ACTIVE = NAVY_ACTIVE

        self.root.configure(bg=BG)

        # ====================================================
        # ttk styling
        # ====================================================
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure("MainAction.TButton",
            background=WHITE, foreground=BLUE, relief="flat",
            borderwidth=1, bordercolor=BORDER, focusthickness=0,
            padding=(10, 8), font=("Segoe UI", 9, "bold"))
        style.map("MainAction.TButton",
            background=[("active", BLUE_SOFT)],
            foreground=[("active", BLUE_DARK)],
            bordercolor=[("active", BLUE)])

        style.configure("MainDanger.TButton",
            background=WHITE, foreground=RED, relief="flat",
            borderwidth=1, bordercolor="#FECACA", focusthickness=0,
            padding=(12, 10), font=("Segoe UI", 9, "bold"))
        style.map("MainDanger.TButton",
            background=[("active", RED_SOFT)],
            foreground=[("active", "#B91C1C")],
            bordercolor=[("active", RED)])

        # ====================================================
        # Root layout: sidebar (col 0) + main area (col 1)
        # ====================================================
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

        # ====================================================
        # Sidebar
        # ====================================================
        SIDEBAR_FULL = 264
        SIDEBAR_MINI = 64
        self._sidebar_expanded = True
        sidebar = Frame(self.root, bg=NAVY, width=SIDEBAR_FULL)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        # Toggle button at the top of sidebar
        toggle_row = Frame(sidebar, bg=NAVY)
        toggle_row.pack(fill=X, padx=14, pady=(16, 0))

        def toggle_sidebar():
            if self._sidebar_expanded:
                sidebar.configure(width=SIDEBAR_MINI)
                for w in self._sidebar_labels:
                    w.pack_forget()
                toggle_btn.configure(text="☰")
                brand_label.pack_forget()
            else:
                sidebar.configure(width=SIDEBAR_FULL)
                for icon_lbl, text_lbl in self._sidebar_label_pairs:
                    text_lbl.pack(side=LEFT, padx=(14, 0))
                toggle_btn.configure(text="✕")
                brand_label.pack(side=LEFT, padx=(14, 0))
            self._sidebar_expanded = not self._sidebar_expanded

        toggle_btn = Label(toggle_row, text="✕", bg=NAVY, fg=WHITE,
                           font=("Segoe UI", 13, "bold"), cursor="hand2",
                           padx=6, pady=4)
        toggle_btn.pack(side=RIGHT)
        toggle_btn.bind("<Button-1>", lambda e: toggle_sidebar())

        brand_row = Frame(sidebar, bg=NAVY)
        brand_row.pack(fill=X, padx=18, pady=(14, 26))

        try:
            from PIL import Image, ImageTk
            _logo_img = Image.open(os.path.join(IMAGE_DIR, "Face-Recognition-Software.png"))
            _logo_img = _logo_img.resize((40, 40), Image.LANCZOS)
            self._sidebar_logo = ImageTk.PhotoImage(_logo_img)
            mark = Label(brand_row, image=self._sidebar_logo, bg=NAVY)
        except Exception:
            mark = Frame(brand_row, bg=BLUE, width=46, height=46)
            mark.pack_propagate(False)
            Label(mark, text="FR", bg=BLUE, fg=WHITE,
                  font=("Segoe UI", 13, "bold")).pack(expand=True)
        mark.pack(side=LEFT)

        brand_label = Label(brand_row, text="Attendance\nSystem", bg=NAVY, fg=WHITE,
              font=("Segoe UI", 12, "bold"), justify=LEFT)
        brand_label.pack(side=LEFT, padx=(14, 0))

        nav_items = [
            ("\U0001F3E0", "Home", None),
            ("\U0001F393", "Students", self.student_pannels),
            ("\U0001F4C5", "Attendance", self.attendance_pannel),
            ("\U0001F4F7", "Face Recognition", self.face_rec),
            ("\U0001F464", "Student Panel", self.student_pannels),
            ("\U0001F5C4", "Data Train", self.train_pannels),
            ("</>" , "Developers", self.developr),
            ("\u2753", "Help & Support", self.helpSupport),
        ]

        self.nav_buttons = []
        self._sidebar_labels = []
        self._sidebar_label_pairs = []
        nav_wrap = Frame(sidebar, bg=NAVY)
        nav_wrap.pack(fill=X)

        for icon, label, cmd in nav_items:
            active_bg = NAVY_ACTIVE if label == "Home" else NAVY
            row = Frame(nav_wrap, bg=active_bg, cursor="hand2")
            row.pack(fill=X, padx=12, pady=3)

            inner = Frame(row, bg=active_bg)
            inner.pack(fill=X, padx=14, pady=12)

            icon_lbl = Label(inner, text=icon, bg=active_bg, fg=WHITE,
                  font=("Segoe UI", 12))
            icon_lbl.pack(side=LEFT)
            text_lbl = Label(inner, text=label, bg=active_bg,
                  fg=WHITE if label == "Home" else "#CBD5F5",
                  font=("Segoe UI", 10, "bold" if label == "Home" else "normal")
                  )
            text_lbl.pack(side=LEFT, padx=(14, 0))
            self._sidebar_labels.append(text_lbl)
            self._sidebar_label_pairs.append((icon_lbl, text_lbl))

            if cmd is not None:
                def bind_click(widget, callback):
                    widget.bind("<Button-1>", lambda e: callback())
                    for child in widget.winfo_children():
                        bind_click(child, callback)
                bind_click(row, cmd)

                def on_enter(e, r=row, i=inner):
                    r.configure(background=NAVY_SOFT)  # type: ignore
                    i.configure(background=NAVY_SOFT)  # type: ignore
                    for c in i.winfo_children():
                        c.configure(background=NAVY_SOFT)  # type: ignore

                def on_leave(e, r=row, i=inner, ab=active_bg):
                    r.configure(background=ab)  # type: ignore
                    i.configure(background=ab)  # type: ignore
                    for c in i.winfo_children():
                        c.configure(background=ab)  # type: ignore

                row.bind("<Enter>", on_enter)
                row.bind("<Leave>", on_leave)

        sidebar_footer = Frame(sidebar, bg=NAVY)
        sidebar_footer.pack(side=BOTTOM, fill=X, padx=22, pady=28)

        Frame(sidebar_footer, bg=NAVY_ACTIVE, height=1).pack(fill=X, pady=(0, 16))

        Label(sidebar_footer, text="Better Security\nSmarter Attendance",
              bg=NAVY, fg="#8FA3D6", font=("Segoe UI", 9, "bold"),
              justify=LEFT).pack(anchor="w", pady=(0, 14))

        ttk.Button(sidebar_footer, text="\u23FB  Exit", style="MainDanger.TButton",
                   command=self.Close).pack(fill=X)


        # ====================================================
        # Main column
        # ====================================================
        main_col = Frame(self.root, bg=BG)
        main_col.grid(row=0, column=1, sticky="nsew")
        main_col.grid_rowconfigure(1, weight=1)
        main_col.grid_columnconfigure(0, weight=1)

        # ---------------- Header ----------------
        header = Frame(main_col, bg=WHITE, height=80)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        head_left = Frame(header, bg=WHITE)
        head_left.grid(row=0, column=0, sticky="w", padx=24, pady=14)

        try:
            _hlogo_img = Image.open(os.path.join(IMAGE_DIR, "Face-Recognition-Software.png"))
            _hlogo_img = _hlogo_img.resize((44, 44), Image.LANCZOS)
            self._header_logo = ImageTk.PhotoImage(_hlogo_img)
            small_mark = Label(head_left, image=self._header_logo, bg=WHITE)
        except Exception:
            small_mark = Frame(head_left, bg=BLUE, width=44, height=44)
            small_mark.pack_propagate(False)
            Label(small_mark, text="FR", bg=BLUE, fg=WHITE,
                  font=("Segoe UI", 12, "bold")).pack(expand=True)
        small_mark.pack(side=LEFT)

        head_text = Frame(head_left, bg=WHITE)
        head_text.pack(side=LEFT, padx=(12, 0))
        Label(head_text, text="Face Recognition Attendance System",
              bg=WHITE, fg=BLUE_DARK, font=("Segoe UI", 15, "bold")
              ).pack(anchor="w")
        Label(head_text, text="Smart student management  \u2022  recognition  \u2022  attendance",
              bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))

        head_right = Frame(header, bg=WHITE)
        head_right.grid(row=0, column=1, sticky="e", padx=24)

        avatar = Frame(head_right, bg=BLUE_SOFT, width=34, height=34)
        avatar.pack(side=LEFT)
        avatar.pack_propagate(False)
        Label(avatar, text="\U0001F464", bg=BLUE_SOFT, fg=BLUE,
              font=("Segoe UI", 12)).pack(expand=True)

        Label(head_right, text=f"Welcome, {self.user_name}", bg=WHITE, fg=TEXT,
              font=("Segoe UI", 10, "bold")).pack(side=LEFT, padx=(10, 0))
                # Profile button
        def bind_profile_click(widget):
            widget.bind("<Button-1>", lambda e: self.open_profile())
            widget.configure(cursor="hand2")
            for child in widget.winfo_children():
                bind_profile_click(child)

        bind_profile_click(head_right)

        Frame(header, bg=BORDER, height=1).place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")

        # ---------------- Body ----------------
        body = Frame(main_col, bg=BG)
        body.grid(row=1, column=0, sticky="nsew", padx=22, pady=20)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(2, weight=1)

        # ---- top row: banner + total students (col 0) ----
        top_row = Frame(body, bg=BG)
        top_row.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        top_row.grid_columnconfigure(0, weight=3)
        top_row.grid_columnconfigure(1, weight=1)

        banner = Frame(top_row, bg=BLUE_SOFT, highlightbackground=BORDER, highlightthickness=1)
        banner.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        banner.grid_columnconfigure(0, weight=1)

        banner_inner = Frame(banner, bg=BLUE_SOFT)
        banner_inner.pack(fill=BOTH, expand=True, padx=26, pady=24)

        Label(banner_inner, text="Welcome back,", bg=BLUE_SOFT, fg=BLUE_DARK,
              font=("Segoe UI", 22, "bold")).pack(anchor="w")
        Label(banner_inner,
              text="Use the sidebar to manage students, training,\nrecognition and attendance.",
              bg=BLUE_SOFT, fg=MUTED, font=("Segoe UI", 10), justify=LEFT
              ).pack(anchor="w", pady=(8, 14))
        Frame(banner_inner, bg=BLUE, width=90, height=4).pack(anchor="w")

        # Live counts for this account
        total_students, present_today = self._get_dashboard_stats()

        total_card = Frame(top_row, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        total_card.grid(row=0, column=1, sticky="nsew")
        total_inner = Frame(total_card, bg=WHITE)
        total_inner.pack(fill=BOTH, expand=True, padx=20, pady=20)

        tc_icon = Frame(total_inner, bg=BLUE_SOFT, width=44, height=44)
        tc_icon.pack(anchor="w")
        tc_icon.pack_propagate(False)
        Label(tc_icon, text="\U0001F465", bg=BLUE_SOFT, fg=BLUE,
              font=("Segoe UI", 14)).pack(expand=True)

        Label(total_inner, text="Total Students", bg=WHITE, fg=MUTED,
              font=("Segoe UI", 9)).pack(anchor="w", pady=(14, 0))
        Label(total_inner, text=str(total_students), bg=WHITE, fg=BLUE_DARK,
              font=("Segoe UI", 26, "bold")).pack(anchor="w")
        Frame(total_inner, bg=PURPLE, width=40, height=3).pack(anchor="w", pady=(6, 0))

        # ---- Quick Actions panel (col 1, row 0) ----
        quick_panel = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        quick_panel.grid(row=0, column=1, sticky="nsew", padx=(14, 0), pady=(0, 14))
        quick_inner = Frame(quick_panel, bg=WHITE)
        quick_inner.pack(fill=BOTH, expand=True, padx=18, pady=16)

        qtitle = Frame(quick_inner, bg=WHITE)
        qtitle.pack(fill=X, pady=(0, 14))
        Label(qtitle, text="\u26A1", bg=WHITE, fg=ORANGE,
              font=("Segoe UI", 11)).pack(side=LEFT)
        Label(qtitle, text="Quick Actions", bg=WHITE, fg=TEXT,
              font=("Segoe UI", 11, "bold")).pack(side=LEFT, padx=(8, 0))

        # Task-level shortcuts only — each calls the same handler as its
        # sidebar entry, so there is exactly one code path per feature.
        quick_actions = [
            ("\U0001F464", "Add new student", self.student_pannels, BLUE, BLUE_SOFT),
            ("\U0001F4F7", "Start recognition", self.face_rec, PINK, PINK_SOFT),
            ("\U0001F5C4", "Retrain model", self.train_pannels, ORANGE, ORANGE_SOFT),
        ]

        for icon, title, cmd, accent, accent_soft in quick_actions:
            self._quick_action_tile(quick_inner, icon, title, cmd, accent, accent_soft).pack(
                fill=X, pady=6)

        # ---- Stats strip (full width, row 1) ----
        stats_strip = Frame(body, bg=BG)
        stats_strip.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        for c in range(3):
            stats_strip.grid_columnconfigure(c, weight=1, uniform="stats")

        present_label = f"{present_today} / {total_students}" if total_students else "0 / 0"
        attendance_rate = (
            f"{round((present_today / total_students) * 100)}%" if total_students else "0%"
        )
        stat_tiles = [
            ("\U0001F4C5", "Present today", present_label, GREEN, "#E7F9F1"),
            ("\U0001F4CA", "Attendance rate", attendance_rate, BLUE, BLUE_SOFT),
            ("\U0001F5C4", "Model status", "Trained", PURPLE, PURPLE_SOFT),
        ]
        for col, (icon, label, value, accent, accent_soft) in enumerate(stat_tiles):
            self._stat_tile(stats_strip, icon, label, value, accent, accent_soft).grid(
                row=0, column=col, sticky="nsew",
                padx=(0 if col == 0 else 8, 8 if col < 2 else 0))

        # ---- Recent activity (col 0, row 2) ----
        activity_panel = self._build_recent_activity(body)
        activity_panel.grid(row=2, column=0, sticky="nsew")

        # ---- System Status panel (col 1, row 2) ----
        status_panel = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        status_panel.grid(row=2, column=1, sticky="new", padx=(14, 0))
        status_inner = Frame(status_panel, bg=WHITE)
        status_inner.pack(fill=BOTH, expand=True, padx=18, pady=16)

        stitle = Frame(status_inner, bg=WHITE)
        stitle.pack(fill=X, pady=(0, 12))
        Label(stitle, text="System Status", bg=WHITE, fg=TEXT,
              font=("Segoe UI", 11, "bold")).pack(side=LEFT)
        online_dot = Frame(stitle, bg=GREEN, width=8, height=8)
        online_dot.pack(side=RIGHT, pady=4)
        Label(stitle, text="Online", bg=WHITE, fg=GREEN,
              font=("Segoe UI", 9, "bold")).pack(side=RIGHT, padx=(0, 6))

        status_items = [
            ("\U0001F5C4", "Database", "Connected"),
            ("\U0001F4F7", "Face Recognition", "Ready"),
            ("\U0001F551", "Last Backup", "Today"),
        ]
        for icon, label, value in status_items:
            srow = Frame(status_inner, bg=WHITE)
            srow.pack(fill=X, pady=6)
            ic = Frame(srow, bg=BLUE_SOFT, width=30, height=30)
            ic.pack(side=LEFT)
            ic.pack_propagate(False)
            Label(ic, text=icon, bg=BLUE_SOFT, fg=BLUE,
                  font=("Segoe UI", 9)).pack(expand=True)
            txt = Frame(srow, bg=WHITE)
            txt.pack(side=LEFT, padx=(10, 0), anchor="w")
            Label(txt, text=label, bg=WHITE, fg=TEXT,
                  font=("Segoe UI", 9, "bold")).pack(anchor="w")
            Label(txt, text=value, bg=WHITE, fg=MUTED,
                  font=("Segoe UI", 8)).pack(anchor="w")

        # ---- Bottom banner ----
        bottom_banner = Frame(body, bg=NAVY)
        bottom_banner.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        bb_inner = Frame(bottom_banner, bg=NAVY)
        bb_inner.pack(fill=X, padx=26, pady=18)

        Label(bb_inner, text="Secure  \u2022  Simple  \u2022  Connected", bg=NAVY, fg=WHITE,
              font=("Segoe UI", 13, "bold")).pack(anchor="w")
        Label(bb_inner, text="Advanced face recognition technology for a safer and smarter campus.",
              bg=NAVY, fg="#B7C3E6", font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))

    # ========================================================
    # Dashboard tile builders (visual only)
    # ========================================================
    def _stat_tile(self, parent, icon, label, value, accent, accent_soft):
        WHITE = self.C_WHITE
        TEXT = self.C_TEXT
        MUTED = self.C_MUTED
        BORDER = self.C_BORDER

        tile = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        inner = Frame(tile, bg=WHITE)
        inner.pack(fill=BOTH, expand=True, padx=16, pady=14)

        icon_box = Frame(inner, bg=accent_soft, width=36, height=36)
        icon_box.pack(anchor="w")
        icon_box.pack_propagate(False)
        Label(icon_box, text=icon, bg=accent_soft, fg=accent,
              font=("Segoe UI", 12)).pack(expand=True)

        Label(inner, text=label, bg=WHITE, fg=MUTED,
              font=("Segoe UI", 9)).pack(anchor="w", pady=(10, 0))
        Label(inner, text=value, bg=WHITE, fg=TEXT,
              font=("Segoe UI", 17, "bold")).pack(anchor="w")
        return tile

    def _quick_action_tile(self, parent, icon, title, command, accent, accent_soft):
        WHITE = self.C_WHITE
        TEXT = self.C_TEXT
        BORDER = self.C_BORDER

        tile = Frame(parent, bg=WHITE, highlightbackground=BORDER,
                     highlightthickness=1, cursor="hand2")
        inner = Frame(tile, bg=WHITE)
        inner.pack(fill=BOTH, expand=True, padx=14, pady=12)

        row = Frame(inner, bg=WHITE)
        row.pack(fill=X)

        icon_box = Frame(row, bg=accent_soft, width=34, height=34)
        icon_box.pack(side=LEFT)
        icon_box.pack_propagate(False)
        Label(icon_box, text=icon, bg=accent_soft, fg=accent,
              font=("Segoe UI", 12)).pack(expand=True)

        Label(row, text=title, bg=WHITE, fg=TEXT,
              font=("Segoe UI", 10, "bold")).pack(side=LEFT, padx=(12, 0))
        Label(row, text="\u203A", bg=WHITE, fg=self.C_MUTED,
              font=("Segoe UI", 11, "bold")).pack(side=RIGHT)

        def bind_click(widget, callback):
            widget.bind("<Button-1>", lambda e: callback())
            for child in widget.winfo_children():
                bind_click(child, callback)
        bind_click(tile, command)

        return tile

    def _build_recent_activity(self, parent):
        WHITE = self.C_WHITE
        TEXT = self.C_TEXT
        MUTED = self.C_MUTED
        BORDER = self.C_BORDER
        GREEN = COLORS["success"]
        RED = COLORS["danger"]

        panel = Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        inner = Frame(panel, bg=WHITE)
        inner.pack(fill=BOTH, expand=True, padx=20, pady=18)

        title_row = Frame(inner, bg=WHITE)
        title_row.pack(fill=X, pady=(0, 12))
        Label(title_row, text="Recent activity", bg=WHITE, fg=TEXT,
              font=("Segoe UI", 12, "bold")).pack(side=LEFT)

        view_all = Label(title_row, text="View all \u203A", bg=WHITE, fg=self.C_NAVY,
                          font=("Segoe UI", 9, "bold"), cursor="hand2")
        view_all.pack(side=RIGHT)
        view_all.bind("<Button-1>", lambda e: self.attendance_pannel())

        rows = self._get_recent_activity(limit=6)
        if not rows:
            Label(inner, text="No attendance recorded yet.", bg=WHITE, fg=MUTED,
                  font=("Segoe UI", 9)).pack(anchor="w", pady=8)
        else:
            for name, roll_no, std_time, std_date, status in rows:
                row = Frame(inner, bg=WHITE)
                row.pack(fill=X, pady=6)

                is_present = (status or "").strip().lower() == "present"
                dot = Frame(row, bg=GREEN if is_present else RED, width=8, height=8)
                dot.pack(side=LEFT, pady=4)

                text_col = Frame(row, bg=WHITE)
                text_col.pack(side=LEFT, padx=(10, 0), anchor="w")
                Label(text_col, text=f"{name}  \u00b7  Roll {roll_no}", bg=WHITE, fg=TEXT,
                      font=("Segoe UI", 9, "bold")).pack(anchor="w")
                Label(text_col, text=f"{status}  \u2022  {std_date} {std_time}",
                      bg=WHITE, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w")

        return panel

    # ========================================================
    # Dashboard data (live, scoped to the signed-in owner)
    # ========================================================
    def _get_dashboard_stats(self):
        """Return (total_students, present_today) for the signed-in owner."""
        total_students = 0
        present_today = 0
        today_dash = datetime.now().strftime("%d-%m-%Y")
        today_slash = datetime.now().strftime("%d/%m/%Y")
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()

            cur.execute(
                "SELECT COUNT(*) FROM student WHERE Owner_Email=%s",
                (self.user_email,),
            )
            row = cur.fetchone()
            total_students = row[0] if row else 0

            cur.execute(
                "SELECT COUNT(*) FROM stdattendance "
                "WHERE Owner_Email=%s AND std_attendance='Present' "
                "AND std_date IN (%s, %s)",
                (self.user_email, today_dash, today_slash),
            )
            row = cur.fetchone()
            present_today = row[0] if row else 0

            cur.close()
            conn.close()
        except Exception:
            pass
        return total_students, present_today

    def _get_recent_activity(self, limit=6):
        """Return the most recent attendance rows for the signed-in owner,
        newest first. std_date is stored as text in mixed '-'/'/' formats,
        so it is normalized before sorting rather than sorted as-is."""
        rows = []
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute(
                "SELECT std_name, std_roll_no, std_time, std_date, std_attendance "
                "FROM stdattendance WHERE Owner_Email=%s "
                "ORDER BY STR_TO_DATE(REPLACE(std_date, '/', '-'), '%%d-%%m-%%Y') DESC, "
                "std_time DESC LIMIT %s",
                (self.user_email, limit),
            )
            rows = cur.fetchall()
            cur.close()
            conn.close()
        except Exception:
            rows = []
        return rows

       # ========================================================
    # Existing navigation functions — functionality preserved
    # ========================================================

    def open_profile(self):
        profile_window = Toplevel(self.root)
        self.profile_window = profile_window

        self.profile_app = Profile(
            profile_window,
            user_name=self.user_name,
            user_email=self.user_email,
            on_logout=lambda: self.logout(
                parent=profile_window,
                confirm=False
            ),
        )

    def open_img(self):
        dataset_path = os.path.join(BASE_DIR, "dataset")

        if os.path.exists(dataset_path):
            os.startfile(dataset_path)
        else:
            messagebox.showerror(
                "Error",
                "Dataset folder not found."
            )

    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(
            self.new_window,
            authenticated=True,
            owner_email=self.user_email,
            owner_name=self.user_name,
        )

    def train_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(
            self.new_window,
            authenticated=True,
            owner_email=self.user_email
        )

    def face_rec(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(
            self.new_window,
            authenticated=True,
            owner_email=self.user_email
        )

    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(
            self.new_window,
            authenticated=True,
            owner_email=self.user_email
        )

    def developr(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(
            self.new_window,
            authenticated=True
        )

    def helpSupport(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(
            self.new_window,
            authenticated=True
        )

    def logout(self, parent=None, confirm=True):
        # Normal dashboard logout still asks for confirmation.
        # Profile logout already confirmed with the Profile window.
        if confirm:
            if not messagebox.askyesno(
                "Logout",
                "Are you sure you want to log out?",
                parent=parent or self.root,
            ):
                return

        # Clear the current login session.
        from Session_utils import clear_session
        clear_session()

        # Remove the dashboard UI.
        for widget in self.root.winfo_children():
            widget.destroy()

        # Rebuild Login in the same dashboard window.
        from login import Login
        Login(self.root)

    def Close(self):
        self.root.destroy()


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    root = Tk()
    from login import Login
    obj = Login(root)
    root.mainloop()