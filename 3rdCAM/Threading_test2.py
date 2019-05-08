import tkinter
import time
import threading
import queue
import random




# import tkinter.ttk
from Serial_communicationSend import *

receivedCount=0

class Mailbox(threading.Thread):

    def __init__(self,q):
        threading.Thread.__init__(self)
        self.q =q
        self.num = 0

    def run(self):
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

        self.t_label = tkinter.IntVar(self, 0)
        self.label = tkinter.Label(self, textvariable=self.t_label)
        self.label.pack()
        self.button = tkinter.Button(self, text="start", command=self.start_timer)
        self.button.pack()
        self.mailbox=[0]
        self.q = queue.Queue(10)

        self.frame2 = tkinter.Frame(self)
        self.listbox2 = tkinter.Listbox(self.frame2)
        for line in range(1, 20):
            self.listbox2.insert(line, str(line) + "/20")
        self.listbox2.pack()
        self.frame2.pack()

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
            self.after(5, self.check_Mailbox)

root = MyAPP()
root.start_timer()
root.mainloop()












