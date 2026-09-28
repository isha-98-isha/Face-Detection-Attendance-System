import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

from db_config import DB_CONFIG


class Profile:
    def __init__(
        self,
        root,
        user_name="User",
        user_email="",
        on_logout=None,
        on_theme_toggle=None,
        theme_mode="light",
    ):
        self.root = root
        self.user_name = user_name
        self.user_email = user_email
        self.on_logout = on_logout
        self.on_theme_toggle = on_theme_toggle

        self.theme_mode = tk.StringVar(value=theme_mode)

        self.root.title("Profile & Settings")
        self.root.geometry("900x700+250+80")
        self.root.minsize(700, 600)
        self.root.configure(bg="#F5F7FB")

        # Open the profile page maximized.
        try:
            self.root.state("zoomed")
        except Exception:
            pass

        self._build_styles()
        self._build_ui()
        self._apply_theme()

    # =========================================================
    # Styles
    # =========================================================

    def _build_styles(self):
        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Profile.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 7),
        )

        style.configure(
            "ProfileCheck.TCheckbutton",
            font=("Segoe UI", 9, "bold"),
        )

    # =========================================================
    # Colors
    # =========================================================

    def _colors(self):
        if self.theme_mode.get() == "dark":
            return {
                "bg": "#0F172A",
                "card": "#1E293B",
                "text": "#F8FAFC",
                "muted": "#94A3B8",
                "border": "#334155",
                "blue": "#60A5FA",
                "blue_soft": "#1E3A5F",
                "button": "#2563EB",
                "button_text": "#FFFFFF",
                "logout": "#DC2626",
                "entry": "#0F172A",
            }

        return {
            "bg": "#F5F7FB",
            "card": "#FFFFFF",
            "text": "#172033",
            "muted": "#64748B",
            "border": "#E2E8F0",
            "blue": "#2563EB",
            "blue_soft": "#DBEAFE",
            "button": "#2563EB",
            "button_text": "#FFFFFF",
            "logout": "#DC2626",
            "entry": "#FFFFFF",
        }

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self):
        # Header
        self.header = tk.Frame(self.root)
        self.header.pack(fill="x")

        self.title_frame = tk.Frame(self.header)
        self.title_frame.pack(side="left", padx=28, pady=16)

        self.title_label = tk.Label(
            self.title_frame,
            text="Profile",
            font=("Segoe UI", 18, "bold"),
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = tk.Label(
            self.title_frame,
            text="Manage your account and application settings",
            font=("Segoe UI", 9),
        )
        self.subtitle_label.pack(anchor="w", pady=(3, 0))

        # Main content
        self.content = tk.Frame(self.root)
        self.content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(0, 10),
        )

        # Profile card
        self.profile_card = tk.Frame(
            self.content,
            highlightthickness=1,
        )
        self.profile_card.pack(fill="x")

        self.profile_inner = tk.Frame(self.profile_card)
        self.profile_inner.pack(fill="x", padx=24, pady=24)

        self.avatar = tk.Frame(
            self.profile_inner,
            width=64,
            height=64,
        )
        self.avatar.pack(side="left")
        self.avatar.pack_propagate(False)

        self.avatar_label = tk.Label(
            self.avatar,
            text="👤",
            font=("Segoe UI", 24),
        )
        self.avatar_label.pack(expand=True)

        self.user_info = tk.Frame(self.profile_inner)
        self.user_info.pack(side="left", padx=(18, 0))

        self.username_caption = tk.Label(
            self.user_info,
            text="Username",
            font=("Segoe UI", 9),
        )
        self.username_caption.pack(anchor="w")

        self.username_label = tk.Label(
            self.user_info,
            text=self.user_name,
            font=("Segoe UI", 14, "bold"),
        )
        self.username_label.pack(anchor="w", pady=(2, 8))

        self.email_caption = tk.Label(
            self.user_info,
            text="Email",
            font=("Segoe UI", 9),
        )
        self.email_caption.pack(anchor="w")

        self.email_label = tk.Label(
            self.user_info,
            text=self.user_email or "Not available",
            font=("Segoe UI", 10),
        )
        self.email_label.pack(anchor="w", pady=(2, 0))

        # Security card
        self.security_card = tk.Frame(
            self.content,
            highlightthickness=1,
        )
        self.security_card.pack(fill="x", pady=(18, 0))

        self.security_inner = tk.Frame(self.security_card)
        self.security_inner.pack(fill="x", padx=24, pady=20)

        self.security_title = tk.Label(
            self.security_inner,
            text="Security",
            font=("Segoe UI", 12, "bold"),
        )
        self.security_title.pack(anchor="w")

        self.security_description = tk.Label(
            self.security_inner,
            text="Change your account password.",
            font=("Segoe UI", 9),
        )
        self.security_description.pack(anchor="w", pady=(4, 14))

        self.reset_button = ttk.Button(
            self.security_inner,
            text="Reset Password",
            style="Profile.TButton",
            command=self.open_password_reset,
        )
        self.reset_button.pack(anchor="w")

        # Settings card
        self.settings_card = tk.Frame(
            self.content,
            highlightthickness=1,
        )
        self.settings_card.pack(fill="x", pady=(18, 0))

        self.settings_inner = tk.Frame(self.settings_card)
        self.settings_inner.pack(fill="x", padx=24, pady=20)

        self.settings_title = tk.Label(
            self.settings_inner,
            text="Settings",
            font=("Segoe UI", 12, "bold"),
        )
        self.settings_title.pack(anchor="w")

        self.theme_row = tk.Frame(self.settings_inner)
        self.theme_row.pack(fill="x", pady=(14, 0))

        self.theme_text = tk.Frame(self.theme_row)

        self.theme_text.pack(side="left")

        self.theme_title = tk.Label(
            self.theme_text,
            text="Theme",
            font=("Segoe UI", 10, "bold"),
        )
        self.theme_title.pack(anchor="w")

        self.theme_description = tk.Label(
            self.theme_text,
            text="Switch between light and dark appearance.",
            font=("Segoe UI", 8),
        )
        self.theme_description.pack(anchor="w", pady=(2, 0))

        self.theme_check = ttk.Checkbutton(
            self.theme_row,
            text="Dark mode",
            variable=self.theme_mode,
            onvalue="dark",
            offvalue="light",
            style="ProfileCheck.TCheckbutton",
            command=self._theme_changed,
        )
        self.theme_check.pack(side="right")

        # ---------------------------------------------------------
        # Fixed bottom action bar
        # ---------------------------------------------------------
        # Keeping this outside the scrolling content guarantees that
        # Logout stays visible even when the window is resized smaller.
        self.action_bar = tk.Frame(self.root)
        self.action_bar.pack(
            side="bottom",
            fill="x",
            padx=28,
            pady=(4, 20),
        )

        self.logout_button = ttk.Button(
            self.action_bar,
            text="Logout",
            style="Profile.TButton",
            command=self._logout,
        )
        self.logout_button.pack(side="right")

    # =========================================================
    # Theme
    # =========================================================

    def _theme_changed(self):
        self._apply_theme()

        if self.on_theme_toggle:
            self.on_theme_toggle(self.theme_mode.get())

    def _apply_theme(self):
        c = self._colors()

        self.root.configure(bg=c["bg"])

        # Main containers
        frames = [
            self.header,
            self.title_frame,
            self.content,
            self.profile_card,
            self.profile_inner,
            self.avatar,
            self.user_info,
            self.security_card,
            self.security_inner,
            self.settings_card,
            self.settings_inner,
            self.theme_row,
            self.theme_text,
            self.action_bar,
        ]

        for widget in frames:
            widget.configure(bg=c["card"] if "card" in str(widget) else c["bg"])

        # Explicit card/background assignments
        self.header.configure(bg=c["card"])
        self.title_frame.configure(bg=c["card"])
        self.content.configure(bg=c["bg"])
        self.profile_card.configure(bg=c["card"], highlightbackground=c["border"])
        self.profile_inner.configure(bg=c["card"])
        self.avatar.configure(bg=c["blue_soft"])
        self.user_info.configure(bg=c["card"])

        self.security_card.configure(
            bg=c["card"],
            highlightbackground=c["border"],
        )
        self.security_inner.configure(bg=c["card"])

        self.settings_card.configure(
            bg=c["card"],
            highlightbackground=c["border"],
        )
        self.settings_inner.configure(bg=c["card"])

        self.theme_row.configure(bg=c["card"])
        self.theme_text.configure(bg=c["card"])

        self.action_bar.configure(bg=c["bg"])

        # Labels
        labels = [
            (self.title_label, c["text"]),
            (self.subtitle_label, c["muted"]),
            (self.avatar_label, c["blue"]),
            (self.username_caption, c["muted"]),
            (self.username_label, c["text"]),
            (self.email_caption, c["muted"]),
            (self.email_label, c["text"]),
            (self.security_title, c["text"]),
            (self.security_description, c["muted"]),
            (self.settings_title, c["text"]),
            (self.theme_title, c["text"]),
            (self.theme_description, c["muted"]),
        ]

        for widget, fg in labels:
            widget.configure(
                bg=(
                    c["blue_soft"]
                    if widget == self.avatar_label
                    else c["card"]
                ),
                fg=fg,
            )

        # ttk styles
        style = ttk.Style(self.root)

        style.configure(
            "Profile.TButton",
            background=c["button"],
            foreground=c["button_text"],
            font=("Segoe UI", 9, "bold"),
            padding=(12, 7),
        )

        style.map(
            "Profile.TButton",
            background=[
                ("active", c["button"]),
                ("pressed", c["button"]),
            ],
            foreground=[
                ("active", c["button_text"]),
                ("pressed", c["button_text"]),
            ],
        )

        style.configure(
            "ProfileCheck.TCheckbutton",
            background=c["card"],
            foreground=c["text"],
            font=("Segoe UI", 9, "bold"),
        )

        style.map(
            "ProfileCheck.TCheckbutton",
            background=[
                ("active", c["card"]),
                ("pressed", c["card"]),
            ],
            foreground=[
                ("active", c["text"]),
                ("pressed", c["text"]),
            ],
        )

        self._update_logout_style(c)

    def _update_logout_style(self, c):
        style = ttk.Style(self.root)

        style.configure(
            "ProfileLogout.TButton",
            background=c["logout"],
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            padding=(12, 7),
        )

        style.map(
            "ProfileLogout.TButton",
            background=[
                ("active", c["logout"]),
                ("pressed", c["logout"]),
            ],
            foreground=[
                ("active", "#FFFFFF"),
                ("pressed", "#FFFFFF"),
            ],
        )

        self.logout_button.configure(style="ProfileLogout.TButton")

    # =========================================================
    # Logout
    # =========================================================

    def _logout(self):
        confirm = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out?",
            parent=self.root,
        )

        if not confirm:
            return

        if self.on_logout:
            self.on_logout()

    # =========================================================
    # Password Reset
    # =========================================================

    def open_password_reset(self):
        reset_window = tk.Toplevel(self.root)
        reset_window.title("Reset Password")
        reset_window.geometry("420x360+460+200")
        reset_window.resizable(False, False)
        reset_window.configure(bg="#FFFFFF")

        tk.Label(
            reset_window,
            text="Reset Password",
            bg="#FFFFFF",
            fg="#172554",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(24, 20))

        form = tk.Frame(reset_window, bg="#FFFFFF")
        form.pack(fill="x", padx=40)

        tk.Label(
            form,
            text="Current Password",
            bg="#FFFFFF",
            fg="#172033",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        current_password = ttk.Entry(form, show="*")
        current_password.pack(fill="x", pady=(5, 14))

        tk.Label(
            form,
            text="New Password",
            bg="#FFFFFF",
            fg="#172033",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        new_password = ttk.Entry(form, show="*")
        new_password.pack(fill="x", pady=(5, 14))

        tk.Label(
            form,
            text="Confirm New Password",
            bg="#FFFFFF",
            fg="#172033",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        confirm_password = ttk.Entry(form, show="*")
        confirm_password.pack(fill="x", pady=(5, 20))

        def change_password():
            current = current_password.get()
            new = new_password.get()
            confirm = confirm_password.get()

            if not current or not new or not confirm:
                messagebox.showerror(
                    "Error",
                    "Please fill all password fields.",
                    parent=reset_window,
                )
                return

            if len(new) < 8:
                messagebox.showerror(
                    "Error",
                    "Password must be at least 8 characters long.",
                    parent=reset_window,
                )
                return

            if new != confirm:
                messagebox.showerror(
                    "Error",
                    "New passwords do not match.",
                    parent=reset_window,
                )
                return

            conn = None
            cursor = None

            try:
                conn = mysql.connector.connect(**DB_CONFIG)
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT pwd FROM regteach WHERE email=%s",
                    (self.user_email,),
                )
                row = cursor.fetchone()

                if not row:
                    messagebox.showerror(
                        "Error",
                        "User account was not found.",
                        parent=reset_window,
                    )
                    return

                if current != row[0]:
                    messagebox.showerror(
                        "Error",
                        "Current password is incorrect.",
                        parent=reset_window,
                    )
                    return

                cursor.execute(
                    "UPDATE regteach SET pwd=%s WHERE email=%s",
                    (new, self.user_email),
                )

                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Password changed successfully.",
                    parent=reset_window,
                )

                reset_window.destroy()

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"Unable to change password:\n{error}",
                    parent=reset_window,
                )

            finally:
                if cursor is not None:
                    cursor.close()

                if conn is not None:
                    conn.close()