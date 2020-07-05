from tkinter import *
from tkinter import messagebox
from mysqldb import *
from tools import *



win = Tk()
win.iconbitmap('image\Farm.ico')
# reset the window and background color
canvas = Canvas(win, width=600, height=500, bg='white')
canvas.pack(expand=YES, fill=BOTH)
# show window in center of the screen
width =win.winfo_screenwidth()
height =win.winfo_screenheight()
x = int(width / 2 - 600 / 2)
y = int(height / 2 - 500 / 2)
str1 = "600x500+" + str(x) + "+" + str(y)
win.geometry(str1)

 # disable resize of the window
win.resizable(width=False, height=False)

win.title("WELCOME | Login Window | ADMINISTRATOR")


frame = Frame(win, height=400, width=450)
frame.place(x=80, y=50)

x, y = 70, 20

img = PhotoImage(file='image\login.png')
label = Label(frame, image=img)
label.place(x = x + 80, y = y + 0)

    #now create a login form
label = Label(frame, text="Administrator Login")
label.config(font=("Courier", 20, 'bold'),fg='red')
label.place(x=90, y = y + 150)

emlabel = Label(frame, text="Enter User Name")
emlabel.config(font=("Courier", 12, 'bold'))
emlabel.place(x=40, y= y + 230)

email = Entry(frame, font='Courier 12')
email.place(x=200, y= y + 230)

pslabel = Label(frame, text="Enter Password")
pslabel.config(font=("Courier", 12, 'bold'))
pslabel.place(x=40, y=y+260)

password = Entry(frame,show='*', font='Courier 12')
password.place(x=200, y=y+260)
def login():
    #get the data and store it into tuple (data)
    if email.get() == "":
        msgbox("Enter User Name First")
    elif password.get() == "":
       msgbox("Enter Password first")
    else:
	    try:
		    conn = mysql.connector.connect(
			    host='localhost',
			    user=email.get(),
			    passwd=password.get()
,
			    database='pi'
		    )
		    if conn:
			    msgbox("Login Successfully")
			    win.destroy()
			    import dbtest
		    #else:
	    except mysql.connector.Error as e:
		    msgbox("Wrong username/password")
		    print(e)


button = Button(frame, text="Login", font='Courier 15 bold',fg='blue',
                             command=login)
button.place(x=170, y=y+290)

win.mainloop()


