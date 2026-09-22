import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_FILE = os.path.join(BASE_DIR, "session.json")


def save_session(email):
    """Persist the 'keep me signed in' session for this email."""
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump({"email": email}, f)
    except Exception:
        pass


def load_session():
    """Return the remembered email, or None if there is no valid session."""
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
        return data.get("email")
    except Exception:
        return None


def clear_session():
    """Forget any remembered session (used on logout or unchecked login)."""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
    except Exception:
        pass


def redirect_to_login(root):
    """Replace an unauthorized page with the normal login entry screen."""
    for widget in root.winfo_children():
        widget.destroy()

    from login import Login
    Login(root)