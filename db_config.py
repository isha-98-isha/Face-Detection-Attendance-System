import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_env_file():
    env_path = os.path.join(BASE_DIR, ".env")

    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "face_recognition"),
    "port": int(os.getenv("DB_PORT", "3306")),
}


def owner_key(owner_email):
    return hashlib.sha256(owner_email.encode("utf-8")).hexdigest()[:16]


def owner_data_dir(owner_email):
    path = os.path.join(BASE_DIR, "data_img", owner_key(owner_email))
    os.makedirs(path, exist_ok=True)
    return path


def owner_model_path(owner_email):
    model_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(model_dir, exist_ok=True)
    return os.path.join(model_dir, f"clf_{owner_key(owner_email)}.xml")


def owner_attendance_path(owner_email):
    return os.path.join(BASE_DIR, f"attendance_{owner_key(owner_email)}.csv")


def ensure_owner_columns():
    """Add the tenant key used to isolate each teacher's records."""
    import mysql.connector

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    try:
        for table in ("student", "stdattendance"):
            try:
                cursor.execute(
                    f"ALTER TABLE {table} ADD COLUMN Owner_Email VARCHAR(255) NULL"
                )
            except mysql.connector.Error as error:
                if getattr(error, "errno", None) != 1060:
                    raise
        conn.commit()
    finally:
        cursor.close()
        conn.close()