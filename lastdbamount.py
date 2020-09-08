from mysqldb import *
from tools import *
import datetime
import calendar
def amont():
    today = datetime.date.today()
    Dete_f = dbget("SELECT Date FROM fields WHERE field_id = 2")
    # print(Dete_f)
    dd = Dete_f[0][0]
    print(dd)

    between = today-dd
    inputDays = between.days
    print(inputDays)
    plantT=dbget("SELECT  plant_type FROM fields WHERE field_id = 2")
    PT = plantT[0][0]
    print(PT)
    #pId = dbget("SELECT  * FROM planttype WHERE pTypeID =2" )#pTypeName"+str(PT)+""
    pId = dbget("SELECT  pTypeID FROM planttype WHERE pTypeName like '"+PT+"'" )#pTypeName"+str(PT)+""

    plabntId = pId[0][0]
    print(plabntId)

    # stages=dbget("SELECT * FROM stagetable where plantId="+str(plabntId)+"")
    stages=dbget("select * from plantstageduration where ptId='"+str(plabntId)+"'")

    count = stages.__len__()
    print(stages)
    duration = 0
    for  i in range(count) :
        if (i==0) & (inputDays <= stages[i][3]):
            print(stages[i][0])
            print('The input days is in stage 1 ')
            dbrun("UPDATE fields SET water_mm ='"+str(stages[i][0])+"', Day_of_plant = '"+str(inputDays)+"' where field_id =" + str(plabntId))
            break
        elif (i <= count-1) :#& (inputDays <= stages[i][3]) :
            duration += stages[i-1][3]
            if inputDays <= duration:
                print(stages[i][0])
                dbrun("UPDATE fields SET water_mm ='" + str(stages[i][0])+ "', Day_of_plant = '" + str(inputDays) + "' where field_id =" + str(plabntId))
                duration = 0
                break
        if (i == count-1):
            messagebox.showinfo('! Alarm',""+str(inputDays)+"  Days Are Larg Of Season  The Season Days Are "+str(duration)+"")
