"""
camera_config.py — Central camera source management.

Reads/writes camera settings to camera_settings.json in the project root.
Both student.py (photo capture) and face_recognition.py use get_camera_source()
so changing the source here affects the whole app automatically.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_SETTINGS_FILE = os.path.join(BASE_DIR, "camera_settings.json")

_DEFAULTS = {
    "source_type": "local",   # "local" | "ip_webcam"
    "local_index": 0,         # camera index for local webcam (usually 0)
    "ip_url": "",             # e.g. "http://192.168.1.5:8080/video"
}


def _load() -> dict:
    if os.path.exists(_SETTINGS_FILE):
        try:
            with open(_SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Fill in any missing keys with defaults
            return {**_DEFAULTS, **data}
        except Exception:
            pass
    return dict(_DEFAULTS)


def _save(settings: dict) -> None:
    with open(_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def get_camera_source():
    """
    Returns the value to pass to cv2.VideoCapture().
    - Local webcam  → int index (e.g. 0)
    - IP Webcam     → stream URL string (e.g. "http://192.168.1.5:8080/video")
    """
    s = _load()
    if s["source_type"] == "ip_webcam":
        url = s.get("ip_url", "").strip()
        if not url:
            raise ValueError(
                "IP Webcam is selected but no URL is set.\n"
                "Go to Face Recognition → Camera Settings and enter your phone's stream URL."
            )
        return url
    return int(s.get("local_index", 0))


def get_settings() -> dict:
    return _load()


def save_settings(source_type: str, local_index: int = 0, ip_url: str = "") -> None:
    _save({
        "source_type": source_type,
        "local_index": local_index,
        "ip_url": ip_url.strip(),
    })
