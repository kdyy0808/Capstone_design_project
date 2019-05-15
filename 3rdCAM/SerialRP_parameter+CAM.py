import serial
import threading
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import os
import math
import numpy as np
import tkinter.ttk
from tkinter import messagebox
import queue

s = serial.Serial('COM3', 38400)
command_count = 0
receivedCount = 0
receiving_Data=list()
semicolonFlag = False
btext = ""

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        # self.s = serial.Serial('COM3',38400)
        global receivedCount, receiving_Data, semicolonFlag, btext
        while True:
            if s.inWaiting():
                text = s.readline(s.inWaiting())
                text=text.decode()
                # text = str(text)
                # text = text[1:]
                btext += text
                if text.find(';') != -1:
                    if btext =="":
                        btext = text
                    # semicolonFlag = True
                    self.queue.put(btext)
                    receivedCount += 1
                    btext=""


class Color_catagory:
    def __init__(self):
        self.H_min = 0
        self.H_max = 180
        self.S_min = 0
        self.S_max = 255
        self.V_min = 0
        self.V_max = 255
        self.max_x = 0
        self.max_y = 0
        self.max_width = 0
        self.max_height = 0
        self.max_area = 0


class App(tkinter.Tk, Color_catagory):
    btnGrayFlag=0
    RadioFlag =0
    Outframe = None
    frame_Red = None
    frame_Green = None
    frame_Blue = None

    def __init__(self, window, window_title, video_source=0):
        tkinter.TK.__init__(self)
        self.Red = Color_catagory()
        self.Green = Color_catagory()
        self.Blue = Color_catagory()
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1500x500+100+100")
        self.video_source = video_source
        self.Scroll_H_min = tkinter.Scale()
        self.vid = MyVideoCapture(self.video_source)
        self.HSVdatafile()
        self.screen_init(self.window)
        self.delay = 15
        self.update()

        self.window.mainloop()
    def HSVdatafile(self):
        hsv_values = list()
        if os.path.exists('./HSV_parameters.txt'):
            file = open('./HSV_parameters.txt', 'r')
            All = file.read()
            file.close()
            words = All.split()
            for word in words:
                if word.isdigit():
                    hsv_values.append(word)
        else:
            file = open('./HSV_parameters.txt', 'w')
            file.write("HSV_parameters\n============================\n")
            file.write("Red H_min : 0 \t Red H_max : 180\n")
            file.write("Red S_min : 0 \t Red S_max : 255\n")
            file.write("Red V_min : 0 \t Red V_max : 255\n")
            file.write("============================\n")
            file.write("Green H_min : 0 \t Green H_max : 180\n")
            file.write("Green S_min : 0 \t Green S_max : 255\n")
            file.write("Green V_min : 0 \t Green V_max : 255\n")
            file.write("============================\n")
            file.write("Blue H_min : 0 \t Blue H_max : 180\n")
            file.write("Blue S_min : 0 \t Blue S_max : 255\n")
            file.write("Blue V_min : 0 \t Blue V_max : 255\n")
            file.write("============================\n")
            file.close()
            hsv_values=[0, 180, 0, 255, 0, 255, 0, 180, 0, 255, 0, 255, 0, 180, 0, 255, 0, 255]
        self.Red.H_min = int(hsv_values[0])
        self.Red.H_max = int(hsv_values[1])
        self.Red.S_min = int(hsv_values[2])
        self.Red.S_max = int(hsv_values[3])
        self.Red.V_min = int(hsv_values[4])
        self.Red.V_max = int(hsv_values[5])

        self.Green.H_min = int(hsv_values[6])
        self.Green.H_max = int(hsv_values[7])
        self.Green.S_min = int(hsv_values[8])
        self.Green.S_max = int(hsv_values[9])
        self.Green.V_min = int(hsv_values[10])
        self.Green.V_max = int(hsv_values[11])

        self.Blue.H_min = int(hsv_values[12])
        self.Blue.H_max = int(hsv_values[13])
        self.Blue.S_min = int(hsv_values[14])
        self.Blue.S_max = int(hsv_values[15])
        self.Blue.V_min = int(hsv_values[16])
        self.Blue.V_max = int(hsv_values[17])
        del hsv_values

    def screen_init(self,window):
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        # self.canvas.grid(columnspan=30, rowspan=20)
        self.canvas.place(x=0,y=0)
        def radio_control_R():
            self.Rbtn_Color_Green.deselect()
            self.Rbtn_Color_Blue.deselect()
            self.Rbtn_Color_All.deselect()
            self.Scroll_H_min.set(self.Red.H_min)
            self.Scroll_H_max.set(self.Red.H_max)
            self.Scroll_S_min.set(self.Red.S_min)
            self.Scroll_S_max.set(self.Red.S_max)
            self.Scroll_V_min.set(self.Red.V_min)
            self.Scroll_V_max.set(self.Red.V_max)
            show_values(event=1)
            self.RadioFlag=1

        def radio_control_G():
            self.Rbtn_Color_Red.deselect()
            self.Rbtn_Color_Blue.deselect()
            self.Rbtn_Color_All.deselect()
            self.Scroll_H_min.set(self.Green.H_min)
            self.Scroll_H_max.set(self.Green.H_max)
            self.Scroll_S_min.set(self.Green.S_min)
            self.Scroll_S_max.set(self.Green.S_max)
            self.Scroll_V_min.set(self.Green.V_min)
            self.Scroll_V_max.set(self.Green.V_max)
            show_values(event=1)
            self.RadioFlag=2

        def radio_control_B():
            self.Rbtn_Color_Red.deselect()
            self.Rbtn_Color_Green.deselect()
            self.Rbtn_Color_All.deselect()
            self.Scroll_H_min.set(self.Blue.H_min)
            self.Scroll_H_max.set(self.Blue.H_max)
            self.Scroll_S_min.set(self.Blue.S_min)
            self.Scroll_S_max.set(self.Blue.S_max)
            self.Scroll_V_min.set(self.Blue.V_min)
            self.Scroll_V_max.set(self.Blue.V_max)
            show_values(event=1)
            self. RadioFlag=3

        def radio_control_All():
            self.Rbtn_Color_Red.deselect()
            self.Rbtn_Color_Blue.deselect()
            self.Rbtn_Color_Green.deselect()
            self.Scroll_H_min.set(0)
            self.Scroll_H_max.set(180)
            self.Scroll_S_min.set(0)
            self.Scroll_S_max.set(255)
            self.Scroll_V_min.set(0)
            self.Scroll_V_max.set(255)
            show_values(event=1)
            self.RadioFlag=0

        self.var = tkinter.IntVar()

        self.Rbtn_Color_Red = tkinter.Radiobutton(window, text='Red',value = 1, variable=self.var, command=radio_control_R)
        self.Rbtn_Color_Red.place(x=640, y=380)
        self.Rbtn_Color_Green = tkinter.Radiobutton(window, text='Green',value = 2, variable=self.var, command=radio_control_G)
        self.Rbtn_Color_Green.place(x=695, y=380)
        self.Rbtn_Color_Blue = tkinter.Radiobutton(window, text='Blue', value=3, variable=self.var, command=radio_control_B)
        self.Rbtn_Color_Blue.place(x=750, y=380)
        self.Rbtn_Color_All = tkinter.Radiobutton(window, text='All', value=4, variable=self.var,command=radio_control_All)
        self.Rbtn_Color_All.place(x=640, y=400)
        self.L1 = tkinter.Label(window,text="H_min: ", width=10, height=2, fg="red", relief="solid")
        self.L1.place(x=650, y=250)

        self.L2 = tkinter.Label(window, text="H_max: ", width=10, height=2, fg="red", relief="solid")
        self.L2.place(x=730, y=250)

        self.L3 = tkinter.Label(window, text="S_min: ", width=10, height=2, fg="red", relief="solid")
        self.L3.place(x=650, y=290)

        self.L4 = tkinter.Label(window, text="S_max: ", width=10, height=2, fg="red", relief="solid")
        self.L4.place(x=730, y=290)
        self.L5 = tkinter.Label(window, text="V_min: ", width=10, height=2, fg="red", relief="solid")
        self.L5.place(x=650, y=330)
        self.L6 = tkinter.Label(window, text="V_max: ", width=10, height=2, fg="red", relief="solid")
        self.L6.place(x=730, y=330)
        self.btnColormap = tkinter.Button(window, text="Colormap", width=10, command=self.ShowColormap)
        self.btnColormap.place(x=815,y=254)
        self.btnload = tkinter.Button(window, text="Load", width=10, command=self.loadParameter)
        self.btnload.place(x=815, y=293)
        self.btnsave = tkinter.Button(window, text="Save", width=10, command=self.saveParameter)
        self.btnsave.place(x=815, y=333)

        def show_values(event):

            if self.var.get() ==1:
                self.thisColor = self.Red
            elif self.var.get() ==2:
                self.thisColor = self.Green
            elif self.var.get() ==3:
                self.thisColor = self.Blue
            else:
                return
            self.thisColor.H_min = self.Scroll_H_min.get()
            self.thisColor.H_max = self.Scroll_H_max.get()
            self.thisColor.S_min = self.Scroll_S_min.get()
            self.thisColor.S_max = self.Scroll_S_max.get()
            self.thisColor.V_min = self.Scroll_V_min.get()
            self.thisColor.V_max = self.Scroll_V_max.get()

            value1 = "H_min :" + str( self.thisColor.H_min)
            self.L1.config(text=value1)
            value2 = "H_max :" + str( self.thisColor.H_max)
            self.L2.config(text=value2)
            value3 = "S_min :" + str( self.thisColor.S_min)
            self.L3.config(text=value3)
            value4 = "S_max :" + str( self.thisColor.S_max)
            self.L4.config(text=value4)
            value5 = "V_min :" + str( self.thisColor.V_min)
            self.L5.config(text=value5)
            value6 = "V_max :" + str( self.thisColor.V_max)
            self.L6.config(text=value6)

        self.Scroll_H_min = tkinter.Scale(window, from_=0, to=180, orient=tkinter.HORIZONTAL)
        self.Scroll_H_min.set(0)
        self.Scroll_H_min.place(x=650, y=0)
        self.Scroll_H_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_H_max = tkinter.Scale(window, from_=0, to=180, orient=tkinter.HORIZONTAL)
        self.Scroll_H_max.set(255)
        self.Scroll_H_max.place(x=650, y=40)
        self.Scroll_H_max.bind("<ButtonRelease-1>", show_values)
        self.Scroll_S_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_S_min.set(0)
        self.Scroll_S_min.place(x=650, y=80)
        self.Scroll_S_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_S_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_S_max.set(255)
        self.Scroll_S_max.place(x=650, y=120)
        self.Scroll_S_max.bind("<ButtonRelease-1>", show_values)
        self.Scroll_V_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_V_min.set(0)
        self.Scroll_V_min.place(x=650, y=160)
        self.Scroll_V_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_V_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_V_max.set(255)
        self.Scroll_V_max.place(x=650, y=200)
        self.Scroll_V_max.bind("<ButtonRelease-1>", show_values)

        #------------------------------------------------------------------------------------------------------------------------------------------------------------

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

        def Portopen():
            messagebox.showinfo("Port를 연결합니다", combobox_Baudrate.get() + "와 연결을 시도합니다")
            # s = serial.Serial(str(combobox_Baudrate.get()), 38400)

        btnOpen = tkinter.Button(window, text="OPEN", command=Portopen)
        frame = tkinter.Frame(window)
        listbox = tkinter.Listbox(frame)
        for line in range(1, 10):
            listbox.insert(line, " ")

        frame2 = tkinter.Frame(window)
        self.listbox2 = tkinter.Listbox(frame2)
        for line in range(1, 20):
            self.listbox2.insert(line, "")

        txtsendcommand = tkinter.Text(window, width=41, height=1, autoseparators=True)

        btnMotionparameter.place(x=950, y=50, width=200, height=30)

        lbl_1.place(x=960, y=110)
        lbl_2.place(x=960, y=150)
        lbl_3.place(x=1000, y=85)
        lbl_4.place(x=1080, y=85)
        txtRVvalue.place(x=1000, y=110)
        txtRVsteps.place(x=1080, y=110)
        txtRRvalue.place(x=1000, y=150)
        txtRRsteps.place(x=1080, y=150)
        btnMove.place(x=1000, y=220)
        btnStop.place(x=1080, y=220)
        lbl_5.place(x=1200, y=20)
        radio_Brate38400.place(x=1200, y=40)
        radio_Brate115200.place(x=1280, y=40)
        lbl_6.place(x=1190, y=70)
        combobox_Baudrate.place(x=1250, y=70)
        combobox_Baudrate.set("COM3")
        btnOpen.place(x=1330, y=70)
        listbox.pack()
        frame.place(x=1180, y=100)
        self.listbox2.pack()
        frame2.place(x=1330, y=100)
        txtsendcommand.place(x=1180, y=265)

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

    def sendCommandtoDSP(self, string):
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

        #-----------------------------------------------------------------------------------------------------------------------------------------------------------





    def snapshot(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()

         if ret:
             cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
         #self.Outframe
         if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            self.imgproc(frame)
            self.Outframe = cv2.cvtColor(self.Outframe, cv2.COLOR_HSV2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.Outframe))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

         self.window.after(self.delay, self.update)
    def imgproc(self, frame):
        #create Red image
        if self.Red.H_min > self.Red.H_max:
            lower_H = cv2.inRange(frame, (0, self.Red.S_min, self.Red.V_min), (self.Red.H_max, self.Red.S_max, self.Red.V_max))
            upper_H = cv2.inRange(frame, (self.Red.H_min, self.Red.S_min, self.Red.V_min), (180, self.Red.S_max, self.Red.V_max))
            added_H = cv2.addWeighted(lower_H, 1.0, upper_H, 1.0, 0.0)
            self.frame_Red = cv2.bitwise_and(frame, frame, mask=added_H)
        else:
            h = cv2.inRange(frame, (self.Red.H_min, self.Red.S_min, self.Red.V_min), (self.Red.H_max, self.Red.S_max, self.Red.V_max))
            self.frame_Red = cv2.bitwise_and(frame, frame, mask=h)
        # create Green image
        if self.Green.H_min > self.Green.H_max:
            lower_H = cv2.inRange(frame, (0, self.Green.S_min, self.Green.V_min), (self.Green.H_max, self.Green.S_max, self.Green.V_max))
            upper_H = cv2.inRange(frame, (self.Green.H_min, self.Green.S_min, self.Green.V_min), (180, self.Green.S_max, self.Green.V_max))
            added_H = cv2.addWeighted(lower_H, 1.0, upper_H, 1.0, 0.0)
            self.frame_Green = cv2.bitwise_and(frame, frame, mask=added_H)
        else:
            h = cv2.inRange(frame, (self.Green.H_min, self.Green.S_min, self.Green.V_min), (self.Green.H_max, self.Green.S_max, self.Green.V_max))
            self.frame_Green = cv2.bitwise_and(frame, frame, mask=h)
        # create Blue image
        if self.Blue.H_min > self.Blue.H_max:
            lower_H = cv2.inRange(frame, (0, self.Blue.S_min, self.Blue.V_min), (self.Blue.H_max, self.Blue.S_max, self.Blue.V_max))
            upper_H = cv2.inRange(frame, (self.Blue.H_min, self.Blue.S_min, self.Blue.V_min), (180, self.Blue.S_max, self.Blue.V_max))
            added_H = cv2.addWeighted(lower_H, 1.0, upper_H, 1.0, 0.0)
            self.frame_Blue = cv2.bitwise_and(frame, frame, mask=added_H)
        else:
            h = cv2.inRange(frame, (self.Blue.H_min, self.Blue.S_min, self.Blue.V_min), (self.Blue.H_max, self.Blue.S_max, self.Blue.V_max))
            self.frame_Blue = cv2.bitwise_and(frame, frame, mask=h)

        self.labeling()

        if self.RadioFlag == 1:
            self.Outframe = self.frame_Red

        elif self.RadioFlag == 2:
            self.Outframe = self.frame_Green

        elif self.RadioFlag == 3:
            self.Outframe = self.frame_Blue

        else:
            self.Outframe = frame
        cv2.rectangle(self.Outframe, (self.Red.max_x, self.Red.max_y), (self.Red.max_x + self.Red.max_width, self.Red.max_y + self.Red.max_height), (80, 180, 200), 5, cv2.LINE_8)
        cv2.rectangle(self.Outframe, (self.Green.max_x, self.Green.max_y), (self.Green.max_x + self.Green.max_width, self.Green.max_y + self.Green.max_height), (0, 150, 200), 5, cv2.LINE_8)
        cv2.rectangle(self.Outframe, (self.Blue.max_x, self.Blue.max_y), (self.Blue.max_x + self.Blue.max_width, self.Blue.max_y + self.Blue.max_height), (255, 255, 255), 5, cv2.LINE_8)
    def labeling(self):
        kernel = np.ones((5,5), np.uint8)
        self.frame_Red = cv2.morphologyEx(self.frame_Red, cv2.MORPH_OPEN, kernel)
        self.frame_Green = cv2.morphologyEx(self.frame_Green, cv2.MORPH_OPEN, kernel)
        self.frame_Blue = cv2.morphologyEx(self.frame_Blue, cv2.MORPH_OPEN, kernel)

        frame_Red_lab = cv2.cvtColor(self.frame_Red, cv2.COLOR_RGB2GRAY)
        _, th_Red = cv2.threshold(frame_Red_lab, 1, 255, cv2.THRESH_BINARY)
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(th_Red, connectivity=8)

        self.Red.max_x = 0
        self.Red.max_y = 0
        self.Red.max_width = 0
        self.Red.max_height = 0
        self.Red.max_area = 0
        self.Green.max_x = 0
        self.Green.max_y = 0
        self.Green.max_width = 0
        self.Green.max_height = 0
        self.Green.max_area = 0
        self.Blue.max_x = 0
        self.Blue.max_y = 0
        self.Blue.max_width = 0
        self.Blue.max_height = 0
        self.Blue.max_area = 0

        for i in range(retval):
            if stats[i, 4] < 30000 and stats[i, 4] > self.Red.max_area:
                self.Red.max_x = stats[i, 0]
                self.Red.max_y = stats[i, 1]
                self.Red.max_width = stats[i, 2]
                self.Red.max_height = stats[i, 3]
                self.Red.max_area = stats[i, 4]

        frame_Green_lab = cv2.cvtColor(self.frame_Green, cv2.COLOR_RGB2GRAY)
        _, th_Green = cv2.threshold(frame_Green_lab, 1, 255, cv2.THRESH_BINARY)
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(th_Green, connectivity=8)

        for i in range(retval):
            if stats[i, 4] < 30000 and stats[i, 4] > self.Green.max_area:
                self.Green.max_x = stats[i, 0]
                self.Green.max_y = stats[i, 1]
                self.Green.max_width = stats[i, 2]
                self.Green.max_height = stats[i, 3]
                self.Green.max_area = stats[i, 4]

        frame_Blue_lab = cv2.cvtColor(self.frame_Blue, cv2.COLOR_RGB2GRAY)
        _, th_Blue = cv2.threshold(frame_Blue_lab, 1, 255, cv2.THRESH_BINARY)
        retval, labels, stats, centroids = cv2.connectedComponentsWithStats(th_Blue, connectivity=8)

        for i in range(retval):
            if stats[i, 4] < 30000 and stats[i, 4] > self.Blue.max_area:
                self.Blue.max_x = stats[i, 0]
                self.Blue.max_y = stats[i, 1]
                self.Blue.max_width = stats[i, 2]
                self.Blue.max_height = stats[i, 3]
                self.Blue.max_area = stats[i, 4]


    def ShowColormap(self):
        colormap = cv2.imread("colormap.jpg", cv2.IMREAD_ANYCOLOR)
        #ori_colormap = cv2.imread("colormap.jpg", cv2.IMREAD_ANYCOLOR)

        cv2.line(colormap, (150, 150), (int(150 + 145 * math.cos(math.radians(90 - self.Red.H_min * 2))), int(150 - 145 * math.sin(math.radians(90 - self.Red.H_min * 2)))), (0, 0, 0), 3, cv2.LINE_AA)
        cv2.line(colormap, (150, 150), (int(150 + 145 * math.cos(math.radians(90 - self.Red.H_max * 2))), int(150 - 145 * math.sin(math.radians(90 - self.Red.H_max * 2)))), (0, 0, 0), 3, cv2.LINE_AA)
        cv2.line(colormap, (150, 150), (int(150 + 145 * math.cos(math.radians(90 - self.Green.H_min * 2))), int(150 - 145 * math.sin(math.radians(90 - self.Green.H_min * 2)))), (0, 0, 0), 3, cv2.LINE_AA)
        cv2.line(colormap, (150, 150), (int(150 + 145 * math.cos(math.radians(90 - self.Green.H_max * 2))), int(150 - 145 * math.sin(math.radians(90 - self.Green.H_max * 2)))), (0, 0, 0), 3, cv2.LINE_AA)
        cv2.line(colormap, (150, 150), (int(150 + 145 * math.cos(math.radians(90 - self.Blue.H_min * 2))), int(150 - 145 * math.sin(math.radians(90 - self.Blue.H_min * 2)))), (0, 0, 0), 3, cv2.LINE_AA)
        cv2.line(colormap, (150, 150), (int(150 + 145 * math.cos(math.radians(90 - self.Blue.H_max * 2))), int(150 - 145 * math.sin(math.radians(90 - self.Blue.H_max * 2)))), (0, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow("Colormap", colormap)

    def saveParameter(self):
        file = open('./HSV_parameters.txt', 'w')
        file.write("HSV_parameters\n============================\n")
        file.write("Red H_min : %d \t Red H_max : %d\n"%(self.Red.H_min, self.Red.H_max))
        file.write("Red S_min : %d \t Red S_max : %d\n"%(self.Red.S_min, self.Red.S_max))
        file.write("Red V_min : %d \t Red V_max : %d\n"%(self.Red.V_min, self.Red.V_max))
        file.write("============================\n")
        file.write("Green H_min : %d \t Green H_max : %d\n"%(self.Green.H_min, self.Green.H_max))
        file.write("Green S_min : %d \t Green S_max : %d\n"%(self.Green.S_min, self.Green.S_max))
        file.write("Green V_min : %d \t Green V_max : %d\n"%(self.Green.V_min, self.Green.V_max))
        file.write("============================\n")
        file.write("Blue H_min : %d \t Blue H_max : %d\n"%(self.Blue.H_min, self.Blue.H_max))
        file.write("Blue S_min : %d \t Blue S_max : %d\n"%(self.Blue.S_min, self.Blue.S_max))
        file.write("Blue V_min : %d \t Blue V_max : %d\n"%(self.Blue.V_min, self.Blue.V_max))
        file.write("============================\n")
        file.close()
    def loadParameter(self):
        self.HSVdatafile()

        if self.var.get() == 1:
            self.thisColor = self.Red
        elif self.var.get() == 2:
            self.thisColor = self.Green
        elif self.var.get() == 3:
            self.thisColor = self.Blue
        else:
            return

        self.Scroll_H_min.set(self.thisColor.H_min)
        self.Scroll_H_max.set(self.thisColor.H_max)
        self.Scroll_S_min.set(self.thisColor.S_min)
        self.Scroll_S_max.set(self.thisColor.S_max)
        self.Scroll_V_min.set(self.thisColor.V_min)
        self.Scroll_V_max.set(self.thisColor.V_max)
        value1 = "H_min :" + str(self.thisColor.H_min)
        self.L1.config(text=value1)
        value2 = "H_max :" + str(self.thisColor.H_max)
        self.L2.config(text=value2)
        value3 = "S_min :" + str(self.thisColor.S_min)
        self.L3.config(text=value3)
        value4 = "S_max :" + str(self.thisColor.S_max)
        self.L4.config(text=value4)
        value5 = "V_min :" + str(self.thisColor.V_min)
        self.L5.config(text=value5)
        value6 = "V_max :" + str(self.thisColor.V_max)
        self.L6.config(text=value6)

class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

     def get_frame(self):

         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:

                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                 # Return a boolean success flag and the current frame converted to BGR
             else:
                 return (ret, None)
         else:
             return (ret, None)

     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

 # Create a window and pass it to the Application object
# App(tkinter.Tk(), "Tkinter and OpenCV")
app = App(tkinter.Tk(),"Tkinter and OpenCV")
app.mainloop()