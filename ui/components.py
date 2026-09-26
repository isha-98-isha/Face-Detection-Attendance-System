"""
UI Components for the Face Detection Attendance System.
Reusable layouts and widgets.
"""
import tkinter as tk
from tkinter import ttk
from ui.theme import COLORS, FONTS, SPACING

def create_header(parent, title_text, subtitle_text=None):
    """Creates a standardized page header."""
    header_frame = ttk.Frame(parent, style="TFrame")
    
    title = ttk.Label(header_frame, text=title_text, style="Title.TLabel")
    title.pack(anchor="w", pady=(0, SPACING["xs"]))
    
    if subtitle_text:
        subtitle = ttk.Label(header_frame, text=subtitle_text, style="Muted.TLabel")
        subtitle.pack(anchor="w")
        
    return header_frame

def create_card(parent):
    """Creates a card container for grouping related content."""
    card = tk.Frame(parent, bg=COLORS["bg_card"], highlightbackground=COLORS["border"], highlightthickness=1, bd=0)
    return card

def create_section_header(parent, text):
    """Creates a subheader for a section within a page or card."""
    lbl = ttk.Label(parent, text=text, style="Header.TLabel")
    return lbl

def create_info_row(parent, label_text, value_text):
    """Creates a two-column row for displaying label-value pairs."""
    row = ttk.Frame(parent, style="TFrame")
    lbl = ttk.Label(row, text=label_text, style="body_bold.TLabel", font=FONTS["body_bold"])
    lbl.pack(side="left", padx=(0, SPACING["sm"]))
    val = ttk.Label(row, text=value_text)
    val.pack(side="left")
    return row

def create_primary_button(parent, text, command, **kwargs):
    btn = ttk.Button(parent, text=text, command=command, style="Primary.TButton", **kwargs)
    return btn

def create_secondary_button(parent, text, command, **kwargs):
    btn = ttk.Button(parent, text=text, command=command, style="Secondary.TButton", **kwargs)
    return btn

def create_danger_button(parent, text, command, **kwargs):
    btn = ttk.Button(parent, text=text, command=command, style="Danger.TButton", **kwargs)
    return btn

def create_status_badge(parent, text, status="success"):
    """Creates a small colored status badge."""
    style = "SuccessBadge.TLabel" if status == "success" else "DangerBadge.TLabel"
    # Fallbacks for other statuses
    if status not in ["success", "danger"]:
        style = "TLabel" 
    lbl = ttk.Label(parent, text=text, style=style)
    return lbl
