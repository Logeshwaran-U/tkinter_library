import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
from tkcalendar import DateEntry ,Calendar
from datetime import date,datetime
import mysql.connector
import os

master=Tk()
#Notes{
# some libraries are not pre installed,so install the required libraries using pip command or from the site.
# pip install tkcalendar
# pip install mysql-connector-python
# pip install pyinstaller
# }*
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "widget_images")

global mysql_password
mysql_password='logumysql2005'

class parent_window:
    def __init__(self,master):
        self.tk_parent=Menu(master)
        master.config(menu=self.tk_parent)
        #master.attributes("-fullscreen", True)
        master.state('zoomed')
        self.win_p1 = PhotoImage(file=os.path.join(IMAGE_DIR, "b3.png"))
        self.win_img_l1=Label(master,image=self.win_p1)
        self.win_img_l1.place(x=0,y=0,relwidth=1,relheight=1)        
        #creating masterentry in menu
        self.mstr=Menu(self.tk_parent,font=("Comic Sans MS",15),fg="blue",tearoff=0)
        self.tk_parent.add_cascade(label="master entry",menu=self.mstr)
        self.mstr.add_command(label="new book",command=self.new_book)#command1
        self.mstr.add_command(label="Member",command=self.new_member)#command2
        #creating book_issue_return menu
        self.tsecn=Menu(self.tk_parent,font=("Comic Sans MS",15),fg="blue",tearoff=0)
        self.tk_parent.add_cascade(label="book_issue_return",menu=self.tsecn)
        self.tsecn.add_command(label="book issue",command=self.book_Borrow)#command1
        self.tsecn.add_command(label="book return",command=self.book_Return)#command2
        #creating list of totoal books,total members 
        self.rept=Menu(self.tk_parent,font=("Comic Sans MS",15),fg="blue",tearoff=0)
        self.tk_parent.add_cascade(label="library report",menu=self.rept)
        self.rept.add_command(label="book list",command=self.total_books_list)#command1
        self.rept.add_command(label="member list",command=self.manipulate_memb_datas)#command2        
        #creating history of lended books
        self.hist_book=Menu(self.tk_parent,font=("Comic Sans MS",15),fg="blue",tearoff=0)
        self.tk_parent.add_cascade(label="history ofbooks",menu=self.hist_book)
        self.hist_book.add_command(label="issued book",command=self.hist_of_borrowed_books)
        self.hist_book.add_command(label="not returned books",command=self.hist_of_not_retn_books)        
        #about author
        self.author=Menu(self.tk_parent,font=("Comic Sans MS",15),fg="blue",tearoff=0)
        self.tk_parent.add_cascade(label="Extra",menu=self.author)
        self.author.add_command(label="fine amount",command=self.fine_details)       
        self.author.add_command(label="Password",command=self.change_password)  
        #creating exit in mneu
        self.exit=Menu(self.tk_parent,font=("Comic Sans MS",15),fg="blue",tearoff=0)
        self.tk_parent.add_cascade(label="exit",menu=self.exit)
        self.exit.add_command(label="exit",command=self.exit_window)               
        self.dataBaseCreator()
    def dataBaseCreator(self):
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password)
            self.cur=self.con.cursor()
            self.cur.execute("show databases")
            self.details=self.cur.fetchall()
            self.exist=False
            for detail in self.details:
                if detail[0]=='library':
                    self.exist=True
            if self.exist:
                pass#database exists
            else:
                self.cur.execute("create database library")                
                self.con_1=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
                self.cur_1=self.con_1.cursor()
                self.cur_1.execute("CREATE TABLE IF NOT EXISTS books(bookId int PRIMARY KEY,bookName varchar(40) NOT NULL,author varchar(30) NOT NULL,price bigint,dateOfPurchase date default(CURRENT_DATE))")
                self.cur_1.execute("CREATE TABLE IF NOT EXISTS members(memberId int PRIMARY KEY,name varchar(30) NOT NULL,phoneNo varchar(15),dateOfJoining date default(CURRENT_DATE))")
                self.cur_1.execute("CREATE TABLE IF NOT EXISTS lendbook(memberId int,BookId int,lendDate date default(CURRENT_DATE) NOT NULL,returnDate date NOT NULL)")
                self.cur_1.execute("CREATE TABLE IF NOT EXISTS fine(memberId int,fineAmount int,dateOfFine date default(CURRENT_DATE))")
                self.cur_1.execute("CREATE TABLE IF NOT EXISTS pinNum(pin varchar(30))")
                self.cur_1.execute("INSERT INTO pinNum values('csc')")
                self.con.commit()
                self.con_1.commit()
                #databasse created
        except Exception:
            pass#errors occurs when there is problem in conneting with sql
        
    def passwordGen(self):
        try:
            self.Pcon=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.cur=self.Pcon.cursor()
            self.cur.execute("select pin from pinNum")
            self.Pdetails=self.cur.fetchall()
            for detail in self.Pdetails:
                self.val=detail[0]
            self.Pcon.commit()
            return self.val
        except Exception:
            pass
        finally:
            self.Pcon.close()
    def geometry__(self,win_geometry,x_in,y_in):#reusing geometry code
        try:
            self.tk_width=x_in#width of child window
            self.tk_height=y_in #height of child window
            self.scrn_width=win_geometry.winfo_screenwidth()#whole width of our screen
            self.scrn_height=win_geometry.winfo_screenheight()#whole height odf our screen
            self.x=(self.scrn_width/2)-(self.tk_width/2)#x position
            self.y=(self.scrn_height/2)-(self.tk_height/2)#y position
            win_geometry.geometry(f'{self.tk_width}x{self.tk_height}+{int(self.x)}+{int(self.y)}')
        except Exception:
            pass
    
    def exit_window(self):
        master.destroy()

class new_book_member(parent_window):
    def new_book(self):     
        self.top_book=Toplevel(master)        
        self.top_book.title("NEW BOOKS")#title
        self.geometry__(self.top_book,565,215)#centerinng window
        self.top_book.resizable('False','False')
        self.top_book_frame=Frame(self.top_book,highlightbackground="black",highlightthickness=2,background='aqua')#,highlightcolor="green"        #creaating widget
        self.top_book_frame.grid(row=1,column=1,padx=15,pady=15)#labelframe

        Label(self.top_book_frame,text="Book ID",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13),anchor="w").grid(row=1,column=1,padx=5,pady=8)
        self.b_b1=StringVar(self.top_book)      
        self.b_e1=Entry(self.top_book_frame,textvariable=self.b_b1,font=("Segoe UI Semibold",11))
        self.b_e1.grid(row=1,column=2,pady=8,padx=6)
        self.b_e1.focus_set()
       
        Label(self.top_book_frame,text="Book Name",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=1,column=3,pady=8)
        self.b_b2=StringVar(self.top_book)
        Entry(self.top_book_frame,textvariable=self.b_b2,font=("Segoe UI Semibold",11)).grid(row=1,column=4 ,pady=8,padx=10)
        
        Label(self.top_book_frame,text="Author",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=2,column=1,padx=5,pady=8)
        self.b_b3=StringVar(self.top_book)
        Entry(self.top_book_frame,textvariable=self.b_b3,font=("Segoe UI Semibold",11)).grid(row=2,column=2 ,pady=8)
        
        Label(self.top_book_frame,text="Book Price",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=2,column=3,pady=8)
        self.b_b4=StringVar(self.top_book)        
        self.b_e2=Entry(self.top_book_frame,textvariable=self.b_b4,font=("Segoe UI Semibold",11))
        self.b_e2.grid(row=2,column=4 ,pady=8,padx=10)
     
        Label(self.top_book_frame,text="date",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=3,column=1,padx=5,pady=8)
        self.d1=DateEntry(self.top_book_frame,width=24, background="#13B3AC",foreground="black",date_pattern='yyyy/mm/dd')
        self.d1.grid(row=3,column=2)
        
        Button(self.top_book_frame,text="Save",bg="#39FF14",fg="black", activebackground="black", activeforeground="#39FF14",font=("Comic Sans MS",10),command=self.new_book_function).grid(row=4,column=1,padx=5,pady=8)    
        Button(self.top_book_frame,text="clear",bg="#f5084f",fg="black", activebackground="black", activeforeground="#f5084f",font=("Comic Sans MS",10),command=self.new_book_clear).grid(row=4,column=2,padx=5,pady=8)

    def new_book_function(self):
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.cur=self.con.cursor()

            if self.b_b1.get()!="" and self.b_b2.get()!="" and self.b_b3.get()!="" and self.b_b4.get()!="":
                if self.b_b1.get().replace(" ","").startswith('0')==False and self.b_b1.get().replace(" ","").isdigit() and self.b_b4.get().replace(" ","").isdigit():
                    self.cur.execute("select bookId from books where bookId='%d'"%(int(self.b_b1.get().replace(" ",""))))#to check existence of book ge=atehr detial
                    self.list=self.cur.fetchall()
                    self.check=0
                    for i in self.list:
                        if i[0]==int(self.b_b1.get().replace(" ","")):
                            self.check+=1    
                    if self.check==0:
                        self.sql="insert into books values('%d','%s','%s','%d','%s')"%(int(self.b_b1.get().replace(" ","")),self.b_b2.get(),self.b_b3.get(),int(self.b_b4.get().replace(" ","")),self.d1.get())
                        self.cur.execute(self.sql)
                        self.con.commit()
                        self.con.close()
                        self.m1=messagebox.showinfo("info","Saved succesfully")
                        self.top_book.grab_set()
                    else:
                        self.m1=messagebox.showinfo("info","BookId Exists")        
                        self.b_e1.focus_set()
                        self.top_book.grab_set()          
                else:
                    if self.b_b1.get().replace(" ","").startswith('0') :
                        self.m1=messagebox.showinfo("info","Avoid inputting ZERO at the beginning of the value in the book ID")        
                        self.b_e1.focus_set()
                        self.top_book.grab_set()
                    elif self.b_b1.get().isdigit()==False:                        
                        self.m1=messagebox.showinfo("info","please only input numerical digits in the book ID")        
                        self.b_e1.focus_set()
                        self.top_book.grab_set()                        
                    elif self.b_b4.get().isdigit()==False:
                        self.m1=messagebox.showinfo("info","please only input numerical digits the price ID")        
                        self.b_e2.focus_set()
                        self.top_book.grab_set()                   
                    else:
                        self.m1=messagebox.showinfo("info","Invalid data")        
                        self.top_book.grab_set()
            else:
                self.m1=messagebox.showinfo("info","Provide the necessary particulars")        
                self.b_e1.focus_set()
                self.top_book.grab_set()          
        except ValueError:
            self.m1=messagebox.showinfo("info","Invalid data")        
            self.top_book.grab_set()          
        except Exception:
            self.b_b1.set("")
            self.b_b2.set("")
            self.b_b3.set("")
            self.b_b4.set("")
            pass        
        finally:
            self.con.close()
    def new_book_clear(self):
        self.b_b1.set("")
        self.b_b2.set("")
        self.b_b3.set("")
        self.b_b4.set("")
        self.b_e1.focus_set()
        self.d1.set_date(date.today())

    def new_member(self):
        self.top_member=Toplevel(master) 
        self.geometry__(self.top_member,650,170)#centering window
        self.top_member.resizable('False','False')
        self.top_member.title("NEW MEMBERS")#title
        #labelframe
        self.top_member_frame=Frame(self.top_member,highlightthickness=2,highlightbackground='black',background='aqua')
        self.top_member_frame.grid(row=1,column=1,padx=15,pady=15)

        Label(self.top_member_frame,text="Member id",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=1,column=1,padx=5,pady=8)
        self.m_m1=StringVar(self.top_member)
        self.m_e1=Entry(self.top_member_frame,textvariable=self.m_m1,font=("Segoe UI Semibold",12))
        self.m_e1.grid(row=1,column=2,padx=5,pady=8)
        self.m_e1.focus_set()

        Label(self.top_member_frame,text="Member Name",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=1,column=3,padx=5,pady=8)
        self.m_m2=StringVar(self.top_member)
        Entry(self.top_member_frame,textvariable=self.m_m2,font=("Segoe UI Semibold",12)).grid(row=1,column=4,padx=5,pady=8)

        Label(self.top_member_frame,text="Phone no",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=2,column=1,padx=5,pady=8)
        self.m_m3=StringVar(self.top_member)        
        self.m_e2=Entry(self.top_member_frame,textvariable=self.m_m3,font=("Segoe UI Semibold",12))
        self.m_e2.grid(row=2,column=2,padx=5,pady=8)

        Label(self.top_member_frame,text="Date of Joining",bg='aqua',fg="black",font=("Bahnschrift SemiBold",13)).grid(row=2,column=3,padx=5,pady=8)
        self.m_d1=DateEntry(self.top_member_frame,width=24,background="#13B3AC",foreground="black",date_pattern='yyyy/mm/dd')
        self.m_d1.grid(row=2,column=4,padx=5,pady=8)
        
        self.m_btn1=Button(self.top_member_frame,text="Save",bg="#39FF14",fg="black", activebackground="black", activeforeground="#39FF14",font=("Comic Sans MS",10),command=self.new_member_funtion).grid(row=3,column=1,padx=5,pady=8)
        self.m_btn2=Button(self.top_member_frame,text="clear",bg="#f5084f",fg="black", activebackground="black", activeforeground="#f5084f",font=("Comic Sans MS",10),command=self.new_member_clear).grid(row=3,column=2,padx=5,pady=8)

    def new_member_funtion(self):
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.cur=self.con.cursor()
            if self.m_m1.get()!=0 and self.m_m2.get()!="" and self.m_m3.get()!="":
                if self.m_m1.get().replace(" ","").startswith('0')==False and self.m_m1.get().replace(" ","").isdigit():
                    self.cur.execute("select memberId from members where memberId='%d'"%(int(self.m_m1.get().replace(" ",""))))#to check existence of member gatehr detial
                    self.list=self.cur.fetchall()
                    self.check=0
                    for i in self.list:
                        if i[0]==int(self.m_m1.get().replace(" ","")):
                            self.check+=1
                    if self.check==0 and len(str(self.m_m3.get().replace(" ","")))>=10 and self.m_m3.get().replace(" ","").isnumeric()==True:
                        self.sql="insert into members values('%d','%s','%s','%s')"%(int(self.m_m1.get().replace(" ","")),self.m_m2.get(),self.m_m3.get().replace(" ",""),self.m_d1.get())
                        self.cur.execute(self.sql)
                        self.con.commit()
                        self.con.close()
                        self.m1=messagebox.showinfo("info","Saved succesfully")
                        self.top_member.grab_set()
                    else:
                        if self.check!=0:
                            self.m1=messagebox.showinfo("info","MemberId Exist")       
                            self.m_e1.focus_set()
                            self.top_member.grab_set()          
                        elif self.m_m3.get().replace(" ","").isnumeric()==False:
                            self.m1=messagebox.showinfo("info","please only input numerical digits in mobile no")       
                            self.m_e2.focus_set()
                            self.top_member.grab_set()          
                        else:
                            self.m1=messagebox.showinfo("info","kindly provide the correct phone no")
                            self.m_e2.focus_set()
                            self.top_member.grab_set()          
                else:
                    if self.m_m1.get().replace(" ","").startswith('0') :
                        self.m1=messagebox.showinfo("info","Avoid inputting zero at the beginning of the value in member ID")        
                        self.m_e1.focus_set()
                        self.top_member.grab_set()
                    else:
                        self.m1=messagebox.showinfo("info","please only input numerical digits in member ID")        
                        self.m_e1.focus_set()
                        self.top_member.grab_set()
            else:
                self.m1=messagebox.showinfo("info","Provide the necessary particulars")        
                self.m_e1.focus_set()
                self.top_member.grab_set()          
        except Exception:
            self.m_m1.set("")
            self.m_m3.set("")
            self.m_m2.set("")
            pass
        finally:
            self.con.close()

    def new_member_clear(self):
        self.m_m1.set("")
        self.m_m2.set("")
        self.m_m3.set("")
        self.m_e1.focus_set()
        self.m_d1.set_date(date.today())

class book_borrow_and_return(new_book_member):
    def book_Borrow(self):
        self.book_borrow=Toplevel(master)
        self.geometry__(self.book_borrow,665,170)#centering wiget
        self.book_borrow.resizable('False','False')
        self.book_borrow.title("BOOK BORROW")
        #frame
        self.fgn='black'#chose foreground
        self.bgn='orange'#chose background
        
        self.book_borrow_frame=Frame(self.book_borrow,highlightthickness=2,highlightbackground="black",background='orange')
        self.book_borrow_frame.grid(row=1,column=1,padx=10,pady=10)

        Label(self.book_borrow_frame,text="Memeber id",fg=self.fgn,bg=self.bgn,font=("Bahnschrift SemiBold",13)).grid(row=1,column=1,padx=10,pady=8)
        self.i_m1=StringVar(self.book_borrow)
        self.i_e1=Entry(self.book_borrow_frame,font=("Segoe UI Semibold",12),textvariable=self.i_m1)
        self.i_e1.grid(row=1,column=2,padx=5,pady=8)
        self.i_e1.focus_set()

        Label(self.book_borrow_frame,text="Book id",fg=self.fgn,bg=self.bgn,font=("Bahnschrift SemiBold",13)).grid(row=1,column=3,pady=8)
        self.i_m2=StringVar(self.book_borrow)
        self.i_e2=Entry(self.book_borrow_frame,font=("Segoe UI Semibold",12),textvariable=self.i_m2)
        self.i_e2.grid(row=1,column=4,padx=5,pady=8)

        Label(self.book_borrow_frame,text="Lending date",fg=self.fgn,bg=self.bgn,font=("Bahnschrift SemiBold",13)).grid(row=2,column=1,pady=8)
        self.iLend_d1=DateEntry(self.book_borrow_frame,width=27,background="orange",foreground="black",date_pattern='yyyy/mm/dd')
        self.iLend_d1.grid(row=2,column=2,padx=5)

        Label(self.book_borrow_frame,text="Returning date",fg=self.fgn,bg=self.bgn,font=("Bahnschrift SemiBold",13)).grid(row=2,column=3,pady=8)
        self.iReturn_d1=DateEntry(self.book_borrow_frame,width=27,background="orange",foreground="black",date_pattern='yyyy/mm/dd')
        self.iReturn_d1.grid(row=2,column=4)
        
        Button(self.book_borrow_frame,text="Check out book",bg="#39FF14",fg="black", activebackground="black", activeforeground="#39FF14",font=("Comic Sans MS",11),command=self.book_borrow_function).grid(row=3,column=1,padx=5,pady=8)
        Button(self.book_borrow_frame,text="Clear",bg="#f5084f",fg="black", activebackground="black", activeforeground="#f5084f",font=("Comic Sans MS",11),command=self.book_borrow_clear).grid(row=3,column=2,padx=5,pady=8)
        #grid
    def book_borrow_function(self):
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.cur_check1=self.con.cursor()#memeber
            self.cur_check2=self.con.cursor()#books
            self.cur_check3=self.con.cursor()#no of times
            self.cur_save=self.con.cursor()

            if self.i_m1.get()!="" and self.i_m2.get()!="":
                if self.i_m1.get().replace(" ","").startswith('0')==False and self.i_m1.get().replace(" ","").isdigit() and self.i_m2.get().replace(" ","").startswith('0')==False and self.i_m2.get().replace(" ","").isdigit():
                    self.cur_check1.execute("select memberId from members where memberId='%d'"%(int(self.i_m1.get().replace(" ",""))))#to check existence of member gatehr detial
                    self.list_l1=self.cur_check1.fetchall()#cheking existence of the member in member database
                    self.cur_check2.execute("select bookId from books where bookId='%d'"%(int(self.i_m2.get().replace(" ",""))))#to check existence of member gatehr detial
                    self.list_l2=self.cur_check2.fetchall()#checking the esistence of the book in book database
                    self.cur_check3.execute("select memberId,bookId from lendbook where memberId='%d'"%(int(self.i_m1.get().replace(" ",""))))#to check the no of boroown time
                    self.list_l3=self.cur_check3.fetchall()
                    self.con.commit()
                    
                    self.check_c1=0
                    self.check_c2=0
                    self.check_c3=0
                    self.check_c4=0
                    for i in self.list_l1:#member checking loop
                        if i[0]==int(self.i_m1.get().replace(" ","")):
                            self.check_c1+=1
                    self.cur_check1.close()
                    for j in self.list_l2:#boook checking loop
                        if j[0]==int(self.i_m2.get().replace(" ","")):
                            self.check_c2+=1
                    self.cur_check2.close()
                    
                    for k in self.list_l3:
                        if k[0]==int(self.i_m1.get().replace(" ","")):#member iterate
                            self.check_c3+=1
                        if k[1]==int(self.i_m2.get().replace(" ","")):#same bookcheck
                            self.check_c4+=1
                    self.cur_check3.close()

                    if self.check_c1!=0 and self.check_c2!=0:
                        if self.check_c3 <10 and self.check_c4 <2:
                            self.sql="insert into lendbook values('%d','%d','%s','%s')"%(int(self.i_m1.get().replace(" ","")),int(self.i_m2.get().replace(" ","")),self.iLend_d1.get(),self.iReturn_d1.get())
                            self.cur_save.execute(self.sql)
                            self.con.commit()
                            self.con.close()
                            self.m1=messagebox.showinfo("info","Saved succesfully")
                            self.book_borrow.grab_set()
                        else:
                            if self.check_c3>9:
                                self.m1=messagebox.showinfo("info","You have the reached the maximum limit [10])")
                                self.book_borrow.grab_set()
                            else:
                                self.m1=messagebox.showinfo("info","You can only borrow the same book twice")
                                self.book_borrow.grab_set()
                    else:
                        if self.check_c1==0 and self.check_c2==0:
                            self.m1=messagebox.showinfo("info","Both Bookid and Member didnt exist")
                            self.i_e1.focus_set()
                            self.book_borrow.grab_set()
                        elif self.check_c1==0:
                            self.m1=messagebox.showinfo("info","Enroll to acess book lending services!")
                            self.i_e1.focus_set()
                            self.book_borrow.grab_set()
                        else:
                            self.m1=messagebox.showinfo("info","provide a valid book id")    
                            self.i_e2.focus_set()
                            self.book_borrow.grab_set()
                else:
                    if self.i_m1.get().replace(" ","").startswith('0')==True or self.i_m1.get().isdigit()==False:
                        if self.i_m1.get().replace(" ","").startswith('0'):
                            self.m1=messagebox.showinfo("info","Avoid inputting zero at the beginning of the member id value")    
                            self.i_e1.focus_set()
                            self.book_borrow.grab_set()
                        else:
                            self.m1=messagebox.showinfo("info","please only input numerical digits in member id")    
                            self.i_e1.focus_set()
                            self.book_borrow.grab_set()
                    else:
                        if self.i_m2.get().startswith('0'):
                            self.m1=messagebox.showinfo("info","Avoid inputting zero at the beginning of the bookid value")    
                            self.i_e2.focus_set()
                            self.book_borrow.grab_set()
                        else:
                            self.m1=messagebox.showinfo("info","please only input numerical digits")    
                            self.i_e2.focus_set()
                            self.book_borrow.grab_set()
            else:
                self.m1=messagebox.showinfo("info","provide the necessary particulars")        
                self.i_e1.focus_set()
                self.book_borrow.grab_set()
        except Exception:
            self.i_m1.set("")
            self.i_m2.set("")
            pass
        finally:
            self.con.close()

    def book_borrow_clear(self):
        self.i_m1.set("")
        self.i_m2.set("")
        self.i_e1.focus_set()
        self.iLend_d1.set_date(date.today())
        self.iReturn_d1.set_date(date.today())

    def book_Return(self):
        self.book_return=Toplevel(master)
        self.geometry__(self.book_return,605,185)
        self.book_return.resizable('False','False')
        self.book_return.title("BORROW BOOK")
        #color
        self.r_fgn='black'
        self.r_bgn='orange' 
        self.book_return_frame=Frame(self.book_return,highlightbackground="black",highlightthickness=2,background=self.r_bgn)
        self.book_return_frame.grid(row=1,column=1,padx=15,pady=15)

        Label(self.book_return_frame,text="Meber id",fg=self.r_fgn,bg=self.r_bgn,font=("Bahnschrift SemiBold",13)).grid(row=1,column=1,padx=5,pady=7)
        self.br_t1=StringVar()
        self.r_e1=Entry(self.book_return_frame,textvariable=self.br_t1,font=("Segoe UI Semibold",12))
        self.r_e1.grid(row=1,column=2,padx=5,pady=7)
        self.r_e1.focus_set()
        
        Label(self.book_return_frame,text="Book id",fg=self.r_fgn,bg=self.r_bgn,font=("Bahnschrift SemiBold",13)).grid(row=1,column=3,padx=5,pady=7)
        self.br_t2=StringVar()
        self.r_e2=Entry(self.book_return_frame,textvariable=self.br_t2,font=("Segoe UI Semibold",12))
        self.r_e2.grid(row=1,column=4,padx=5,pady=7)
        
        Label(self.book_return_frame,text="Fine amount",fg=self.r_fgn,bg=self.r_bgn,font=("Bahnschrift SemiBold",13)).grid(row=2,column=1,padx=5,pady=7)
        self.br_t3=IntVar()
        Entry(self.book_return_frame,textvariable=self.br_t3,font=("Segoe UI Semibold",12)).grid(row=2,column=2,padx=5,pady=7)

        Button(self.book_return_frame,text="Verify",bg="#0ff4dd",fg="black", activebackground="black", activeforeground="#0ff4dd",font=("Comic Sans MS",11),command=self.book_return_check).grid(row=2,column=4,padx=5,pady=7)
        self.chk_c1_btn=Button(self.book_return_frame,text="return",bg="#0ff422",fg="black", activebackground="black", activeforeground="#0ff422",font=("Comic Sans MS",11),command=self.chk_chkbtn_used)
        self.chk_c1_btn.grid(row=3,column=1,padx=5,pady=13)
        Button(self.book_return_frame,text="Clear",bg="#f5084f",fg="black", activebackground="black", activeforeground="#f5084f",font=("Comic Sans MS",11),command=self.book_return_clear).grid(row=3,column=2)
        
        
    def chk_chkbtn_used(self):
        try:
            if self.br_t1.get()!="" and self.br_t2.get()!="":            
                self.m1=messagebox.showinfo("info","Engage the verify button to proceed further")            
            else:
                self.m1=messagebox.showinfo("info","provide the necessary particulars")
            self.book_return.grab_set()
        except Exception:
            self.br_t1.set("")
            self.br_t2.set("")
    def book_return_check(self):
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.cur_check1=self.con.cursor()
            if self.con.is_connected:
                if self.br_t1.get()!="" and self.br_t2.get()!="":
                    if self.br_t1.get().replace(" ","").startswith('0')==False and self.br_t1.get().replace(" ","").isdigit() and self.br_t2.get().replace(" ","").startswith('0')==False and self.br_t2.get().replace(" ","").isdigit():
                        self.sql_1="select * from lendbook where memberId='%d'  and bookId='%d'"%(int(self.br_t1.get().replace(" ","")),int(self.br_t2.get().replace(" ","")))
                        self.cur_check1.execute(self.sql_1)
                        self.list_1=self.cur_check1.fetchall()
                        self.con.commit()
                        if self.list_1!=[]:#exixstence of book and meber in return table
                            self.sql_2="select * from lendbook where CURRENT_DATE>returnDate and memberId='%d' and bookId='%d'"%(int(self.br_t1.get().replace(" ","")),int(self.br_t2.get().replace(" ","")))
                            self.cur_check1.execute(self.sql_2)
                            self.store=self.cur_check1.fetchall()
                            if self.store!=[]:        
                                self.br_t3.set(5)
                                self.chk_c1_btn.config(command=self.book_return_funtion)
                            else:                  
                                self.br_t3.set(0.00)
                                self.chk_c1_btn.config(command=self.book_return_funtion)
                            
                        else:
                            self.sql_3="select memberId from lendbook where memberId='%d'"%(int(self.br_t1.get().replace(" ","")))
                            self.cur_check1.execute(self.sql_3)
                            self.list_2=self.cur_check1.fetchall()
                            self.con.commit()
                            if self.list_2==[]:
                                self.m1=messagebox.showinfo("info","User didn't check out the book")
                                self.book_return.grab_set()
                            else:
                                self.m1=messagebox.showinfo("info","verify the id number of book")
                                self.book_return.grab_set()
                    else:
                        if self.br_t1.get().replace(" ","").startswith('0')==True or self.br_t1.get().isdigit()==False:
                            if self.br_t1.get().replace(" ","").startswith('0'):
                                self.m1=messagebox.showinfo("info","Avoid inputting zero at the beginning of the member value")    
                                self.r_e1.focus_set()
                                self.book_return.grab_set()
                            else:
                                self.m1=messagebox.showinfo("info","please only input numerical digits in member id")    
                                self.r_e1.focus_set()
                                self.book_return.grab_set() 
                        else:
                            if self.br_t2.get().replace(" ","").startswith('0'):
                                self.m1=messagebox.showinfo("info","Avoid inputting zero at the beginning of the book value")    
                                self.r_e2.focus_set()
                                self.book_return.grab_set()
                            else:
                                self.m1=messagebox.showinfo("info","please only input numerical digits in book id")    
                                self.r_e2.focus_set()
                                self.book_return.grab_set()
                else:
                    self.m1=messagebox.showinfo("info","provide the necessary particulars")
                    self.r_e1.focus_set()
                    self.book_return.grab_set()
            else:
                pass
        except Exception:
            self.br_t1.set("")            
            self.br_t2.set("")            
            self.book_return.grab_set()
            pass

    def book_return_funtion(self):#deleting the deatils
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.cur=self.con.cursor()#delete 
        
            if self.br_t1.get()!="" and self.br_t2.get()!="":            
                self.sql_1="select * from lendbook where memberId='%d'  and bookId='%d'"%(int(self.br_t1.get().replace(" ","")),int(self.br_t2.get().replace(" ","")))
                self.cur.execute(self.sql_1)
                self.list_1=self.cur.fetchall()
                self.con.commit()
                if self.list_1!=[]:                        
                    self.sql_d1="delete from lendbook where memberId='%d' and bookId='%d' limit 1"%(int(self.br_t1.get().replace(" ","")),int(self.br_t2.get().replace(" ","")))
                    self.cur.execute(self.sql_d1)
                    self.con.commit()
                    self.m1=messagebox.showinfo("info","The borrowed book has been sucessfully returneed")
                    self.book_return.grab_set()
                    self.chk_c1_btn.config(command=self.chk_chkbtn_used)
                    if self.br_t3.get()!=0:
                        self.sql_i1="insert into fine(memberId,fineAmount) values('%d','%d')"%(int(self.br_t1.get().replace(" ","")),self.br_t3.get() )
                        self.cur.execute(self.sql_i1)
                        self.con.commit()                    
                else:
                    self.m1=messagebox.showinfo("info","Check the details")                     
                    self.book_return.grab_set()
            else:
                self.m1=messagebox.showinfo("info","provide the necessary particulars")           
                self.r_e1.focus_set()
                self.book_return.grab_set()
        except Exception:
            self.br_t3.set("")
            self.br_t1.set("")
            self.br_t2.set(0)
            pass
            self.m1=messagebox.showinfo("info","went wrong")       
            self.book_return.grab_set()
        finally:
            self.con.close()
    def book_return_clear(self):
        self.br_t3.set("")
        self.br_t1.set("")
        self.br_t2.set("")
        self.r_e1.focus_set()
class library_report(book_borrow_and_return):
    def total_books_list(self):
        self.book_list=Toplevel(master)
        self.book_list.configure(background='#101820')
        self.geometry__(self.book_list,750,480)#centerinng window
        self.book_list.resizable('False','False')
        self.Lframe=LabelFrame(self.book_list,text="book list",border=2,borderwidth=15,background='aqua')        #frame
        self.Lframe.grid(row=1,column=1,padx=20,pady=15)

        self.frame1=Frame(self.Lframe)         
        self.frame1.grid(row=1,column=1)        
        #style
        self.style=ttk.Style(self.book_list)
        self.style.theme_use("clam")
        self.style.configure("Treeview",background="#ccffcc")
        self.style.map('Treeview',background=[('selected','green')])
         
        self.book_tree_view=ttk.Treeview(self.frame1,height=5)
        self.book_tree_view.grid(row=1,column=1)
        
        self.book_tree_view['columns']=("book_id","book_name","author","price","Date_of_purchase")
        #format
        self.book_tree_view.column("#0",width=0,minwidth=20,anchor=CENTER)
        self.book_tree_view.column("book_id",width= 135,minwidth=20,anchor=CENTER)
        self.book_tree_view.column("book_name",width=135,minwidth=20,anchor=CENTER)
        self.book_tree_view.column("author",width=135,minwidth=20,anchor=CENTER)
        self.book_tree_view.column("price",width=135,minwidth=20,anchor=CENTER)
        self.book_tree_view.column("Date_of_purchase",width=120,minwidth=20,anchor=CENTER)
        #heading
        self.book_tree_view.heading("#0",text="S.no",anchor=CENTER) 
        self.book_tree_view.heading("book_id",text="book id",anchor=CENTER)
        self.book_tree_view.heading("book_name",text="book name",anchor=CENTER)
        self.book_tree_view.heading("author",text="author",anchor=CENTER)
        self.book_tree_view.heading("price",text="book price",anchor=CENTER)
        self.book_tree_view.heading("Date_of_purchase",text="date of purchase",anchor=CENTER)       

        self.sb=ttk.Scrollbar(self.frame1,orient='vertical',command=self.book_tree_view.yview)       
        self.book_tree_view.configure(yscrollcommand=self.sb.set)
        self.sb.grid(row=1,column=2,sticky=N+S)
        
        #binding
        self.book_tree_view.bind("<Double-1>",self.select_book)

        #self.Lframe_search=LabelFrame(self.book_list,text="search",border=2,borderwidth=15,background='aqua',foreground='black',highlightbackground='black')
        self.Lframe_search=Frame(self.book_list,border=2,borderwidth=15,background='aqua',highlightthickness=3,highlightbackground='black')
        self.Lframe_search.grid(row=2,column=1,sticky=E+W,padx=20,pady=10)
        Label(self.Lframe_search,bg='aqua',fg='black',text="search",font=("Bahnschrift SemiBold",10)).grid(row=1,column=2,padx=10,pady=3)
        self.ser_var=StringVar()
        Entry(self.Lframe_search,textvariable=self.ser_var).grid(row=1,column=3,padx=10,pady=3)
        Button(self.Lframe_search,text="search",bg="#01ff27",fg="black", activebackground="black", activeforeground="#0ff485",font=("Comic Sans MS",9),command=self.search_books).grid(row=1,column=4,padx=10,pady=3)
        Button(self.Lframe_search,text="clear",bg="#ffabab",fg="black", activebackground="black", activeforeground="#ffabab",font=("Comic Sans MS",9),command=self.ser_book_retriev_clr).grid(row=1,column=5,padx=10,pady=3)       
        #update and delete opton
        self.Lframe1=LabelFrame(self.book_list,text="edit here",border=2,borderwidth=15,background='aqua',foreground='black',highlightbackground='black') 
        self.Lframe1.grid(row=3,column=1,padx=20,pady=10,sticky=E+W)       
        self.frame2=Frame(self.Lframe1,background='aqua')
        self.frame2.grid(row=1,column=1)
        #color
        self.t_bgn='aqua'
        self.t_fgn='black'
        Label(self.frame2,text="Book ID",fg=self.t_fgn,bg=self.t_bgn,font=("Bahnschrift SemiBold",10)).grid(row=1,column=1,padx=10,pady=3)
        self.b_edit_l2=Label(self.frame2,text=" \t\t ",bg="grey")
        self.b_edit_l2.grid(row=1,column=2,padx=10,pady=3)

        Label(self.frame2,text="Book name",fg=self.t_fgn,bg=self.t_bgn,font=("Bahnschrift SemiBold",10)).grid(row=1,column=3,padx=10,pady=3)
        self.b_edit_t1=StringVar()
        Entry(self.frame2,textvariable=self.b_edit_t1,font=("Segoe UI Semibold",10)).grid(row=1,column=4,padx=10,pady=3)

        Label(self.frame2,text="Author",fg=self.t_fgn,bg=self.t_bgn,font=("Bahnschrift SemiBold",10)).grid(row=2,column=1,padx=10,pady=3)
        self.b_edit_t2=StringVar()
        Entry(self.frame2,textvariable=self.b_edit_t2,font=("Segoe UI Semibold",10)).grid(row=2,column=2,padx=10,pady=3)

        Label(self.frame2,text="Book price",fg=self.t_fgn,bg=self.t_bgn,font=("Bahnschrift SemiBold",10)).grid(row=2,column=3,padx=10,pady=3)
        self.b_edit_t3=IntVar()
        self.b_edit_t3.set("")
        Entry(self.frame2,textvariable=self.b_edit_t3,font=("Segoe UI Semibold",10)).grid(row=2,column=4,padx=10,pady=3)

        Label(self.frame2,text="Purchase Date",fg=self.t_fgn,bg=self.t_bgn,font=("Bahnschrift SemiBold",10)).grid(row=3,column=1,padx=10,pady=3)
        self.b_edit_d1=DateEntry(self.frame2,width=21,background="#13B3AC",foreground="black",date_pattern='yyyy/mm/dd')
        self.b_edit_d1.grid(row=3,column=2,padx=10,pady=3)

        Label(self.frame2,text="Password",fg=self.t_fgn,bg=self.t_bgn,font=("Bahnschrift SemiBold",10)).grid(row=3,column=3,padx=10,pady=3)
        self.b_edit_t4=StringVar()
        self.b_edit_e4=Entry(self.frame2,show="*",textvariable=self.b_edit_t4,font=("Segoe UI Semibold",10))
        self.b_edit_e4.grid(row=3,column=4,padx=10,pady=3)
        self.b_edit_t5=IntVar()
        self.b_edit_c1=Checkbutton(self.frame2,variable=self.b_edit_t5,fg="green",text="<o>",font=("Bahnschrift SemiBold",10),indicatoron=NO,command=self.show_password)
        self.b_edit_c1.grid(row=3,column=5,padx=10,pady=3)

        Button(self.frame2,text="Update",bg="#223af0",fg="black", activebackground="black", activeforeground="#223af0",font=("Comic Sans MS",9),command=self.book_widget_update).grid(row=4,column=1,padx=10,pady=3)
        Button(self.frame2,text="Delete",bg="#ff1414",fg="black", activebackground="black", activeforeground="#ff1414",font=("Comic Sans MS",9),command=self.book_widget_delete).grid(row=4,column=2,padx=10,pady=3)
        Button(self.frame2,text="Clear",bg="#ffabab",fg="black", activebackground="black", activeforeground="#ffabab",font=("Comic Sans MS",9),command=self.clear_books_widget).grid(row=4,column=3,padx=10,pady=3)

        self.show_detailsOfBook()#callling values loading datas

    def show_detailsOfBook(self):
        try:
            self.con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.select_detail=self.con.cursor()#memeber
            self.select_detail.execute("select * from books")
            self.listOfBook=self.select_detail.fetchall()
            
            self.book_tree_view.tag_configure('odd',background='white')
            self.book_tree_view.tag_configure('even',background='lightblue')        
            self.color_count=0
            for details in self.listOfBook:
                if self.color_count%2==0:
                    self.book_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4]),tags=('even',))
                else:
                    self.book_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4]),tags=('odd',))
                self.color_count+=1
        except Exception:
            pass    
    def show_password(self):
        if self.b_edit_t5.get()==1:
            self.b_edit_c1.config(fg="red")
            self.b_edit_e4.config(show="")
        else:
            self.b_edit_c1.config(fg="green")
            self.b_edit_e4.config(show="*")
        
    def ser_book_retriev_clr(self):
        try:
            for  item in  self.book_tree_view.get_children():
                self.book_tree_view.delete(item)
            self.ser_var.set("")
            self.show_detailsOfBook()
        except Exception:
            pass
    def search_books(self):
        try:
            for  item in  self.book_tree_view.get_children():
                self.book_tree_view.delete(item)

            self.ser_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.ser_cur=self.ser_con.cursor()#books

            if self.ser_var.get()!="":
                if self.ser_var.get().isdigit():
                    self.ser_cur.execute("select * from books where bookId='%d'"%(int(self.ser_var.get())))
                    self.listOfBook=self.ser_cur.fetchall()
                else:
                    self.ser_cur.execute("select * from books where bookName like '%s' "%("%"+self.ser_var.get()+"%"))
                    self.listOfBook=self.ser_cur.fetchall()

            self.book_tree_view.tag_configure('odd',background='white')
            self.book_tree_view.tag_configure('even',background='lightblue')        
            self.color_count=0
            for details in self.listOfBook:
                if self.color_count%2==0:
                    self.book_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4]),tags=('even',))
                else:
                    self.book_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4]),tags=('odd',))
                self.color_count+=1
        except Exception:
            pass    
    def book_widget_update(self):
        try:
            self.updt_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.updt_cur=self.updt_con.cursor()#books          
            if self.b_edit_t1.get()!="" and self.b_edit_t2.get()!="" and self.b_edit_t3.get()!=0:
                if self.b_edit_t4.get()==self.passwordGen():
                    self.m2=messagebox.askyesno('confirmation','Would you like to update the information ?')
                    if self.m2==True:                     
                        self.new=int(self.b_edit_l2.cget("text"))#getiing the bookId
                        self.updt_cur.execute("update books set bookName='%s', author='%s', price='%d', dateOfPurchase='%s' where bookId='%d'"%(self.b_edit_t1.get(),self.b_edit_t2.get(),self.b_edit_t3.get(),self.b_edit_d1.get(),self.new))
                        self.updt_con.commit()
                        self.m1=messagebox.showinfo("info","Updated sucessfully!")
                        self.book_list.grab_set()
                elif self.b_edit_t4.get()=='':
                    self.m1=messagebox.showwarning("PIN","kindly Enter password")
                    self.book_list.grab_set()
                else:
                    self.m1=messagebox.showwarning("PIN","the password entered is incorrect")
                    self.book_list.grab_set()
            else:
                self.m1=messagebox.showinfo("info","provide the necessary particulars")
                self.book_list.grab_set()
            
        except Exception:
            self.m1=messagebox.showwarning("warning","detilas entered is wrong")
            self.book_list.grab_set()
            pass

    def book_widget_delete(self):
        try:
            self.delt_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.delt_cur=self.delt_con.cursor()#books        
        
            if self.b_edit_t1.get()!="" and self.b_edit_t2.get()!="" and self.b_edit_t3.get()!=0:
                if self.b_edit_t4.get()==self.passwordGen():
                    self.m2=messagebox.askyesno('confirmation','would you like to remove the information ?')
                    if self.m2==True:
                        self.new=int(self.b_edit_l2.cget("text"))#getiing the bookId
                        self.delt_cur.execute("delete from books where bookId='%d'"%(self.new))
                        self.delt_con.commit()
                        self.m1=messagebox.showinfo("info","deleted succesfully")
                        self.book_list.grab_set()
                    else:
                        self.book_list.grab_set()
                elif self.b_edit_t4.get()=='':
                    self.m1=messagebox.showwarning("PIN","kindly enter password")
                    self.book_list.grab_set()
                else:
                    self.m1=messagebox.showwarning("PIN","the password entered is incorrect")
                    self.book_list.grab_set()
            else:
                self.m1=messagebox.showinfo("info","provide the necessary particulars")
                self.book_list.grab_set()
            
        except Exception:
            self.m1=messagebox.showwarning("warning","wrong details")
            self.book_list.grab_set()
            pass
              
    def clear_books_widget(self):
        self.b_edit_l2.config(text="\t\t")
        self.b_edit_t1.set("")
        self.b_edit_t2.set("")
        self.b_edit_t3.set("")
        self.b_edit_t4.set("")
        self.b_edit_d1.set_date(date.today())

    def select_book(self,event):#binding option
        try:
            self.book_v1=self.book_tree_view.focus()
            self.book_v=self.book_tree_view.item(self.book_v1,'values')   
            self.b_edit_l2.config(text=self.book_v[0]),self.b_edit_t1.set(self.book_v[1]),self.b_edit_t2.set(self.book_v[2])
            self.b_edit_t3.set(self.book_v[3])
            self.b_edit_d1.set_date(self.book_v[4])
        except Exception:
            pass
            
    #member details
    def manipulate_memb_datas(self):
        self.member_list=Toplevel(master)
        self.member_list.configure(background='#101820')
        self.geometry__(self.member_list,655,495)#centering widget
        self.member_list.resizable('False','False')
        
        self.Lframe_m1=LabelFrame(self.member_list,text="member list",background='aqua',border=2,borderwidth=15)        
        self.Lframe_m2=LabelFrame(self.member_list,text="update member data",background='aqua',border=2,borderwidth=15)
        self.frame1_m1=Frame(self.Lframe_m1)

        self.Lframe_m1.grid(row=1,column=1,padx=20,pady=15,sticky=E+W)
        self.frame1_m1.grid(row=1,column=1)        
        
        self.style=ttk.Style(self.member_list)
        #alt,default,clam
        self.style.theme_use("clam")
        self.style.configure("Treeview",background="#ccffcc")        
        self.style.map('Treeview',background=[('selected','green')])
        
        self.memb_tree_view=ttk.Treeview(self.frame1_m1,height=5)
        self.memb_tree_view.grid(row=1,column=1)
        self.memb_tree_view['columns']=("member_id","member_name","mobile_no","join_date")
        #format
        self.memb_tree_view.column("#0",width=0,minwidth=25,anchor=CENTER)
        self.memb_tree_view.column("member_id",width=140,minwidth=25,anchor=CENTER)
        self.memb_tree_view.column("member_name",width=140,minwidth=25,anchor=CENTER)
        self.memb_tree_view.column("mobile_no",width=140,minwidth=25,anchor=CENTER)
        self.memb_tree_view.column("join_date",width=140,minwidth=25,anchor=CENTER)         
        #heading
        self.memb_tree_view.heading("#0",text="S.no",anchor=CENTER) 
        self.memb_tree_view.heading("member_id",text="member id",anchor=CENTER)
        self.memb_tree_view.heading("member_name",text="member name",anchor=CENTER)
        self.memb_tree_view.heading("mobile_no",text="phone no",anchor=CENTER)
        self.memb_tree_view.heading("join_date",text="date of joining",anchor=CENTER)

        self.sb_m1=ttk.Scrollbar(self.frame1_m1,orient='vertical',command=self.memb_tree_view.yview)       
        self.memb_tree_view.configure(yscrollcommand=self.sb_m1.set)
        self.sb_m1.grid(row=1,column=2,sticky=N+S)

        #binding
        self.memb_tree_view.bind("<Double-1>",self.select_memb)
        #creating searching option
        self.Lframe_mem_search=Frame(self.member_list,border=2,borderwidth=15,background='aqua',highlightthickness=3,highlightbackground='black')
        self.Lframe_mem_search.grid(row=2,column=1,sticky=E+W,padx=20,pady=10)
        Label(self.Lframe_mem_search,fg="black",bg="aqua",text="search",font=("Bahnschrift SemiBold",10)).grid(row=1,column=2,padx=10,pady=3)
        self.ser_var_memb=StringVar()
        Entry(self.Lframe_mem_search,textvariable=self.ser_var_memb,font=("Segoe UI Semibold",10)).grid(row=1,column=3,padx=10,pady=3)
        Button(self.Lframe_mem_search,text="search",bg="#01ff27",fg="black", activebackground="black", activeforeground="#0ff485",font=("Comic Sans MS",9),command=self.search_memb).grid(row=1,column=4,padx=10,pady=3)
        Button(self.Lframe_mem_search,text="clear",bg="#ff7b7b",fg="black", activebackground="black", activeforeground="#ff7b7b",font=("Comic Sans MS",9),command=self.search_memb_clr).grid(row=1,column=5,padx=10,pady=3)
        
        #Label frame2
        self.Lframe_m2.grid(row=3,column=1,padx=20,pady=10,sticky=E+W)
        #creating editing option
        self.frame2_m2=Frame(self.Lframe_m2,background='aqua')        
        self.frame2_m2.grid(row=2,column=2,pady=10)
        self.m_bg='aqua'
        self.m_fg='black'
        
        Label(self.frame2_m2,text=" member id",fg=self.m_fg,bg=self.m_bg,font=("Bahnschrift SemiBold",10)).grid(row=1,column=1,padx=10,pady=3)
        self.m_edit_l2=Label(self.frame2_m2,text=" \t\t ",bg='grey')
        self.m_edit_l2.grid(row=1,column=2,padx=10,pady=3)
         
        Label(self.frame2_m2,text="member name",fg=self.m_fg,bg=self.m_bg,font=("Bahnschrift SemiBold",10)).grid(row=1,column=3,padx=10,pady=3)
        self.m_edit_t1=StringVar()
        Entry(self.frame2_m2,textvariable=self.m_edit_t1,font=("Segoe UI Semibold",10)).grid(row=1,column=4,padx=10,pady=3)
         
        Label(self.frame2_m2,text="phone no",fg=self.m_fg,bg=self.m_bg,font=("Bahnschrift SemiBold",10)).grid(row=2,column=1,padx=10,pady=3)
        self.m_edit_t2=StringVar()
        Entry(self.frame2_m2,textvariable=self.m_edit_t2,font=("Segoe UI Semibold",10)).grid(row=2,column=2,padx=10,pady=3)
 
        Label(self.frame2_m2,text="date of joining",fg=self.m_fg,bg=self.m_bg,font=("Bahnschrift SemiBold",10)).grid(row=2,column=3,padx=10,pady=3)
        self.m_edit_d1=DateEntry(self.frame2_m2,width=21, background="#13B3AC",foreground="black",date_pattern='yyyy/mm/dd')
        self.m_edit_d1.grid(row=2,column=4,padx=10,pady=3)

        self.m_edit_l6=Label(self.frame2_m2,text="password",fg=self.m_fg,bg=self.m_bg,font=("Bahnschrift SemiBold",10)).grid(row=3,column=1,padx=10,pady=3)
        self.m_edit_t3=StringVar()
        self.m_edit_e3=Entry(self.frame2_m2,show="*",font=("Segoe UI Semibold",10),textvariable=self.m_edit_t3)
        self.m_edit_e3.grid(row=3,column=2,padx=10,pady=3)
        self.m_edit_t4=IntVar()
        self.m_edit_c1=Checkbutton(self.frame2_m2,variable=self.m_edit_t4,fg="green",text="<o>",font=("Bahnschrift SemiBold",10),indicatoron=NO,command=self.show_memb_password)
        self.m_edit_c1.grid(row=3,column=3,padx=10,pady=3)

        Button(self.frame2_m2,text="clear",bg="#ff7b7b",fg="black", activebackground="black", activeforeground="#ff7b7b",font=("Comic Sans MS",9),command=self.clear_memb_widget).grid(row=3,column=4,padx=10,pady=3)
        Button(self.frame2_m2,text="update",bg="#223af0",fg="black", activebackground="black", activeforeground="#223af0",font=("Comic Sans MS",9),command=self.memb_update).grid(row=4,column=1,padx=10,pady=3)
        Button(self.frame2_m2,text="delete",bg="#ff1414",fg="black", activebackground="black", activeforeground="#ff1414",font=("Comic Sans MS",9),command=self.memb_delete).grid(row=4,column=2,padx=10,pady=3)
        
        self.memb_data()#loading datas

    def memb_data(self):
        try:
            self.memb_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.memb_cur=self.memb_con.cursor()#memeber
            self.memb_cur.execute("select * from members")
            self.listOfMembers=self.memb_cur.fetchall()
            
            self.memb_tree_view.tag_configure('odd',background='white')
            self.memb_tree_view.tag_configure('even',background='lightblue')        
            self.color_count=0
            for details in self.listOfMembers:
                if self.color_count%2==0:
                    self.memb_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3]),tags=('even',))
                else:
                    self.memb_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3]),tags=('odd',))
                self.color_count+=1
        except Exception:
            pass    

    def search_memb(self):
        try:
            for  item in  self.memb_tree_view.get_children():
                self.memb_tree_view.delete(item)

            self.srch=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.ser_memb_cur=self.srch.cursor()#books

            if self.ser_var_memb.get()!="":
                if self.ser_var_memb.get().isdigit():
                    self.ser_memb_cur.execute("select * from members where memberId='%d'"%(int(self.ser_var_memb.get())))
                    self.listOfMembers=self.ser_memb_cur.fetchall()
                else:
                    self.ser_memb_cur.execute("select * from members where name like '%s' "%("%"+self.ser_var_memb.get()+"%"))
                    self.listOfMembers=self.ser_memb_cur.fetchall()

            self.memb_tree_view.tag_configure('odd',background='white')
            self.memb_tree_view.tag_configure('even',background='lightblue')        
            self.color_count=0
            for details in self.listOfMembers:
                if self.color_count%2==0:
                    self.memb_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3]),tags=('even',))
                else:
                    self.memb_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3]),tags=('odd',))
                self.color_count+=1
        except Exception:
            pass    
    def search_memb_clr(self):
        try:
            for  item in  self.memb_tree_view.get_children():
                self.memb_tree_view.delete(item)
            self.ser_var_memb.set("")
            self.memb_data()
        except Exception:
            pass

    def show_memb_password(self):
        if self.m_edit_t4.get()==1:
            self.m_edit_c1.config(fg="red")
            self.m_edit_e3.config(show="")
        else:
            self.m_edit_c1.config(fg="green")
            self.m_edit_e3.config(show="*")

    def memb_update(self):
        try:
            self.updt_memb_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.updt_memb_cur=self.updt_memb_con.cursor()#books      
        
            if self.m_edit_t1.get()!="" and self.m_edit_t2.get()!=0:
                if self.m_edit_t3.get()==self.passwordGen() and len(str(self.m_edit_t2.get()))>=10:
                    self.m2=messagebox.askyesno('confirmation','would you like to update the information ?')
                    if self.m2==True:                     
                        self.new_var=int(self.m_edit_l2.cget("text"))#getiing the memberkId
                        self.updt_memb_cur.execute("update members set name='%s', phoneNo='%s', dateOfJoining='%s' where memberId='%d'"%(self.m_edit_t1.get(),self.m_edit_t2.get(),self.m_edit_d1.get(),self.new_var))
                        self.updt_memb_con.commit()
                        self.m1=messagebox.showinfo("info","Updated succesfully!")
                        self.member_list.grab_set()
                elif self.m_edit_t3.get()=='':
                    self.m1=messagebox.showwarning("PIN","Enter password")
                    self.member_list.grab_set()
                elif self.m_edit_t3.get()!=self.passwordGen():
                    self.m1=messagebox.showwarning("PIN","The password entered is incorrect")
                    self.member_list.grab_set()
                elif len(str(self.m_edit_t2.get()))<10:
                    self.m1=messagebox.showwarning("PIN","Wrong phone no")
                    self.member_list.grab_set()
            else:
                self.m1=messagebox.showwarning("info","Provide the necessary particulars")
                self.member_list.grab_set()
        except Exception:
            self.m1=messagebox.showwarning("INFO","Wrong details")
            self.member_list.grab_set()
            pass

    
    def memb_delete(self):
        try:
            self.delt_memb_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.delt_memb_cur=self.delt_memb_con.cursor()#books        
        
            if self.m_edit_t1.get()!="" and self.m_edit_t2.get()!=0:
                if self.m_edit_t3.get()==self.passwordGen():
                    self.m2=messagebox.askyesno('confirmation','would you like to remove the information')
                    if self.m2==True:
                        self.new_memb=int(self.m_edit_l2.cget("text"))#getiing the bookId
                        self.delt_memb_cur.execute("delete from members where memberId='%d'"%(self.new_memb))
                        self.delt_memb_con.commit()
                        self.m1=messagebox.showinfo("info","deleted succesfully")
                        self.member_list.grab_set()
                elif self.b_edit_t4.get()=='':
                    self.m1=messagebox.showwarning("pin","Enter password")
                    self.member_list.grab_set()
                else:
                    self.m1=messagebox.showwarning("pin","The password entered is incorrect")
                    self.member_list.grab_set()
            else:
                self.m1=messagebox.showwarning("INFO","Provide the necessary particulars")
                self.member_list.grab_set()
        except Exception:
            self.m1=messagebox.showwarning("INFO","wrong details")
            self.member_list.grab_set()
            pass
    
    def clear_memb_widget(self):
        self.m_edit_l2.config(text="\t\t")
        self.m_edit_t1.set("")
        self.m_edit_t2.set("")
        self.m_edit_t3.set("")
        self.m_edit_d1.set_date(date.today())
    def select_memb(self,e):#binding option
        try:
            self.memb_v1=self.memb_tree_view.focus()
            self.memb_v=self.memb_tree_view.item(self.memb_v1,'values')   
            self.m_edit_l2.config(text=self.memb_v[0]),self.m_edit_t1.set(self.memb_v[1]),self.m_edit_t2.set(self.memb_v[2])
            self.m_edit_d1.set_date(self.memb_v[3])            
        except Exception:
            pass        
    
class books_history(library_report):
    def hist_of_borrowed_books(self):
        self.book_history=Toplevel(master)
        self.book_history.configure(background='#101820')
        self.Lframe_h1=LabelFrame(self.book_history,text="history of issued books",background='aqua',border=2,borderwidth=15)
        #centering winndow
        self.geometry__(self.book_history,780,225)
        self.book_history.resizable('False','False')
        self.frame1_h1=Frame(self.Lframe_h1)
        self.Lframe_h1.grid(row=1,column=1,pady=15,padx=15)
        self.frame1_h1.grid(row=1,column=1)
        
        self.style=ttk.Style(self.frame1_h1)
        self.style.theme_use("clam")
        self.style.configure("Treeview",background="#ccffcc")
        self.style.map('Treeview',background=[('selected','green')])
        
        self.hist_tree_view=ttk.Treeview(self.frame1_h1,height=5)
        self.hist_tree_view.grid(row=1,column=1)
        self.hist_tree_view['columns']=("member_id","book_id","member_name","mobile_no","borrowed_date")
        #format
        self.hist_tree_view.column("#0",width=0,minwidth=25,anchor=CENTER)
        self.hist_tree_view.column("member_id",width=140,minwidth=25,anchor=CENTER)
        self.hist_tree_view.column("member_name",width=140,minwidth=25,anchor=CENTER)
        self.hist_tree_view.column("book_id",width=140,minwidth=25,anchor=CENTER)
        self.hist_tree_view.column("mobile_no",width=140,minwidth=25,anchor=CENTER)
        self.hist_tree_view.column("borrowed_date",width=140,minwidth=25,anchor=CENTER)         
        #heading
        self.hist_tree_view.heading("#0",text="S.no",anchor=CENTER) 
        self.hist_tree_view.heading("member_id",text="member id",anchor=CENTER)
        self.hist_tree_view.heading("member_name",text="member name",anchor=CENTER)
        self.hist_tree_view.heading("book_id",text="book id",anchor=CENTER)
        self.hist_tree_view.heading("mobile_no",text="mobile no",anchor=CENTER)
        self.hist_tree_view.heading("borrowed_date",text="date of borrow",anchor=CENTER)
        #grid
        self.sb_h1=ttk.Scrollbar(self.frame1_h1,orient='vertical',command=self.hist_tree_view.yview)       
        self.hist_tree_view.configure(yscrollcommand=self.sb_h1.set)
        self.sb_h1.grid(row=1,column=2,sticky=N+S)
        
        self.book_history_show()
        #button to show the list
        self.hist_b1=Button(self.book_history,fg='black',bg="#0aff74",activebackground='black',activeforeground="#0aff74",text="refresh",command=self.book_history_refresh)
        self.hist_b1.grid(row=5,column=1)
    def book_history_show(self):
        try:
            self.hist_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.hist_detail=self.hist_con.cursor()#memeber
            self.hist_detail.execute("select members.memberId,lendbook.bookId,members.name,members.phoneNO,lendbook.lendDate from lendbook inner join members on lendbook.memberId=members.memberId")
            self.listOfBook=self.hist_detail.fetchall()

            self.hist_tree_view.tag_configure('odd',background='white')
            self.hist_tree_view.tag_configure('even',background='lightblue')        
            self.color_count=0
            for details in self.listOfBook:
                if self.color_count%2==0:
                    self.hist_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4]),tags=('even',))
                else:
                    self.hist_tree_view.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4]),tags=('odd',))
                self.color_count+=1
        except Exception:
            pass    

    def book_history_refresh(self):
        try:
            for  item in  self.hist_tree_view.get_children():
                self.hist_tree_view.delete(item)
            self.book_history_show()
        except Exception:
            pass    

    def hist_of_not_retn_books(self):
        self.not_return=Toplevel(master)
        self.not_return.configure(background='#101820')
        #centering window
        self.geometry__(self.not_return,930,225)
        self.not_return.resizable('False','False')
        self.Lframe_n1=LabelFrame(self.not_return,text="not returned book",background='aqua',border=2,borderwidth=15)
        
        self.frame1_n1=Frame(self.Lframe_n1)
        self.Lframe_n1.grid(row=1,column=1,pady=15,padx=15)
        self.frame1_n1.grid(row=1,column=1)        
        
        self.style=ttk.Style(self.frame1_n1)
        self.style.theme_use("clam")
        self.style.configure("Treeview",background="#ccffcc")
        self.style.map('Treeview',background=[('selected','green')])
        
        self.hist_not_return=ttk.Treeview(self.frame1_n1,height=5)
        self.hist_not_return.grid(row=1,column=1)
        self.hist_not_return['columns']=("member_id","member_name","book_id","mobile_no","borrowed_date","return_date")
        #format
        self.hist_not_return.column("#0",width=0,minwidth=25,anchor=CENTER)
        self.hist_not_return.column("member_id",width=135,minwidth=25,anchor=CENTER)
        self.hist_not_return.column("member_name",width=135,minwidth=25,anchor=CENTER)
        self.hist_not_return.column("book_id",width=145,minwidth=25,anchor=CENTER)
        self.hist_not_return.column("mobile_no",width=145,minwidth=25,anchor=CENTER)
        self.hist_not_return.column("borrowed_date",width=145,minwidth=25,anchor=CENTER)         
        self.hist_not_return.column("return_date",width=145,minwidth=25,anchor=CENTER)         
        #heading
        self.hist_not_return.heading("#0",text="S.no",anchor=CENTER) 
        self.hist_not_return.heading("member_id",text="member id",anchor=CENTER)
        self.hist_not_return.heading("member_name",text="member name",anchor=CENTER)
        self.hist_not_return.heading("book_id",text="book id",anchor=CENTER)
        self.hist_not_return.heading("mobile_no",text="mobile no",anchor=CENTER)
        self.hist_not_return.heading("borrowed_date",text="date of borrow",anchor=CENTER)
        self.hist_not_return.heading("return_date",text='date of return',anchor=CENTER)         
        #grid
        self.sb_n1=ttk.Scrollbar(self.frame1_n1,orient='vertical',command=self.hist_not_return.yview)       
        self.hist_not_return.configure(yscrollcommand=self.sb_n1.set)
        self.sb_n1.grid(row=1,column=2,sticky=N+S)

        self.not_return_b1=Button(self.not_return,fg='black',bg="#0aff74",activebackground='black',activeforeground="#0aff74",text="refresh",command=self.not_returned_books)
        self.not_return_b1.grid(row=5,column=1)
        self.show_not_returned_books()

    def show_not_returned_books(self):
        try:
            self.hist_not_con=mysql.connector.connect(user='root',host='localhost',password=mysql_password,database='library')
            self.hist_not_detail=self.hist_not_con.cursor()#memeber
            self.hist_not_detail.execute("select members.memberId,members.name,lendbook.bookId,members.phoneNO,lendbook.lendDate,lendbook.returnDate from lendbook inner join members on lendbook.memberId=members.memberId where CURRENT_DATE>returnDate")
            
            self.listOfBook=self.hist_not_detail.fetchall()

            self.hist_not_return.tag_configure('odd',background='white')
            self.hist_not_return.tag_configure('even',background='lightblue')        
            self.color_count=0
            for details in self.listOfBook:
                if self.color_count%2==0:
                    self.hist_not_return.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4],details[5]),tags=('even',))
                else:
                    self.hist_not_return.insert(parent="",index='end',iid=self.color_count,values=(details[0],details[1],details[2],details[3],details[4],details[5]),tags=('odd',))
                self.color_count+=1
        except Exception:
            pass    
    def not_returned_books(self):
        try:
            for  item in  self.hist_not_return.get_children():
                self.hist_not_return.delete(item)
            self.show_not_returned_books()
            #trv.delete(*trv)
        except Exception:
            pass
class about_author(books_history):
    def fine_details(self):
        self.fine_amount=Toplevel(master)
        self.geometry__(self.fine_amount,400,140)
        self.fine_amount.configure(background='#101820')
        self.fine_amount_frame=Frame(self.fine_amount,highlightbackground='black',background='aqua',highlightthickness=2)
        self.fine_amount_frame.grid(row=1,column=1,padx=17,pady=17)
        self.f_l1=Label(self.fine_amount_frame,text="\t \t",width=17,bg="grey")
        self.f_l1.grid(row=3,column=1,padx=5,pady=7)        
        self.f_date_d1=DateEntry(self.fine_amount_frame,width=16, background="#13B3AC",foreground="black",date_pattern='yyyy/mm/dd')        
        self.f_date_d2=DateEntry(self.fine_amount_frame,width=16,background="#13B3AC",foreground="black",date_pattern='yyyy/mm/dd')
        self.f_date_d1.grid(row=2,column=1,padx=10,pady=4)
        self.f_date_d2.grid(row=2,column=2,padx=10,pady=4)

        self.a_ret=IntVar()
        Checkbutton(self.fine_amount_frame,text="fine btwn",bg='aqua',variable=self.a_ret).grid(row=2,column=3)
        Button(self.fine_amount_frame,text="fetch fine",width=16,fg='black',bg="#0aff74",activebackground='black',activeforeground="#0aff74",command=self.full).grid(row=4,column=1,pady=5)
        
    def full(self):
        try:
            self.con=mysql.connector.connect(host='localhost',user='root',password=mysql_password,database='library')
            self.cur=self.con.cursor()
            if self.a_ret.get()==1:
                self.cur.execute("select sum(fineAmount) from fine where dateOfFine between '%s' and '%s' "%(self.f_date_d1.get(),self.f_date_d2.get()))
                self.re=self.cur.fetchall()
                self.f_l1.config(text=self.re)
            else:
                self.cur.execute("select sum(fineAmount) from fine")
                self.re=self.cur.fetchall()
                self.f_l1.config(text=self.re)
        except Exception:
            pass
    def change_password(self):
        self.pswrd=Toplevel(master)
        self.geometry__(self.pswrd,315,150)
        self.pswrd_root=Frame(self.pswrd,border=2,borderwidth=15,background='aqua',highlightthickness=3,highlightbackground='black')
        self.pswrd_root.grid(row=1,column=1,padx=7,pady=7)
        Label(self.pswrd_root,text="new password",bg='aqua',fg="black",font=("Bahnschrift SemiBold",11)).grid(row=1,column=1,padx=4,pady=4)
        self.pt1=StringVar()
        Entry(self.pswrd_root,textvariable=self.pt1,font=("Segoe UI Semibold",9)).grid(row=1,column=2,padx=4,pady=4)

        Label(self.pswrd_root,text="old password",bg='aqua',fg="black",font=("Bahnschrift SemiBold",11)).grid(row=2,column=1,padx=4,pady=4)
        self.pt2=StringVar()
        Entry(self.pswrd_root,textvariable=self.pt2,font=("Segoe UI Semibold",9)).grid(row=2,column=2,padx=4,pady=4)

        Button(self.pswrd_root,text="change password",fg='black',bg="#0aff74",activebackground='black',activeforeground="#0aff74",command=self.change_pswrd_fun).grid(row=3,column=1,pady=4,padx=4)
    def change_pswrd_fun(self):        
        try:
            self.updt_con=mysql.connector.connect(host='localhost',user='root',password=mysql_password,database='library')
            self.updt_cur=self.updt_con.cursor()
            
            if self.pt1.get()!="" and self.pt2.get()!="":
                if self.pt2.get()==self.passwordGen():
                    self.m2=messagebox.askyesno('confirmation','would you like to change password')
                    if self.m2==True:                 
                        self.updt_cur.execute("update pinNum set pin='%s'"%(self.pt1.get().replace(" ","")))
                        self.updt_con.commit()
                        self.m1=messagebox.showinfo("info","changed succefully ")
                        self.pswrd.grab_set()
                else:
                    print()
                    self.m1=messagebox.showinfo("info","kindly enter prev ious passwrd to proceed with updating")
                    self.pswrd.grab_set()
            else:
                self.m1=messagebox.showinfo("info","provide the necessary particulars")
                self.pswrd.grab_set()
        except Exception:
            self.pt1.set("")
            self.pt2.set("")
            pass
        finally:
            self.con.close()
        
p1=about_author(master)
master.mainloop()
