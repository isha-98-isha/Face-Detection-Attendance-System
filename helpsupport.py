import os
import webbrowser
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")


class Helpsupport:
    def __init__(self, root, authenticated=False):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.root.title("Help and Support - Face Recognition Attendance System")
        self.root.geometry("1180x760")
        self.root.minsize(900, 620)
        try:
            self.root.state("zoomed")
        except Exception:
            pass

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

        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure(
            "Help.Secondary.TButton", background=WHITE, foreground=TEXT,
            relief="flat", borderwidth=1, bordercolor=BORDER, padding=(16, 9),
            font=("Segoe UI", 10, "bold"))
        style.map("Help.Secondary.TButton", background=[("active", "#F8FAFC")])
        style.configure(
            "Help.Primary.TButton", background=BLUE, foreground=WHITE,
            relief="flat", borderwidth=0, padding=(14, 9),
            font=("Segoe UI", 10, "bold"))
        style.map("Help.Primary.TButton", background=[("active", "#1D4ED8")])

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = Frame(self.root, bg=WHITE, height=82)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        mark = Frame(header, bg=BLUE, width=48, height=48)
        mark.grid(row=0, column=0, padx=(24, 14), pady=17)
        mark.grid_propagate(False)
        Label(mark, text="FR", bg=BLUE, fg=WHITE,
              font=("Segoe UI", 14, "bold")).pack(expand=True)

        brand = Frame(header, bg=WHITE)
        brand.grid(row=0, column=1, sticky="nsw", pady=13)
        Label(brand, text="Face Recognition Attendance System", bg=WHITE,
              fg=DARK_BLUE, font=("Segoe UI", 18, "bold")).pack(anchor="w")
        Label(brand, text="Support, resources and project links", bg=WHITE,
              fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(2, 0))
        ttk.Button(header, text="Back to Dashboard", command=self.root.destroy,
                   style="Help.Secondary.TButton").grid(
                       row=0, column=2, padx=(10, 24), pady=19)
        Frame(header, bg=BORDER, height=1).place(
            relx=0, rely=1.0, relwidth=1.0, anchor="sw")

        content = Frame(self.root, bg=BG)
        content.grid(row=1, column=0, sticky="nsew", padx=24, pady=22)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        intro = Frame(content, bg=BG)
        intro.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        Label(intro, text="How can we help?", bg=BG, fg=TEXT,
              font=("Segoe UI", 23, "bold")).pack(anchor="w")
        Label(intro, text="Find project resources or contact the team through the links below.",
              bg=BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))

        cards = Frame(content, bg=BG)
        cards.grid(row=1, column=0, sticky="nsew")
        for column in range(3):
            cards.grid_columnconfigure(column, weight=1, uniform="help")
        cards.grid_rowconfigure(0, weight=1)

        links = [
            ("web.png", "Project Reference", "Read the face-recognition attendance reference material.",
             self.website, BLUE, SOFT_BLUE),
            ("yt.png", "Video Resources", "Open video tutorials and related learning resources.",
             self.youtube, PINK, SOFT_PINK),
            ("gmail.png", "Contact Support", "Open Gmail to contact the project support team.",
             self.gmail, BLUE, SOFT_BLUE),
        ]
        self.photos = []
        for column, (filename, title, description, command, accent, soft) in enumerate(links):
            card = Frame(cards, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
            card.grid(row=0, column=column, sticky="nsew",
                      padx=(0 if column == 0 else 8, 8 if column < 2 else 0))
            Frame(card, bg=accent, height=8).pack(fill=X)

            image_box = Frame(card, bg=soft, width=160, height=160)
            image_box.pack(pady=(38, 25))
            image_box.pack_propagate(False)
            try:
                image = Image.open(os.path.join(IMAGE_DIR, filename)).resize(
                    (150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.photos.append(photo)
                Label(image_box, image=photo, bg=soft).pack(expand=True)
            except Exception:
                Label(image_box, text="LINK", bg=soft, fg=accent,
                      font=("Segoe UI", 16, "bold")).pack(expand=True)

            Label(card, text=title, bg=WHITE, fg=TEXT,
                  font=("Segoe UI", 15, "bold")).pack()
            Label(card, text=description, bg=WHITE, fg=MUTED,
                  font=("Segoe UI", 9), wraplength=230, justify="center").pack(
                      padx=20, pady=(8, 22))
            ttk.Button(card, text="Open resource", command=command,
                       style="Help.Primary.TButton").pack(fill=X, padx=36, pady=(0, 30))

    def website(self):
        webbrowser.open(
            "https://www.researchgate.net/publication/341876647_Face_Recognition_based_Attendance_Management_System"
        )

    def youtube(self):
        webbrowser.open("https://www.youtube.com/")

    def gmail(self):
        webbrowser.open("https://www.gmail.com")


if __name__ == "__main__":
    root = Tk()
    Helpsupport(root)
    root.mainloop()
