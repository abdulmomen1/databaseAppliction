from tkinter import messagebox

import tools
import requests
#
#
# def check_internet():
#     url='http://www.google.com/'
#     timeout=5
#     try:
#         _ = requests.get(url, timeout=timeout)
#         return True
#     except requests.ConnectionError:
#         print("İnternet bağlantısı yok.")
#     return False



# url = "http://www.kite.com"
# timeout = 5
# try:
# 	request = requests.get(url, timeout=timeout)
# 	print("Connected to the Internet")
# except (requests.ConnectionError, requests.Timeout) as exception:
#     messagebox.showerror("","internet is not conncted")
#     print("No internet connection.")

import urllib
import urllib.request as url
from tkinter import *

form = Tk()
form.geometry("250x50")
form.resizable(False, False)
form.config(bg="#4b4b4b")
form.overrideredirect(True)
form.wm_geometry("-0-40")

connectStatus = Label(bg="yellow", fg="#000", width=28, height=2, text="Pending", font="Bahnscrift 12")
connectStatus.place(x=10,y=8)

def runRefresh():
    print("Checking .....")
    connectStatus.config(bg="yellow", fg="#000", width=28, height=2, text="Pending", font="Bahnscrift 12")
    attemptConnect()

def attemptConnect():
    try:
        ping = url.urlopen("https://www.google.com", timeout=1)
        connectStatus.config(text="Connected", font="Bahnscrift 12", bg="green")
        tools.msgbox("inter net is conncted")
        return True

    except urllib.error.URLError:
        connectStatus.config(text="Not Connected", bg="#ff4d4d", font="Bahnscrift 12")
        tools.mserror("internet is not conncted")
        form.destroy()
#form.after(10000, runRefresh)
runRefresh()
form.mainloop()