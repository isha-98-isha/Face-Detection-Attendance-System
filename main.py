from tkinter import *
from tkinter import ttk, messagebox
from train import Train
from student import Student
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from helpsupport import Helpsupport
from db_config import ensure_owner_columns
import os
from ui.theme import COLORS, apply_theme, FONTS
from ui.components import *
from ui.icons import ICONS
from ui.assets import get_image_path, load_image, BASE_DIR
import mysql.connector
import pymysql

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
            padding=(10, 8), font=("Segoe UI", 9, "bold"))
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
        sidebar = Frame(self.root, bg=NAVY, width=224)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        brand_row = Frame(sidebar, bg=NAVY)
        brand_row.pack(fill=X, padx=20, pady=(24, 26))

        mark = Frame(brand_row, bg=BLUE, width=46, height=46)
        mark.pack(side=LEFT)
        mark.pack_propagate(False)
        Label(mark, text="FR", bg=BLUE, fg=WHITE,
              font=("Segoe UI", 13, "bold")).pack(expand=True)

        Label(brand_row, text="Attendance\nSystem", bg=NAVY, fg=WHITE,
              font=("Segoe UI", 11, "bold"), justify=LEFT).pack(
              side=LEFT, padx=(12, 0))

        nav_items = [
            ("\U0001F3E0", "Home", None),
            ("\U0001F393", "Students", self.student_pannels),
            ("\U0001F4C5", "Attendance", self.attendance_pannel),
            ("\U0001F4F7", "Face Recognition", self.face_rec),
            ("\U0001F464", "Student Panel", self.student_pannels),
            ("\U0001F5C4", "Data Train", self.train_pannels),
            ("</>", "Developers", self.developr),
            ("\u2753", "Help & Support", self.helpSupport),
        ]

        self.nav_buttons = []
        nav_wrap = Frame(sidebar, bg=NAVY)
        nav_wrap.pack(fill=X)

        for icon, label, cmd in nav_items:
            active_bg = NAVY_ACTIVE if label == "Home" else NAVY
            row = Frame(nav_wrap, bg=active_bg, cursor="hand2")
            row.pack(fill=X, padx=12, pady=3)

            inner = Frame(row, bg=active_bg)
            inner.pack(fill=X, padx=10, pady=10)

            Label(inner, text=icon, bg=active_bg, fg=WHITE,
                  font=("Segoe UI", 11)).pack(side=LEFT)
            Label(inner, text=label, bg=active_bg,
                  fg=WHITE if label == "Home" else "#CBD5F5",
                  font=("Segoe UI", 10, "bold" if label == "Home" else "normal")
                  ).pack(side=LEFT, padx=(12, 0))

            if cmd is not None:
                def bind_click(widget, callback):
                    widget.bind("<Button-1>", lambda e: callback())
                    for child in widget.winfo_children():
                        bind_click(child, callback)
                bind_click(row, cmd)

                def on_enter(e, r=row, i=inner):
                    r.configure(bg=NAVY_SOFT)
                    i.configure(bg=NAVY_SOFT)
                    for c in i.winfo_children():
                        c.configure(bg=NAVY_SOFT)

                def on_leave(e, r=row, i=inner, ab=active_bg):
                    r.configure(bg=ab)
                    i.configure(bg=ab)
                    for c in i.winfo_children():
                        c.configure(bg=ab)

                row.bind("<Enter>", on_enter)
                row.bind("<Leave>", on_leave)

        sidebar_footer = Frame(sidebar, bg=NAVY)
        sidebar_footer.pack(side=BOTTOM, fill=X, padx=20, pady=22)

        Frame(sidebar_footer, bg=NAVY_ACTIVE, height=1).pack(fill=X, pady=(0, 14))

        Label(sidebar_footer, text="Better Security\nSmarter Attendance",
              bg=NAVY, fg="#8FA3D6", font=("Segoe UI", 9, "bold"),
              justify=LEFT).pack(anchor="w", pady=(0, 12))

        ttk.Button(sidebar_footer, text="\u21BB  Logout", style="MainDanger.TButton",
                   command=self.logout).pack(fill=X, pady=(0, 8))

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

        small_mark = Frame(head_left, bg=BLUE, width=44, height=44)
        small_mark.pack(side=LEFT)
        small_mark.pack_propagate(False)
        Label(small_mark, text="FR", bg=BLUE, fg=WHITE,
              font=("Segoe UI", 12, "bold")).pack(expand=True)

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

        Frame(header, bg=BORDER, height=1).place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")

        # ---------------- Body ----------------
        body = Frame(main_col, bg=BG)
        body.grid(row=1, column=0, sticky="nsew", padx=22, pady=20)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(1, weight=1)

        # ---- top row: banner + total modules (col 0) ----
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
              text="Choose a module to manage students, training,\nrecognition and attendance.",
              bg=BLUE_SOFT, fg=MUTED, font=("Segoe UI", 10), justify=LEFT
              ).pack(anchor="w", pady=(8, 14))
        Frame(banner_inner, bg=BLUE, width=90, height=4).pack(anchor="w")

        total_card = Frame(top_row, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        total_card.grid(row=0, column=1, sticky="nsew")
        total_inner = Frame(total_card, bg=WHITE)
        total_inner.pack(fill=BOTH, expand=True, padx=20, pady=20)

        tc_icon = Frame(total_inner, bg=BLUE_SOFT, width=44, height=44)
        tc_icon.pack(anchor="w")
        tc_icon.pack_propagate(False)
        Label(tc_icon, text="\U0001F465", bg=BLUE_SOFT, fg=BLUE,
              font=("Segoe UI", 14)).pack(expand=True)

        Label(total_inner, text="Total Modules", bg=WHITE, fg=MUTED,
              font=("Segoe UI", 9)).pack(anchor="w", pady=(14, 0))
        Label(total_inner, text="7", bg=WHITE, fg=BLUE_DARK,
              font=("Segoe UI", 26, "bold")).pack(anchor="w")
        Frame(total_inner, bg=PURPLE, width=40, height=3).pack(anchor="w", pady=(6, 0))

        # ---- Quick Access panel (col 1, row 0) ----
        quick_panel = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        quick_panel.grid(row=0, column=1, sticky="nsew", padx=(14, 0), pady=(0, 14))
        quick_inner = Frame(quick_panel, bg=WHITE)
        quick_inner.pack(fill=BOTH, expand=True, padx=18, pady=16)

        qtitle = Frame(quick_inner, bg=WHITE)
        qtitle.pack(fill=X, pady=(0, 10))
        Label(qtitle, text="\u26A1", bg=WHITE, fg=ORANGE,
              font=("Segoe UI", 11)).pack(side=LEFT)
        Label(qtitle, text="Quick Access", bg=WHITE, fg=TEXT,
              font=("Segoe UI", 11, "bold")).pack(side=LEFT, padx=(8, 0))

        quick_items = [
            ("\U0001F464", "Add New Student", self.student_pannels),
            ("\U0001F4C5", "Mark Attendance", self.attendance_pannel),
            ("\U0001F5C4", "Train Model", self.train_pannels),
            ("\U0001F4CA", "View Reports", self.attendance_pannel),
        ]

        for icon, label, cmd in quick_items:
            qrow = Frame(quick_inner, bg=WHITE, cursor="hand2")
            qrow.pack(fill=X, pady=6)
            Label(qrow, text=icon, bg=WHITE, fg=MUTED,
                  font=("Segoe UI", 10)).pack(side=LEFT)
            Label(qrow, text=label, bg=WHITE, fg=TEXT,
                  font=("Segoe UI", 9, "bold")).pack(side=LEFT, padx=(10, 0))
            Label(qrow, text="\u203A", bg=WHITE, fg=MUTED,
                  font=("Segoe UI", 11, "bold")).pack(side=RIGHT)

            def bind_click(widget, callback):
                widget.bind("<Button-1>", lambda e: callback())
                for child in widget.winfo_children():
                    bind_click(child, callback)
            bind_click(qrow, cmd)

        # ---- Module cards grid (col 0, row 1) ----
        modules_wrap = Frame(body, bg=BG)
        modules_wrap.grid(row=1, column=0, sticky="nsew")
        modules_wrap.grid_rowconfigure(0, weight=1)
        modules_wrap.grid_rowconfigure(1, weight=1)
        for c in range(3):
            modules_wrap.grid_columnconfigure(c, weight=1, uniform="mrow0")

        wide_modules = [
            ("\U0001F393", "Students", "Manage student profiles\nand information.",
             self.student_pannels, BLUE, BLUE_SOFT, "\u2192"),
            ("\U0001F4F7", "Face Recognition", "Train and recognize\nstudent faces.",
             self.face_rec, PINK, PINK_SOFT, "\u2192"),
            ("\U0001F4C5", "Attendance", "View, update and manage\nattendance records.",
             self.attendance_pannel, GREEN, "#E7F9F1", "\u2192"),
        ]

        for col, (icon, title, desc, cmd, accent, accent_soft, arrow) in enumerate(wide_modules):
            self._make_card(modules_wrap, 0, col, icon, title, desc, cmd,
                             accent, accent_soft, arrow=arrow, big=True,
                             padx=(0 if col == 0 else 8, 8 if col < 2 else 0))

        small_row = Frame(modules_wrap, bg=BG)
        small_row.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(14, 0))
        for c in range(4):
            small_row.grid_columnconfigure(c, weight=1, uniform="mrow1")

        small_modules = [
            ("\U0001F464", "Student Panel", "Create and manage\nstudent profiles.",
             self.student_pannels, PURPLE, PURPLE_SOFT),
            ("\U0001F5C4", "Data Train", "Train the face-\nrecognition model.",
             self.train_pannels, ORANGE, ORANGE_SOFT),
            ("</>", "Developers", "Project and developer\ninformation.",
             self.developr, TEAL, TEAL_SOFT),
            ("\U0001F3A7", "Help & Support", "Support, guides\nand resources.",
             self.helpSupport, PINK, PINK_SOFT),
        ]

        for col, (icon, title, desc, cmd, accent, accent_soft) in enumerate(small_modules):
            self._make_card(small_row, 0, col, icon, title, desc, cmd,
                             accent, accent_soft, arrow="\u2192", big=False,
                             padx=(0 if col == 0 else 8, 8 if col < 3 else 0))

        # ---- System Status panel (col 1, row 1) ----
        status_panel = Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        status_panel.grid(row=1, column=1, sticky="new", padx=(14, 0))
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
        bottom_banner.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(16, 0))
        bb_inner = Frame(bottom_banner, bg=NAVY)
        bb_inner.pack(fill=X, padx=26, pady=18)

        Label(bb_inner, text="Secure  \u2022  Simple  \u2022  Connected", bg=NAVY, fg=WHITE,
              font=("Segoe UI", 13, "bold")).pack(anchor="w")
        Label(bb_inner, text="Advanced face recognition technology for a safer and smarter campus.",
              bg=NAVY, fg="#B7C3E6", font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))

    # ========================================================
    # Card builder helper (visual only)
    # ========================================================
    def _make_card(self, parent, row, col, icon, title, desc, command,
                    accent, accent_soft, arrow="\u2192", big=False, padx=(0, 0)):
        WHITE = self.C_WHITE
        TEXT = self.C_TEXT
        MUTED = self.C_MUTED
        BORDER = self.C_BORDER

        card = Frame(parent, bg=WHITE, highlightbackground=BORDER,
                     highlightthickness=1, cursor="hand2")
        card.grid(row=row, column=col, sticky="nsew", padx=padx,
                  pady=(0, 0) if big else (0, 0))
        card.grid_columnconfigure(0, weight=1)

        pad = 22 if big else 16
        inner = Frame(card, bg=WHITE)
        inner.pack(fill=BOTH, expand=True, padx=pad, pady=pad)

        top = Frame(inner, bg=WHITE)
        top.pack(fill=X)

        icon_size = 56 if big else 46
        icon_box = Frame(top, bg=accent_soft, width=icon_size, height=icon_size)
        icon_box.pack(side=LEFT)
        icon_box.pack_propagate(False)
        Label(icon_box, text=icon, bg=accent_soft, fg=accent,
              font=("Segoe UI", 16 if big else 13)).pack(expand=True)

        if big:
            arrow_box = Frame(top, bg=accent, width=32, height=32)
            arrow_box.pack(side=RIGHT)
            arrow_box.pack_propagate(False)
            Label(arrow_box, text=arrow, bg=accent, fg=WHITE,
                  font=("Segoe UI", 11, "bold")).pack(expand=True)

        Label(inner, text=title, bg=WHITE, fg=TEXT,
              font=("Segoe UI", 13 if big else 11, "bold"),
              anchor="w").pack(fill=X, pady=(16 if big else 12, 4), anchor="w")

        Label(inner, text=desc, bg=WHITE, fg=MUTED,
              font=("Segoe UI", 9 if big else 8), justify=LEFT,
              anchor="nw").pack(fill=X, anchor="w")

        def bind_click(widget, callback):
            widget.bind("<Button-1>", lambda e: callback())
            for child in widget.winfo_children():
                bind_click(child, callback)
        bind_click(card, command)

        return card

    # ========================================================
    # Existing navigation functions — functionality preserved
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
        self.app = Train(self.new_window, authenticated=True, owner_email=self.user_email)

    def face_rec(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window, authenticated=True, owner_email=self.user_email)

    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window, authenticated=True, owner_email=self.user_email)

    def developr(self):
        self.new_window = Toplevel(self.root)
        self.app = Developer(self.new_window, authenticated=True)

    def helpSupport(self):
        self.new_window = Toplevel(self.root)
        self.app = Helpsupport(self.new_window, authenticated=True)

    def logout(self):
        if not messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            return

        # Forget the "keep me signed in" session so next launch shows the
        # login screen instead of jumping straight back to this dashboard.
        from Session_utils import clear_session
        clear_session()

        # Close any feature windows this dashboard has open, then rebuild
        # the login screen in the same window instead of exiting the app.
        for widget in self.root.winfo_children():
            widget.destroy()

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