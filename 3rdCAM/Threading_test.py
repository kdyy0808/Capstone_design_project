import tkinter
import time
import threading
import queue
import random

import tkinter.ttk
from Serial_communicationSend import *

receivedData = list()
receivedCount=0

class Data_receive(threading.Thread):
    global receivedData

    def __init__(self):
        threading.Thread.__init__(self)
        #self.q =q
        #self.num = 0

    def run(self):
        while True:
            global receivedCount

            time.sleep(0.01+1)
            if ser.readable():
                res = ser.readline()
                print(res.decode()[:len(res) - 1])
                receivedData.append(res.decode()[:len(res) - 1])
                receivedCount+=1
                print(receivedCount)
            # if random.randint(1, 5) == 2:
            #     self.num = random.randint(1, 100)
            #     self.q.put(self.num)

class MyAPP(tkinter.Tk):
    command_count = 0
    def __init__(self):
        # tkinter.Tk.__init__(self)

        # self.t_label = tkinter.IntVar(self, 0)
        # self.label = tkinter.Label(self, textvariable=self.t_label)
        # self.label.pack()
        # self.button = tkinter.Button(self, text="start", command=self.start_timer)
        # self.button.pack()
        # self.mailbox=[]
        # self.q = queue.Queue(10)

        window = tkinter.Tk()
        window.title("Walking parameter assistance")
        window.geometry("640x400+100+100")
        window.resizable(False, False)

        btnMotionparameter = tkinter.Button(window, text="Motion Parameter")
        lbl_1 = tkinter.Label(window, text="RV")
        lbl_2 = tkinter.Label(window, text="RR")
        lbl_3 = tkinter.Label(window, text="Value")
        lbl_4 = tkinter.Label(window, text="Steps")
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
        lbl_5 = tkinter.Label(window, text="Serial Communication")
        RadioVariety_1 = tkinter.IntVar()
        radio_Brate38400 = tkinter.Radiobutton(window, value=38400, text="38400", variable=RadioVariety_1)
        radio_Brate115200 = tkinter.Radiobutton(window, value=115200, text="115200", variable=RadioVariety_1)
        lbl_6 = tkinter.Label(window, text="PORT")
        values = ["COM" + str(i) for i in range(1, 10)]
        combobox_Baudrate = tkinter.ttk.Combobox(window, width=7, height=15, values=values)
        btnOpen = tkinter.Button(window, text="OPEN")

        frame = tkinter.Frame(window)
        listbox = tkinter.Listbox(frame)
        for line in range(1, 10):
            listbox.insert(line, " ")

        frame2 = tkinter.Frame(window)
        listbox2 = tkinter.Listbox(frame2)
        for line in range(1, 20):
            listbox2.insert(line, str(line) + "/20")

        txtsendcommand = tkinter.Text(window, width=41, height=1, autoseparators=True)

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
        # command_count = 0
        k=len(receivedData)
        print("k======{}".format(k))
        if receivedCount>0:
            listbox2.insert(0.0, receivedData[receivedCount-1])
        def sendCommand(event):

            global command_count

            str = txtsendcommand.get(0.0, tkinter.END)
            str = str.split()
            str = str[self.command_count]
            sendCommandtoDSP(str)
            listbox.insert(30000 - self.command_count, str)
            listbox.see(30000 - self.command_count)
            self.command_count += 1
        def receiveCommand(self):
            print("cccddc")
            try:
                for data in range(receivedCount):
                    n = self.q.get(0)
                    # self.mailbox.append(n)
                    listbox2.insert(30000 - receivedCount, receivedData[receivedCount-1])
                    print("cccc")
            except queue.Empty:
                pass
            finally:
                self.after(10, self.receiveCommand)


            # listbox2.insert(30000 - receivedCount , receivedData[receivedCount-1])
            # listbox2.see(30000 - receivedCount)
        btnMotionparameter.bind("<Button-1>", sendCommand)
        txtsendcommand.bind("<Return>", sendCommand)

        Data_receive().start()
        # self.after(10,self.receiveCommand)
        # self.after(0, self.check_Mailbox)
        window.mainloop()

    # def check_Mailbox(self):
    #     try:
    #         for mail in range(0,10):
    #             n = self.q.get(0)
    #             self.mailbox.append(n)
    #             self.t_label.set(self.mailbox)
    #     except queue.Empty:
    #         pass
    #     finally:
    #         self.after(3000, self.check_Mailbox)
root = MyAPP()
root.mainloop()














# import serial
#
# ser = serial.Serial('COM8', 9600)
# print('port opened')
# while ser.isOpen():
#     try:
#         sdata= input('Type a word & Enter:')
#         sdata+='\n'
#         ser.write(sdata.encode('ASCII'))
#         buff=byte=b'0'
#         while byte != b'\n':
#             byte=ser.read(1)
#             if byte not in [b'\r', b'\n']:
#                 buff+=byte
#         print(buff.decaode('ASCII'))
#     except:
#         ser.close()
#         pass