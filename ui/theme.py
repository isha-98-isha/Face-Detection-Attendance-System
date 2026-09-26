"""
Theme definitions for the Face Detection Attendance System.
Contains colors, fonts, spacing, and styles.
"""
from tkinter import ttk
import tkinter as tk

# Visual system defined by requirements
COLORS = {
    "primary": "#2563EB",
    "primary_dark": "#1d4ed8",
    "primary_light": "#EFF6FF",
    "secondary": "#172554",
    "accent_pink": "#EC4899",
    "accent_pink_soft": "#FDF2F8",
    "accent_teal": "#14B8A6",
    "accent_purple": "#7C3AED",
    "accent_orange": "#F59E0B",
    "bg_main": "#F7F9FC",
    "bg_card": "#FFFFFF",
    "text_main": "#1E293B",
    "text_muted": "#64748B",
    "border": "#E2E8F0",
    "success": "#10B981",
    "danger": "#DC2626",
    "white": "#FFFFFF"
}

FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "header": ("Segoe UI", 18, "bold"),
    "subheader": ("Segoe UI", 14, "bold"),
    "body": ("Segoe UI", 11),
    "body_bold": ("Segoe UI", 11, "bold"),
    "small": ("Segoe UI", 9)
}

SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "xxl": 48
}

def apply_theme(root):
    """Applies the central theme styles to the provided root or Toplevel."""
    style = ttk.Style(root)
    
    # Configure colors
    root.configure(bg=COLORS["bg_main"])
    
    # Base TFrame
    style.configure("TFrame", background=COLORS["bg_main"])
    
    # Card TFrame
    style.configure("Card.TFrame", background=COLORS["bg_card"], borderwidth=1, relief="solid", bordercolor=COLORS["border"])
    
    # Labels
    style.configure("TLabel", background=COLORS["bg_main"], foreground=COLORS["text_main"], font=FONTS["body"])
    style.configure("Title.TLabel", font=FONTS["title"], foreground=COLORS["text_main"])
    style.configure("Header.TLabel", font=FONTS["header"], foreground=COLORS["secondary"])
    style.configure("Subheader.TLabel", font=FONTS["subheader"], foreground=COLORS["text_main"])
    style.configure("Muted.TLabel", foreground=COLORS["text_muted"], font=FONTS["small"])
    
    # Primary Button
    style.configure("Primary.TButton", 
                    background=COLORS["primary"], 
                    foreground=COLORS["white"], 
                    font=FONTS["body_bold"],
                    padding=(SPACING["md"], SPACING["sm"]))
    style.map("Primary.TButton", 
              background=[("active", COLORS["primary_dark"])])
              
    # Secondary Button
    style.configure("Secondary.TButton", 
                    background=COLORS["secondary"], 
                    foreground=COLORS["white"], 
                    font=FONTS["body_bold"],
                    padding=(SPACING["md"], SPACING["sm"]))
    style.map("Secondary.TButton", 
              background=[("active", "#1e3a8a")]) # a bit lighter navy
              
    # Danger Button
    style.configure("Danger.TButton", 
                    background=COLORS["danger"], 
                    foreground=COLORS["white"], 
                    font=FONTS["body_bold"],
                    padding=(SPACING["md"], SPACING["sm"]))
    style.map("Danger.TButton", 
              background=[("active", "#b91c1c")])
              
    # Entries
    style.configure("TEntry", padding=SPACING["sm"], font=FONTS["body"])
    
    # Combobox
    style.configure("TCombobox", padding=SPACING["sm"], font=FONTS["body"])
    
    # Treeview
    style.configure("Treeview", 
                    background=COLORS["bg_card"],
                    foreground=COLORS["text_main"],
                    rowheight=30,
                    fieldbackground=COLORS["bg_card"],
                    font=FONTS["body"])
    style.map("Treeview", background=[("selected", COLORS["primary_light"])], foreground=[("selected", COLORS["primary"])])
    
    # Treeview Heading
    style.configure("Treeview.Heading", 
                    background=COLORS["bg_main"], 
                    foreground=COLORS["text_main"], 
                    font=FONTS["body_bold"],
                    padding=SPACING["sm"])
                    
    # Status badges
    style.configure("SuccessBadge.TLabel", background=COLORS["success"], foreground=COLORS["white"], padding=(SPACING["sm"], SPACING["xs"]), font=FONTS["small"])
    style.configure("DangerBadge.TLabel", background=COLORS["danger"], foreground=COLORS["white"], padding=(SPACING["sm"], SPACING["xs"]), font=FONTS["small"])
    
    return style
