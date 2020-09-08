from mysqldb import *
from tools import *
import datetime
import calendar
# inputDays=20
plabntId = 2

today = datetime.date.today()
#today1 = today + datetime.timedelta(days=days_till_end_month + 1)
Dete_f = dbget("SELECT Date FROM fields WHERE field_id = 1")
# print(Dete_f)
dd = Dete_f[0][0]
print(dd)

between = today-dd

inputDays = between.days
print(inputDays)
# stages=dbget("SELECT * FROM stagetable where plantId="+str(plabntId)+"")
stages=dbget("select * from plantstageduration where ptId='"+str(plabntId)+"'")


count = stages.__len__()
print(stages)
for  i in range(count) :
    if (i==0) & (inputDays <= stages[i][3]):
        print(stages[i][0])
        print('The input days is in stage 1 ')
    elif (i!=0) & (inputDays > stages[i][3]) :
        duration=0
        for j in range(i):
            duration+=stages[j][3]
            if inputDays<=duration:
                print(stages[j][0])
                break
