from tools import *
from mysqldb import *
from lastdbamount import *

import os
import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
import time
from time import sleep
import datetime
from datetime import date
import calendar

import glob
import picamera
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(18, GPIO.OUT, initial=0)
GPIO.output(24, 0)
import dht11

watered = False
field_Id = 2
def getTime(ID_var):
    amont(ID_var)
    Width = dbget("SELECT  Width_F FROM fields WHERE field_id = " + str(ID_var) + "")
    Height = dbget("SELECT  Height_F FROM fields WHERE field_id = " + str(ID_var) + "")
    depth = dbget("SELECT  water_mm FROM fields WHERE field_id = " + str(ID_var) + "")
    WidthF = Width[0][0]
    HeightF = Height[0][0]
    depthF = depth[0][0]

    print("the width of field  ="+WidthF+"CM")
    print("the Height of field  ="+HeightF+"CM")
    print("the depth of field  ="+depthF+"MM")

    literFun = ((WidthF * HeightF * (depthF / 10)) / 1000)
    print("Need aliter of water  =" +literFun)

    timeFun = (literFun * 34)
    print("Time to oprate pump  ="+timeFun)

    return timeFun

    return timeFun



def water_soil_funl():
    #water_l  = dbget("SELECT water_l FROM fields WHERE field_id = 1")
    #waterl   = water_l[0][0]
    #print(waterl)
    conn = 1
    while(True):
        if conn <= 10:
            if(ser.in_waiting >0):
                line = ser.readline()
                if "soil  = " in  str(line)  :
                    #time.sleep(1)
                    soil = (int(line[9:12]))
                    print("soilfrom serial  = " , soil)
                    #firebase.put('1','soil',soil)
                    dbrun("UPDATE fields SET soil ="+str(soil)+" where field_id = '"+str(field_Id)+"'")
                elif "water  =" in  str(line) :
                         #time.sleep(1)alarm_state:
                    waterl = int(line[10:12])
                    print("waterfrom serial  = " ,waterl)
                    #firebase.put('1','water',waterl)
                    dbrun("UPDATE fields SET water_l ='"+str(waterl)+"' where field_id = '"+str(field_Id)+"'")
                    date1 =date.today()
                    Date1 =date1.strftime("%d/%m/%Y")
                    d = "\" "
                    dbrun("UPDATE fields SET Date_s ='"+str(date1)+"' where field_id = '"+str(field_Id)+"'")
                   
                    #firebase.put('1','Date_s',"\" "+Date1+"\"")
                else:
                    print("ther are problem no meature")
                            
            else :
                print("no data in serial port")
                conn+=1
                sleep(0.5)
                
        else:
            break
            #conn+=1
            #sleep(1)
        
        
def alarm_funl():
    i = GPIO.input(23)
    if i == 1:  # When output from motion sensor is HIGH
        print("Intruder detected", i)
        GPIO.output(24, 1)
        sleep(5)
        GPIO.output(24, 0)
                    
    else:
        print("Alarm is off")


def dht11_funl():
    instance = dht11.DHT11(pin=27)
    result = instance.read()
    if result.is_valid():
        #firebase.put('1','Temperature',result.temperature)
        dbrun("UPDATE fields SET temp ="+str(result.temperature)+" where field_id = 1")
        #firebase.put('1','Humidity',result.humidity)
        dbrun("UPDATE fields SET humidity ="+str(result.humidity)+" where field_id = 1")
            
        print("Temp: %d C" % result.temperature +'\n'+"Humid: %d %%" % result.humidity)

    time.sleep(1)
    


def pump_funl():

    thresh = 30
    global watered
    watered =False
    print("watered?", watered)
    time = datetime.datetime.now().strftime("%H:%M")
    print("current time", time)
    if not watered:
        while True:
            moisture = dbget("SELECT soil FROM fields WHERE field_id = 1")
            sleep(1)
            print("soile00   =", str(moisture[0][0]))
            if (((time > "22:45") and (time < "00:55")) or ((time > "00:00") and (time < "01:45"))):
                if (str(moisture[0][0]) > str(thresh)):
                    GPIO.output(18, 0)
                    watered = True
                    break
                elif(str(moisture[0][0]) < str(thresh)) :
                    timeToSleep = getTime("1")
                    GPIO.output(18, 1)
                    sleep(timeToSleep)
                    GPIO.output(18, 0)
                    watered = False
                    break
            else:
               break
def mainfun():
    while True:
        water_soil_funl()
        
        
        pump_funl()
       
        dht11_funl()
        
        alarm_funl()
        
        

#if __name__ == '__main__':main()
            
