import cx_Freeze
import sys
import tkinter
from tools import *
from mysqldb import *

base = None
executables =[cx_Freeze.Executable("login.py", base=base)]

cx_Freeze.setup(
	name = "My_Field",
	option = {"build_exe":{"packages":["tkinter"]}},
	version ="1.0",
	description= "lllllllllllllllllllllll",
	executables = executables



)