import mysql.connector
from tools import *
global all_err
global myuser
global mypass
global myhost
global database

all_err   = ""
myuser   = 'pi'
mypass   = 'raspberry'
myhost   = 'localhost'
mydatabase = 'pi'
try:
	cn = mysql.connector.connect(
		host     = myhost,
		user     = myuser,
		passwd   = mypass)
	cu = cn.cursor()
	cu.execute("""
		CREATE DATABASE IF NOT EXISTS pi DEFAULT CHARACTER SET utf8
	    DEFAULT COLLATE utf8_general_ci""")
except mysql.connector.Error as e:
	all_err+= str(e) + ".Plase check Mysql server and user. , "

try:
	conn = mysql.connector.connect(
		host=myhost,
		user=myuser,
		passwd=mypass,
		database = mydatabase
	)

except mysql.connector.Error as e:
	all_err+= str(e) + " .Plase check Mysql server and user. ,"

def dbrun(sql):
	try:
		if 'conn'in globals():
			cur = conn.cursor()
			cur.execute(sql)
			conn.commit()
			return True
		else:
			return False
	except mysql.connector.Error as e:
		return False

def dbget(sql):
	try:
		if 'conn'in globals():
			conn.commit()
			cur = conn.cursor()
			cur.execute(sql)
			all_rows =cur.fetchall()
			conn.commit()
			return all_rows
		else:
			return []
	except mysql.connector.Error as e:
		return[]

def dbautonum(table, column):
	try:
		if 'conn' in globals():
			cur = conn.cursor()
			cur.execute("SELECT MAX(%s)+1 FROM %s" %(column,table ))
			row = cur.fetchone()
			if row[0] ==None: return "1"
			else:return row[0]
		else:
			mserror("no connection to database plase turn on zamp")
			return 0

	except mysql.connector.Error as e:
			return ""


