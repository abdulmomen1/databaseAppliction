from local import *
import requests
from tools import *
from mysqldb import *
from lastdbamount import *

import os
import smtplib

import serial
ser = serial.Serial('/dev/ttyUSB0', 9600)
import time
from time import sleep
import datetime
from datetime import date
from firebase import firebase
import calendar
import glob
import picamera
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN)#pir
GPIO.setup(24, GPIO.OUT)#pazzer
GPIO.setup(18, GPIO.OUT)#relay
GPIO.output(24, 0)
import dht11

watered = False

#alarm----------------------------------------------------------------------------------
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender = 'raspberrypi.cnds@gmail.com'
password = 'Raspberry.cnds'
receiver = 'raspberrypi.cnds@gmail.com'
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)

firebase = firebase.FirebaseApplication('https://ito-smart-agriculture.firebaseio.com/', None)
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

con = 1
def water_soil_fun():

    global con
    def sendmail(recipient, subject, content):
        headers = ["From: " + sender, "Subject: " + subject, "To: " + recipient,
                       "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)

        #Connect to Gmail Server
        session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        session.ehlo()
        session.starttls()
        session.ehlo()

        #Login to Gmail
        session.login(sender, password)

        #Send Email & Exit
        session.sendmail(sender, recipient, headers + "\r\n\r\n" + content)
        session.quit
        
    conn = 1
    while(True):
        if conn <= 2:
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
                    conn+=1
                    #firebase.put('1','Date_s',"\" "+Date1+"\"")
                #firebase.put('1','Date_s',"\" "+Date1+"\"")
                else:
                    print("no data in serial port")
                    conn+=1
                    sleep(0.5)
                water_l  = dbget("SELECT water_l FROM fields WHERE field_id = '"+str(field_Id)+"'")
                waterl   = water_l[0][0]
                if waterl < 80 :
                    motor_state = firebase.get('1', 'motor_state')
                    if (motor_state == '"ON"'):# turn on motor
                        GPIO.output(18, 0)
                        firebase.put('1','motor_state',"AUTO")
                    if con == 1:
                        pass
                    else:
                        sendTo = 'raspberrypi.cnds@gmail.com'
                        emailSubject = "Water level in tank !"
                        emailContent = ("The  Water level In Tank Is Very Low  Time is: " + time.ctime())
                        sendmail(sendTo, emailSubject, emailContent)
                        print("Email Sent")
                        con = 1
                elif waterl > 80 :
                    if (motor_state == '"OFF"'):# turn on motor
                        GPIO.output(18, 0)
                        firebase.put('1','motor_state',"AUTO")
                    con= 0
                else:
                    print("ther are problem no meature")
                                
        else:
            break   

def alarm_fun():
    DIR = './Database/'
    FILE_PREFIX = 'image'

    def send_mail():
        print('Sending E-Mail')
        # Create the directory if not exists
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        # Find the largest ID of existing images.
        # Start new images after this ID value.
        files = sorted(glob.glob(os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].jpg')))
        count = 0

        if len(files) > 0:
            # Grab the count from the last filename.
            count = int(files[-1][-7:-4]) + 1

        # Save image to file
        filename = os.path.join(DIR, FILE_PREFIX + '%03d.jpg' % count)
        # Capture the face
        with picamera.PiCamera() as camera:
            pic = camera.capture(filename)
        # Sending mail
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Movement Detected'

        body = 'Picture is Attached.'
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()
    cona=0
    while True:
        if cona <= 10:
            i = GPIO.input(23)
            if (alarm_state == '"ON"'):
                if i == 0:  # When output from motion sensor is LOW
                    print("No intruders", i)
                    sleep(0.3)
                    cona+=1
                elif i == 1:  # When output from motion sensor is HIGH
                    print("Intruder detected", i)
                    GPIO.output(24, 1)
                    send_mail()
                    GPIO.output(24, 0)
                    break
        elif cona > 10:
            break
        if (alarm_state == '"OFF"'):
            print("Alarm is off")
            pass



def dht11_fun():
    instance = dht11.DHT11(pin=27)
    con = 0
    while True:
        result = instance.read()
        #print(result)
        if con == 4:
            break
        if result.is_valid():
            #firebase.put('1','Temperature',result.temperature)
            dbrun("UPDATE fields SET temp = '"+str(result.temperature)+"' where field_id = "+str(field_Id)+"")
            #firebase.put('1','Humidity',result.humidity)
            dbrun("UPDATE fields SET humidity ="+str(result.humidity)+" where field_id = "+str(field_Id)+"")
                
            print("Temp: %d C" % result.temperature +'\n'+"Humid: %d %%" % result.humidity)
            con+=1
        else:
            con+=1
            print(" temp problem")
        #time.sleep(1)

def pump_fun():
    
    def automate():
        thresh = 30
        global watered
        print("watered?", watered)
        time = datetime.datetime.now().strftime("%H:%M")
        print("current time =", time)
        if not watered: 
            while True:
                moisture = dbget("SELECT soil FROM fields WHERE field_id = "+str(field_Id)+"")
                print("soil to water   =", str(moisture[0][0]))
                if (((time > "13:45") and (time < "17:45")) or ((time > "01:45") and (time < "03:15"))):
                    if (moisture[0][0] > thresh):
                        GPIO.output(18, 0)
                        watered = True
                        break
                    elif(str(moisture[0][0]) < str(thresh)) :
                        timeToSleep = getTime(field_Id)
                        GPIO.output(18, 1)
                        sleep(timeToSleep)
                        GPIO.output(18, 0)
                        break
            
    print("motor_state  ="+motor_state)
    if (motor_state == '"ON"'):# turn on motor
        water_l  = dbget("SELECT water_l FROM fields WHERE field_id = '"+str(field_Id)+"'")
        waterl   = water_l[0][0]
        if waterl < 80:
            con= 0
            water_soil_fun()
        else:   
            timeToSleep = getTime(field_Id)
            GPIO.output(18, 1)
            sleep(timeToSleep)
            firebase.put('1','motor_state',"AUTO")
    # Turn on
      
    elif (motor_state == '"OFF"'):
        GPIO.output(18, 0)
        
    elif (motor_state == '"AUTO"'):
        automate()
    else:
        GPIO.output(18, 0)

def update_fun():
    soil     = dbget("SELECT soil FROM fields WHERE field_id = "+str(field_Id)+"")
    water_l  = dbget("SELECT water_l FROM fields WHERE field_id = "+str(field_Id)+"")
    humidity = dbget("SELECT humidity FROM fields WHERE field_id = "+str(field_Id)+"")
    temp     = dbget("SELECT temp FROM fields WHERE field_id = "+str(field_Id)+"")
    Date_s   = dbget("SELECT Date_s FROM fields WHERE field_id = "+str(field_Id)+"")
    print("soil updated to firebse  ="+str(soil[0][0])+"",'\n'," water level updated to firebse  ="+str(water_l[0][0])+"",'\n',"humidity updated to firebse  ="+str(humidity[0][0])+"",'\n'," date updated to firebse  ="+str(Date_s[0][0])+"",'\n'," temp updated to firebse  ="+str(temp[0][0]))
    
    firebase.put('1','Humidity',humidity[0][0])
    firebase.put('1','Temperature',temp[0][0])
    firebase.put('1','soil',soil[0][0])
    firebase.put('1','water',water_l[0][0])
    firebase.put('1','Date_s',Date_s[0][0])
    firebase.put('1', 'update', str(0))


def main():
    global alarm_state
    global motor_state
    global con
    while True:
        url = "http://www.kite.com"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
            print("Connected to the Internet")
            #messagebox.showerror("","internet is conncted")
            water_soil_fun()
            alarm_state = firebase.get('1', 'alarm_state')
            motor_state = firebase.get('1', 'motor_state')
            update = firebase.get('1', 'update')
            if (update == "1"):
                dht11_fun()
                #sleep(2)
                update_fun()
                #sleep(2)

            elif (motor_state == '"ON"') | (motor_state == '"OFF"') |  (motor_state == '"AUTO"'):
                pump_fun()
                #sleep(1)
            print("alarm_state    ="+alarm_state)
            if alarm_state == '"ON"' :
                alarm_fun()
        except (requests.ConnectionError, requests.Timeout) as exception:
            #messagebox.showerror("","internet is not conncted")
            print("No internet connection.")
            water_soil_funl()
            sleep(5)
            pump_funl()
            sleep(1)
            dht11_funl()
            sleep(1)
            alarm_funl()
            sleep(1)
        
            
        

if __name__ == '__main__':main()









