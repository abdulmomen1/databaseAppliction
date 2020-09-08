from threading import *
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
GPIO.setup(23, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(18, GPIO.OUT, initial=0)
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


def getTime(ID_var):
    amont(ID_var)
    Width = dbget("SELECT  Width_F FROM fields WHERE field_id = " + str(ID_var) + "")
    Height = dbget("SELECT  Height_F FROM fields WHERE field_id = " + str(ID_var) + "")
    depth = dbget("SELECT  water_mm FROM fields WHERE field_id = " + str(ID_var) + "")
    WidthF = Width[0][0]
    HeightF = Height[0][0]
    depthF = depth[0][0]

    print(WidthF)
    print(HeightF)
    print(depthF)

    literFun = ((WidthF * HeightF * (depthF / 10)) / 1000)
    print(literFun)

    timeFun = (literFun * 34)
    print(timeFun)

    return timeFun

con = 1
def water_soil_fun():
    global con
    water_l  = dbget("SELECT water_l FROM fields WHERE field_id = 1")
    waterl   = water_l[0][0]
    print(waterl)

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
            
    if(ser.in_waiting >0):
        line = ser.readline()
        if "soil  = " in  str(line)  :
             #time.sleep(1)
            soil = (int(line[9:11]))
            print("soil  = " , soil)
            #firebase.put('1','soil',soil)
            dbrun("UPDATE fields SET soil ="+str(soil)+" where field_id = 1")
        elif "water  =" in  str(line) :
                 #time.sleep(1)alarm_state:
            waterl = int(line[10:12])
            print("water  = " ,waterl)
            #firebase.put('1','water',waterl)
            dbrun("UPDATE fields SET water_l ='"+str(waterl)+"' where field_id = 1")
            date1 =date.today()
            Date1 =date1.strftime("%d/%m/%Y")
            d = "\" "
            dbrun("UPDATE fields SET Date_s ='"+str(date1)+"' where field_id = 1")
            #firebase.put('1','Date_s',"\" "+Date1+"\"")
            if waterl < 80 :
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
                con= 0
        else:
            print("ther are problem no meature")
                    
    else :
        print("no data in serial port")
        sleep(1)
            

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

    i = GPIO.input(23)
    if (alarm_state == '"ON"'):
        if i == 0:  # When output from motion sensor is LOW
            print("No intruders", i)
            sleep(0.3)
        elif i == 1:  # When output from motion sensor is HIGH
            print("Intruder detected", i)
            GPIO.output(24, 1)
            send_mail()
            GPIO.output(24, 0)
                    
    if (alarm_state == '"OFF"'):
        print("Alarm is off")
        pass



def dht11_fun():
    instance = dht11.DHT11(pin=27)
    result = instance.read()
    if result.is_valid():
        #firebase.put('1','Temperature',result.temperature)
        dbrun("UPDATE fields SET temp ="+str(result.temperature)+" where field_id = 1")
        #firebase.put('1','Humidity',result.humidity)
        dbrun("UPDATE fields SET humidity ="+str(result.humidity)+" where field_id = 1")
            
        print("Temp: %d C" % result.temperature +'\n'+"Humid: %d %%" % result.humidity)

    time.sleep(1)

def pump_fun():
    
    def automate():
        thresh = 30
        global watered
        print("watered?", watered)
        time = datetime.datetime.now().strftime("%H:%M")
        print("current time", time)
        if not watered:
            while True:
                moisture = dbget("SELECT soil FROM fields WHERE field_id = 1")
                print("soile   =", str(moisture[0][0]))
                if (((time > "19:45") and (time < "20:45")) or ((time > "01:45") and (time < "03:15"))):
                    if (str(moisture[0][0]) > str(thresh)):
                        GPIO.output(18, 0)
                        watered = True
                        break
                    elif(str(moisture[0][0]) < str(thresh)) :
                        timeToSleep = getTime("1")
                        GPIO.output(18, 1)
                        sleep(timeToSleep)
                        GPIO.output(18, 0)
                    break
            

    print("watered?")
    print(motor_state)
    if (motor_state == '"ON"'):# turn on motor
        timeToSleep = getTime("1")
        GPIO.output(18, 1)
        sleep(timeToSleep)
        GPIO.output(18, 0)# Turn on
      
    elif (motor_state == '"OFF"'):
        GPIO.output(18, 0)
        
    elif (motor_state == '"AUTO"'):
        automate()
    else:
        GPIO.output(18, 0)

def update_fun():
    soil     = dbget("SELECT soil FROM fields WHERE field_id = 1")
    water_l  = dbget("SELECT water_l FROM fields WHERE field_id = 1")
    humidity = dbget("SELECT humidity FROM fields WHERE field_id = 1")
    temp     = dbget("SELECT temp FROM fields WHERE field_id = 1")
    Date_s   = dbget("SELECT Date_s FROM fields WHERE field_id = 1")
    print(soil[0][0],water_l[0][0],humidity[0][0],Date_s[0][0],temp[0][0])
    
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
        alarm_state = firebase.get('1', 'alarm_state')
        motor_state = firebase.get('1', 'motor_state')
        update = firebase.get('1', 'update')
        if (update == "1"):
            con = 0
            dht11_fun()
            update_fun()

        elif (motor_state == '"ON"') | (motor_state == '"OFF"') |  (motor_state == '"AUTO"'):
            pump_fun()
            if alarm_state == '"ON"' :
                alarm_fun()
        water_soil_fun()

if __name__ == '__main__':main()









