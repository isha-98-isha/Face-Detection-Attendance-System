import os
from tkinter import* 
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import pymysql
import re  # Adding regex for validation
from db_config import DB_CONFIG
pymysql.install_as_MySQLdb()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "Images_GUI")

class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1366x768+0+0")

        # ============ Variables =================
        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_cnum=StringVar()
        self.var_email=StringVar()
        self.var_ssq=StringVar()
        self.var_sa=StringVar()
        self.var_pwd=StringVar()
        self.var_cpwd=StringVar()
        self.var_check=IntVar()

        self.bg = ImageTk.PhotoImage(file=os.path.join(IMAGE_DIR, "bgReg.jpg"))
        
        lb1_bg=Label(self.root,image=self.bg)
        lb1_bg.place(x=0,y=0, relwidth=1,relheight=1)

        frame= Frame(self.root,bg="#F2F2F2")
        frame.place(x=190,y=50,width=900,height=580)
        
        reg_lb = Label(frame,text="Welcome to Face Detection Attendance System",font=("times new roman",25,"bold"),fg="#03045e")
        reg_lb.place(x=140,y=20)
        

        get_str = Label(frame,text="Registration",font=("times new roman",30,"bold"),fg="#002B53",bg="#F2F2F2")
        get_str.place(x=350,y=130)

        #label1 
        fname =lb1= Label(frame,text="First Name:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        fname.place(x=100,y=200)

        #entry1 
        self.txtuser=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15,"bold"))
        self.txtuser.place(x=103,y=225,width=270)


        #label2 
        lname =lb1= Label(frame,text="Last Name:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        lname.place(x=100,y=270)

        #entry2 
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15,"bold"))
        self.txtpwd.place(x=103,y=295,width=270)

        # ==================== section 2 -------- 2nd Columan===================

        #label1 
        cnum =lb1= Label(frame,text="Contact No:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        cnum.place(x=530,y=200)

        #entry1 
        self.txtuser=ttk.Entry(frame,textvariable=self.var_cnum,font=("times new roman",15,"bold"))
        self.txtuser.place(x=533,y=225,width=270)


        #label2 
        email =lb1= Label(frame,text="Email:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        email.place(x=530,y=270)

        #entry2 - Adding a placeholder text for email
        self.txtemail=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15,"bold"))
        self.txtemail.place(x=533,y=295,width=270)
        self.var_email.set("example@gmail.com")  # Placeholder text
        
        # Bind focus events to clear/restore placeholder
        self.txtemail.bind("<FocusIn>", self.on_email_focus_in)
        self.txtemail.bind("<FocusOut>", self.on_email_focus_out)

        # ========================= Section 3 --- 1 Columan=================

        #label1 
        ssq =lb1= Label(frame,text="Select Security Question:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        ssq.place(x=100,y=350)

        #Combo Box1
        self.combo_security = ttk.Combobox(frame,textvariable=self.var_ssq,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security["values"]=("Select","Your Date of Birth","Your Nick Name","Your Favorite Book")
        self.combo_security.current(0)
        self.combo_security.place(x=103,y=375,width=270)


        #label2 
        sa =lb1= Label(frame,text="Security Answer:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        sa.place(x=100,y=420)

        #entry2 
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_sa,font=("times new roman",15,"bold"))
        self.txtpwd.place(x=103,y=445,width=270)

        # ========================= Section 4-----Column 2=============================

        #label1 
        pwd =lb1= Label(frame,text="Password:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        pwd.place(x=530,y=350)

        #entry1 - Password with show="*" to hide characters
        self.txtpwd=ttk.Entry(frame,textvariable=self.var_pwd,font=("times new roman",15,"bold"), show="*")
        self.txtpwd.place(x=533,y=375,width=270)
        
        # Password hint label
        pwd_hint = Label(frame,text="Minimum 8 characters with numbers and symbols",font=("times new roman",10),fg="gray",bg="#F2F2F2")
        pwd_hint.place(x=533,y=400)

        #label2 
        cpwd =lb1= Label(frame,text="Confirm Password:",font=("times new roman",15,"bold"),fg="#002B53",bg="#F2F2F2")
        cpwd.place(x=530,y=420)

        #entry2 - Confirm password with show="*" to hide characters
        self.txtcpwd=ttk.Entry(frame,textvariable=self.var_cpwd,font=("times new roman",15,"bold"), show="*")
        self.txtcpwd.place(x=533,y=445,width=270)

        # Show/Hide Password Checkbox
        self.var_showpwd = IntVar()
        show_pwd_check = Checkbutton(frame, variable=self.var_showpwd, text="Show Password", 
                                    font=("times new roman", 10), fg="#002B53", bg="#F2F2F2",
                                    command=self.toggle_password)
        show_pwd_check.place(x=533, y=470, width=120)

        # Checkbutton for terms and conditions
        checkbtn = Checkbutton(frame,variable=self.var_check,text="I Agree the Terms & Conditions",font=("times new roman",13,"bold"),fg="#002B53",bg="#F2F2F2")
        checkbtn.place(x=100,y=480,width=270)


        # Creating Button Register
        loginbtn=Button(frame,command=self.reg,text="Register",font=("times new roman",15,"bold"),bd=0,relief=RIDGE,fg="#fff",bg="#002B53",activeforeground="white",activebackground="#007ACC")
        loginbtn.place(x=103,y=510,width=270,height=35)

        # Creating Button Login - Modified to return to login
        loginbtn=Button(frame,command=self.open_login,text="Login",font=("times new roman",15,"bold"),bd=0,relief=RIDGE,fg="#fff",bg="#002B53",activeforeground="white",activebackground="#007ACC")
        loginbtn.place(x=533,y=510,width=270,height=35)

    def on_email_focus_in(self, event):
        """Clear placeholder text when entry gets focus"""
        if self.var_email.get() == "example@gmail.com":
            self.var_email.set("")
    
    def on_email_focus_out(self, event):
        """Restore placeholder text if field is empty"""
        if self.var_email.get() == "":
            self.var_email.set("example@gmail.com")
    
    def toggle_password(self):
        """Toggle between showing and hiding passwords"""
        if self.var_showpwd.get():
            self.txtpwd.config(show="")
            self.txtcpwd.config(show="")
        else:
            self.txtpwd.config(show="*")
            self.txtcpwd.config(show="*")

    def validate_email(self, email):
        """Validate email format and check for @gmail.com"""
        # Check if email ends with @gmail.com
        if not email.endswith("@gmail.com"):
            return False
        
        # Check for basic email format using regex
        pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
        if not re.match(pattern, email):
            return False
            
        return True
    
    def validate_password(self, password):
        """Validate password strength"""
        # Check length
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # Check for at least one digit
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one number"
        
        # Check for at least one special character
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~" for char in password):
            return False, "Password must contain at least one special character"
            
        return True, "Password is valid"

    def open_login(self):
        # Close the current Register window
        self.root.destroy()
        
        # Import Login class from login.py
        from login import Login
        
        # Create new Login window
        root=Tk()
        app=Login(root)
        root.mainloop()

    def reg(self):
        # Get values and strip whitespace
        fname = self.var_fname.get().strip()
        lname = self.var_lname.get().strip()
        cnum = self.var_cnum.get().strip()
        email = self.var_email.get().strip()
        ssq = self.var_ssq.get()
        sa = self.var_sa.get().strip()
        pwd = self.var_pwd.get()
        cpwd = self.var_cpwd.get()
        
        # Basic validation for empty fields
        if (fname == "" or lname == "" or cnum == "" or 
            email == "" or ssq == "Select" or sa == "" or 
            pwd == "" or cpwd == ""):
            messagebox.showerror("Error", "All Fields Required!")
            return
            
        # Check if email is still the placeholder
        if email == "example@gmail.com":
            messagebox.showerror("Error", "Please enter your email address")
            return
            
        # Validate email format
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid Gmail address (example@gmail.com)")
            return
            
        # Validate password
        pwd_valid, pwd_msg = self.validate_password(pwd)
        if not pwd_valid:
            messagebox.showerror("Error", pwd_msg)
            return
            
        # Check if passwords match
        if pwd != cpwd:
            messagebox.showerror("Error", "Password and Confirm Password do not match!")
            return
            
        # Check terms and conditions
        if self.var_check.get() == 0:
            messagebox.showerror("Error", "Please check the 'I Agree Terms and Conditions'!")
            return
            
        # Contact number validation (optional)
        if not cnum.isdigit() or len(cnum) < 10:
            messagebox.showerror("Error", "Please enter a valid contact number")
            return
            
        # Database operations
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            mycursor = conn.cursor()
            
            # Check if user already exists
            query=("select * from regteach where email=%s")
            value=(email,)
            mycursor.execute(query,value)
            row=mycursor.fetchone()
            
            if row!=None:
                messagebox.showerror("Error","User already exists, please try another email")
            else:
                # Insert new user
                mycursor.execute("insert into regteach values(%s,%s,%s,%s,%s,%s,%s)",(
                fname,
                lname,
                cnum,
                email,
                ssq,
                sa,
                pwd
                ))

                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Registration Successful!")
                
                # Optional: Clear fields after successful registration
                self.var_fname.set("")
                self.var_lname.set("")
                self.var_cnum.set("")
                self.var_email.set("example@gmail.com")
                self.var_ssq.set("Select")
                self.var_sa.set("")
                self.var_pwd.set("")
                self.var_cpwd.set("")
                self.var_check.set(0)
                
        except Exception as es:
            messagebox.showerror("Error",f"Due to: {str(es)}")

if __name__ == "__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()