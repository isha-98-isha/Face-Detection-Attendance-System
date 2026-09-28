import os
from ui.theme import COLORS, apply_theme, FONTS
from ui.components import *
from ui.icons import ICONS
from ui.assets import get_image_path, load_image, BASE_DIR
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")


class Developer:
    def __init__(self, root, authenticated=False):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.root.title("Developers - Face Recognition Attendance System")
        self.root.geometry("1180x760")
        self.root.minsize(900, 620)
        try:
            self.root.state("zoomed")
        except Exception:
            pass

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

        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Developer.Primary.TButton", background=BLUE, foreground=WHITE,
            relief="flat", borderwidth=0, padding=(16, 9),
            font=("Segoe UI", 10, "bold"))
        style.map("Developer.Primary.TButton", background=[("active", "#1D4ED8")])
        style.configure(
            "Developer.Secondary.TButton", background=WHITE, foreground=TEXT,
            relief="flat", borderwidth=1, bordercolor=BORDER, padding=(16, 9),
            font=("Segoe UI", 10, "bold"))
        style.map("Developer.Secondary.TButton",
            background=[("active", "#F8FAFC"), ("pressed", "#F1F5F9")],
            bordercolor=[("focus", BLUE)])

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = Frame(self.root, bg=WHITE, height=82)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        try:
            _logo = Image.open(os.path.join(IMAGE_DIR, "Face-Recognition-Software.png"))
            _logo = _logo.resize((44, 44), Image.LANCZOS)
            self._hdr_logo = ImageTk.PhotoImage(_logo)
            mark = Label(header, image=self._hdr_logo, bg=WHITE)
            mark.grid(row=0, column=0, padx=(24, 14), pady=17)
        except Exception:
            mark = Frame(header, bg=BLUE, width=48, height=48)
            mark.grid(row=0, column=0, padx=(24, 14), pady=17)
            mark.grid_propagate(False)
            Label(mark, text="FR", bg=BLUE, fg=WHITE,
                  font=("Segoe UI", 14, "bold")).pack(expand=True)

        brand = Frame(header, bg=WHITE)
        brand.grid(row=0, column=1, sticky="nsw", pady=13)
        Label(brand, text="Face Recognition Attendance System", bg=WHITE,
              fg=DARK_BLUE, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        Label(brand, text="Project and developer information", bg=WHITE,
              fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
        ttk.Button(header, text="Back to Dashboard", command=self.root.destroy,
                   style="Developer.Secondary.TButton").grid(
                       row=0, column=2, padx=(10, 24), pady=19)
        Frame(header, bg=BORDER, height=1).place(
            relx=0, rely=1.0, relwidth=1.0, anchor="sw")

        content = Frame(self.root, bg=BG)
        content.grid(row=1, column=0, sticky="nsew", padx=24, pady=22)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        intro = Frame(content, bg=BG)
        intro.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        Label(intro, text="Meet the developers", bg=BG, fg=TEXT,
              font=("Segoe UI", 23, "bold")).pack(anchor="w")
        Label(intro, text="The people behind this attendance management project.",
              bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        cards = Frame(content, bg=BG)
        cards.grid(row=1, column=0, sticky="nsew")
        cards.grid_columnconfigure(0, weight=1, uniform="developer")
        cards.grid_columnconfigure(1, weight=1, uniform="developer")
        cards.grid_rowconfigure(0, weight=1)

        developers = [
            ("phong.jpg", "Bhumika Chaudhari", "Developer", BLUE, SOFT_BLUE),
            ("developer.jpg", "Isha Chaudhari", "Developer", PINK, SOFT_PINK),
        ]
        self.photos = []
        for column, (filename, name, role, accent, soft) in enumerate(developers):
            card = Frame(cards, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=0, column=column, sticky="nsew",
                      padx=(0 if column == 0 else 9, 9 if column == 0 else 0))
            Frame(card, bg=accent, height=8).pack(fill=X)

            photo_frame = Frame(card, bg=soft, width=190, height=190)
            photo_frame.pack(pady=(42, 24))
            photo_frame.pack_propagate(False)
            try:
                image = Image.open(os.path.join(IMAGE_DIR, filename)).resize(
                    (180, 180), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.photos.append(photo)
                Label(photo_frame, image=photo, bg=soft).pack(expand=True)
            except Exception:
                Label(photo_frame, text="PHOTO", bg=soft, fg=accent,
                      font=("Segoe UI", 16, "bold")).pack(expand=True)

            Label(card, text=name, bg=WHITE, fg=TEXT,
                  font=("Segoe UI", 17, "bold")).pack()
            Label(card, text=role, bg=WHITE, fg=accent,
                  font=("Segoe UI", 10, "bold")).pack(pady=(5, 0))
            Frame(card, bg=BORDER, height=1).pack(fill=X, padx=32, pady=24)
            Label(card, text="Face Recognition Attendance System",
                  bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(pady=(0, 28))


if __name__ == "__main__":
    root = Tk()
    Developer(root)
    root.mainloop()
