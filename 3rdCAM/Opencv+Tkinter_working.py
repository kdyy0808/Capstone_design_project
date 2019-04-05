import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
    btnGrayFlag=0
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.grid(columnspan=30,rowspan=20)

        self.btn_dd = tkinter.Button(window, text="dd", width=10, command=self.ActiveRGB2GRAY)
        #self.btn_dd.pack(anchor='e', expand=True)
        self.btn_dd.grid(column=31,row=0)
        '''
        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=10, command=self.snapshot)
        #self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        self.btn_snapshot.grid(column=21,row=1)
        '''
        #Button that make the screen grayscale

        self.btn_GRAYSCALE = tkinter.Button(window, text="GrayScale", width=10, command=self.ActiveRGB2GRAY)
        self.btn_GRAYSCALE.grid(column=31, row=1)
        '''
        self.L1 = tkinter.Label(window)
        self.L1.grid(column=31, row=3)
        '''
        self.Scroll_H_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL, command=self.show_values)
        self.Scroll_H_min.set(0)
        self.Scroll_H_min.grid(column=31, row=2)
        self.Scroll_H_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL, command=self.show_values)
        self.Scroll_H_max.set(255)
        self.Scroll_H_max.grid(column=31, row=3)
        self.Scroll_S_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL, command=self.show_values)
        self.Scroll_S_min.set(0)
        self.Scroll_S_min.grid(column=31, row=4)
        self.Scroll_S_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL, command=self.show_values)
        self.Scroll_S_max.set(255)
        self.Scroll_S_max.grid(column=31, row=5)
        self.Scroll_V_min = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL, command=self.show_values)
        self.Scroll_V_min.set(0)
        self.Scroll_V_min.grid(column=31, row=6)
        self.Scroll_V_max = tkinter.Scale(window, from_=0, to=255, orient=tkinter.HORIZONTAL, command=self.show_values)
        self.Scroll_V_max.set(255)
        self.Scroll_V_max.grid(column=31, row=7)

         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

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
    def show_values(self):
        value = "값 :" + str(self.Scroll_H.get())
        self.L1.config(text=value)

        #self.L1.config(font= 'Consolas 15 bold' , text="sum is :"+ str(self.Scroll_H.get()))
        #self.L1.config




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
