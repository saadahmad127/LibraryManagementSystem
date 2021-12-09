#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import StringVar
from functools import partial
import pyodbc
import time
from PIL import ImageTk,Image
import datetime
from tkinter import ttk
from tkinter.ttk import Treeview, Scrollbar


# ### Making connection with Database

# In[2]:


conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=./db.accdb;')
cursor = conn.cursor()


# ### Code:

# #### 1. Home_Page:

# In[3]:


def home_page(window):
    tk.Label(window, text="Welcome",font="Times 30",fg = "royal blue").place(x=395, y=10)
    tk.Label(window, text="Login",font="Times 20 bold",fg = "royal blue").place(x=420, y=150)
    loginButton = tk.Button(window, text="USER",font="Times 15",fg = "royal blue",command=user_login).place(x=360, y=230)  
    loginButton = tk.Button(window, text="ADMIN",font="Times 15",fg = "royal blue",command=admin_login).place(x=495, y=230)


# #### 2. User Login Page

# In[4]:


def user_login():
    for widget in window.winfo_children():
        widget.destroy()
    path = "lb2.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window, image=img)
    panel.photo = img
    panel.place(x=500, y=150) 
    window.configure(background="khaki")
    tk.Label(window, text="User Sign In ",font="Times 30",fg = "royal blue").place(x=100,y=150) 
    tk.Label(window, text="Roll No",font="Times 15",fg = "royal blue").place(x=100,y=250) 
    tk.Label(window, text="Password",font="Times 15",fg = "royal blue").place(x=100,y=300) 
    username = StringVar()
   
    r_n = tk.Entry(window, textvariable=username).place(x=200, y=255)
    password = StringVar()
   
    passs = tk.Entry(window, textvariable=password,show='*').place(x=200,y=302) 
#     global user_validateLogin
# #     user_validateLogin()
#     user_validateLogin = partial(user_validateLogin, username, password)
    
    loginButton = tk.Button(window, text="Login",command=lambda:user_validateLogin(username,password)).place(x=280, y=350)  
    


# #### 2.1 Validating Password from user

# In[5]:


def user_validateLogin(username,pp):
    user=username.get()
    passs=pp.get()
    cursor = conn.cursor()
    cursor.execute("select login,password from students where login=? and password=?;",[user,passs])
    rows = cursor.fetchall()
    #fetching password from database
    c2 = conn.cursor()
    c2.execute("select First_name,fine,department,books_borrowed,roll_num,password from students where login=? and password=?;",[user,passs])
    r2 = c2.fetchone()
    #checking if password is correct or not
    if rows:
         user_features(r2)
    else:
        tk.Label(window, text="Wrong ID or Password Enter Again",font="Times 15",fg = "red").place(x=100,y=500) 
        window.update()
        time.sleep(2)
        user_login()


# #### 2.2 User Features

# In[6]:


def user_features(r2):
    for widget in window.winfo_children():
        widget.destroy()
    tk.Label(window, text="Welcome "+r2[0],font="Times 30",fg = "green").place(x=355, y=10)      
    Available_Button = tk.Button(window, text="Available Books",font="Times 15",width=20,bg='azure3',command=Available_Books).place(x=100, y=150)       
    
#     global search_book
#     search_book=partial(search_book, r2)
    SearchButton = tk.Button(window, text="Search Book",font="Times 15",width=20,bg='azure3',command=lambda:search_book(r2)).place(x=100, y=200)
    
    
#     global user_billing
    
    path = "lb2.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window, image=img)
    panel.photo = img
    panel.place(x=600, y=150) 

    
#     user_billing = partial(user_billing, r2)
    BillButton = tk.Button(window, text="Check Fine If Any",font="Times 15",fg = "red",width=20,bg='azure3',command=lambda:user_billing(r2)).place(x=100, y=250)    
    
#     global change_pass
#     change_pass = partial(change_pass, r2)
    
    Change_passButton = tk.Button(window, text="Change Password",font="Times 15",width=20,bg='azure3',command=lambda:change_pass(r2)).place(x=100, y=300)
    
    signoutButton = tk.Button(window, text="Sign out",font="Times 15",width=20,bg='azure3',command=signout).place(x=100, y=400)       
    
#     global view_borrowed_books
#     view_borrowed_books = partial(view_borrowed_books, r2)
    
    borrowed_book = tk.Button(window, text="Borrowed Books",font="Times 15",width=20,bg='azure3',command=lambda:view_borrowed_books(r2)).place(x=100, y=350)       
    
    


# #### 2.2.1 Available Books

# In[7]:



def Available_Books():
    window2 = tk.Toplevel()
    window2.title("Avaliable Books")
    window2.geometry("900x650")
    window2.resizable(0,0)
    window2.configure(background="saddle brown")
    tree = ttk.Treeview(window2, column=("c1", "c2"), show='headings',selectmode ='browse',height=30)
    tk.Label(window2, text="Avaliable Books",font="Times 30",fg = "green").place(x=330, y=10)
    
    style = ttk.Style()

    verscrlbar = ttk.Scrollbar(window2, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='x')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=2, bd=2, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 

    tree.column("#1", anchor=tk.CENTER,width=70)
    tree.heading("#1", text="Book ID")
    tree.column("#2", anchor=tk.CENTER,width=600)
    tree.heading("#2", text="Book Name")
    
    tree.place(x=100,y=100)
    cursor = conn.cursor()
    cursor.execute("SELECT ID,book_name FROM books where copies>0")
    
    
    rows = cursor.fetchall()   
    for row in rows:
        tree.insert("",tk.END, values=(row[0],row[1]))
    


# #### 2.2.2 Search Books

# In[8]:


def search_book(r2):
    window2 = tk.Toplevel()
    window2.title("Search Book")
    window2.geometry("900x700")
    window2.resizable(0,0)
    window2.configure(background="Brown")
#     tk.Label(window2, text="Search Books",font="Times 30",fg = "green").place(x=330, y=10)
    tk.Label(window2, text="Search Books",font="Times 30",fg = "royal blue").place(x=385, y=5)
    tk.Label(window2, text="Search",font="Times 10",fg = "royal blue").place(x=20,y=100) 
    query = StringVar()
    r_n = tk.Entry(window2, textvariable=query).place(x=80, y=100)    

    tk.Button(window2, text="Submit",font="Times 10",fg = "royal blue",command=lambda:final_search_book(query,r2,window2)).place(x=200, y=130)   

    
#ANOTHER FUNCTION

            
def final_search_book(query,r2,window2):   
    for widget in window2.winfo_children():
        widget.destroy()
    cursor = conn.cursor()
    filterr =query.get()
    
    
    tree = ttk.Treeview(window2, column=("c1", "c2"), show='headings',selectmode ='browse',height=15)
    tk.Label(window2, text="Search Books",font="Times 30",fg = "green").place(x=330, y=10)
    
    style = ttk.Style()

    verscrlbar = ttk.Scrollbar(window2, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='x')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=2, bd=2, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 

    tree.column("#1", anchor=tk.CENTER,width=70)
    tree.heading("#1", text="Book ID")
    tree.column("#2", anchor=tk.CENTER,width=600)
    tree.heading("#2", text="Book Name")
    tree.place(x=100,y=200)
    
    sql = "SELECT ID,book_name FROM books WHERE book_name LIKE ? and copies>0"
    param = f'%{filterr}%'
    rows = cursor.execute(sql, param).fetchall()
    
    for row in rows:
        tree.insert("",tk.END, values=(row[0],row[1])) 
    
    
    
        
    tk.Label(window2, text="Borrow A Book",font="Times 10",fg = "green").place(x=60, y=585)
    tk.Label(window2, text="Book ID",font="Times 10",fg = "green").place(x=60, y=610)
    book_id = StringVar()
    borrow= tk.Entry(window2, textvariable=book_id).place(x=130, y=610)    
    
    Borrow_button= tk.Button(window2, text="Submit",font="Times 10",width=8,bg='green',command=lambda:b_borrow(r2,book_id,window2)).place(x=260, y=630)       

    


# #### 2.2.2.1 Borrow Book

# In[9]:



def b_borrow(r2,book_id,window2):
window3 = tk.Tk()
window3.title("Borrow Book")
window3.geometry("800x400")
window3.resizable(0,0)
window3.configure(background="white")
cursor = conn.cursor()
    
if r2[1]>0:
#         for widget in window2.winfo_children():
#             widget.destroy()
    tk.Label(window3, text="Pending Fine Cannot Borrow Book Contact Admin For More Information.",font="Times15",fg = "red").place(x=10,y=100) 
    return None
if r2[3]>=4:
#         for widget in window2.winfo_children():
#             widget.destroy()
    tk.Label(window3, text="Please Return Previously Borrowed Books To Get New One.",font="Times15",fg = "red").place(x=10,y=100) 
    return None
   

b=book_id.get()
bb=b.isdigit()
if bb:
    try:
        cursor.execute("select ID,book_name,author_name,copies FROM books where ID=? ;",[b])
        rows = cursor.fetchone()
#             print(rows)
        tk.Label(window3, text="Are You Sure You Want To Borrow This Book",font="Times15",fg = "red").place(x=230,y=10) 
        tk.Label(window3, text=str(rows[1])+" By "+str(rows[2]),font="Times 13",fg = "green").place(x=10,y=150) 

#         global yes_book
#         yes_book = partial(yes_book, window2,rows,r2)

        no=tk.Button(window3, text="NO",font="Times 15",width=10,fg='red',command=window3.destroy).place(x=50, y=250)
        yes=tk.Button(window3, text="Yes",font="Times 15",width=10,fg='green',command=lambda:yes_book(window3,rows,r2)).place(x=50, y=350)
    except:
        tk.Label(window3, text="Something went wrong. Please Enter a valid input.",font="Times15",fg = "red").place(x=230,y=10) 
else:
     tk.Label(window3, text="Wrong Input",font="Times15",fg = "red").place(x=280,y=100) 



# REQUEST ADMIN    
def yes_book(window3,rows,r2):

for widget in window3.winfo_children():
    widget.destroy()

cursor = conn.cursor()   

#     cursor.execute("select copies from books where id=?;",[rows[0]])   


cursor = conn.cursor()
if rows[3]-1<0:
    tk.Label(window3, text="Book Not Avaliable",font="Times 12",fg = "green").place(x=30,y=100) 
else:
    cursor = conn.cursor()
    cursor.execute("insert into requests(user_id,user_name,user_department,borrow_date,return_date,book_name,book_id) values (?,?,?,?,?,?,?)",[r2[4],r2[0],r2[2],datetime.date.today(),datetime.date.today()+datetime.timedelta(7),rows[1],rows[0]])
    conn.commit()
    tk.Label(window3, text="Request For "+str(rows[1])+" Has Been Submitted Kindly Wait For Approval",font="Times 12",fg = "green").place(x=30,y=100) 


# #### 2.2.3 User Billing

# In[10]:


def user_billing(r2): 
    window2 = tk.Toplevel()
    window2.title("Fine")
    window2.geometry("400x400")
    window2.resizable(0,0)
    window2.configure(background="saddle brown")
    
    tk.Label(window2, text="Billing Information ",font="Times 15",fg = "royal blue").place(x=130, y=10)   
    tk.Label(window2, text="Dear "+str(r2[0])+" your Fine is "+str(r2[1]),font="Times 15",fg = "red").place(x=20, y=150)      
 


# #### 2.2.4 Change Password (User)

# In[11]:


def change_pass(r2):
    print()
    window2 = tk.Toplevel()
    window2.title("Change Password")
    window2.geometry("800x400")
    window2.resizable(0,0)
    window2.configure(background="white")
    
    old= StringVar()
    new= StringVar()
    new_con=StringVar()
    
    tk.Label(window2, text="Old Password",font="Times 15",width=20,fg = "royal blue").place(x=20,y=100) 
    a=tk.Entry(window2, textvariable=old,show="*").place(x=300, y=100)    
    
    tk.Label(window2, text="New Password",font="Times 15",width=20,fg = "royal blue").place(x=20,y=150) 
    tk.Entry(window2, textvariable=new,show="*").place(x=300, y=150)    
    
    tk.Label(window2, text="Confirm New Password",font="Times 15",width=20,fg = "royal blue").place(x=20,y=200) 
    tk.Entry(window2, textvariable=new_con,show="*").place(x=300, y=200)    
    
#     global final_pass_change
#     final_pass_change= partial(final_pass_change, r2,window2,old,new,new_con)
    
    tk.Button(window2, text="Submit",font="Times 10",bg = "royal blue",command=lambda:final_pass_change(r2,window2,old,new,new_con)).place(x=390, y=260)
    
def final_pass_change(r2,window2,old,new,new_con):
    olda=old.get()
    newa=new.get()
    new_cona=new_con.get()
    cursor = conn.cursor()
    cursor.execute("select password from students where roll_num=?;",[r2[4]])    
    rows = cursor.fetchone()
    if olda==rows[0]:
        for widget in window2.winfo_children():
                widget.destroy()
#         print(rows[0],olda)
        if newa==new_cona:
            if len(newa)<8:
                tk.Label(window2, text="Password to Short",font="Times 15",fg = "red").place(x=280,y=100) 
            else :
                cursor = conn.cursor()
                cursor.execute("UPDATE students set password=? where roll_num=?;",[newa,r2[4]])
                conn.commit()
                tk.Label(window2, text="password updated",font="Times 15",fg = "green").place(x=280,y=100) 
        else:
            tk.Label(window2, text="password Does Not Match",font="Times 15",fg = "red").place(x=280,y=100) 
    else:    
        for widget in window2.winfo_children():
            widget.destroy()
        tk.Label(window2, text="Old Password Not Correct",font="Times 15",fg = "red").place(x=280,y=100) 


# #### 2.2.5 SignOut (User and Admin) 

# In[12]:


def signout():
    for widget in window.winfo_children():
        widget.destroy()
    tk.Label(window, text="signed out",font="Times 30",fg = "red").place(x=370,y=100) 


# #### 2.2.6 View Borrowed Books

# In[13]:


def view_borrowed_books(r2):
#     print(r2)
    window2 = tk.Toplevel()
    window2.title("Borrowed Books")
    window2.geometry("900x650")
    window2.resizable(0,0)
    window2.configure(background="saddle brown")
    style = ttk.Style()

    tree = ttk.Treeview(window2, column=("c1", "c2", "c3", "c4" ,"c5"), show='headings',selectmode ='browse')
    verscrlbar = ttk.Scrollbar(window2, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='y')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 
    
    tree.column("#1", anchor=tk.CENTER,width=50)
    tree.heading("#1", text="User ID")
    tree.column("#2", anchor=tk.CENTER,width=70)
    tree.heading("#2", text="Book ID")
    tree.column("#3", anchor=tk.CENTER,width=500)
    tree.heading("#3", text="Book Name")
    tree.column("#4", anchor=tk.CENTER,width=100)
    tree.heading("#4", text="Borrow Date")
    tree.column("#5", anchor=tk.CENTER,width=100)
    tree.heading("#5", text="Return Name")
    tree.place(x=10,y=100)
    
    cur1 = conn.cursor()
    cur1.execute("SELECT user_id,book_id,book_name,Format(CDate(borrowed_date)),Format(CDate(return_date)) FROM books_borrowed where user_id=?",[r2[4]])
    rows = cur1.fetchall()    
   
    for row in rows:
#         print(row) 
        tree.insert("",tk.END, values=(row[0],row[1],row[2],row[3],row[4]))
    tk.Label(window2, text="Enter Book ID To Return",font="Times 12",fg='green').place(x=10, y=350)
    return_book_id=StringVar()
    req= tk.Entry(window2, textvariable=return_book_id,width=15).place(x=180, y=352)    
    
    refresh=tk.Button(window2,text="Refresh",font="Times 10",bg='red',command=lambda:refresh_books(window2,r2)).place(x=0,y=0)
    requests_button= tk.Button(window2, text="Return",font="Times 8",bg='green',command=lambda:return_book(return_book_id,r2,rows)).place(x=236, y=382)
    
def refresh_books(window2,r2):
    for widget in window2.winfo_children():
            widget.destroy()  
    window2.destroy()
    view_borrowed_books(r2)
    
def return_book(return_book_id,r2,rows): 
    print()   
    req1=return_book_id.get()
    window2 = tk.Toplevel()
    window2.title("Return Book")
    window2.geometry("800x400")
    window2.resizable(0,0)
    window2.configure(background="White")
#     print("req1",req1)
#     print("rows",r2[4])    
    try:
        cur1 = conn.cursor()
        cur1.execute("SELECT book_id,book_name,user_id FROM books_borrowed where user_id=? and book_id=? ;",[r2[4],req1])
        rowss = cur1.fetchall()  
        rowss=rowss[0]
        tk.Label(window2, text="Are You Sure You Want to return this Book "+str(rowss[1]),font="Times 10",fg = "royal blue").place(x=20, y=60)         
        no=tk.Button(window2, text="NO",font="Times 15",width=10,fg='red',command=window2.destroy).place(x=50, y=250)
        yes=tk.Button(window2, text="Yes",font="Times 15",width=10,fg='green',command=lambda:final_return(rowss,window2)).place(x=50, y=350)
    except:
        print()
        tk.Label(window2, text="Book Not Borrowed! Wrong Entry",font="Times 10",fg = "royal blue").place(x=20, y=60) 
        
def final_return(rowss,window2):
#     print(rowss[2])
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books_borrowed where user_id=? and book_id=?;",[rowss[2],rowss[0]])
    conn.commit()
    
    cursor = conn.cursor()
    cursor.execute("select books_borrowed from students where roll_num=?",[rowss[2]])
    a=cursor.fetchone()
    aa=int(a[0])
#     print(aa)
    
    cursor = conn.cursor()
    cursor.execute("UPDATE students set books_borrowed=? where roll_num=?",[aa-1,rowss[2]])
    conn.commit()
    
    
    cursor = conn.cursor()
    cursor.execute("select copies from books where ID=?",[rowss[0]])
    c=cursor.fetchone()
    cc=int(c[0])
    print(cc)
    print(rowss[0])
    cursor = conn.cursor()
    cursor.execute("UPDATE books set copies=? where ID=?",[cc+1,rowss[0]])
    conn.commit()
    
    for widget in window2.winfo_children():
        widget.destroy()
    tk.Label(window2, text="Book Returned Successfully",font="Times 10",fg = "royal blue").place(x=20, y=60)             


# ### 3. Admin Login

# In[14]:


def admin_login():
    for widget in window.winfo_children():
        widget.destroy()     
    path = "lb2.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window, image=img)
    panel.photo = img
    panel.place(x=500, y=150) 
    
    window.configure(background="khaki")
        
    tk.Label(window, text="Admin Sign In ",font="Times 30",fg = "royal blue").place(x=100,y=150) 
    tk.Label(window, text="Login Id",font="Times 15",fg = "royal blue").place(x=100,y=250) 
    tk.Label(window, text="Password",font="Times 15",fg = "royal blue").place(x=100,y=300) 
    username = StringVar()
    r_n = tk.Entry(window, textvariable=username).place(x=200, y=255)
    password = StringVar()
    passs = tk.Entry(window, textvariable=password,show='*').place(x=200,y=302) 
    loginButton = tk.Button(window, text="Login",command=lambda:admin_validateLogin(username, password)).place(x=280, y=350)  
    

  


# ### 3.1 Validating Admin Login

# In[15]:


def admin_validateLogin(username,pp):
    user=username.get()
    passs=pp.get()    
    cursor = conn.cursor()
    cursor.execute("select login_id,password from admin where login_id=? and password=?;",[user,passs])
    rows = cursor.fetchall()
    
    c2 = conn.cursor()
    c2.execute("select emp_id,login_id,password from admin where login_id=? and password=?;",[user,passs])
    r2 = c2.fetchone()
#     print(r2)
    
    if rows:
         admin_features(r2)
    else:
        a=tk.Label(window, text="Wrong ID or Password Enter Again",font="Times 15",fg = "royal blue").place(x=100,y=500) 
        window.update()
        time.sleep(2)
        admin_login()


# ### 3.2 Admin Features

# In[16]:


def admin_features(r2):
    for widget in window.winfo_children():
        widget.destroy()
    
    tk.Label(window, text="Welcome ",font="Times 30",fg = "green").place(x=355, y=10)      
   
    creat_user_Button = tk.Button(window, text="Create User Account",font="Times 15",width=20,bg='azure3',command=lambda:create_account(r2)).place(x=100, y=150)       

#     Remove_user_Button = tk.Button(window, text="Remove User Account",font="Times 15",fg = "red",width=20,bg='azure3',command=removeUser).place(x=100, y=150)

    View_borrowed_Button = tk.Button(window, text="View Borrowed Books",font="Times 15",width=20,bg='azure3',command=see_borrowed_books).place(x=100, y=200)
   
    Edit_DB_Button = tk.Button(window, text="Edit DataBase",font="Times 15",width=20,bg='azure3',command=lambda:edit_db(r2)).place(x=100, y=250)
    
    View_requests_Button = tk.Button(window, text="View Requests",font="Times 15",width=20,bg='azure3',command=requests).place(x=100, y=300)
    
    Manage_fines_Button = tk.Button(window, text="Manage Fine",font="Times 15",width=20,bg='azure3',command= manage_fine).place(x=100, y=350)
    
    Change_passButton = tk.Button(window, text="Change Password",font="Times 15",width=20,bg='azure3',command=lambda:change_admin_pass(r2)).place(x=100, y=400)
    
    signoutButton = tk.Button(window, text="Sign out",font="Times 15",width=20,bg='azure3',command=signout).place(x=100, y=450)
    
    path = "lb2.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window, image=img)
    panel.photo = img
    panel.place(x=600, y=150) 


# ### 3.2.1 Create Account (User) by admin

# In[17]:


def create_account(r2):
    for widget in window.winfo_children():
        widget.destroy()     
    path = "lb2.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window, image=img)
    panel.photo = img
    panel.place(x=580, y=150) 
    
    window.configure(background="khaki")
    tk.Label(window, text="Create User Account",font="Times 30",fg = "green").place(x=300, y=10)
    
    tk.Label(window, text="Roll Number",font="Times 15",fg = "royal blue",width=10).place(x=5,y=100)
    roll_num = StringVar()
    tk.Entry(window, textvariable=roll_num).place(x=150, y=105)    
    
    tk.Label(window, text="Department",font="Times 15",fg = "royal blue",width=10).place(x=5,y=140)
    department = StringVar()
    tk.Entry(window, textvariable=department).place(x=150, y=145)   
    
    tk.Label(window, text="Semester",font="Times 15",fg = "royal blue",width=10).place(x=5,y=180)
    semester = StringVar()
    tk.Entry(window, textvariable=semester).place(x=150, y=185)    

    tk.Label(window, text="First Name",font="Times 15",fg = "royal blue",width=10).place(x=5,y=220)
    first_name = StringVar()
    tk.Entry(window, textvariable=first_name ).place(x=150, y=225)    
    
    tk.Label(window, text="Last Name",font="Times 15",fg = "royal blue",width=10).place(x=5,y=260)
    last_name = StringVar()
    tk.Entry(window, textvariable=last_name).place(x=150, y=265)    
    
    tk.Label(window, text="Login Id",font="Times 15",fg = "royal blue",width=10).place(x=5,y=300)
    login = StringVar()
    tk.Entry(window, textvariable=login ).place(x=150, y=305)    
    
    tk.Label(window, text="Password",font="Times 15",fg = "royal blue",width=10).place(x=5,y=340)
    password= StringVar()
    tk.Entry(window, textvariable=password,show='*').place(x=150, y=345)    
    
    summit_Button = tk.Button(window, text="Submit",font="Times 15",fg = "royal blue",command=lambda:final_create_user(password,login,last_name,roll_num,department,semester,first_name,r2)).place(x=180, y=400) 
    
def final_create_user(password,login,last_name,roll_num,department,semester,first_name,r2):
    password_final=password.get()
    login_final=login.get()
    last_name_final=last_name.get()
    roll_num_final=roll_num.get()
    department_final=department.get()
    semester_final=semester.get()
    first_name_final=first_name.get()
    
    if len(password_final)>=8 and login_final and last_name_final and roll_num_final and department_final and semester_final and first_name_final:
        try:
            cursor = conn.cursor()
            cursor.execute("insert into students(roll_num,department,semester,fine,books_borrowed,first_name,last_name,login,password) values (?,?,?,?,?,?,?,?,?)",[roll_num_final,department_final,semester_final,0,0,first_name_final,last_name_final,login_final,password_final])
            conn.commit()
            tk.Label(window, text="Account Added Successfully",font="Times 15",fg = "green").place(x=90, y=500) 
            window.update()
            time.sleep(2)
            admin_features(r2)
        except:
            tk.Label(window, text="Error! Roll Number Or Login Duplicated Or Wrong Data Entered",font="Times 15",fg = "red").place(x=90, y=500) 
            window.update()
            time.sleep(2)
            create_account(r2)  
    else:
        tk.Label(window, text="Error! Fields Cannot Be Empty or Password less than 8 characters",font="Times 15",fg = "red").place(x=90, y=500) 
        window.update()
        time.sleep(2)
        create_account(r2)


# ### 3.2.2 See All Borrowed Books

# In[18]:


def see_borrowed_books():
    
    window2 = tk.Toplevel()
    window2.title("Borrowed Books")
    window2.geometry("900x650")
    window2.resizable(0,0)
    window2.configure(background="brown")
    tree = ttk.Treeview(window2, column=("c1", "c2", "c3", "c4" ,"c5"), show='headings',selectmode ='browse')
    tk.Label(window2, text="Borrowed Books",font="Times 30",fg = "green").place(x=320, y=10)
        
    style = ttk.Style()

    verscrlbar = ttk.Scrollbar(window2, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='y')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 

    tree.column("#1", anchor=tk.CENTER,width=50)
    tree.heading("#1", text="User Id")
    tree.column("#2", anchor=tk.CENTER,width=150)
    tree.heading("#2", text="User Name")
    tree.column("#3", anchor=tk.CENTER,width=300)
    tree.heading("#3", text="Book Name")
    tree.column("#4", anchor=tk.CENTER,width=50)
    tree.heading("#4", text="Book Id")
    tree.column("#5", anchor=tk.CENTER,width=100)
    tree.heading("#5", text="Borrow Date")
    tree.place(x=90,y=150)
    
    cur1 = conn.cursor()
    cur1.execute("SELECT user_id,user_name,book_name,book_id,Format(CDate(borrowed_date)) FROM books_borrowed ")
    rows = cur1.fetchall()
   
    for row in rows:
#         print(row) 
        tree.insert("",tk.END, values=(row[0],row[1],row[2],row[3],row[4]))  
#     Format(CDate(borrowed_date))


# ### 3.2.3 Edit Database

# In[19]:



def edit_db(r2):
print()
window2 = tk.Toplevel()
window2.title("Edit DB")
window2.geometry("600x400")
window2.resizable(0,0)
window2.configure(background="White")
tk.Button(window2, text="Add Book ",font="Times 15",width=20,bg='azure3',command=add_book_db).place(x=10, y=10)      
tk.Button(window2, text="Remove Book ",font="Times 15",width=20,bg='azure3',command=remove_book_db).place(x=10, y=60)      


# ### 3.2.3.1 Add a Book in Database

# In[20]:


def add_book_db():
    print()
    path = "lb2.png"
    
    window3 = tk.Toplevel()
    window3.title("Edit DB")
    window3.geometry("800x600")
    window3.resizable(0,0)
    window3.configure(background="White")
    
    
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window3, image=img)
    panel.photo = img
    panel.place(x=480, y=150) 
    
    cursor = conn.cursor()
    cursor.execute("select count(ID) from books")
    recommend=cursor.fetchall()
    recommend=recommend[0][0]
    recommend=recommend+1
    
    tk.Label(window3, text="Book ID",font="Times 15",fg = "royal blue",width=12).place(x=10,y=100)
    idd = StringVar()
    tk.Entry(window3, textvariable=idd ).place(x=160, y=105)    
    tk.Label(window3, text="Recommended Id "+str(recommend),font="Times 11",fg = "royal blue",width=17).place(x=300,y=105)
    
    tk.Label(window3, text="Book Name",font="Times 15",fg = "royal blue",width=12).place(x=10,y=140)
    BookName = StringVar()
    tk.Entry(window3, textvariable=BookName).place(x=160, y=145)   
    
    tk.Label(window3, text="Author Name",font="Times 15",fg = "royal blue",width=12).place(x=10,y=180)
    AuthorName = StringVar()
    tk.Entry(window3, textvariable=AuthorName).place(x=160, y=185)    

    tk.Label(window3, text="ISBN",font="Times 15",fg = "royal blue",width=12).place(x=10,y=220)
    ISBN = StringVar()
    tk.Entry(window3, textvariable=ISBN).place(x=160, y=225)    
    
    tk.Label(window3, text="Publisher",font="Times 15",fg = "royal blue",width=12).place(x=10,y=260)
    Publisher= StringVar()
    tk.Entry(window3, textvariable=Publisher).place(x=160, y=265)    
    
    tk.Label(window3, text="Publications Date",font="Times 15",fg = "royal blue",width=12).place(x=10,y=300)
    Publications = StringVar()
    tk.Entry(window3, textvariable=Publications).place(x=160, y=305)    
    
    tk.Label(window3, text="MM/DD/YY",font="Times 12",fg = "royal blue",width=12).place(x=300,y=305)
    
    
    tk.Label(window3, text="Average Rating",font="Times 15",fg = "royal blue",width=12).place(x=10,y=340)
    Rating= StringVar()
    tk.Entry(window3, textvariable=Rating).place(x=160, y=345)  
    
    tk.Label(window3, text="Number of copies",font="Times 15",fg = "royal blue",width=12).place(x=10,y=380)
    copies= StringVar()
    tk.Entry(window3, textvariable=copies).place(x=160, y=385)  
    
    summit_Button = tk.Button(window3, text="Submit",font="Times 12",fg = "green",command=lambda:add_book_final(idd,BookName,AuthorName,ISBN,Publisher,Publications,Rating,copies,window3)).place(x=230, y=420) 
    
def add_book_final(idd,BookName,AuthorName,ISBN,Publisher,Publications,Rating,copies,window3):
    print()
    aidd=idd.get()
    aBookName=BookName.get()
    aAuthorName=AuthorName.get()
    aISBN=ISBN.get()
    aPublisher=Publisher.get()
    aPublications=Publications.get()
    aRating=Rating.get()
    acopies=copies.get()
     
    if aidd and aBookName and aAuthorName and aISBN and aPublisher and aPublications and aRating and acopies:
        try:
            date_reg=aPublications.replace('/','')
            new_date=datetime.datetime.strptime(date_reg, "%d%m%Y")
            final_date=str(new_date.month)+str('/')+str(new_date.day)+str('/')+str(new_date.year)
            cursor = conn.cursor()
            cursor.execute("insert into books(ID,book_name,author_name,isbn_num,publisher,publication_date,average_rating,copies) values (?,?,?,?,?,?,?,?)",[aidd,aBookName,aAuthorName,aISBN,aPublisher,final_date,aRating,acopies])
            conn.commit()
            for widget in window3.winfo_children():
                    widget.destroy()
            tk.Label(window3, text="Book Added Successfully",font="Times 15",fg = "green").place(x=90, y=500) 
        except:
           
             tk.Label(window3, text="Wrong Data Type Entered Or ISBN/ID May Be Duplicated",font="Times 15",fg = "red").place(x=90, y=500) 
    else:
        tk.Label(window3, text="Fields Cannot Be Empty",font="Times 15",fg = "red").place(x=90, y=500) 


# ### 3.2.3.2 Remove a book from Database

# In[21]:


def remove_book_db():
    print()
    path = "lb2.png"
    
    window3 = tk.Toplevel()
    window3.title("Edit DB")
    window3.geometry("800x600")
    window3.resizable(0,0)
    window3.configure(background="brown")
    
    
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(window3, image=img)
    panel.photo = img
    panel.place(x=480, y=150)
    
    tree = ttk.Treeview(window3, column=("c1", "c2", "c3"), show='headings',selectmode ='browse')

    tk.Label(window3, text="Remove Book",font="Times 15",fg = "royal blue").place(x=350,y=10)
    
    style = ttk.Style()

    verscrlbar = ttk.Scrollbar(window3, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='x')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 

    tree.column("#1", anchor=tk.CENTER,width=50)
    tree.heading("#1", text="Book ID")
    tree.column("#2", anchor=tk.CENTER,width=260)
    tree.heading("#2", text="Book Name")
    tree.column("#3", anchor=tk.CENTER,width=140)
    tree.heading("#3", text="Publisher")
    tree.place(x=5,y=150)
    
    cur1 = conn.cursor()
    cur1.execute("SELECT ID,book_name,publisher FROM books")
    rows = cur1.fetchall()    
    for row in rows:
        tree.insert("",tk.END, values=(row[0],row[1],row[2])) 
    
    
    tk.Label(window3, text="Enter Book ID To Remove",font="Times 12",fg='green').place(x=10, y=450)
    delete_book_id=StringVar()
    del_id= tk.Entry(window3, textvariable=delete_book_id,width=15).place(x=200, y=453)    
    
#     global final_remove_book
#     final_remove_book= partial(final_remove_book, delete_book_id,window3)
    
    
    del_button= tk.Button(window3, text="Delete",font="Times 8",bg='green',command=lambda:final_remove_book(delete_book_id,window3)).place(x=257, y=482)

    
def final_remove_book(del_id,window3):
    ddel_id=del_id.get()
    cur1 = conn.cursor()
    cur1.execute("SELECT ID,book_name,publisher FROM books where Id=? and (ID not in (select book_id from books_borrowed where book_id=?))",[ddel_id,ddel_id])
    rows = cur1.fetchall()   
    
    if rows:
        window4_remove_book(rows,window3)
        
    else:
        for widget in window3.winfo_children():
            widget.destroy()
        tk.Label(window3, text="No Book Found Or Book Already Borrowed",font="Times 15",fg = "royal blue").place(x=230, y=200)

def window4_remove_book(rows,window3):
#     print(rows[0][1])
    for widget in window3.winfo_children():
        widget.destroy()
    tk.Label(window3, text="Are You Sure You Want Delete "+str(rows[0][1]),font="Times10",fg = "red").place(x=100,y=70) 
    no=tk.Button(window3, text="NO",font="Times 15",width=10,fg='red',command=window3.destroy).place(x=50, y=250)
    
#     global yes_del_book
#     yes_del_book= partial(yes_del_book,rows,window3)
    
    
    yes=tk.Button(window3, text="Yes",font="Times 15",width=10,fg='green',command=lambda:yes_del_book(rows,window3)).place(x=50, y=320)
    
def yes_del_book(rows,window3):
    print(rows[0][0])
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books where ID=?;",[rows[0][0]])
        conn.commit()
        
        for widget in window3.winfo_children():
            widget.destroy() 
        tk.Label(window3, text="Book Deleted",font="Times 11",width=25,fg = "red").place(x=325,y=200) 
    
    except:
        for widget in window3.winfo_children():
            widget.destroy()
        tk.Label(window3, text="Something Went Wrong :(",font="Times 11",width=25,fg = "red").place(x=300,y=200) 
    
    

        


# ### 3.2.4 See User Requests for borrowing a Book

# In[22]:


def requests():
    print()
    window2 = tk.Toplevel()
    window2.title("Requests")
    window2.geometry("900x650")
    window2.resizable(0,0)
    window2.configure(background="saddle brown")
    tree = ttk.Treeview(window2, column=("c1", "c2", "c3", "c4" ,"c5"), show='headings',selectmode ='browse')
    tk.Label(window2, text="Requests",font="Times 30",fg = "green").place(x=360, y=10)
    
    style = ttk.Style()

    verscrlbar = ttk.Scrollbar(window2, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='y')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 

    tree.column("#1", anchor=tk.CENTER,width=70)
    tree.heading("#1", text="Request ID")
    tree.column("#2", anchor=tk.CENTER,width=50)
    tree.heading("#2", text="User Id")
    tree.column("#3", anchor=tk.CENTER,width=50)
    tree.heading("#3", text="Book Id")
    tree.column("#4", anchor=tk.CENTER,width=600)
    tree.heading("#4", text="Book Name")
    tree.column("#5", anchor=tk.CENTER,width=100)
    tree.heading("#5", text="Borrow Date")
    tree.place(x=10,y=100)
    
    cur1 = conn.cursor()
    cur1.execute("SELECT request_num,user_id,book_id,book_name,Format(CDate(borrow_date)) FROM requests ")
    rows = cur1.fetchall()    
    for row in rows:
#         print(row) 
        tree.insert("",tk.END, values=(row[0],row[1],row[2],row[3],row[4]))   
    
    

    tk.Label(window2, text="Enter Request Id To Accept/Reject",font="Times 12",fg = "green").place(x=10, y=350)
    req_id = StringVar()
    req= tk.Entry(window2, textvariable=req_id,width=15).place(x=250, y=352)    
#     print('row[0]',row[0])
    requests_button= tk.Button(window2, text="View",font="Times 10",width=8,bg='green',command=lambda:view(req_id)).place(x=278, y=382)

    
def view(r):
    window3 = tk.Toplevel()
    window3.title("Request(yes/no)")
    window3.geometry("200x200")
    window3.resizable(0,0)
    window3.configure(background="white")
    rr=r.get()
    
    cursor = conn.cursor()
    cursor.execute("select request_num FROM requests where request_num=?;",[rr])
    rows = cursor.fetchall()    
    if rows:
        no=tk.Button(window3, text="Reject Request",font="Times 14",width=14,fg='red',command=lambda:reject_request(window3,rr)).place(x=15, y=10)
        yes=tk.Button(window3, text="Approve Request",font="Times 14",width=14,fg='green',command=lambda:yes_request(window3,rr)).place(x=15, y=80)
    else:
        tk.Label(window3, text="Request Not Found ",font="Times 11",width=25,fg = "red").place(x=0,y=20) 
    


# ### 3.2.4.1 Accept Request

# In[23]:


def yes_request(window3,rr):
    for widget in window3.winfo_children():
        widget.destroy()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id,user_name,user_department,Format(CDate(borrow_date)),Format(CDate(return_date)),book_name,book_id FROM requests where request_num=?;",[rr])
    r2= cursor.fetchall() 
    print(r2)
    
    if r2:
        r2=r2[0]
        cursor = conn.cursor()
        cursor.execute("insert into books_borrowed(user_id,user_name,user_department,borrowed_date,return_date,fine,book_name,book_id) values (?,?,?,?,?,?,?,?)",[r2[0],r2[1],r2[2],r2[3],r2[4],0,r2[5],r2[6]])
        conn.commit()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM requests where request_num=?;",[rr])
        conn.commit()
        tk.Label(window3, text="Request number "+str(rr)+" Accepted",font="Times 11",width=25,fg = "red").place(x=0,y=20) 
        
        c=conn.cursor()
        c.execute("select books_borrowed from students where roll_num=?;",[r2[0]])
        r_borrow=c.fetchall() 
        r_borrow=r_borrow[0][0]
#         print(r_borrow)
        
        cursor = conn.cursor()
        cursor.execute("UPDATE students set books_borrowed=? where roll_num=?;",[r_borrow+1,r2[0]])
        conn.commit()
        cursor = conn.cursor()

        
        cursor = conn.cursor()
        cursor.execute("SELECT copies FROM books where ID=?;",[r2[6]])
        r= cursor.fetchone()
        print (r)
        
    
        print (r2[6]) 
#         tk.Label(window3, text="Request For "+str(rows[1])+" Has Been Submitted Kindly Wait For Approval",font="Times 12",fg = "green").place(x=30,y=100) 
        cursor.execute("UPDATE books set copies=? where id=?;",[r[0]-1,r2[6]])
        conn.commit()
    else:
        tk.Label(window3, text="Someting Went Wrong",font="Times 11",width=25,fg = "red").place(x=0,y=20) 
    


# ### 3.2.4.2 Reject Request

# In[24]:


def reject_request(window3,rr):
    for widget in window3.winfo_children():
        widget.destroy() 
        
    cursor = conn.cursor()
    cursor.execute("DELETE FROM requests where request_num=?;",[rr])
    conn.commit()
    tk.Label(window3, text="Request number "+str(rr)+" Rejected",font="Times 11",width=25,fg = "red").place(x=0,y=20) 


# ### 3.2.5 Manage Fine

# In[25]:


def manage_fine():
#     window2.destroy()
    window2 = tk.Toplevel()
    window2.title("Manage fine")
    window2.geometry("900x650")
    window2.resizable(0,0)
    window2.configure(background="brown")
    
    tree = ttk.Treeview(window2, column=("c1", "c2", "c3", "c4" ,"c5","c6"), show='headings',selectmode ='browse')
    tk.Label(window2, text="Borrowed Books",font="Times 30",fg = "green").place(x=320, y=10)
    
    style = ttk.Style()

    verscrlbar = ttk.Scrollbar(window2, orient ="vertical", command = tree.yview)  
    verscrlbar.pack(side ='right', fill ='y')
    tree.configure(xscrollcommand = verscrlbar.set)
    
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri',5))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 5,'bold')) 

    tree.column("#1", anchor=tk.CENTER,width=50)
    tree.heading("#1", text="User Id")
    tree.column("#2", anchor=tk.CENTER,width=180)
    tree.heading("#2", text="User Name")
    tree.column("#3", anchor=tk.CENTER,width=70)
    tree.heading("#3", text="Book ID")
    tree.column("#4", anchor=tk.CENTER,width=150)
    tree.heading("#4", text="Boorrowed Date")
    tree.column("#5", anchor=tk.CENTER,width=150)
    tree.heading("#5", text="Return Date")
    tree.column("#6", anchor=tk.CENTER,width=80)
    tree.heading("#6", text="Current Fine")
    tree.place(x=90,y=150)
    
    try:
        cursor = conn.cursor()
        cursor.execute("select user_id,user_name,book_id,borrowed_date,return_date,fine from books_borrowed where return_date<?",[datetime.date.today()])
        rows = cursor.fetchall()
        a=rows[0]
        final_borrowed=str(a[3].month)+str('/')+str(a[3].day)+str('/')+str(a[3].year)
        final_return=str(a[4].month)+str('/')+str(a[4].day)+str('/')+str(a[4].year)
    
        for row in rows:
            tree.insert("",tk.END, values=(row[0],row[1],row[2],final_borrowed,final_return,row[5]))  
    
        tk.Label(window2, text="Enter User ID To Add Fine",font="Times 12",fg='green',width=21).place(x=10, y=450)
        fine=StringVar()
        fine_id= tk.Entry(window2, textvariable=fine,width=15).place(x=220, y=453)  
      
        fine_button= tk.Button(window2, text="Fine",font="Times 10",bg='red',command=lambda:add_fine(fine,window2,a)).place(x=280, y=482)
    
        tk.Label(window2, text="Enter User ID To Remove Fine",font="Times 12",fg='green',width=21).place(x=10, y=550)
        remove_fine_i=StringVar()
        remove_fine_id= tk.Entry(window2, textvariable=remove_fine_i,width=15).place(x=220, y=553)
    
        refresh=tk.Button(window2,text="Refresh",font="Times 10",bg='red',command=lambda:destroy(window2)).place(x=0,y=0)
    
        remove_fine_button= tk.Button(window2, text="Remove Fine",font="Times 10",bg='red',command=lambda:remove_fine(remove_fine_i,window2,a)).place(x=235, y=582)
    except:
        for widget in window2.winfo_children():
            widget.destroy()  
        tk.Label(window2, text="NO Fine To Be Imposed",font="Times 13",fg='green',width=21).place(x=10, y=150)

def destroy(window2):
    for widget in window2.winfo_children():
            widget.destroy()  
    window2.destroy()
    manage_fine()


# ### 3.2.5.1 Add Fine

# In[26]:


def add_fine(fine,window2,a):
    f_fine=fine.get()
    
    window3 = tk.Toplevel()
    window3.title("Fine(yes/no)")
    window3.geometry("600x300")
    window3.resizable(0,0)
    window3.configure(background="white")
   
    try:
        cursor = conn.cursor()
        cursor.execute("select user_id,user_name from books_borrowed where return_date<? and user_id=?",[datetime.date.today(),f_fine])
        rows = cursor.fetchall()
#         a=rows[0][0]
        if rows:
            tk.Label(window3, text="Fine "+str(rows[0][1])+str(" For Rs 100"),font="Times 15",fg = "green").place(x=180, y=10)
            
            yes=tk.Button(window3, text="Yes",font="Times 14",width=12,fg='red',command=lambda:yes_fine(rows,window3)).place(x=15, y=100)
            no=tk.Button(window3, text="No",font="Times 14",width=12,fg='green',command=window3.destroy).place(x=15, y=150)
        else:
            tk.Label(window3, text="Wrong Id Entered",font="Times 15",fg = "green").place(x=200, y=10)
    except:
        for widget in window3.winfo_children():
            widget.destroy()
        tk.Label(window3, text="Something Went Wrong ",font="Times 15",fg = "green").place(x=180, y=10)


def yes_fine(rows,window3):
    a=rows[0][0]
    
    pre_fine=0
    cursor = conn.cursor()
    cursor.execute("select fine from students where roll_num=?",[a])
    b = cursor.fetchall()
    pre_fine=b[0][0]
        
    cursor = conn.cursor() 
    cursor.execute("UPDATE students set fine=? where roll_num=?;",[pre_fine+100,a])
    conn.commit()
    
    cursor = conn.cursor() 
    cursor.execute("UPDATE books_borrowed set fine=? where user_id=?;",[pre_fine+100,a])
    conn.commit()
    
    
    for widget in window3.winfo_children():
        widget.destroy()
    tk.Label(window3, text="User Fined",font="Times 15",fg = "green").place(x=240, y=10)



# ### 3.2.5.2 Remove Fine

# In[27]:


def remove_fine(remove_fine_i,window2,a):
    remove_id=remove_fine_i.get()
    window3 = tk.Toplevel()
    window3.title("Remove Fine(yes/no)")
    window3.geometry("600x300")
    window3.resizable(0,0)
    window3.configure(background="white")
    try:
        cursor = conn.cursor()
        cursor.execute("select user_id,user_name from books_borrowed where return_date<? and user_id=?",[datetime.date.today(),remove_id])
        rows = cursor.fetchall()
        print(rows)
        if rows:
            tk.Label(window3, text="Remove Fine Of "+str(rows[0][1]),font="Times 15",fg = "green").place(x=180, y=10)
            
            yes=tk.Button(window3, text="Yes",font="Times 14",width=12,fg='red',command=lambda:final_remove_fine(rows,window3)).place(x=15, y=100)
            no=tk.Button(window3, text="No",font="Times 14",width=12,fg='green',command=window3.destroy).place(x=15, y=150)
        else:
            tk.Label(window3, text="Wrong Id Entered",font="Times 15",fg = "green").place(x=200, y=10)
    except:
        for widget in window3.winfo_children():
            widget.destroy()
        tk.Label(window3, text="Something Went Wrong ",font="Times 15",fg = "green").place(x=180, y=10)

def final_remove_fine(rows,window3):
    a=rows[0][0]  
    pre_fine=0
    try:
        cursor = conn.cursor() 
        cursor.execute("UPDATE students set fine=? where roll_num=?;",[0,a])
        conn.commit()
    
        cursor = conn.cursor() 
        cursor.execute("UPDATE books_borrowed set fine=? where user_id=?;",[0,a])
        conn.commit()
    
    
        for widget in window3.winfo_children():
            widget.destroy()
        tk.Label(window3, text="Fine Removed",font="Times 15",fg = "green").place(x=240, y=10)
    except:
        tk.Label(window3, text="Something Went Wrong ",font="Times 15",fg = "green").place(x=180, y=10)
        


# ### 3.2.6 Change Admin Password

# In[28]:


def change_admin_pass(r2):
    print()
    window2 = tk.Toplevel()
    window2.title("Change Password")
    window2.geometry("800x400")
    window2.resizable(0,0)
    window2.configure(background="white")
    old= StringVar()
    new= StringVar()
    new_con=StringVar()
    
    tk.Label(window2, text="Old Password",font="Times 15",width=20,fg = "royal blue").place(x=20,y=100) 
    a=tk.Entry(window2, textvariable=old,show="*").place(x=300, y=100)    
    
    tk.Label(window2, text="New Password",font="Times 15",width=20,fg = "royal blue").place(x=20,y=150) 
    tk.Entry(window2, textvariable=new,show="*").place(x=300, y=150)    
    
    tk.Label(window2, text="Confirm New Password",font="Times 15",width=20,fg = "royal blue").place(x=20,y=200) 
    tk.Entry(window2, textvariable=new_con,show="*").place(x=300, y=200)  
    
#     global final_change_pass_admin
#     final_change_pass_admin= partial(final_change_pass_admin,window2,r2,old,new,new_con)
    
    tk.Button(window2, text="Submit",font="Times 10",bg = "royal blue",command=lambda:final_change_pass_admin(window2,r2,old,new,new_con)).place(x=390, y=260)   

    
def final_change_pass_admin(window2,r2,old,new,new_con):
    olda=old.get()
    newa=new.get()
    new_cona=new_con.get()
#     print(r2[2])
#     cursor = conn.cursor()
#     cursor.execute("select password from students where roll_num=?;",[r2[4]])    
#     rows = cursor.fetchone()
    if olda==r2[2]:
        for widget in window2.winfo_children():
                widget.destroy()

        if newa==new_cona:
            if len(newa)<8:
                tk.Label(window2, text="Password to Short",font="Times 15",fg = "red").place(x=280,y=100) 
            else :
                cursor = conn.cursor()
                cursor.execute("UPDATE admin set password=? where login_id=?;",[newa,r2[1]])
                conn.commit()
                tk.Label(window2, text="password updated",font="Times 15",fg = "green").place(x=280,y=100) 
        else:
            tk.Label(window2, text="password Does Not Match",font="Times 15",fg = "red").place(x=280,y=100) 
    else:    
        for widget in window2.winfo_children():
            widget.destroy()
        tk.Label(window2, text="Old Password Not Correct",font="Times 15",fg = "red").place(x=280,y=100) 
    


# In[30]:


window = tk.Tk()
window.title("Library Management System")
window.geometry("950x655")
window.resizable(0,0)
bg =tk.PhotoImage(file = "lb.png")
label1 =tk.Label( window, image = bg)
label1.place(x = 0, y = 0)
home_page(window)
window.mainloop()


# In[ ]:





# In[ ]:




