import tkinter
import tkinter.ttk
from Serial_communicationSend import *
from tkinter import *
import serial

window=tkinter.Tk()
window.title("Walking parameter assistance")
window.geometry("640x400+100+100")
window.resizable(False, False)

btnMotionparameter=tkinter.Button(window, text="Motion Parameter")
lbl_1= tkinter.Label(window, text="RV")
lbl_2= tkinter.Label(window, text="RR")
lbl_3= tkinter.Label(window, text="Value")
lbl_4= tkinter.Label(window, text="Steps")
txtRVvalue = tkinter.Text(window, width=6, height=1)
txtRVsteps = tkinter.Text(window, width=6, height=1)
txtRRvalue = tkinter.Text(window, width=6, height=1)
txtRRsteps = tkinter.Text(window, width=6, height=1)
txtRVvalue.insert(0.0, "0")
txtRVsteps.insert(0.0, "0")
txtRRvalue.insert(0.0, "0")
txtRRsteps.insert(0.0, "0")
btnMove = tkinter.Button(window, text="Move", width=7, height=1)
btnStop = tkinter.Button(window, text="Stop", width=7, height=1)
lbl_5= tkinter.Label(window, text="Serial Communication")
RadioVariety_1=tkinter.IntVar()
radio_Brate38400 = tkinter.Radiobutton(window, value = 38400,text="38400",variable=RadioVariety_1)
radio_Brate115200 = tkinter.Radiobutton(window, value = 115200,text="115200",variable=RadioVariety_1)
lbl_6= tkinter.Label(window, text="PORT")
values=["COM"+str(i) for i in range(1, 10)]
combobox_Baudrate=tkinter.ttk.Combobox(window, width=7, height=15, values=values)
btnOpen=tkinter.Button(window, text="OPEN")

frame=tkinter.Frame(window)
listbox=tkinter.Listbox(frame)
for line in range(1,10):
   listbox.insert(line, " ")

frame2=tkinter.Frame(window)
listbox2=tkinter.Listbox(frame2)
for line in range(1,20):
   listbox2.insert(line, str(line) + "/20")

txtsendcommand = tkinter.Text(window, width=41, height=1, autoseparators= True)

btnMotionparameter.place(x=50, y=50, width=200, height=30)

lbl_1.place(x=60, y=110)
lbl_2.place(x=60, y=150)
lbl_3.place(x=100, y=85)
lbl_4.place(x=180, y=85)
txtRVvalue.place(x=100, y=110)
txtRVsteps.place(x=180, y=110)
txtRRvalue.place(x=100, y=150)
txtRRsteps.place(x=180, y=150)
btnMove.place(x=100, y=220)
btnStop.place(x=180, y=220)
lbl_5.place(x=300, y=20)
radio_Brate38400.place(x=300, y=40)
radio_Brate115200.place(x=380, y=40)
lbl_6.place(x=290, y=70)
combobox_Baudrate.place(x=350, y=70)
combobox_Baudrate.set("COM4")
btnOpen.place(x=430, y=70)
listbox.pack()
frame.place(x=280, y=100)
listbox2.pack()
frame2.place(x=430, y=100)
txtsendcommand.place(x=280, y=265)
command_count = 0

def sendCommand(event):
    global command_count
    str = txtsendcommand.get(0.0, tkinter.END)
    str = str.split()
    str = str[command_count]
    sendCommandtoDSP(str)
    listbox.insert(30000-command_count, str)
    listbox.see(30000-command_count)
    command_count += 1

btnMotionparameter.bind("<Button-1>", sendCommand)
txtsendcommand.bind("<Return>", sendCommand)

window.mainloop()



'''
import serial

ser = serial.Serial(
    port='COM8',
    baudrate=9600,
)

while True:
    print("insert op :", end=' ')
    op = input()
    ser.write(op.encode())
'''