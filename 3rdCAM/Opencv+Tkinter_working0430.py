import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class Color_catagory:
    def __init__(self):
        self.H_min = 0
        self.H_max = 180
        self.S_min = 0
        self.S_max = 255
        self.V_min = 0
        self.V_max = 255

class App(Color_catagory):
    btnGrayFlag=0
    RadioFlag =0

    def __init__(self, window, window_title, video_source=0):
        self.Red = Color_catagory()
        self.Green = Color_catagory()
        self.Blue = Color_catagory()

        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.Scroll_H_min = tkinter.Scale()
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        # Create a canvas that can fit the above video source size

        self.screen_init(self.window)
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def screen_init(self,window):
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(columnspan=30, rowspan=20)
        self.btn_dd = tkinter.Button(window, text="dd", width=10, command=self.ActiveRGB2GRAY)
        # self.btn_dd.pack(anchor='e', expand=True)
        self.btn_GRAYSCALE = tkinter.Button(window, text="GrayScale", width=10, command=self.ActiveRGB2GRAY)
        self.btn_GRAYSCALE.grid(column=31, row=1)
        self.btn_dd.grid(column=31, row=0)

        #def check():
        def radio_control_R():
            #self.RadioVariety_Red.get() == 1:
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
            #self.RadioVariety_Green.get() == 1:
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
            #self.RadioVariety_Blue.get() == 1:
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
        self.Rbtn_Color_Red.grid(column=31,row=11)
        self.Rbtn_Color_Green = tkinter.Radiobutton(window, text='Green',value = 2, variable=self.var, command=radio_control_G)
        self.Rbtn_Color_Green.grid(column=32, row=11)
        self.Rbtn_Color_Blue = tkinter.Radiobutton(window, text='Blue', value=3, variable=self.var, command=radio_control_B)
        self.Rbtn_Color_Blue.grid(column=33, row=11)

        self.Rbtn_Color_All = tkinter.Radiobutton(window, text='All', value=4, variable=self.var,command=radio_control_All)
        self.Rbtn_Color_All.grid(column=31, row=12)

        self.L1 = tkinter.Label(window,text="H_min: ", width=10, height=2, fg="red", relief="solid")
        self.L1.grid(column=31, row=8)
        self.L2 = tkinter.Label(window, text="H_max: ", width=10, height=2, fg="red", relief="solid")
        self.L2.grid(column=32, row=8)
        self.L3 = tkinter.Label(window, text="S_min: ", width=10, height=2, fg="red", relief="solid")
        self.L3.grid(column=31, row=9)
        self.L4 = tkinter.Label(window, text="S_max: ", width=10, height=2, fg="red", relief="solid")
        self.L4.grid(column=32, row=9)
        self.L5 = tkinter.Label(window, text="V_min: ", width=10, height=2, fg="red", relief="solid")
        self.L5.grid(column=31, row=10)
        self.L6 = tkinter.Label(window, text="V_max: ", width=10, height=2, fg="red", relief="solid")
        self.L6.grid(column=32, row=10)


        def show_values(event):

            if self.var.get() ==1:
                self.thisColor = self.Red
            elif self.var.get() ==2:
                self.thisColor = self.Green
            else: #self.var.get() ==3:
                self.thisColor = self.Blue

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
        self.Scroll_H_min.grid(column=31, row=2)
        self.Scroll_H_min.bind("<ButtonRelease-1>", show_values)

        self.Scroll_H_max = tkinter.Scale(window, from_=0, to=180, orient=tkinter.HORIZONTAL)
        self.Scroll_H_max.set(255)
        self.Scroll_H_max.grid(column=31, row=3)
        self.Scroll_H_max.bind("<ButtonRelease-1>", show_values)
        self.Scroll_S_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_S_min.set(0)
        self.Scroll_S_min.grid(column=31, row=4)
        self.Scroll_S_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_S_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_S_max.set(255)
        self.Scroll_S_max.grid(column=31, row=5)
        self.Scroll_S_max.bind("<ButtonRelease-1>", show_values)
        self.Scroll_V_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_V_min.set(0)
        self.Scroll_V_min.grid(column=31, row=6)
        self.Scroll_V_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_V_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_V_max.set(255)
        self.Scroll_V_max.grid(column=31, row=7)
        self.Scroll_V_max.bind("<ButtonRelease-1>", show_values)

            # self.L1.config(font= 'Consolas 15 bold' , text="sum is :"+ str(self.Scroll_H.get()))
            # self.L1.config


    def snapshot(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()

         if ret:
             cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()

         if ret:
            if self.btnGrayFlag==1:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if self.RadioFlag==1:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h = cv2.inRange(frame, (self.Red.H_min, self.Red.S_min, self.Red.V_min), (self.Red.H_max, self.Red.S_max, self.Red.V_max))
                frame = cv2.bitwise_and(frame, frame, mask = h)
                frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            elif self.RadioFlag==2:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h = cv2.inRange(frame, (self.Green.H_min, self.Green.S_min, self.Green.V_min), (self.Green.H_max, self.Green.S_max, self.Green.V_max))
                frame = cv2.bitwise_and(frame, frame, mask = h)
                frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
            elif self.RadioFlag==3:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                h = cv2.inRange(frame, (self.Blue.H_min, self.Blue.S_min, self.Blue.V_min), (self.Blue.H_max, self.Blue.S_max, self.Blue.V_max))
                frame = cv2.bitwise_and(frame, frame, mask = h)
                frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

         self.window.after(self.delay, self.update)
    def ActiveRGB2GRAY(self):
        ret, frame = self.vid.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.btnGrayFlag==0:
            self.btnGrayFlag=1
        else:
            self.btnGrayFlag=0

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
App(tkinter.Tk(), "Tkinter and OpenCV")
