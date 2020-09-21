from mysqldb import *
from tools import *
import datetime
from lastdbamount import *
def create_table():
	iscreated = dbrun("""CREATE TABLE IF NOT EXISTS fields( 
                            field_id int ,
                             field_name varchar(99) ,
                             plant_type varchar(99),
                             water_mm float,
                             Day_of_plant int,
                             Width_F int,
                             Height_F int,
                             soil_H int,
                             water_l int,
                             temp int,
                             humidity int,
                             Date_s date,
                             Date date) """)
	if iscreated: msgbox("Table is Created")

bg = 'lightblue'
fg = 'navy'
ft = 'verdana 16'
ft1 = 'verdana 11'
pad = 5

frm = form("900x630")
frm.iconbitmap('image\Farm.ico')
frm.resizable(width=False, height=False)
frm.title("WELCOME | Control Window | ADMINISTRATOR")

button(frm,"Create Table", create_table).pack(pady=pad)
fieldno_var   = intvar()
fieldname_var = strvar()
plant_var     = strvar()
water_var     = strvar()
width_var     = strvar()
heigh_var     = strvar()
season_var     = strvar()
soil_var     = strvar()
waterl_var     = strvar()
temp_var     = strvar()
humidity_var = strvar()
dates_var       = strvar()
date_var       = strvar()
def check_field():
	if frm.winfo_children()[1].winfo_children()[1].get().strip()=="":
		msgbox("Field Id Is Empty")
		frm.winfo_children()[1].winfo_children()[3].focus()
		return False
	elif fieldname_var.get().strip()=="":
		msgbox("FieldName Id Is Empty")
		frm.winfo_children()[1].winfo_children()[3].focus()
		return False
	elif plant_var.get().strip()=="":
		msgbox("Plant Is Empty")
		frm.winfo_children()[1].winfo_children()[5].focus()
		return False
	elif frm.winfo_children()[1].winfo_children()[7].get().strip()=="":
		msgbox("Water need Is Empty")
		frm.winfo_children()[1].winfo_children()[7].focus()
		return False
	elif frm.winfo_children()[1].winfo_children()[9].get().strip()=="":
		msgbox("season period Is Empty")
		frm.winfo_children()[1].winfo_children()[9].focus()
		return False
	elif frm.winfo_children()[1].winfo_children()[21].get().strip()=="":
		msgbox("Date Is Empty")
		frm.winfo_children()[1].winfo_children()[21].focus()
		return False
	else:
		return True

def clear_field():
	num =dbautonum('fields','field_id')
	if num == 0:
		frm.destroy()
	else:
		fieldno_var.set(num)
		fieldname_var.set("")
		plant_var.set("potato")
		width_var.set("vlaue in cm")
		heigh_var.set("vlaue in cm")
		water_var.set(" 0.0")
		season_var.set("0 ")
		soil_var.set(" 0 ")
		waterl_var.set("0 ")
		temp_var.set(" 0 ")
		humidity_var.set("0")
		dates_var.set(0)
		date_var.set(datetime.datetime.today().date())
		frm.winfo_children()[2].winfo_children()[0].config(state='enable')
		frm.winfo_children()[2].winfo_children()[2].config(state='disable')
		frm.winfo_children()[2].winfo_children()[3].config(state='disable')
		frm.winfo_children()[1].winfo_children()[3].focus()
def add_field():
	if check_field():
		is_added =dbrun("insert into fields (field_id, field_name, plant_type,Width_F,Height_F, water_mm, Day_of_plant, Date)  values(%s,'%s','%s',%s,%s,%s,%s,'%s')" %(fieldno_var.get(),fieldname_var.get(),plant_var.get(),width_var.get(),heigh_var.get(),water_var.get(),season_var.get(),date_var.get()))
		if is_added:
			msgbox("Field Is Added")
		clear_field()

def find_field(Field_id = None):

	if Field_id == None:
		fnum = inbox("Enter Field Number",True)
	else:
		fnum =Field_id
	if fnum =="": fnum=0
	amont(fnum)
	rows = dbget("select * from fields where field_id="+str(fnum))
	if len(rows)< 1 :msgbox("Field ID Not Found")
	else:
		row = rows[0]
		fieldno_var.set(row[0])
		fieldname_var.set(row[1])
		plant_var.set(row[2])
		width_var.set(""+str(row[3])+" cm")
		heigh_var.set(""+str(row[4])+ " cm")
		water_var.set(""+str(row[5])+" mm")
		season_var.set(""+str(row[6])+" days")
		soil_var.set(""+str(row[7])+" %")
		waterl_var.set(""+str(row[8])+" %")
		temp_var.set(""+str(row[9])+" C'")
		humidity_var.set(""+str(row[10])+" %")
		dates_var.set(row[11])
		date_var.set(row[12])
		frm.winfo_children()[2].winfo_children()[0].config(state='disable')
		frm.winfo_children()[2].winfo_children()[2].config(state='enable')
		frm.winfo_children()[2].winfo_children()[3].config(state='enable')

def update_field():
	isedet = dbrun("UPDATE fields SET field_name ='"+fieldname_var.get()+"',Width_F ='"+width_var.get()+"',Height_F ='"+heigh_var.get()+"' ,Date = '"+str(date_var.get())+"'  where field_id ="+str(fieldno_var.get()))
	if isedet:
		msgbox("Field Is Updated")
		clear_field()
	else:
		msgbox("Field Is Not Updated")

def delete_field():
	if msgask("Do You Sure To Delet "):
		is_del = dbrun("delete from fields where field_id ="+str(fieldno_var.get()))
		if is_del:msgbox("Field Is Dleleted")
		clear_field()


f1 = frame(frm)
label(f1 ,"FieldNo     :").grid(row=0,column=0,pady=pad,padx=pad)
textbox(f1,fieldno_var,True,True).grid(row=0,column=1,pady=pad)

label(f1 ,"FieldName :").grid(row=0,column=2,pady=pad,padx=pad)
textbox(f1,fieldname_var).grid(row=0,column=3,pady=pad)

label(f1,"PlantName :").grid(row=1,column=0,pady=pad,padx=pad)
textbox(f1,plant_var,None,True).grid(row=1,column=1,pady=pad)

label(f1,"WidthField :").grid(row=1,column=2,pady=pad,padx=pad)
textbox(f1,width_var,True).grid(row=1,column=3,pady=pad)

label(f1,"HeightField :").grid(row=2,column=0,pady=pad,padx=pad)
textbox(f1,heigh_var,True).grid(row=2,column=1,pady=pad)

label(f1,"WaterNeed :").grid(row=2,column=2,pady=pad,padx=pad)
textbox(f1,water_var,True,True).grid(row=2,column=3,pady=pad)



label(f1,"Dayofplant :").grid(row=3,column=0,pady=pad,padx=pad)
textbox(f1,season_var,True,True).grid(row=3,column=1,pady=pad)

label(f1,"SoilHumidity :").grid(row=3,column=2,pady=pad,padx=pad)
textbox(f1,soil_var,True,True).grid(row=3,column=3,pady=pad)

label(f1,"Water_l :").grid(row=4,column=0,pady=pad,padx=pad)
textbox(f1,waterl_var,True,True).grid(row=4,column=1,pady=pad)

label(f1,"Temperature :").grid(row=4,column=2,pady=pad,padx=pad)
textbox(f1,temp_var,True,True).grid(row=4,column=3,pady=pad)

label(f1,"Humidity :").grid(row=5,column=0,pady=pad,padx=pad)
textbox(f1,humidity_var,True,True).grid(row=5,column=1,pady=pad)

label(f1,"DateSensor :").grid(row=5,column=2,pady=pad,padx=pad)
textbox(f1,dates_var,None,True).grid(row=5,column=3,pady=pad)
label(f1,"Date :").grid(row=6,column=0,pady=pad,columnspan=2,padx=pad)
textbox(f1,date_var).grid(row=6,column=1,columnspan=2,pady=pad)
f1.pack(pady=pad)

f2 = frame(frm)
button(f2,"Add",add_field).grid(row=0,column=0,padx=pad)
button(f2,"Find",find_field).grid(row=0,column=1,padx=pad)
button(f2,"Update",update_field).grid(row=0,column=2,padx=pad)
button(f2,"Delete",delete_field).grid(row=0,column=3,padx=pad)
button(f2 ,"Clear",clear_field).grid(row=0,column=4,padx=pad)
button(f2,"Exite",frm.destroy).grid(row=0,column=5,padx=pad)
f2.pack(pady=pad)

def show_data():
	frm_data = toplevel("830x400")
	frm_data.iconbitmap('image\Farm.ico')
	frm_data.resizable(width=False, height=False)
	frm_data.title("WELCOME | Show Window | ADMINISTRATOR")
	btn = button(frm_data, "View ")
	btn.config(width=12)
	btn.pack()
	f_searche = frame(frm_data)
	txt_searche = textbox(f_searche)
	btn_searche = button(f_searche ,"Searche")
	txt_searche.grid(row=0 ,column=0)
	btn_searche.grid(row=0 ,column=1)
	f_searche.pack()

	cols = ["FieldID","FielName","planttype","WidF","HeighF","WaterNeed","Days","Soil","Waterl","Temp","Humidity","DateS","DateF"]
	rows = dbget("select * from fields")
	tbl = table(frm_data,cols,rows)

	def fun_searche():
		s = txt_searche.get()
		cols_serche = ["FieldID","FielName","planttype","WidF","HeighF","WaterNeed","Days","Soil","Waterl","Temp","Humidity","DateS","DateF"]
		rows_searche = dbget("select * from fields where Field_name like '%"+s+"%' or plant_type like'%"+s+"%'")
		tbl.change_data(cols_serche,rows_searche )
		tbl.bind()
		bgall(frm_data, bg)
		fgall(frm_data, fg)
		fontall(frm_data, ft1)


	btn_searche.config(command=fun_searche)
	tbl.bind()
	tkcenter(frm_data)
	bgall(frm_data, bg)
	fgall(frm_data, fg)
	fontall(frm_data, ft1)
	justall(frm_data, "center")
	def view():
		fnum = tbl.current_row()[0]['text']
		find_field(fnum)
		frm_data.destroy()

	btn.config(command=view)

	frm_data.grab_set()
button(frm,"Show Data",show_data ).pack()

canvas = Canvas(frm, width=800, height=700, bg='white')
canvas.pack(expand='YES', fill='both')
img = PhotoImage(file= "image/farm1.PNG")
label = ttk.Label(f2, image=img)
label.grid(row=1,column=0,columnspan=6)


tkcenter(frm)
bgall(frm,bg)
fgall(frm,fg)
fontall(frm,ft)
justall(frm,"center")

widthall(frm,13)
widthall(f2,7)

clear_field()
frm.mainloop()
