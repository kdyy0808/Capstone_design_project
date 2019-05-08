import serial
import threading
import queue
import tkinter
import tkinter.ttk

s = serial.Serial('COM3', 38400)
command_count = 0
receivedCount = 0

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        # self.s = serial.Serial('COM3',38400)
        global receivedCount
        while True:
            if s.inWaiting():
                text = s.readline(s.inWaiting())
                self.queue.put(text)
                receivedCount += 1
class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Walking parameter assistance")
        self.geometry("640x400+100+100")
        self.resizable(False, False)

        btnMotionparameter = tkinter.Button(self, text="Motion Parameter")
        lbl_1 = tkinter.Label(self, text="RV")
        lbl_2 = tkinter.Label(self, text="RR")
        lbl_3 = tkinter.Label(self, text="Value")
        lbl_4 = tkinter.Label(self, text="Steps")
        txtRVvalue = tkinter.Text(self, width=6, height=1)
        txtRVsteps = tkinter.Text(self, width=6, height=1)
        txtRRvalue = tkinter.Text(self, width=6, height=1)
        txtRRsteps = tkinter.Text(self, width=6, height=1)
        txtRVvalue.insert(0.0, "0")
        txtRVsteps.insert(0.0, "0")
        txtRRvalue.insert(0.0, "0")
        txtRRsteps.insert(0.0, "0")
        btnMove = tkinter.Button(self, text="Move", width=7, height=1)
        btnStop = tkinter.Button(self, text="Stop", width=7, height=1)
        lbl_5 = tkinter.Label(self, text="Serial Communication")
        RadioVariety_1 = tkinter.IntVar()
        radio_Brate38400 = tkinter.Radiobutton(self, value=38400, text="38400", variable=RadioVariety_1)
        radio_Brate115200 = tkinter.Radiobutton(self, value=115200, text="115200", variable=RadioVariety_1)
        lbl_6 = tkinter.Label(self, text="PORT")
        values = ["COM" + str(i) for i in range(1, 10)]
        combobox_Baudrate = tkinter.ttk.Combobox(self, width=7, height=15, values=values)
        btnOpen = tkinter.Button(self, text="OPEN")
        frame = tkinter.Frame(self)
        listbox = tkinter.Listbox(frame)
        for line in range(1, 10):
            listbox.insert(line, " ")

        frame2 = tkinter.Frame(self)
        self.listbox2 = tkinter.Listbox(frame2)
        for line in range(1, 20):
            self.listbox2.insert(line, "")

        txtsendcommand = tkinter.Text(self, width=41, height=1, autoseparators=True)

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
        self.listbox2.pack()
        frame2.place(x=430, y=100)
        txtsendcommand.place(x=280, y=265)
        # command_count = 0

        def sendCommand(event):
            global command_count
            str = txtsendcommand.get(0.0, tkinter.END)
            str = str.split()
            str = str[command_count]
            self.sendCommandtoDSP(str)
            listbox.insert(30000 - command_count, str)
            listbox.see(30000 - command_count)
            command_count += 1

        btnMotionparameter.bind("<Button-1>", sendCommand)
        txtsendcommand.bind("<Return>", sendCommand)

        self.queue = queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    def sendCommandtoDSP(self,string):
        s.write(string.encode())

    def process_serial(self):
        while self.queue.qsize():
            try:
                n = self.queue.get()
                if n is not None:
                    self.listbox2.insert(30000 - receivedCount, n)
                    self.listbox2.see(30000 - receivedCount)

            except queue.Empty:
                pass
        self.after(10, self.process_serial)

app = App()
app.mainloop()