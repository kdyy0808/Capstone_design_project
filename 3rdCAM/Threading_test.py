# import tkinter
# import time
# import threading
# import queue
# import random
#
# class Mailbox(threading.Thread):
#     def __init__(self, q):
#         threading.Thread.__init__(self)
#         self.q =q
#         self.num = 0
#
#     def run(self):
#         while True:
#             time.sleep(1)
#             if random.randint(1, 5) == 2:
#                 self.num = random.randint(1, 100)
#                 self.q.put(self.num)
#
# class MyAPP(tkinter.Tk):
#     def __init__(self):
#         tkinter.Tk.__init__(self)
#         self.t_label = tkinter.IntVar(self, 0)
#         self.label = tkinter.Label(self, textvariable=self.t_label)
#         self.label.pack()
#         self.button = tkinter.Button(self, text="start", command=self.start_timer)
#         self.button.pack()
#         self.mailbox=[]
#         self.q = queue.Queue(10)
#
#     def start_timer(self):
#         Mailbox(self.q).start()
#         self.after(0, self.check_Mailbox)
#
#     def check_Mailbox(self):
#         try:
#             for mail in range(0,10):
#                 n = self.q.get(0)
#                 self.mailbox.append(n)
#                 self.t_label.set(self.mailbox)
#         except queue.Empty:
#             pass
#         finally:
#             self.after(3000, self.check_Mailbox)
# root = MyAPP()
# root.mainloop()

import serial

ser = serial.Serial('COM8', 9600)
print('port opened')
while ser.isOpen():
    try:
        sdata= input('Type a word & Enter:')
        sdata+='\n'
        ser.write(sdata.encode('ASCII'))
        buff=byte=b'0'
        while byte != b'\n':
            byte=ser.read(1)
            if byte not in [b'\r', b'\n']:
                buff+=byte
        print(buff.decaode('ASCII'))
    except:
        ser.close()
        pass