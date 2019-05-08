import tkinter
import time
import threading
import queue
import random


command_count=0

import tkinter.ttk
from Serial_communicationSend import *

receivedCount=0

class Mailbox(threading.Thread):

    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q =q
        self.num = 0

    def run(self):
        ser = serial.Serial('COM3', 38400)
        while True:
            time.sleep(0.01)
            # if random.randint(1, 5) == 2:
            #     self.num = random.randint(1, 100)
            #     self.q.put(self.num)
            global receivedCount
            if ser.readable():
                self.res = ser.readline()
                # self.q.put(self.res.decode()[:len(self.res) - 1])
                self.q.put(str(self.res.decode()[:len(self.res) - 1]))
                receivedCount += 1
                print(self.res.decode()[:len(self.res) - 1])


class MyAPP(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)

        self.window = tkinter.Tk()
        self.window.title("Walking parameter assistance")
        self.window.geometry("640x400+100+100")
        self.window.resizable(True, True)




        #self.t_label = tkinter.IntVar(self, 0)
        # self.label = tkinter.Label(self, textvariable=self.t_label)
        # self.label.pack()
        # self.button = tkinter.Button(self, text="start", command=self.start_timer)
        # self.button.pack()
        self.mailbox = [0]

        self.btnMotionparameter = tkinter.Button(self.window, text="Motion Parameter")
        self.lbl_1 = tkinter.Label(self.window, text="RV")
        self.lbl_2 = tkinter.Label(self.window, text="RR")
        self.lbl_3 = tkinter.Label(self.window, text="Value")
        self.lbl_4 = tkinter.Label(self.window, text="Steps")
        self.txtRVvalue = tkinter.Text(self.window, width=6, height=1)
        self.txtRVsteps = tkinter.Text(self.window, width=6, height=1)
        self.txtRRvalue = tkinter.Text(self.window, width=6, height=1)
        self.txtRRsteps = tkinter.Text(self.window, width=6, height=1)
        self.txtRVvalue.insert(0.0, "0")
        self.txtRVsteps.insert(0.0, "0")
        self.txtRRvalue.insert(0.0, "0")
        self.txtRRsteps.insert(0.0, "0")
        self.btnMove = tkinter.Button(self.window, text="Move", width=7, height=1)
        self.btnStop = tkinter.Button(self.window, text="Stop", width=7, height=1)
        self.lbl_5 = tkinter.Label(self.window, text="Serial Communication")
        self.RadioVariety_1 = tkinter.IntVar()
        self.radio_Brate38400 = tkinter.Radiobutton(self.window, value=38400, text="38400", variable=self.RadioVariety_1)
        self.radio_Brate115200 = tkinter.Radiobutton(self.window, value=115200, text="115200", variable=self.RadioVariety_1)
        self.lbl_6 = tkinter.Label(self.window, text="PORT")
        self.values = ["COM" + str(i) for i in range(1, 10)]
        self.combobox_Baudrate = tkinter.ttk.Combobox(self.window, width=7, height=15, values=self.values)
        self.btnOpen = tkinter.Button(self.window, text="OPEN")

        self.frame = tkinter.Frame(self.window)
        self.listbox = tkinter.Listbox(self.frame)
        for line in range(1, 10):
            self.listbox.insert(line, " ")
        self.frame2 = tkinter.Frame(self.window)
        self.listbox2 = tkinter.Listbox(self.frame2)

        # self.frame2 = tkinter.Frame(window)
        # self.listbox2 = tkinter.Listbox(frame2)
        # for line in range(1, 20):
        #     listbox2.insert(line, str(line) + "/20")

        self.txtsendcommand = tkinter.Text(self.window, width=41, height=1, autoseparators=True)

        self.btnMotionparameter.place(x=50, y=50, width=200, height=30)

        self.lbl_1.place(x=60, y=110)
        self.lbl_2.place(x=60, y=150)
        self.lbl_3.place(x=100, y=85)
        self.lbl_4.place(x=180, y=85)
        self.txtRVvalue.place(x=100, y=110)
        self.txtRVsteps.place(x=180, y=110)
        self.txtRRvalue.place(x=100, y=150)
        self.txtRRsteps.place(x=180, y=150)
        self.btnMove.place(x=100, y=220)
        self.btnStop.place(x=180, y=220)
        self.lbl_5.place(x=300, y=20)
        self.radio_Brate38400.place(x=300, y=40)
        self.radio_Brate115200.place(x=380, y=40)
        self.lbl_6.place(x=290, y=70)
        self.combobox_Baudrate.place(x=350, y=70)
        self.combobox_Baudrate.set("COM8")
        self.btnOpen.place(x=430, y=70)


        self.listbox.pack()
        self.frame.place(x=280, y=100)
        self.listbox2.pack()
        self.frame2.place(x=430, y=100)
        self.txtsendcommand.place(x=280, y=265)


        self.q = queue.Queue(10)


        # for line in range(1, 20):
        #     self.listbox2.insert(line, str(line) + "/20")
        def sendCommandtoDSP(string):
            self.ser.write(string.encode())
        def sendCommand(event):
            global command_count
            str = self.txtsendcommand.get(0.0, tkinter.END)
            str = str.split()
            str = str[command_count]
            sendCommandtoDSP(str)
            self.listbox.insert(30000 - command_count, str)
            self.listbox.see(30000 - command_count)
            command_count += 1



        self.btnMotionparameter.bind("<Button-1>", sendCommand)
        self.txtsendcommand.bind("<Return>", sendCommand)





        # self.listbox2.pack()
        # self.frame2.pack()




    def start_timer(self):
        Mailbox(self.q).start()
        self.after(0,self.check_Mailbox)

    def check_Mailbox(self):
        try:
            # for data in range(0, 10):
            n = self.q.get()
            # self.q.popleft()
            # self.mailbox.append(n)
            # self.t_label.set(self.mailbox)
            if n is not None:
                # self.listbox2.insert(30000 - receivedCount, self.mailbox[receivedCount-1])
                self.listbox2.insert(30000 - receivedCount, n)
                self.listbox2.see(30000-receivedCount)

        except queue.Empty:
            pass
        finally:
            self.after(10, self.check_Mailbox)

root = MyAPP()
root.start_timer()
root.mainloop()












