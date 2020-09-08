from threading import *
from tools import *
from mysqldb import *
import datetime
import calendar
# import datetime
# import math
#
# today = datetime.date.today()
# print(today)
# date_s = datetime.date(2020, 7 ,15)
# period_to_irragation = date_s +  datetime.timedelta(days=2)
# if period_to_irragation ==today:
#     print ("complate")
# print(period_to_irragation)
# period_to_irragation = today + datetime.timedelta(days=30)
# print(period_to_irragation)

today = datetime.date.today()
#today1 = today + datetime.timedelta(days=days_till_end_month + 1)
Dete_f = dbget("SELECT Date FROM fields WHERE field_id = 1")
dd = Dete_f[0][0]

between = today-dd
print(between.days)

start = dd
print(start)
#end = 15 #dd + datetime.timedelta(days=15)
days_in_current_month = calendar.monthrange(dd.year, dd.month)[1]
print(days_in_current_month)
days_till_end_month = days_in_current_month - dd.day
print (days_till_end_month )

#stop = dd + datetime.timedelta(days=end)
#stop_f = (stop-dd).days
#print(stop_f)
#print (stop)
season = dbget("SELECT season FROM fields WHERE field_id = 1")
season_day = season[0][0]
print (season_day)
count = 1
stop = dd + datetime.timedelta(days=1)

#print(stop_f)
# waterd = False
# stop = dd + datetime.timedelta(days=1)
# stop_f = (stop - dd).days
# while (stop_f < season_day):
#     if stop_f < 13:
#         stop = today + datetime.timedelta(days=13)
#         stop_f = (stop - dd).days
#         if stop_f != 0 :
#             if waterd != True:
#                 #oprate punp
#                 waterd = True
#                 stop_f -= 1
#                 print("stop if",stop_f)
#             else:
#                 pass
#         else :
#             stop_f= 13
#     elif stop_f < 45:
#         stop = today + datetime.timedelta(days=45)
#         stop_f = (stop - dd).days
#         if  stop_f < 45:
#             if waterd != True:
#                 # oprate punp
#                 waterd = True
#                 stop_f -= 1
#                 print("stop if", stop_f)
#             else:
#                 pass
#         else:
#             stop_f = 45
#     elif count < 60:
#         stop = dd + datetime.timedelta(days=60)
#         stop_f = (stop - dd).days
#         if stop_f != 0:
#             if waterd != True:
#                 # oprate punp
#                 waterd = True
#                 stop_f -= 1
#                 print("stop if", stop_f)
#             else:
#                 pass
#         else:
#             stop_f = 60
#     else:
#         stop = dd + datetime.timedelta(days=season-stop_f)
#         stop_f = (stop - dd).days
#         if stop_f != 0:
#             if waterd != True:
#                 # oprate punp
#                 waterd = True
#                 stop_f -= 1
#                 print("stop if", stop_f)
#             else:
#                 pass
#         else:
#             print("season Coplate")






#end1 = days_in_current_month - today
#stop1 =end1
#stop = end.day
#print(today-end)
#print(end)

#
# days_in_current_month = calendar.monthrange(today.year, today.month)[1]
# print (days_in_current_month)
#
#
# days_till_end_month = days_in_current_month - today.day
# print (days_till_end_month)
#
# start_date = dd + datetime.timedelta(days=12)
# print(start_date)
#
# one_leter = 1000
# x_leter = (((70 *27 )*((800/180)/10))/one_leter)
# print (x_leter)
# time_pump_to_push_water_oneleter = 34
# time_to_irregation = (x_leter * time_pump_to_push_water_oneleter)
# print (time_to_irregation)


# if dd.day <= end.day:
#       print ("good")
# else:
#     print ("pad")






