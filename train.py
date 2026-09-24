from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox
from db_config import owner_data_dir, owner_model_path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")

class Train:

    def __init__(self,root, authenticated=False, owner_email=None):
        self.root = root
        if not authenticated:
            from Session_utils import redirect_to_login
            redirect_to_login(root)
            return
        self.owner_email = owner_email
        self.data_dir = owner_data_dir(owner_email)
        self.model_path = owner_model_path(owner_email)
        self.root.geometry("1180x760")
        self.root.minsize(980, 680)
        self.root.title("Data Training • Face Recognition Attendance System")
        try:
            self.root.state("zoomed")
        except Exception:
            pass
        self.root.configure(bg="#F5F8FD")

        BG = "#F5F8FD"
        WHITE = "#FFFFFF"
        BLUE = "#2563EB"
        BLUE_DARK = "#162A63"
        BLUE_SOFT = "#EAF1FF"
        PINK = "#EC4899"
        PINK_SOFT = "#FDF0F8"
        TEAL = "#14B8A6"
        TEAL_SOFT = "#EAFBF8"
        TEXT = "#17305F"
        MUTED = "#6C7FA2"
        BORDER = "#DCE6F3"
        ORANGE = "#F59E0B"
        ORANGE_SOFT = "#FFF6E8"

        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Train.TButton",
            background=BLUE,
            foreground=WHITE,
            relief="flat",
            borderwidth=0,
            padding=(18, 11),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Train.TButton",
            background=[("active", "#1D4ED8"), ("pressed", "#1E40AF")],
        )

        # Root layout
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Header
        header = Frame(
            self.root, bg=WHITE, height=84,
            highlightbackground=BORDER, highlightthickness=1
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)

        brand = Frame(header, bg=WHITE)
        brand.grid(row=0, column=0, sticky="nsw", padx=(24, 16))

        logo = Frame(brand, bg=BLUE, width=50, height=50)
        logo.pack(side=LEFT, pady=16)
        logo.pack_propagate(False)
        Label(logo, text="FR", bg=BLUE, fg=WHITE,
              font=("Segoe UI", 15, "bold")).pack(expand=True)

        brand_copy = Frame(brand, bg=WHITE)
        brand_copy.pack(side=LEFT, padx=(12, 0), pady=14)
        Label(
            brand_copy, text="Face Recognition Attendance System",
            bg=WHITE, fg=BLUE_DARK, font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")
        Label(
            brand_copy, text="Data training",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(2, 0))

        ttk.Button(header, text="Back to Dashboard", command=self.go_back,
                   style="Train.TButton").grid(
                       row=0, column=1, sticky="e", padx=(10, 18), pady=19)

        Label(
            header, text="● READY", bg=WHITE, fg=TEAL,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=2, sticky="e", padx=(0, 24))

        # Main
        content = Frame(self.root, bg=BG)
        content.grid(row=1, column=0, sticky="nsew", padx=24, pady=22)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        hero = Frame(
            content, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        hero.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        hero.grid_columnconfigure(0, weight=1)

        hero_text = Frame(hero, bg=WHITE)
        hero_text.grid(row=0, column=0, sticky="w", padx=28, pady=22)

        Label(
            hero_text, text="Train the recognition model",
            bg=WHITE, fg=TEXT, font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")
        Label(
            hero_text,
            text="Build the LBPH classifier from the captured student face dataset.",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(5, 10))

        line = Canvas(hero_text, bg=WHITE, width=90, height=6, highlightthickness=0)
        line.pack(anchor="w")
        line.create_rectangle(0, 1, 60, 5, fill=BLUE, outline="")
        line.create_rectangle(60, 1, 90, 5, fill=PINK, outline="")

        # Decorative training illustration
        art = Canvas(hero, width=270, height=125, bg=WHITE, highlightthickness=0)
        art.grid(row=0, column=1, padx=(0, 24), pady=10)
        art.create_oval(125, -18, 275, 122, fill="#FFF4E3", outline="")
        art.create_oval(0, 52, 68, 120, fill="#EAFBF8", outline="")
        art.create_rectangle(75, 20, 190, 95, fill=BLUE_SOFT, outline="#C9D9FF", width=2)
        art.create_rectangle(88, 31, 177, 84, fill=WHITE, outline="")
        art.create_rectangle(99, 42, 125, 72, fill=ORANGE_SOFT, outline="")
        art.create_rectangle(136, 42, 165, 72, fill=TEAL_SOFT, outline="")
        art.create_rectangle(103, 46, 121, 51, fill=ORANGE, outline="")
        art.create_rectangle(103, 56, 121, 61, fill=ORANGE, outline="")
        art.create_rectangle(141, 46, 160, 51, fill=TEAL, outline="")
        art.create_rectangle(141, 56, 160, 61, fill=TEAL, outline="")

        workspace = Frame(content, bg=BG)
        workspace.grid(row=1, column=0, sticky="nsew")
        workspace.grid_rowconfigure(0, weight=1)
        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=1)

        # Main training card
        train_card = Frame(
            workspace, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        train_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        train_card.grid_columnconfigure(0, weight=1)

        Label(
            train_card, text="TRAINING CONTROL",
            bg=WHITE, fg=BLUE,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=24, pady=(24, 10))

        icon_box = Frame(train_card, bg=ORANGE_SOFT, width=92, height=92)
        icon_box.pack(pady=(8, 15))
        icon_box.pack_propagate(False)

        icon = Canvas(icon_box, width=92, height=92, bg=ORANGE_SOFT, highlightthickness=0)
        icon.pack()
        icon.create_rectangle(23, 24, 69, 65, fill=ORANGE, outline="")
        icon.create_rectangle(31, 32, 61, 57, fill=WHITE, outline="")
        icon.create_line(38, 39, 54, 39, fill=ORANGE, width=2)
        icon.create_line(38, 45, 56, 45, fill=ORANGE, width=2)
        icon.create_line(38, 51, 51, 51, fill=ORANGE, width=2)

        Label(
            train_card, text="Ready to train",
            bg=WHITE, fg=TEXT, font=("Segoe UI", 16, "bold")
        ).pack()
        Label(
            train_card,
            text="Load captured images, train the LBPH recognizer,\nand create the classifier file.",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 9),
            justify="center"
        ).pack(pady=(7, 22))

        ttk.Button(
            train_card,
            text="Train Dataset",
            command=self.train_classifier,
            style="Train.TButton",
        ).pack(fill=X, padx=54, pady=(0, 12))

        Label(
            train_card,
            text="The existing training process will run as before.",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 8)
        ).pack()

        # Info/status card
        info = Frame(
            workspace, bg=WHITE,
            highlightbackground=BORDER, highlightthickness=1
        )
        info.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        Label(
            info, text="TRAINING PIPELINE",
            bg=WHITE, fg=PINK,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=24, pady=(24, 12))

        pipeline = [
            ("01", "Dataset", "Read images from data_img.", BLUE, BLUE_SOFT),
            ("02", "Grayscale", "Convert images before training.", PINK, PINK_SOFT),
            ("03", "LBPH", "Build the face recognizer.", TEAL, TEAL_SOFT),
            ("04", "Classifier", "Write the generated clf.xml.", ORANGE, ORANGE_SOFT),
        ]

        for num, title, desc, accent, soft in pipeline:
            row = Frame(info, bg=WHITE)
            row.pack(fill=X, padx=24, pady=8)

            badge = Frame(row, bg=soft, width=44, height=44)
            badge.pack(side=LEFT)
            badge.pack_propagate(False)

            Label(
                badge, text=num, bg=soft, fg=accent,
                font=("Segoe UI", 8, "bold")
            ).pack(expand=True)

            text_box = Frame(row, bg=WHITE)
            text_box.pack(side=LEFT, padx=11)
            Label(
                text_box, text=title, bg=WHITE, fg=TEXT,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")
            Label(
                text_box, text=desc, bg=WHITE, fg=MUTED,
                font=("Segoe UI", 8)
            ).pack(anchor="w", pady=(2, 0))

        Frame(info, bg=BORDER, height=1).pack(fill=X, padx=24, pady=(18, 18))

        Label(
            info, text="MODEL OUTPUT",
            bg=WHITE, fg=TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=24)

        output = Frame(info, bg=BLUE_SOFT)
        output.pack(fill=X, padx=24, pady=(10, 0))

        Label(
            output, text="clf.xml",
            bg=BLUE_SOFT, fg=BLUE,
            font=("Consolas", 11, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 3))
        Label(
            output,
            text="Generated by the existing training workflow.",
            bg=BLUE_SOFT, fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w", padx=14, pady=(0, 12))

        footer = Frame(content, bg=BG)
        footer.grid(row=2, column=0, sticky="ew", pady=(14, 0))

        Label(
            footer,
            text="FACE RECOGNITION ATTENDANCE SYSTEM",
            bg=BG, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(side=LEFT)
        Label(
            footer,
            text="MODEL TRAINING",
            bg=BG, fg=ORANGE,
            font=("Segoe UI", 8, "bold")
        ).pack(side=RIGHT)

    def go_back(self):
        self.root.destroy()

    # ==================Create Function of Traing===================
    def train_classifier(self):
        try:
            image_paths = [
                os.path.join(self.data_dir, filename)
                for filename in os.listdir(self.data_dir)
                if filename.lower().endswith((".jpg", ".jpeg", ".png"))
            ]
            if not image_paths:
                messagebox.showwarning(
                    "No training data",
                    "Capture student face samples before training the model.",
                    parent=self.root,
                )
                return

            if not hasattr(cv2, "face"):
                raise RuntimeError(
                    "OpenCV face recognition is unavailable. Install opencv-contrib-python."
                )

            faces = []
            ids = []
            for image_path in image_paths:
                filename = os.path.basename(image_path)
                parts = filename.split(".")
                if len(parts) < 3 or not parts[1].isdigit():
                    continue
                image = Image.open(image_path).convert("L")
                faces.append(np.array(image, "uint8"))
                ids.append(int(parts[1]))

            if not faces:
                messagebox.showwarning(
                    "Invalid training data",
                    "No valid student face filenames were found in the dataset.",
                    parent=self.root,
                )
                return

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.train(faces, np.array(ids))
            recognizer.write(self.model_path)
            messagebox.showinfo(
                "Training complete",
                f"Training completed with {len(faces)} face samples.",
                parent=self.root,
            )
        except Exception as error:
            messagebox.showerror(
                "Training failed",
                str(error),
                parent=self.root,
            )
        finally:
            cv2.destroyAllWindows()




if __name__ == "__main__":
    root=Tk()
    obj=Train(root)
    root.mainloop()