# Face Recognition Attendance System

## Purpose
A modern, centralized Tkinter desktop application designed to streamline student attendance by utilizing computer vision and face recognition technology. The system allows educators and administrators to manage student profiles, train recognition models, and automate attendance tracking via webcam.

## Technologies
- **Python** (v3.8+)
- **Tkinter / ttk** (GUI and UI architecture)
- **OpenCV** (Face detection and recognition)
- **NumPy** (Image matrix processing)
- **Pillow** (Image handling)
- **MySQL** (Database storage)

## Virtual Environment Setup

It is recommended to run this project in an isolated virtual environment.

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

## Dependency Installation

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## .env Configuration

To securely connect to your database, create a `.env` file in the project root. DO NOT commit this file to version control. 

Example `.env` format:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_secure_password
DB_NAME=face_recognizer
```

## MySQL Setup Overview

1. Install MySQL Server.
2. Create a database (e.g., `face_recognizer` as per your `.env`).
3. Ensure the tables (`student`, `attendance`, etc.) are established. The application will initialize the necessary schema configuration via `db_config.py`.

## How to Run the Application

Execute the main entrypoint script:

```bash
python main.py
```

This will launch the login screen, from which you can either log in or register a new administrative account.

## Camera Testing Overview

The Face Recognition and Data Train modules require access to your webcam. Ensure your primary camera is unblocked and permitted in your OS privacy settings. If the camera preview fails to open, verify that no other applications are using it.

## Model Training Overview

1. Navigate to the **Student Panel** to register a student.
2. Capture their photo samples using the "Take Photo Sample" action.
3. Open the **Data Train** module to train the model on the newly gathered dataset.
4. Test the model in the **Face Recognition** module.

## Project Structure

```
Face-Detection-Attendance-System/
├── main.py                 # Application entrypoint & dashboard
├── student.py              # Student management module
├── attendance.py           # Attendance viewing & management module
├── face_recognition.py     # Live face recognition camera module
├── train.py                # Model training module
├── login.py                # Authentication & login module
├── register.py             # User registration module
├── developer.py            # Developer information module
├── helpsupport.py          # Help and support module
├── databaseTest.py         # DB connection diagnostics
├── db_config.py            # DB and schema configuration
├── session_utils.py        # Active session management
│
├── ui/                     # Centralized UI Architecture
│   ├── __init__.py
│   ├── theme.py            # Global colors, fonts, styles
│   ├── components.py       # Reusable UI widgets
│   ├── icons.py            # Centralized icon definitions
│   └── assets.py           # Asset path management
│
├── Images_GUI/             # UI graphics and images
├── models/                 # Pre-trained Haar Cascades / generated LBPH models
├── data_img/               # Captured student face datasets
├── venv/                   # Virtual environment (ignored in git)
├── .env                    # Environment variables (ignored in git)
├── settings.json           # Application preferences
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
