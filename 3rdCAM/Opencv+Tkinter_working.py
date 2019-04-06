import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    btnGrayFlag=0

    #Scroll_H_max=0
    #Scroll_S_min=0
    #Scroll_S_max = 0
    #Scroll_V_min = 0
    #Scroll_V_max = 0

    def __init__(self, window, window_title, video_source=0):
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

        self.RadioVariety_Red = tkinter.IntVar()
        self.RadioVariety_Blue = tkinter.IntVar()

        self.Rbtn_Color_Red = tkinter.Radiobutton(window, text='Red', variable=self.RadioVariety_Red)
        self.Rbtn_Color_Red.grid(column=31,row=11)
        #self.Rbtn_Color_Blue = tkinter.Radiobutton(window, text='Blue', variable=self.RadioVariety_Red )
        #self.Rbtn_Color_Blue.grid(column=32, row=11)

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
            value1 = "H_min :" + str(self.Scroll_H_min.get())
            self.L1.config(text=value1)
            value2 = "H_max :" + str(self.Scroll_H_max.get())
            self.L2.config(text=value2)
            value3 = "S_min :" + str(self.Scroll_S_min.get())
            self.L3.config(text=value3)
            value4 = "S_max :" + str(self.Scroll_S_max.get())
            self.L4.config(text=value4)
            value5 = "V_min :" + str(self.Scroll_V_min.get())
            self.L5.config(text=value5)
            value6 = "V_max :" + str(self.Scroll_V_max.get())
            self.L6.config(text=value6)



        self.Scroll_H_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_H_min.set(0)
        self.Scroll_H_min.grid(column=31, row=2)
        self.Scroll_H_min.bind("<ButtonRelease-1>", show_values)

        self.Scroll_H_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL)
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
