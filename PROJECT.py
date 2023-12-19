from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msgbox
import sqlite3
from datetime import datetime
import time as tm
from calendar import month_name
from tkcalendar import DateEntry
from PIL import ImageTk,Image

# ====================================================================================================================================================================================
w = Tk()
w.title("Virtual Daily Time Record and Salary System")
w.geometry("800x640+300+50")
w.resizable(0, 0)


style = ttk.Style()
style.theme_use('alt')
style.layout('TNotebook.Tab', [])
#  ================================================================================ Notebook =======================================================================================

notebook = ttk.Notebook(w)
tab1 = Frame(notebook)
tab2 = Frame(notebook)
tab3 = Frame(notebook)
tab4 = Frame(notebook)
notebook.add(tab1)
notebook.add(tab2)
notebook.add(tab3)
notebook.add(tab4)

notebook.pack(expand=TRUE, fill="both")

c = sqlite3.connect("new.db")
cursor = c.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_time2 (
	"Date"	TEXT,
	"Timein"	TEXT,
	"Timeout"	TEXT DEFAULT 'Not Logout',
	"Hourswork"	INTEGER DEFAULT 00.00,
	"Instat"	TEXT DEFAULT 'No',
	"Outstat"	TEXT DEFAULT 'No',
	"UserID"	INTEGER,
	"ID"	INTEGER,
	PRIMARY KEY("ID" AUTOINCREMENT));"""   )

cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_user2 (
	"UserID"	INTEGER UNIQUE,
	"Lastname"	TEXT,
	"Firstname"	TEXT,
	"Middlename"	NUMERIC,
	"Address"	TEXT,
	"Sex"	TEXT,
	"DOB"	TEXT,
	"Contact"	TEXT,
	"Job"	TEXT,
	PRIMARY KEY("UserID")
);""")

c.close()

#  ==================================================================================================================================================================================

now = datetime.now()


def open_tab3():
    notebook.select(tab3)


def view():

    add = "%"
    userid = ent.get()
    mm = str(m.get())
    month = mm + add
    yes = "Yes"
    arg = (userid, month, yes)
    c = sqlite3.connect("new.db")

    id = StringVar()
    lname = StringVar()
    fname = StringVar()
    mi = StringVar()
    ads = StringVar()
    con = StringVar()
    dob = StringVar()
    sex = StringVar()
    job = StringVar()

    cr = c.cursor()
    query1 = "SELECT * FROM tbl_user2 WHERE UserID=?"
    cr.execute(query1, [userid])
    rows = cr.fetchall()
    for i in rows:
        id.set(i[0])
        lname.set(i[1])
        fname.set(i[2])
        mi.set(i[3])
        ads.set(i[4])
        sex.set(i[5])
        dob.set(i[6])
        con.set(i[7])
        job.set(i[8])


    cursor = c.cursor()
    query2 = "SELECT sum(Hourswork) FROM tbl_time2 WHERE UserID=? AND Date LIKE ? AND Outstat LIKE ?  "
    cursor.execute(query2, arg)
    cursor2 = c.cursor()
    query3 = "SELECT count(Hourswork) FROM tbl_time2 WHERE UserID=? AND Date LIKE ? AND Outstat LIKE ? "
    arg = (userid, month, yes)
    cursor2.execute(query3, arg)

    work_hrs = cursor.fetchall()[0][0]
    day = cursor2.fetchall()[0][0]
    regular_hrs = 8*day

    overtime_hrs = work_hrs-regular_hrs

    if job.get() == "Production Supervisor":
        rate = 166

    elif job.get() == "Production Staff":
        rate = 105

    else:  # job.get() == Office Staff:
        rate = 82

    regular_pay = regular_hrs * rate
    overtime_pay = rate*1.5*overtime_hrs
    gross_pay = regular_pay + overtime_pay

    wh = str(float("{0:.2f}".format(work_hrs)))
    dy = str(day)
    rh = str(float("{0:.2f}".format(regular_hrs)))
    oh = str(float("{0:.2f}".format(overtime_hrs)))
    rt = str(float("{0:.2f}".format(rate)))
    rp = str(float("{0:.2f}".format(regular_pay)))
    op = str(float("{0:.2f}".format(overtime_pay)))
    gp = str(float("{0:.2f}".format(gross_pay)))

    p = "₱ "
    h = " hrs."
    wh = wh+h
    rh = rh+h
    oh = oh+h
    rt = p+rt
    rp = p+rp
    op = p+op
    gp = p+gp

    l1 = Label(tab2_frame, textvariable=id, font=('Arial', 8, 'bold')).place(x=645, y=85)
    l2 = Label(tab2_frame, textvariable=fname, font=('Arial', 13, 'bold'), width=66).place(x=21, y=120)
    l3 = Label(tab2_frame, textvariable=lname, font=('Arial', 13, 'bold'), width=20).place(x=21, y=120)
    l4 = Label(tab2_frame, textvariable=mi, font=('Arial', 13, 'bold'), width=15).place(x=500, y=120)
    l5 = Label(tab2_frame, textvariable=ads, font=('Arial', 10, 'bold'), width=51).place(x=77, y=189)
    l6 = Label(tab2_frame, textvariable=con, font=('Arial', 10, 'bold'), width=14).place(x=567, y=189)
    l7 = Label(tab2_frame, textvariable=dob, font=('Arial', 10, 'bold'), width=18).place(x=102, y=244)
    l8 = Label(tab2_frame, textvariable=sex, font=('Arial', 10, 'bold'), width=5).place(x=286, y=244)
    l9 = Label(tab2_frame, textvariable=job, font=('Arial', 10, 'bold'), width=39).place(x=367, y=244)
    l10 = Label(tab2_frame, text=rt, font=('Arial', 10, 'bold'), width=12).place(x=71, y=384)
    l11 = Label(tab2_frame, text=wh, font=('Arial', 10, 'bold'), width=12).place(x=266, y=384)
    l12 = Label(tab2_frame, text=rh, font=('Arial', 10, 'bold'), width=10).place(x=448, y=384)
    l13 = Label(tab2_frame, text=oh, font=('Arial', 10, 'bold'), width=10).place(x=600, y=384)
    l14 = Label(tab2_frame, text=dy, font=('Arial', 10, 'bold'), width=4).place(x=93, y=444)
    l15 = Label(tab2_frame, text=rp, font=('Arial', 10, 'bold'), width=9).place(x=240, y=444)
    l16 = Label(tab2_frame, text=op, font=('Arial', 10, 'bold'), width=9).place(x=435, y=444)
    l17 = Label(tab2_frame, text=gp, font=('Arial', 10, 'bold'), width=9).place(x=610, y=444)


def view2():
         c = sqlite3.connect("new.db")

         id = StringVar()
         lname = StringVar()
         fname = StringVar()
         mi = StringVar()
         ads = StringVar()
         con = StringVar()
         dob = StringVar()
         sex = StringVar()
         job = StringVar()

         userid = ent.get()

         cr = c.cursor()
         query1 = "SELECT * FROM tbl_user2 WHERE UserID=?"
         cr.execute(query1, [userid])
         rows = cr.fetchall()
         for i in rows:
             id.set(i[0])
             lname.set(i[1])
             fname.set(i[2])
             mi.set(i[3])
             ads.set(i[4])
             sex.set(i[5])
             dob.set(i[6])
             con.set(i[7])
             job.set(i[8])

         l1 = Label(tab2_frame, textvariable=id, font=('Arial', 8, 'bold')).place(x=645, y=85)
         l2 = Label(tab2_frame, textvariable=fname, font=('Arial', 13, 'bold'), width=66).place(x=21, y=120)
         l3 = Label(tab2_frame, textvariable=lname, font=('Arial', 13, 'bold'), width=20).place(x=21, y=120)
         l4 = Label(tab2_frame, textvariable=mi, font=('Arial', 13, 'bold'), width=15).place(x=500, y=120)
         l5 = Label(tab2_frame, textvariable=ads, font=('Arial', 10, 'bold'), width=51).place(x=77, y=189)
         l6 = Label(tab2_frame, textvariable=con, font=('Arial', 10, 'bold'), width=14).place(x=567, y=189)
         l7 = Label(tab2_frame, textvariable=dob, font=('Arial', 10, 'bold'), width=18).place(x=102, y=244)
         l8 = Label(tab2_frame, textvariable=sex, font=('Arial', 10, 'bold'), width=5).place(x=286, y=244)
         l9 = Label(tab2_frame, textvariable=job, font=('Arial', 10, 'bold'), width=39).place(x=367, y=244)
         l10 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=12).place(x=71, y=384)
         l11 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=12).place(x=266, y=384)
         l12 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=10).place(x=448, y=384)
         l13 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=10).place(x=600, y=384)
         l14 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=4).place(x=93, y=444)
         l15 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=9).place(x=240, y=444)
         l16 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=9).place(x=435, y=444)
         l17 = Label(tab2_frame, text="", font=('Arial', 10, 'bold'), width=9).place(x=610, y=444)


def month_changed(event):
    yes = msgbox.askyesno(
        title='Confirmation',
        message=f'   You SELECTED {m.get()}!\nDo you want to continue?')
    if yes > 0:
        try:
         view()
        except:
         msgbox.showerror(title='Error', message=f"No data found in your selected month!")
         monthchoosen.set(current_month)

def home():
    notebook.select(tab1)
    show()

def btn_return():
    iexit = msgbox.askyesno("Confirmation", "Confirm if you want to return")
    if iexit > 0:
        show()
        clear_ent()
        return


def outtime():

    try:
        def converttuple(tup):
            str1 = ''.join(tup)
            return str1

        def converttuple2(tup):
            str2 = ''.join(tup)
            return str2

        def time_to_float(time_str):
            hh, mm, ss = map(int, time_str.split(':'))
            return ss + 60 * (mm + 60 * hh)

        userid = ent.get()

        c = sqlite3.connect("new.db")

        cursor = c.cursor()

        insert_query = "UPDATE tbl_time2 SET Timeout = ?  WHERE UserID = ? AND Date = ?"
        date = now.strftime("%B %d, %Y")
        t_out = now.strftime("%H:%M:%S")
        record = (t_out, userid, date)
        cursor.execute(insert_query, record)

        tm.sleep(3)

        db1 = "SELECT Timein FROM tbl_time2 WHERE UserID=?"
        cursor.execute(db1, [userid])

        tin = cursor.fetchone()
        str1 = converttuple(tin)

        db2 = "SELECT Timeout FROM tbl_time2 WHERE UserID=? "
        cursor.execute(db2, [userid])

        tot = cursor.fetchone()
        str2 = converttuple2(tot)

        time_1 = datetime.strptime(str1, "%H:%M:%S")
        time_2 = datetime.strptime(str2, "%H:%M:%S")

        time = time_2 - time_1
        hrs = str(time)
        sec = time_to_float(hrs)
        worked_hrs = sec/3600
        outs = "Yes"

        insert_query2 = "UPDATE tbl_time2 SET Hourswork = ?, Outstat= ? WHERE UserID = ? AND Date = ?"
        record2 = (worked_hrs, outs, userid, date )
        cursor.execute(insert_query2, record2)

        c.commit()

    except sqlite3.Error:
        msgbox.showerror('PROBLEM', 'TIME OUT FAILED')
        exit()
    else:
        msgbox.showinfo(title='Confirmation', message=f'You are successfully LOGOUT!')

        btn2["state"] = DISABLED
        btn2["text"] = "TIMED OUT"
        btn3["state"] = DISABLED
        btn3["text"] = "TIMED IN"


def intime():
    try:
        c = sqlite3.connect("new.db")

        cursor = c.cursor()
        insert_query = """INSERT INTO tbl_time2 (userid,date, timeIn, Instat)
                                VALUES (?, ?, ?, ?) """

        userid = ent.get()
        date = now.strftime("%B %d, %Y")
        t_in = now.strftime("%H:%M:%S")
        ins = "Yes"
        record = (userid, date, t_in, ins)
        cursor.execute(insert_query, record)
        c.commit()

    except sqlite3.Error:
        msgbox.showerror('PROBLEM', 'TIME IN FAILED')
        exit()
    else:
        msgbox.showinfo(title='Confirmation',
                        message=f'You are successfully LOGIN!')

    btn3["state"] = DISABLED
    btn3["text"] = "TIMED IN"


def clear_ent():
    enty.delete(0, END)


def show():
    enty.focus()


    l1 = Label(tab1_frame, text="", font=('calibri', 9, 'bold'), width=5).place(x=645, y=85)
    l2 = Label(tab1_frame, text="", font=('Arial', 13, 'bold'), width=66).place(x=21, y=120)
    l3 = Label(tab1_frame, text="", font=('Arial', 13, 'bold'), width=20).place(x=21, y=120)
    l4 = Label(tab1_frame, text="", font=('Arial', 13, 'bold'), width=15).place(x=500, y=120)
    l5 = Label(tab1_frame, text="", font=('Arial', 10, 'bold'), width=51).place(x=77, y=189)
    l6 = Label(tab1_frame, text="", font=('Arial', 10, 'bold'), width=14).place(x=567, y=189)
    l7 = Label(tab1_frame, text="", font=('Arial', 10, 'bold'), width=18).place(x=102, y=244)
    l8 = Label(tab1_frame, text="", font=('Arial', 10, 'bold'), width=5).place(x=286, y=244)
    l9 = Label(tab1_frame, text="", font=('Arial', 10, 'bold'), width=39).place(x=367, y=244)

    log.place_forget()
    enty["state"] = NORMAL
    btn1["state"] = NORMAL
    lb7["text"] = "ENTER UserID"
    btn3["state"] = DISABLED
    btn3["text"] = ""
    btn3["relief"] = "flat"
    btn2["state"] = DISABLED
    btn2["text"] = ""
    btn2["relief"] = "flat"
    btn4["state"] = DISABLED
    btn4["relief"]= "flat"
    btn4["text"] = ""
    if btn5["state"] == NORMAL:
        btn5["state"] =DISABLED
        btn5["text"] = ""
    else:
        pass


def button():
    btn3["state"] = NORMAL
    btn3["text"] = "IN"
    btn2["state"] = NORMAL
    btn2["text"] = "OUT"


def find():
    button()
    userid = ent.get()
    c = sqlite3.connect("new.db")

    id = StringVar()
    lname = StringVar()
    fname = StringVar()
    mi = StringVar()
    ads = StringVar()
    con = StringVar()
    dob = StringVar()
    sex = StringVar()
    job = StringVar()

    cr = c.cursor()
    query1 = "SELECT * FROM tbl_user2 WHERE UserID=?"
    cr.execute(query1, [userid])
    rows = cr.fetchall()
    for i in rows:
        id.set(i[0])
        lname.set(i[1])
        fname.set(i[2])
        mi.set(i[3])
        ads.set(i[4])
        sex.set(i[5])
        dob.set(i[6])
        con.set(i[7])
        job.set(i[8])

    l1 = Label(tab1_frame, textvariable=id, font=('calibri', 9, 'bold')).place(x=645, y=85)

    l2 = Label(tab1_frame, textvariable=fname, font=('Arial', 13, 'bold'), width=66).place(x=21, y=120)

    l3 = Label(tab1_frame, textvariable=lname, font=('Arial', 13, 'bold'), width=20).place(x=21, y=120)

    l4 = Label(tab1_frame, textvariable=mi, font=('Arial', 13, 'bold'), width=15).place(x=500, y=120)

    l5 = Label(tab1_frame, textvariable=ads, font=('Arial', 10, 'bold'), width=51).place(x=77, y=189)

    l6 = Label(tab1_frame, textvariable=con, font=('Arial', 10, 'bold'), width=14).place(x=567, y=189)

    l7 = Label(tab1_frame, textvariable=dob, font=('Arial', 10, 'bold'), width=18).place(x=102, y=244)

    l8 = Label(tab1_frame, textvariable=sex, font=('Arial', 10, 'bold'), width=5).place(x=286, y=244)

    l9 = Label(tab1_frame, textvariable=job, font=('Arial', 10, 'bold'), width=39).place(x=367, y=244)

    log.place(x=557, y=560)
    enty['state']=DISABLED
    btn1['state']=DISABLED
    btn3["relief"] = "raised"
    btn2["relief"] = "raised"
    btn4["relief"] = "raised"
    enty["state"] = DISABLED
    btn1["state"] = DISABLED
    lb7["text"] = "YOU ENTERED"
    btn4["state"] = NORMAL
    btn4["text"] = "BACK"
    if btn5["state"] == DISABLED:
        btn5["state"] =NORMAL
        btn5["text"] = "---VIEW SALARY---"
    else:
        pass

    dt = StringVar()
    outs = StringVar()
    ins = StringVar()

    cs = c.cursor()
    query3 ="Select Date, instat, outstat FROM tbl_time2 WHERE UserID=?"
    cs.execute(query3,[userid])
    status = cs.fetchall()
    for s in status:
        dt.set(s[0])
        ins.set(s[1])
        outs.set(s[2])

    c_date = now.strftime("%B %d, %Y")
    date = dt.get()
    instat = ins.get()
    outstat = outs.get()

    if date == c_date:
        if instat == "Yes":
            btn3['state']=DISABLED
            btn3["text"] = "TIMED IN"
        else:
            btn3["state"] = NORMAL
            btn3["text"] = "IN"

        if outstat == "Yes":

            btn2['state'] = DISABLED
            btn2["text"] = "TIMED OUT"
        else:
            btn2["state"] = NORMAL
            btn2["text"] = "OUT"

    else:
        btn3["state"] = NORMAL
        btn3["text"] = "IN"
        btn2["state"] = NORMAL
        btn2["text"] = "OUT"


def return_tab1():
    notebook.select(tab1)
    find()


def open_tab4():
    notebook.select(tab4)
    logbook()


def open_tab2():
    notebook.select(tab2)
    try:
        view()
    except:
        m2 = msgbox.askyesno( title='Confirmation',
        message=f" You don't have any salary information this {m.get()}! \nDo you want to proceed and select month?")
        if m2==False:
            notebook.select(tab1)
        else:
            view2()


def check():
    userid = ent.get()
    if len(userid) == 0:
        msgbox.showerror('Attention', 'Please enter your UserID!' )
    else:
        c = sqlite3.connect("new.db")
        check = c.cursor()
        query = "SELECT EXISTS(SELECT UserID from tbl_user2 WHERE UserId=?)"
        check.execute(query, [userid])
        if check.fetchone()==(1,) :
            find()
        else:
            msgbox.showerror('Error', 'No UserID found!')
            enty.delete(0, END)


def limitSizeID(*args):
    value = ent.get()
    if len(value) > 6: ent.set(value[:4])




# ====================================================================================== TAB 1 =======================================================================================

#Frame

tab1_main = LabelFrame(tab1, bg="lightgrey", relief="raised", bd=5)
tab1_main.pack(fill="both", expand=TRUE)

tab1_frame = LabelFrame(tab1_main, height=380, width=720, relief="sunken", bd=5)
tab1_frame.place(y=130, x=35)

# Label

line1 = Label(tab1_frame, text="___________________________________________________", font=('calibri', 20, 'bold'))
lb1 = Label(tab1_frame, text="USER-DETAILS", font=('Calibri', 25, 'bold'))
lb2 = Label(tab1_frame, text="\tLast Name\t\t\tFirst Name\t\t\tMiddle Name", font=('calibri', 10, 'normal'))
lb3 = Label(tab1_frame, text="__________________________________________________________________", font=('calibri', 15, 'normal'))
lb4 = Label(tab1_frame, text="Address: ______________________________________________________________________  Contact No: ____________________", font=('calibri', 10, 'normal'))
lb5 = Label(tab1_frame, text="Date of Birth: __________________________  Sex: ________  Job: ______________________________________________________", font=('calibri', 10, 'normal'))
lb6 = Label(tab1_frame, text="ID no.", font=('Calibri', 8, 'normal'))
lb7 = Label(tab1_main, bg="lightgrey", text="ENTER UserID", font=('calibri', 12, 'normal'))

line1.place(x=20, y=40)
lb1.place(x=20, y=25)
lb2.place(x=35, y=145)
lb3.place(x=21, y=120)
lb4.place(x=21, y=195)
lb5.place(x=21, y=250)
lb6.place(x=610, y=85)
lb7.place(x=298, y=30)


# Entry

ent = StringVar()
ent.trace('w', limitSizeID)
enty = Entry(tab1_main, width=20, font=('Arial', 15, 'bold'), textvariable=ent)
enty.place(x=233, y=50)

# Button

btn1 = Button(tab1_main, text='Search', width=8, font=('calibri', 12, 'normal'), command=check, cursor="hand2")
btn1.place(x=500, y=49)

btn2 = Button(tab1_main, text='OUT', bg="lightgrey", width=8, font=('calibri', 10, 'bold'), command=outtime, cursor="hand2")
btn2.place(x=630, y=560)

btn3 = Button(tab1_main, text='IN', width=8, bg="lightgrey", font=('calibri', 10, 'bold'), command=intime, cursor="hand2")
btn3.place(x=490, y=560)


log = Button(tab1_main, text='VIEW', width=9, bg="lightgrey", font=('calibri', 10, 'bold'), relief='raise', fg='blue', command=open_tab4, cursor="hand2")


btn4 = Button(tab1_main, text='BACK', bg="lightgrey", width=8, font=('calibri', 12, 'bold'), command=btn_return, cursor="hand2")
btn4.place(x=50, y=565)

btn5 = Button(tab1_frame, text='---VIEW SALARY---', width=20, font=('Arial', 15, 'bold'), relief='flat', command=open_tab2, cursor="hand2")
btn5.place(x=230, y=325)

show()


def toggle_win():
    f1 = Frame(tab1_main, width=260, height=800, bg='#6C6C6C')
    f1.place(x=0, y=0)

    enty['state']=DISABLED
    btn1['state']=DISABLED

    def register():
        f1.destroy()
        open_tab3()

    def dele():
        f1.destroy()
        enty['state'] = NORMAL
        btn1['state'] = NORMAL

    def exit():
        w.destroy()

    global img2
    image2 = Image.open('close.png')
    img2 = ImageTk.PhotoImage(image2.resize((25, 25), Image.ANTIALIAS))

    close_btn = Button(f1, image=img2, border=0, activebackground='#6C6C6C', bg='#6C6C6C', cursor='hand2', command=dele)
    close_btn.place(x=5, y=7)

    lbl = Label(f1, text="________________________________________________________", font=('Calibri', 16, 'bold'), fg='white', width=21, bg='#6C6C6C')
    lbl.place(x=10, y=120)
    lbl = Label(f1, text="________________________________________________________", font=('Calibri', 16, 'bold'), fg='white', width=21, bg='#6C6C6C')
    lbl.place(x=10, y=70)

    lbl = Label(f1, text="________________________________________________________", font=('Calibri', 16, 'bold'), fg='white', width=21, bg='#6C6C6C')
    lbl.place(x=10, y=170)


    reg_btn = Button(f1, text="REGISTER", font=('Times', 13,'bold'), width=25, activebackground='#6C6C6C',
                     activeforeground='black', fg='white', bg='#6C6C6C', relief='flat', cursor='hand2', command=register)
    reg_btn.place(x=0, y=105)

    exit_btn = Button(f1, text="EXIT", font=('Times', 13, 'bold'), width=25, activebackground='#6C6C6C',
                      activeforeground='black', fg='white', bg='#6C6C6C', relief='flat', cursor='hand2', command=exit)
    exit_btn.place(x=0, y=155)


image1 = Image.open('open3.png')
img1 = ImageTk.PhotoImage(image1.resize((35, 20), Image.ANTIALIAS))
btn7 = Button(tab1_main, text="open", image=img1, border=0, activebackground='lightgrey', bg='lightgrey', cursor='hand2', command=toggle_win)
btn7.place(x=5, y=7)



# ====================================================================================== TAB 2 =======================================================================================



tab2_main = LabelFrame(tab2, bg="lightgrey", relief="raised", bd=5)
tab2_main.pack(fill="both", expand=TRUE)

tab2_frame = LabelFrame(tab2, width=720, height=520, relief="sunken", bd=5)
tab2_frame.place(y=50, x=35)

editf = ('calibri', 9, 'bold')

style.map('TCombobox', fieldbackground=[('readonly', 'lightgrey')])
style.map('TCombobox', foreground=[('readonly', 'black')])
style.map('TCombobox', selectbackground=[('readonly', 'lightgrey')])
style.map('TCombobox', selectforeground=[('readonly', 'black')])

m = StringVar()

monthchoosen = ttk.Combobox(tab2, width=10, justify='center', font=editf, textvariable=m)
monthchoosen.place(x=686, y=7)
monthchoosen['values'] = [month_name[m][0:10] for m in range(1, 13)]
monthchoosen['state'] = 'readonly'
monthchoosen.bind('<<ComboboxSelected>>', month_changed)
current_month = datetime.now().strftime('%B')
monthchoosen.set(current_month)

btn6 = Button(tab2_main, text='BACK', bg="lightgrey", width=23, font=('calibri', 13, 'bold'), anchor='center', command=return_tab1, cursor="hand2")
btn6.place(x=280, y=580)

lbl3 = Label(tab2_main, text="Select Month:", font=('calibri', 9, 'normal'), bg="lightgrey")
lbl3.place(x=600, y=2)

line9 = Label(tab2_frame, text="___________________________________________________", font=('calibri', 20, 'bold'))
line3 = Label(tab2_frame, text="___________________________________________________", font=('calibri', 20, 'bold'))
ln1 = Label(tab2_frame, text="USER-DETAILS", font=('Calibri', 25, 'bold'))
ln10 = Label(tab2_frame, text="SALARY-DETAILS", font=('Calibri', 25, 'bold'))
ln2 = Label(tab2_frame, text="\tLast Name\t\t\tFirst Name\t\t\tMiddle Name", font=('calibri', 10, 'normal'))
ln3 = Label(tab2_frame, text="__________________________________________________________________", font=('calibri', 15, 'normal'))
ln4 = Label(tab2_frame, text="Address: ______________________________________________________________________  Contact No: ____________________", font=('calibri', 10, 'normal'))
ln5 = Label(tab2_frame, text="Date of Birth: __________________________  Sex: ________  Job: ______________________________________________________", font=('calibri', 10, 'normal'))
ln6 = Label(tab2_frame, text="ID no.", font=('Calibri', 8, 'normal'))
ln7 = Label(tab2_frame, text="Rate/hr: _________________  Worked_hours: _________________  Regulartime: _______________  Overtime: _______________  ", font=('calibri', 10, 'normal'))
ln8 = Label(tab2_frame, text="No. of days: _______  Regular_earnings: _____________  Overtime_earnings: _____________  Gross_earnings:_____________", font=('calibri', 10, 'normal'))


line9.place(x=20, y=320)
line3.place(x=20, y=40)
ln1.place(x=20, y=25)
ln10.place(x=20, y=305)
ln2.place(x=35, y=145)
ln3.place(x=21, y=120)
ln4.place(x=21, y=195)
ln5.place(x=21, y=250)
ln6.place(x=610, y=85)
ln7.place(x=21, y=390)
ln8.place(x=21, y=450)

#  ================================================================================= TAB 3 ===========================================================================================
def cancel():
    notebook.select(tab1)
    enty['state'] = NORMAL
    btn1['state'] = NORMAL

def insert_record():
    check_counter = 0
    warn = ""
    if reg_lname.get() == "":
        warn = "Lastname can't be empty"
    else:
        check_counter += 1

    if reg_fname.get() == "":
        warn = "Firstname can't be empty"
    else:
        check_counter += 1

    if reg_mname.get() == "":
        warn = "Middlename can't be empty"
    else:
        check_counter += 1

    if reg_address.get() == "":
        warn = "Address can't be empty"
    else:
        check_counter += 1

    if reg_con.get() == "":
        warn = "Contact can't be empty"
    else:
        check_counter += 1

    if reg_dob.get() == "":
        warn = "Date of Birth can't be empty"
    else:
        check_counter += 1

    if reg_sex.get() == "":
        warn = "Please select your sex"
    else:
        check_counter += 1

    if reg_job.get() == "":
        warn = "Please select your job"
    else:
        check_counter += 1

    if check_counter == 8:

        c = sqlite3.connect("new.db")
        check = c.cursor()
        query = "SELECT EXISTS(SELECT * from tbl_user2 WHERE Firstname LIKE ? AND Lastname LIKE ?)"
        val = (reg_fname.get(), reg_lname.get())
        check.execute(query, val)
        if check.fetchone() == (1,):
            msgbox.showerror('Error', 'You are already registered!')
            reg_lname.delete(0, END)
            reg_fname.delete(0, END)
            reg_mname.delete(0, END)
            reg_address.delete(0, END)
            reg_con.delete(0, END)
        else:
            try:

                c = sqlite3.connect("new.db")
                cur = c.cursor()
                insert_query = """INSERT INTO tbl_user2 (Lastname, Firstname, Middlename, Address, Sex, DOB, Contact, Job )
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?) """

                data = ( reg_lname.get(),
                         reg_fname.get(),
                         reg_mname.get(),
                         reg_address.get(),
                         reg_sex.get(),
                         reg_dob.get(),
                         reg_con.get(),
                         reg_job.get())

                cur.execute(insert_query, data)

                cur.execute("SELECT UserID FROM tbl_user2 ORDER BY UserID DESC LIMIT 1")
                get_id= str(cur.fetchall())
                id = get_id.strip('[(,)]')


                c.commit()
                msgbox.showinfo('Confirmation', f'You are now registered, this is your UserID:{id},\nPlease do not forgot it')
                yes = msgbox.askyesno('Ask', 'Do you want to make another register?')
                if yes>0:
                    reg_lname.delete(0, END)
                    reg_fname.delete(0, END)
                    reg_mname.delete(0, END)
                    reg_address.delete(0, END)
                    reg_con.delete(0, END)
                    reg_sex.set('')
                    reg_job.set('')

                else:
                    msgbox.showinfo('','Done')
                    reg_lname.delete(0, END)
                    reg_fname.delete(0, END)
                    reg_mname.delete(0, END)
                    reg_address.delete(0, END)
                    reg_con.delete(0, END)
                    reg_sex.set('')
                    reg_job.set('')
                    home()
            except Exception as ep:
                msgbox.showerror('', ep)
    else:
        msgbox.showerror('Error', warn)




default = "yellow"
color = "lightgrey"
f = ('Calibri', 14,'bold')
f2 = ('Calibri', 12)
g = ('Calibri', 12,'bold')

tab3_main = LabelFrame(tab3, bg="lightgrey", relief="raised", bd=5)
tab3_main.pack(fill="both", expand=TRUE)

tab3_frame = LabelFrame(tab3, width=720, height=450, relief="groove", bd=5)
tab3_frame.place(y=70, x=35)

line3 = Label(tab3_frame, text="___________________________________________________",  font=('calibri', 20, 'bold'))
Label(tab3_frame, text="REGISTRATION FORM",width=34, justify='center', font=('Times', 25, 'bold')).place(x=5,y=15)



ln2 = Label(tab3_frame, text="\tLast Name\t\t\tFirst Name\t\t\tMiddle Name", font=('calibri', 10, 'bold'))

ln3 = Label(tab3_frame, text="__________________________________________________________________", font=('calibri', 15, 'bold'))
ln4 = Label(tab3_frame, text="Address: ______________________________________________________________________  Contact No: ____________________",  font=('calibri', 10, 'bold'))
ln5 = Label(tab3_frame, text="Date of Birth: __________________________  Sex: ________  Job: ______________________________________________________", font=('calibri', 10, 'normal'))

ln3.place(x=21, y=120)
line3.place(x=20, y=40)
ln2.place(x=35, y=145)
ln4.place(x=21, y=195)
ln5.place(x=21, y=270)


reg_lname = Entry(tab3_frame, font=f, justify='center', width=21)
reg_lname.place(x=23, y=118)

reg_fname = Entry(tab3_frame, font=f, justify='center', width=23)
reg_fname.place(x=236, y=118)

reg_mname = Entry(tab3_frame, font=f, justify='center', width=21)
reg_mname.place(x=469, y=118)


reg_address = Entry(tab3_frame, font=f, justify='center', width=41)
reg_address.place(x=77, y=184)

reg_con = Entry(tab3_frame, font=f2, justify='center', width=14)
reg_con.place(x=569, y=188)

reg_dob = DateEntry(tab3_frame, width=17, year=2021, month=6, day=22, date_pattern='mm/dd/y', justify='center', font=f2, borderwidth=2,
                 selectbackground='white',
                 selectforeground='red',
                 normalbackground='white',
                 normalforeground='black',
                 background='white',
                 foreground='black',
                 bordercolor='black',
                 othermonthforeground='gray50',
                 othermonthbackground='white',
                 othermonthweforeground='gray50',
                 othermonthwebackground='white',
                 weekendbackground='white',
                 weekendforeground='red',
                 headersbackground='white',
                 headersforeground='black')
reg_dob.place(x=99, y=261)


reg_sex = StringVar()
sex_box= ttk.Combobox(tab3_frame, width=5, justify='center', font=editf, textvariable=reg_sex)
sex_box.place(x=283, y=266)
sex_box['values'] = ['M', 'F']
sex_box['state'] = 'readonly'


reg_job = StringVar()
job_box= ttk.Combobox(tab3_frame, width=49, justify='center', font=editf, textvariable=reg_job)
job_box.place(x=367, y=266)
job_box['values'] = ['Production Supervisor', 'Production Staff', 'Office Staff']
job_box['state'] = 'readonly'

back_btn = Button(tab3_main, text="CANCEL", font=('Arial', 12, 'bold'), width=30, command=cancel)
back_btn.place(x=20, y=565)

cancel_btn = Button(tab3_main, text="REGISTER", font=('Arial', 12, 'bold'), width=30, command=insert_record)
cancel_btn.place(x=450, y=565)

# ======================================================================================== TAB 4 =========================================================================================

def logbook():
    userid = ent.get()
    c = sqlite3.connect("new.db")

    cursor = c.cursor()
    query = "SELECT * FROM tbl_time2 WHERE UserID=?"
    cursor.execute(query, [userid])

    fetchdata = tr_view.get_children()
    for elements in fetchdata:
        tr_view.delete(elements)

    data = cursor.fetchall()
    for d in data:
        tr_view.insert("", END, values=d)

    c.commit()
    c.close()


tab4_main = LabelFrame(tab4, bg="lightgrey", relief="raised", bd=5)
tab4_main.pack(fill="both", expand=TRUE)


tab4_frame = LabelFrame(tab4, width=750, height=400, relief="sunken", bd=10)
tab4_frame.place( x=24, y=130)

Label(tab4_main, text="YOUR LOGBOOK", bg='lightgrey', font=('Times', 30, 'bold')).pack(fill=X, pady=50)

col_val = "Date", "Time_In", "Time_Out",

tr_view = ttk.Treeview(tab4_frame, columns=col_val, selectmode='extended', show='headings', height=22)
tr_view.place(height=380, width=730, x=0, y=0)
for each in col_val:
    tr_view.column(each, width=80, anchor='center')
    tr_view.heading(each, text=each.capitalize())

C = CENTER
style.configure("Treeview")

tab3_back = Button(tab4_main, text='BACK', bg="lightgrey", width=23, font=('calibri', 13, 'bold'), anchor='center', command=return_tab1, cursor="hand2")
tab3_back.place(x=280, y=570)

style.configure("Treeview", highlightthickness=0, bd=0, font=('Times', 11))
style.configure("Treeview.Heading", font=('Times', 12,'bold'))

# ====================================================================================================================================================================================


w.option_add('*TCombobox.font', editf)
w.mainloop()
