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
import re
import random


s = serial.Serial('COM3', 38400)
command_count = 0
receivedCount = 0
receiving_Data=list()
semicolonFlag = False
btext = ""

RP0 = 160
RP1 = 130
RP2 = 40
RP3 = 58
RP4 = 800
RP5 = 40
RP6 = 20
RP7 = 60
RP8 = 30
RP9 = 30
RPA = 30
RPB = 200
RPC = 0
RPD = 300
RPE = 700
RPF = 0
RPG = 0
RP_sign_type = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
RP_ischanged = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
RP_mapping_min = [120,  80,     30,     40,     100,    0,  -10,    0,      0,      0,          -10,        0,      0,      150,      100,      0,      0]
RP_mapping_max = [230,  200,    70,     150,    4000,   60,  40,    1000,   300,    100,        50,         400,    50,     500,      1500,    200,    500]

RP_Rand_checked = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
                print(text)
                text=text.decode()
                btext += text
                if text.find(';') != -1:
                    if btext == "":
                        btext = text
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

class RPwindow(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("RP_Parameter")
        self.geometry("1100x400+100+100")
        self.btnRpload = tkinter.Button(self, text="RP Load", width=10, command=self.LoadRP_parameter)
        self.btnRpload.place(x=50, y=370)
        self.btnRpapply = tkinter.Button(self, text="RP apply", width=10, command=self.ApllyRP_parameter)
        self.btnRpapply.place(x=150, y=370)
        self.btnRpsave = tkinter.Button(self, text="RP Save", width=10, command=self.SaveRP_parameter)
        self.btnRpsave.place(x=250, y=370)
        self.btnRpmode = tkinter.Button(self, text="RP Mode", width=10)
        self.btnRpmode.place(x=350, y=370)
        self.LRP0 = tkinter.Label(self, text="RP0", width=4, height=1)
        self.LRP1 = tkinter.Label(self, text="RP1", width=4, height=1)
        self.LRP2 = tkinter.Label(self, text="RP2", width=4, height=1)
        self.LRP3 = tkinter.Label(self, text="RP3", width=4, height=1)
        self.LRP4 = tkinter.Label(self, text="RP4", width=4, height=1)
        self.LRP5 = tkinter.Label(self, text="RP5", width=4, height=1)
        self.LRP6 = tkinter.Label(self, text="RP6", width=4, height=1)
        self.LRP7 = tkinter.Label(self, text="RP7", width=4, height=1)
        self.LRP8 = tkinter.Label(self, text="RP8", width=4, height=1)
        self.LRP9 = tkinter.Label(self, text="RP9", width=4, height=1)
        self.LRPA = tkinter.Label(self, text="RPA", width=4, height=1)
        self.LRPB = tkinter.Label(self, text="RPB", width=4, height=1)
        self.LRPC = tkinter.Label(self, text="RPC", width=4, height=1)
        self.LRPD = tkinter.Label(self, text="RPD", width=4, height=1)
        self.LRPE = tkinter.Label(self, text="RPE", width=4, height=1)
        self.LRPF = tkinter.Label(self, text="RPF", width=4, height=1)
        self.LRPG = tkinter.Label(self, text="RPG", width=4, height=1)

        self.LRP0.place(x=13, y=17)
        self.LRP1.place(x=13, y=37)
        self.LRP2.place(x=13, y=57)
        self.LRP3.place(x=13, y=77)
        self.LRP4.place(x=13, y=97)
        self.LRP5.place(x=13, y=117)
        self.LRP6.place(x=13, y=137)
        self.LRP7.place(x=13, y=157)
        self.LRP8.place(x=13, y=177)
        self.LRP9.place(x=13, y=197)
        self.LRPA.place(x=13, y=217)
        self.LRPB.place(x=13, y=237)
        self.LRPC.place(x=13, y=257)
        self.LRPD.place(x=13, y=277)
        self.LRPE.place(x=13, y=297)
        self.LRPF.place(x=13, y=317)
        self.LRPG.place(x=13, y=337)

        self.LRP0s = tkinter.Label(self, text="한걸음 걷는데 걸리는 시간[0.001 sec] 기본값 200" , height=1)
        self.LRP1s = tkinter.Label(self, text="걸을때 한 걸음의 기간에 대하여 두발을 모두 땅에 닿고 있는 기간의 비율[0.1%%] 기본값 400", height=1)
        self.LRP2s = tkinter.Label(self, text="몸중심에서 고관절까지의 거리 (양다리중심 사이의 거리/2)", height=1)
        self.LRP3s = tkinter.Label(self, text="다리를 들기 위하여 사용하는 고관절 회전각", height=1)
        self.LRP4s = tkinter.Label(self, text="보폭에 따라서 팔을 앞뒤로 움직이는 양의 보폭을 만드는 고관절각에 대한 비율", height=1)
        self.LRP5s = tkinter.Label(self, text="다리를 들었을때 몸체가 처지지 않도록 땅에 위치한 다리의 고관절을 드는 각도", height=1)
        self.LRP6s = tkinter.Label(self, text="다리를 들었을때 공중에 든 다리의 고관절을 드는 각도", height=1)
        self.LRP7s = tkinter.Label(self, text="걸을때 다리를 앞으로 스윙하는 각도에 대한 다리를 뒤로 스윙하는 각도의 비율", height=1)
        self.LRP8s = tkinter.Label(self, text="다리를 들기 직전에 땅을 치는 기간(180도가 한걸음에 해당하는 기간임)", height=1)
        self.LRP9s = tkinter.Label(self, text="땅을 치는데 사용하는 0.01Sec 당 다리길이 늘이기의 크기", height=1)
        self.LRPAs = tkinter.Label(self, text="땅을 치는데 사용하는 0.01Sec 당 발목관절 회전각 크기",  height=1)
        self.LRPBs = tkinter.Label(self, text="전진 보행속도가 빠를수록 무게중심을 앞으로 옮기는 양의 보행속도(RV 명령어로 설정)에 대한 비율, 후진의 경우 전진의 반",  height=1)
        self.LRPCs = tkinter.Label(self, text="후진보행을 할때 무게중심을 앞으로 일정량 옮기는 거리",  height=1)
        self.LRPDs = tkinter.Label(self, text="회전보행을 할때 들었던 발을 약간 몸 뒤쪽으로 놓기 위한 다리이동량으로서 걸음당 회전각(RR명령어로설정)에 대한 비율",  height=1)
        self.LRPEs = tkinter.Label(self, text="회전보행을 할 때 회전을 원할하게 하기 위하여 팔을 앞뒤로 흔드는데, 팔을 앞뒤로 흔드는 각의 걸음당 회전각(RR명령어로 설정)에대한 비율",  height=1)
        self.LRPFs = tkinter.Label(self, text="측면보행을 할 때 뻗는 다리의 발바닥을 바깥쪽으로 약간 들기 위한 각의 측면 이동을 위한 다리roll 각에 대한 비율",  height=1)
        self.LRPGs = tkinter.Label(self, text="측면 보행을 할때 뻗는 다리의 발바닥을 바깥쪽으로 약간 드는데, 착지후에 원위치로 오게 하는 비율임",  height=1)
        self.LRP0s.place(x=160, y=17)
        self.LRP1s.place(x=160, y=37)
        self.LRP2s.place(x=160, y=57)
        self.LRP3s.place(x=160, y=77)
        self.LRP4s.place(x=160, y=97)
        self.LRP5s.place(x=160, y=117)
        self.LRP6s.place(x=160, y=137)
        self.LRP7s.place(x=160, y=157)
        self.LRP8s.place(x=160, y=177)
        self.LRP9s.place(x=160, y=197)
        self.LRPAs.place(x=160, y=217)
        self.LRPBs.place(x=160, y=237)
        self.LRPCs.place(x=160, y=257)
        self.LRPDs.place(x=160, y=277)
        self.LRPEs.place(x=160, y=297)
        self.LRPFs.place(x=160, y=317)
        self.LRPGs.place(x=160, y=337)

        self.txtRP0value = tkinter.Text(self, width=4, height=1)
        self.txtRP1value = tkinter.Text(self, width=4, height=1)
        self.txtRP2value = tkinter.Text(self, width=4, height=1)
        self.txtRP3value = tkinter.Text(self, width=4, height=1)
        self.txtRP4value = tkinter.Text(self, width=4, height=1)
        self.txtRP5value = tkinter.Text(self, width=4, height=1)
        self.txtRP6value = tkinter.Text(self, width=4, height=1)
        self.txtRP7value = tkinter.Text(self, width=4, height=1)
        self.txtRP8value = tkinter.Text(self, width=4, height=1)
        self.txtRP9value = tkinter.Text(self, width=4, height=1)
        self.txtRPAvalue = tkinter.Text(self, width=4, height=1)
        self.txtRPBvalue = tkinter.Text(self, width=4, height=1)
        self.txtRPCvalue = tkinter.Text(self, width=4, height=1)
        self.txtRPDvalue = tkinter.Text(self, width=4, height=1)
        self.txtRPEvalue = tkinter.Text(self, width=4, height=1)
        self.txtRPFvalue = tkinter.Text(self, width=4, height=1)
        self.txtRPGvalue = tkinter.Text(self, width=4, height=1)

        self.txtRP0value.insert(0.0, str(RP0))
        self.txtRP1value.insert(0.0, str(RP1))
        self.txtRP2value.insert(0.0, str(RP2))
        self.txtRP3value.insert(0.0, str(RP3))
        self.txtRP4value.insert(0.0, str(RP4))
        self.txtRP5value.insert(0.0, str(RP5))
        self.txtRP6value.insert(0.0, str(RP6))
        self.txtRP7value.insert(0.0, str(RP7))
        self.txtRP8value.insert(0.0, str(RP8))
        self.txtRP9value.insert(0.0, str(RP9))
        self.txtRPAvalue.insert(0.0, str(RPA))
        self.txtRPBvalue.insert(0.0, str(RPB))
        self.txtRPCvalue.insert(0.0, str(RPC))
        self.txtRPDvalue.insert(0.0, str(RPD))
        self.txtRPEvalue.insert(0.0, str(RPE))
        self.txtRPFvalue.insert(0.0, str(RPF))
        self.txtRPGvalue.insert(0.0, str(RPG))

        self.txtRP0value.place(x=50, y=20)
        self.txtRP1value.place(x=50, y=40)
        self.txtRP2value.place(x=50, y=60)
        self.txtRP3value.place(x=50, y=80)
        self.txtRP4value.place(x=50, y=100)
        self.txtRP5value.place(x=50, y=120)
        self.txtRP6value.place(x=50, y=140)
        self.txtRP7value.place(x=50, y=160)
        self.txtRP8value.place(x=50, y=180)
        self.txtRP9value.place(x=50, y=200)
        self.txtRPAvalue.place(x=50, y=220)
        self.txtRPBvalue.place(x=50, y=240)
        self.txtRPCvalue.place(x=50, y=260)
        self.txtRPDvalue.place(x=50, y=280)
        self.txtRPEvalue.place(x=50, y=300)
        self.txtRPFvalue.place(x=50, y=320)
        self.txtRPGvalue.place(x=50, y=340)

        def checked():
            for i in range(0,17):
                global RP_Rand_checked
                if i==0:
                    RP_Rand_checked[i] = CheckVariety_0.get()
                elif i==1:
                    RP_Rand_checked[i] = CheckVariety_1.get()
                elif i==2:
                    RP_Rand_checked[i] = CheckVariety_2.get()
                elif i==3:
                    RP_Rand_checked[i] = CheckVariety_3.get()
                elif i==4:
                    RP_Rand_checked[i] = CheckVariety_4.get()
                elif i==5:
                    RP_Rand_checked[i] = CheckVariety_5.get()
                elif i==6:
                    RP_Rand_checked[i] = CheckVariety_6.get()
                elif i==7:
                    RP_Rand_checked[i] = CheckVariety_7.get()
                elif i==8:
                    RP_Rand_checked[i] = CheckVariety_8.get()
                elif i==9:
                    RP_Rand_checked[i] = CheckVariety_9.get()
                elif i==10:
                    RP_Rand_checked[i] = CheckVariety_A.get()
                elif i==11:
                    RP_Rand_checked[i] = CheckVariety_B.get()
                elif i==12:
                    RP_Rand_checked[i] = CheckVariety_C.get()
                elif i==13:
                    RP_Rand_checked[i] = CheckVariety_D.get()
                elif i==14:
                    RP_Rand_checked[i] = CheckVariety_E.get()
                elif i==15:
                    RP_Rand_checked[i] = CheckVariety_F.get()
                elif i==16:
                    RP_Rand_checked[i] = CheckVariety_G.get()
                print(RP_Rand_checked[i])

        CheckVariety_0 = tkinter.IntVar()
        CheckVariety_1 = tkinter.IntVar()
        CheckVariety_2 = tkinter.IntVar()
        CheckVariety_3 = tkinter.IntVar()
        CheckVariety_4 = tkinter.IntVar()
        CheckVariety_5 = tkinter.IntVar()
        CheckVariety_6 = tkinter.IntVar()
        CheckVariety_7 = tkinter.IntVar()
        CheckVariety_8 = tkinter.IntVar()
        CheckVariety_9 = tkinter.IntVar()
        CheckVariety_A = tkinter.IntVar()
        CheckVariety_B = tkinter.IntVar()
        CheckVariety_C = tkinter.IntVar()
        CheckVariety_D = tkinter.IntVar()
        CheckVariety_E = tkinter.IntVar()
        CheckVariety_F = tkinter.IntVar()
        CheckVariety_G = tkinter.IntVar()


        self.RP0_checked = tkinter.Checkbutton(self, variable=CheckVariety_0, command=checked)
        self.RP1_checked = tkinter.Checkbutton(self, variable=CheckVariety_1, command=checked)
        self.RP2_checked = tkinter.Checkbutton(self, variable=CheckVariety_2, command=checked)
        self.RP3_checked = tkinter.Checkbutton(self, variable=CheckVariety_3, command=checked)
        self.RP4_checked = tkinter.Checkbutton(self, variable=CheckVariety_4, command=checked)
        self.RP5_checked = tkinter.Checkbutton(self, variable=CheckVariety_5, command=checked)
        self.RP6_checked = tkinter.Checkbutton(self, variable=CheckVariety_6, command=checked)
        self.RP7_checked = tkinter.Checkbutton(self, variable=CheckVariety_7, command=checked)
        self.RP8_checked = tkinter.Checkbutton(self, variable=CheckVariety_8, command=checked)
        self.RP9_checked = tkinter.Checkbutton(self, variable=CheckVariety_9, command=checked)
        self.RPA_checked = tkinter.Checkbutton(self, variable=CheckVariety_A, command=checked)
        self.RPB_checked = tkinter.Checkbutton(self, variable=CheckVariety_B, command=checked)
        self.RPC_checked = tkinter.Checkbutton(self, variable=CheckVariety_C, command=checked)
        self.RPD_checked = tkinter.Checkbutton(self, variable=CheckVariety_D, command=checked)
        self.RPE_checked = tkinter.Checkbutton(self, variable=CheckVariety_E, command=checked)
        self.RPF_checked = tkinter.Checkbutton(self, variable=CheckVariety_F, command=checked)
        self.RPG_checked = tkinter.Checkbutton(self, variable=CheckVariety_G, command=checked)


        self.RP0_checked.place(x=80, y=15)
        self.RP1_checked.place(x=80, y=35)
        self.RP2_checked.place(x=80, y=55)
        self.RP3_checked.place(x=80, y=75)
        self.RP4_checked.place(x=80, y=95)
        self.RP5_checked.place(x=80, y=115)
        self.RP6_checked.place(x=80, y=135)
        self.RP7_checked.place(x=80, y=155)
        self.RP8_checked.place(x=80, y=175)
        self.RP9_checked.place(x=80, y=195)
        self.RPA_checked.place(x=80, y=215)
        self.RPB_checked.place(x=80, y=235)
        self.RPC_checked.place(x=80, y=255)
        self.RPD_checked.place(x=80, y=275)
        self.RPE_checked.place(x=80, y=295)
        self.RPF_checked.place(x=80, y=315)
        self.RPG_checked.place(x=80, y=335)





    def renewRP_parameter(self):

        self.txtRP0value.delete(0.0, tkinter.END )
        self.txtRP1value.delete(0.0, tkinter.END )
        self.txtRP2value.delete(0.0, tkinter.END )
        self.txtRP3value.delete(0.0, tkinter.END )
        self.txtRP4value.delete(0.0, tkinter.END )
        self.txtRP5value.delete(0.0, tkinter.END )
        self.txtRP6value.delete(0.0, tkinter.END )
        self.txtRP7value.delete(0.0, tkinter.END )
        self.txtRP8value.delete(0.0, tkinter.END )
        self.txtRP9value.delete(0.0, tkinter.END )
        self.txtRPAvalue.delete(0.0, tkinter.END )
        self.txtRPBvalue.delete(0.0, tkinter.END )
        self.txtRPCvalue.delete(0.0, tkinter.END )
        self.txtRPDvalue.delete(0.0, tkinter.END )
        self.txtRPEvalue.delete(0.0, tkinter.END )
        self.txtRPFvalue.delete(0.0, tkinter.END )
        self.txtRPGvalue.delete(0.0, tkinter.END )

        self.txtRP0value.insert(0.0, str(RP0))
        self.txtRP1value.insert(0.0, str(RP1))
        self.txtRP2value.insert(0.0, str(RP2))
        self.txtRP3value.insert(0.0, str(RP3))
        self.txtRP4value.insert(0.0, str(RP4))
        self.txtRP5value.insert(0.0, str(RP5))
        self.txtRP6value.insert(0.0, str(RP6))
        self.txtRP7value.insert(0.0, str(RP7))
        self.txtRP8value.insert(0.0, str(RP8))
        self.txtRP9value.insert(0.0, str(RP9))
        self.txtRPAvalue.insert(0.0, str(RPA))
        self.txtRPBvalue.insert(0.0, str(RPB))
        self.txtRPCvalue.insert(0.0, str(RPC))
        self.txtRPDvalue.insert(0.0, str(RPD))
        self.txtRPEvalue.insert(0.0, str(RPE))
        self.txtRPFvalue.insert(0.0, str(RPF))
        self.txtRPGvalue.insert(0.0, str(RPG))
    def ApllyRP_parameter(self):
        global RP0, RP1,RP2,RP3,RP4,RP5,RP6,RP7,RP8,RP9,RPA,RPB,RPC,RPD,RPE,RPF,RPG
        RP0_list = re.findall("\d+", self.txtRP0value.get(0.0, tkinter.END))
        RP0 = int(RP0_list[0])
        RP1_list = re.findall("\d+", self.txtRP1value.get(0.0, tkinter.END))
        RP1 = int(RP1_list[0])
        RP2_list = re.findall("\d+", self.txtRP2value.get(0.0, tkinter.END))
        RP2 = int(RP2_list[0])
        RP3_list = re.findall("\d+", self.txtRP3value.get(0.0, tkinter.END))
        RP3 = int(RP3_list[0])
        RP4_list = re.findall("\d+", self.txtRP4value.get(0.0, tkinter.END))
        RP4 = int(RP4_list[0])
        RP5_list = re.findall("\d+", self.txtRP5value.get(0.0, tkinter.END))
        RP5 = int(RP5_list[0])
        RP6_list = re.findall("\d+", self.txtRP6value.get(0.0, tkinter.END))
        RP6 = int(RP6_list[0])
        RP7_list = re.findall("\d+", self.txtRP7value.get(0.0, tkinter.END))
        RP7 = int(RP7_list[0])
        RP8_list = re.findall("\d+", self.txtRP8value.get(0.0, tkinter.END))
        RP8 = int(RP8_list[0])
        RP9_list = re.findall("\d+", self.txtRP9value.get(0.0, tkinter.END))
        RP9 = int(RP9_list[0])
        RPA_list = re.findall("\d+", self.txtRPAvalue.get(0.0, tkinter.END))
        RPA = int(RPA_list[0])
        RPB_list = re.findall("\d+", self.txtRPBvalue.get(0.0, tkinter.END))
        RPB = int(RPB_list[0])
        RPC_list = re.findall("\d+", self.txtRPCvalue.get(0.0, tkinter.END))
        RPC = int(RPC_list[0])
        RPD_list = re.findall("\d+", self.txtRPDvalue.get(0.0, tkinter.END))
        RPD = int(RPD_list[0])
        RPE_list = re.findall("\d+", self.txtRPEvalue.get(0.0, tkinter.END))
        RPE = int(RPE_list[0])
        RPF_list = re.findall("\d+", self.txtRPFvalue.get(0.0, tkinter.END))
        RPF = int(RPF_list[0])
        RPG_list = re.findall("\d+", self.txtRPGvalue.get(0.0, tkinter.END))
        RPG = int(RPG_list[0])

        s.write(("RP0," + str(RP0) + ";").encode())
        time.sleep(0.020)
        s.write(("RP1," + str(RP1) + ";").encode())
        time.sleep(0.020)
        s.write(("RP2," + str(RP2) + ";").encode())
        time.sleep(0.020)
        s.write(("RP3," + str(RP3) + ";").encode())
        time.sleep(0.020)
        s.write(("RP4," + str(RP4) + ";").encode())
        time.sleep(0.020)
        s.write(("RP5," + str(RP5) + ";").encode())
        time.sleep(0.020)
        s.write(("RP6," + str(RP6) + ";").encode())
        time.sleep(0.020)
        s.write(("RP7," + str(RP7) + ";").encode())
        time.sleep(0.020)
        s.write(("RP8," + str(RP8) + ";").encode())
        time.sleep(0.020)
        s.write(("RP9," + str(RP9) + ";").encode())
        time.sleep(0.020)
        s.write(("RPA," + str(RPA) + ";").encode())
        time.sleep(0.020)
        s.write(("RPB," + str(RPB) + ";").encode())
        time.sleep(0.020)
        s.write(("RPC," + str(RPC) + ";").encode())
        time.sleep(0.020)
        s.write(("RPD," + str(RPD) + ";").encode())
        time.sleep(0.020)
        s.write(("RPE," + str(RPE) + ";").encode())
        time.sleep(0.020)
        s.write(("RPF," + str(RPF) + ";").encode())
        time.sleep(0.020)
        s.write(("RPG," + str(RPG) + ";").encode())


        # listbox.insert(30000 - command_count, str)
        # listbox.see(30000 - command_count)
        #command_count += 1
        # s.write(("RP1," + self.RP1 + ";").encode())
        # s.write(("RP2," + self.RP2 + ";").encode())
        # s.write(("RP3," + self.RP3 + ";").encode())
        # s.write(("RP4," + self.RP4 + ";").encode())
        # s.write(("RP5," + self.RP5 + ";").encode())
        # s.write(("RP6," + self.RP6 + ";").encode())
        # s.write(("RP7," + self.RP7 + ";").encode())
        # s.write(("RP8," + self.RP8 + ";").encode())
        # s.write(("RP9," + self.RP9 + ";").encode())
        # s.write(("RPA," + self.RPA + ";").encode())
        # s.write(("RPB," + self.RPB + ";").encode())
        # s.write(("RPC," + self.RPC + ";").encode())
        # s.write(("RPD," + self.RPD + ";").encode())
        # s.write(("RPE," + self.RPE + ";").encode())
        # s.write(("RPF," + self.RPF + ";").encode())
        # s.write(("RPG," + self.RPG + ";").encode())



    def SaveRP_parameter(self):

        file = open('./Motion.txt', 'w')
        file.write("/*******************************/\n	 RP PARAMETER      \n/*******************************/\n\n")
        file.write("_FastRP_\n\n")
        file.write("F_RP_val[0] " + str(RP0) + "\n")
        file.write("F_RP_val[1] " + str(RP1) + "\n")
        file.write("F_RP_val[2] " + str(RP2) + "\n")
        file.write("F_RP_val[3] " + str(RP3) + "\n")
        file.write("F_RP_val[4] " + str(RP4) + "\n")
        file.write("F_RP_val[5] " + str(RP5) + "\n")
        file.write("F_RP_val[6] " + str(RP6) + "\n")
        file.write("F_RP_val[7] " + str(RP7) + "\n")
        file.write("F_RP_val[8] " + str(RP8) + "\n")
        file.write("F_RP_val[9] " + str(RP9) + "\n")
        file.write("F_RP_val[10] " + str(RPA) + "\n")
        file.write("F_RP_val[11] " + str(RPB) + "\n")
        file.write("F_RP_val[12] " + str(RPC) + "\n")
        file.write("F_RP_val[13] " + str(RPD) + "\n")
        file.write("F_RP_val[14] " + str(RPE) + "\n")
        file.write("F_RP_val[15] " + str(RPF) + "\n")
        file.write("F_RP_val[16] " + str(RPG) + "\n")
        file.close()

    def LoadRP_parameter(self):
        rp_values = list()
        if os.path.exists('./Motion.txt'):
            file = open('./Motion.txt', 'r')
            All = file.read()
            file.close()
            words = All.split()
            for word in words:
                if word.isdigit():
                    rp_values.append(word)
        else:
            file = open('./Motion.txt', 'w')
            file.write("/*******************************/\n	 RP PARAMETER      \n/*******************************/\n\n")
            file.write("_FastRP_\n\n")
            file.write("F_RP_val[0] 200 \n")
            file.write("F_RP_val[1] 400 \n")
            file.write("F_RP_val[2] 40 \n")
            file.write("F_RP_val[3] 150 \n")
            file.write("F_RP_val[4] 1500 \n")
            file.write("F_RP_val[5] 30 \n")
            file.write("F_RP_val[6] 0 \n")
            file.write("F_RP_val[7] 400 \n")
            file.write("F_RP_val[8] 90 \n")
            file.write("F_RP_val[9] 0 \n")
            file.write("F_RP_val[10] 0 \n")
            file.write("F_RP_val[11] 500 \n")
            file.write("F_RP_val[12] 20 \n")
            file.write("F_RP_val[13] 400 \n")
            file.write("F_RP_val[14] 1000 \n")
            file.write("F_RP_val[15] 200 \n")
            file.write("F_RP_val[16] 500 \n")

            file.close()
            rp_values = [200, 400, 40, 150, 1500, 30, 0, 400, 90, 0, 0, 500, 20, 400, 1000, 200, 500]
        RP0 = int(rp_values[0])
        RP1 = int(rp_values[1])
        RP2 = int(rp_values[2])
        RP3 = int(rp_values[3])
        RP4 = int(rp_values[4])
        RP5 = int(rp_values[5])
        RP6 = int(rp_values[6])
        RP7 = int(rp_values[7])
        RP8 = int(rp_values[8])
        RP9 = int(rp_values[9])
        RPA = int(rp_values[10])
        RPB = int(rp_values[11])
        RPC = int(rp_values[12])
        RPD = int(rp_values[13])
        RPE = int(rp_values[14])
        RPF = int(rp_values[15])
        RPG = int(rp_values[16])
        self.renewRP_parameter()
        del rp_values


class App(tkinter.Tk):
    btnGrayFlag=0
    RadioFlag =0
    RP_Change_flag = True
    RP_Change_count = 10
    RP_Change_threshold_twisted_value = 5
    Outframe = None
    frame_Red = None
    frame_Green = None
    frame_Blue = None

    Run_start_x = 0
    Run_start_y = 0
    Run_start_inclination =0

    Start_Point_mid_x = 0
    Start_Point_mid_y = 0

    Run_end_x = 0
    Run_end_y = 0
    Run_end_inclination =0

    RandChoice =0
    delta_value =0
    delta_sign = 1
    Current_delta_value = 0
    prev_Penalty =0
    current_Peanalty =0
    Start_flag = False
    End_flag = True
    try_count = 0
    CenterPoints_x = list()
    CenterPoints_y = list()
    Distributions = list()
    line_end_x =0
    RP_Change_order = 0

    Penalty_Min = 10000
    Penalty_Min_RP_value = 0


    def __init__(self,video_source=0):
        tkinter.Tk.__init__(self)

        self.Red = Color_catagory()
        self.Green = Color_catagory()
        self.Blue = Color_catagory()
        self.title("Walking parameter assistance")
        self.geometry("1350x650+100+100")
        self.resizable(False, False)

        self.video_source = video_source
        self.Scroll_H_min = tkinter.Scale()
        self.vid = MyVideoCapture(self.video_source)
        self.HSVdatafile()
        self.screen_init(self)
        self.delay = 15
        self.update()

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
            hsv_values = [0, 180, 0, 255, 0, 255, 0, 180, 0, 255, 0, 255, 0, 180, 0, 255, 0, 255]
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

    def screen_init(self, window):
        self.canvas = tkinter.Canvas(self, width=480, height=640)
        # self.canvas.grid(columnspan=30, rowspan=20)
        self.canvas.place(x=0, y=0)

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
            self.RadioFlag = 1

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
            self.RadioFlag = 2

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
            self.RadioFlag = 3

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
            self.RadioFlag = 0

        self.var = tkinter.IntVar()

        self.Rbtn_Color_Red = tkinter.Radiobutton(self, text='Red', value=1, variable=self.var, command=radio_control_R)
        self.Rbtn_Color_Red.place(x=640-160, y=380)
        self.Rbtn_Color_Green = tkinter.Radiobutton(self, text='Green', value=2, variable=self.var, command=radio_control_G)
        self.Rbtn_Color_Green.place(x=695-160, y=380)
        self.Rbtn_Color_Blue = tkinter.Radiobutton(self, text='Blue', value=3, variable=self.var, command=radio_control_B)
        self.Rbtn_Color_Blue.place(x=750-160, y=380)
        self.Rbtn_Color_All = tkinter.Radiobutton(self, text='All', value=4, variable=self.var, command=radio_control_All)
        self.Rbtn_Color_All.place(x=640-160, y=400)
        self.L1 = tkinter.Label(self, text="H_min: ", width=10, height=2, fg="red", relief="solid")
        self.L1.place(x=650-160, y=250)
        self.L2 = tkinter.Label(self, text="H_max: ", width=10, height=2, fg="red", relief="solid")
        self.L2.place(x=730-160, y=250)
        self.L3 = tkinter.Label(self, text="S_min: ", width=10, height=2, fg="red", relief="solid")
        self.L3.place(x=650-160, y=290)
        self.L4 = tkinter.Label(self, text="S_max: ", width=10, height=2, fg="red", relief="solid")
        self.L4.place(x=730-160, y=290)
        self.L5 = tkinter.Label(self, text="V_min: ", width=10, height=2, fg="red", relief="solid")
        self.L5.place(x=650-160, y=330)
        self.L6 = tkinter.Label(self, text="V_max: ", width=10, height=2, fg="red", relief="solid")
        self.L6.place(x=730-160, y=330)
        self.btnColormap = tkinter.Button(self, text="Colormap", width=10, command=self.ShowColormap)
        self.btnColormap.place(x=815-160, y=254)
        self.btnload = tkinter.Button(self, text="Load", width=10, command=self.loadParameter)
        self.btnload.place(x=815-160, y=293)
        self.btnsave = tkinter.Button(self, text="Save", width=10, command=self.saveParameter)
        self.btnsave.place(x=815-160, y=333)

        def show_values(event):

            if self.var.get() == 1:
                self.thisColor = self.Red
            elif self.var.get() == 2:
                self.thisColor = self.Green
            elif self.var.get() == 3:
                self.thisColor = self.Blue
            else:
                return
            self.thisColor.H_min = self.Scroll_H_min.get()
            self.thisColor.H_max = self.Scroll_H_max.get()
            self.thisColor.S_min = self.Scroll_S_min.get()
            self.thisColor.S_max = self.Scroll_S_max.get()
            self.thisColor.V_min = self.Scroll_V_min.get()
            self.thisColor.V_max = self.Scroll_V_max.get()

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

        self.Scroll_H_min = tkinter.Scale(self, from_=0, to=180, orient=tkinter.HORIZONTAL)
        self.Scroll_H_min.set(0)
        self.Scroll_H_min.place(x=650-160, y=0)
        self.Scroll_H_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_H_max = tkinter.Scale(self, from_=0, to=180, orient=tkinter.HORIZONTAL)
        self.Scroll_H_max.set(255)
        self.Scroll_H_max.place(x=650-160, y=40)
        self.Scroll_H_max.bind("<ButtonRelease-1>", show_values)
        self.Scroll_S_min = tkinter.Scale(self, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_S_min.set(0)
        self.Scroll_S_min.place(x=650-160, y=80)
        self.Scroll_S_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_S_max = tkinter.Scale(self, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_S_max.set(255)
        self.Scroll_S_max.place(x=650-160, y=120)
        self.Scroll_S_max.bind("<ButtonRelease-1>", show_values)
        self.Scroll_V_min = tkinter.Scale(self, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_V_min.set(0)
        self.Scroll_V_min.place(x=650-160, y=160)
        self.Scroll_V_min.bind("<ButtonRelease-1>", show_values)
        self.Scroll_V_max = tkinter.Scale(self, from_=0, to=255, orient=tkinter.HORIZONTAL)
        self.Scroll_V_max.set(255)
        self.Scroll_V_max.place(x=650-160, y=200)
        self.Scroll_V_max.bind("<ButtonRelease-1>", show_values)

        btnMotionparameter = tkinter.Button(self, text="Motion Parameter", command=self.OpenRPparameterwindow)
        lbl_1 = tkinter.Label(self, text="RV")
        lbl_2 = tkinter.Label(self, text="RR")
        lbl_3 = tkinter.Label(self, text="Value")
        lbl_4 = tkinter.Label(self, text="Steps")
        self.txtRVvalue = tkinter.Text(self, width=6, height=1)
        self.txtRVsteps = tkinter.Text(self, width=6, height=1)
        self.txtRRvalue = tkinter.Text(self, width=6, height=1)
        self.txtRRsteps = tkinter.Text(self, width=6, height=1)
        self.txtRVvalue.insert(0.0, "200")
        self.txtRVsteps.insert(0.0, "30")
        self.txtRRvalue.insert(0.0, "0")
        self.txtRRsteps.insert(0.0, "0")
        btnMove = tkinter.Button(self, text="Move", width=7, height=1, command = self.Start_RP_move)
        btnStop = tkinter.Button(self, text="Stop", width=7, height=1, command = self.End_RP_move)

        self.txtTwisted_value = tkinter.Text(self, width=6, height=1)
        self.txtTwisted_value.insert(0.0, "None")

        self.txtX_axis_twisted_value = tkinter.Text(self, width = 6, height =1)
        self.txtX_axis_twisted_value.insert(0.0, "None")

        self.Current_Changing_RP = tkinter.Text(self, width=6, height=1)
        self.Current_Changing_RP.insert(0.0, "None")

        self.RP_value_min = tkinter.Text(self,width=6,height=1)
        self.RP_value_min.insert(0.0,"None")
        self.L7 = tkinter.Label(self, text="Min_value")
        self.L8 = tkinter.Label(self, text="Now Changing")

        values_RP = ["RP" + str(i) for i in range(0, 10)]
        values_RP2 = ["RP" + i for i in ["A", "B", "C", "D", "E", "F", "G"]]
        values_RP = values_RP + values_RP2
        self.combobox_Changing_RP = tkinter.ttk.Combobox(self, width=7, height=15, values=values_RP)



        lbl_5 = tkinter.Label(self, text="Serial Communication")
        RadioVariety_1 = tkinter.IntVar()
        radio_Brate38400 = tkinter.Radiobutton(self, value=38400, text="38400", variable=RadioVariety_1)
        radio_Brate115200 = tkinter.Radiobutton(self, value=115200, text="115200", variable=RadioVariety_1)
        lbl_6 = tkinter.Label(self, text="PORT")
        values = ["COM" + str(i) for i in range(1, 10)]
        combobox_Baudrate = tkinter.ttk.Combobox(self, width=7, height=15, values=values)
        def Portopen():
            messagebox.showinfo("Port를 연결합니다",combobox_Baudrate.get()+"와 연결을 시도합니다")
            # s = serial.Serial(str(combobox_Baudrate.get()), 38400)

        btnOpen = tkinter.Button(self, text="OPEN", command=Portopen)
        frame = tkinter.Frame(self)
        listbox = tkinter.Listbox(frame)
        for line in range(1, 10):
            listbox.insert(line, " ")

        frame2 = tkinter.Frame(self)
        frame_Deep_result = tkinter.Frame(self,width=40,height=30)
        self.listbox2 = tkinter.Listbox(frame2)


        txtsendcommand = tkinter.Text(self, width=41, height=1, autoseparators=True)

        self.scrollbar = tkinter.Scrollbar(frame_Deep_result)

        self.txt_Deep = tkinter.Text(frame_Deep_result, width=41, height=20, autoseparators=True, yscrollcommand=self.scrollbar.set)
        btnMotionparameter.place(x=950-160, y=50, width=200, height=30)

        lbl_1.place(x=960-160, y=110)
        lbl_2.place(x=960-160, y=150)
        lbl_3.place(x=1000-160, y=85)
        lbl_4.place(x=1080-160, y=85)
        self.txtRVvalue.place(x=1000-160, y=110)
        self.txtRVsteps.place(x=1080-160, y=110)
        self.txtRRvalue.place(x=1000-160, y=150)
        self.txtRRsteps.place(x=1080-160, y=150)
        btnMove.place(x=1000-160, y=220)
        btnStop.place(x=1080-160, y=220)
        self.txtTwisted_value.place(x=1080-160, y=270)
        self.txtX_axis_twisted_value.place(x = 1000-160, y = 270)
        self.Current_Changing_RP.place(x=1000-160, y=300)
        self.combobox_Changing_RP.place(x=1000-160,y=330)
        self.combobox_Changing_RP.set("RP?")

        self.RP_value_min.place(x=1080-160, y=330)
        self.L7.place(x=1080-160, y=305)
        self.L8.place(x=910-160, y=330)

        lbl_5.place(x=1200-160, y=20)
        radio_Brate38400.place(x=1200-160, y=40)
        radio_Brate115200.place(x=1280-160, y=40)
        lbl_6.place(x=1190-160, y=70)
        combobox_Baudrate.place(x=1250-160, y=70)
        combobox_Baudrate.set("COM3")
        btnOpen.place(x=1330-160, y=70)
        listbox.pack()
        frame.place(x=1180-160, y=100)
        self.listbox2.pack()
        frame2.place(x=1330-160, y=100)
        frame_Deep_result.place(x= 1180-160, y = 300)
        txtsendcommand.place(x=1180-160, y=265)
        self.scrollbar.pack(side="right", fill="both", expand=True)
        self.txt_Deep.pack()

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

        # btnMotionparameter.bind("<Button-1>", sendCommand)
        txtsendcommand.bind("<Return>", sendCommand)

        self.queue = queue.Queue()
        thread = SerialThread(self.queue)
        thread.start()
        self.process_serial()

    # def sendCommand(self,str):
    #     global command_count
    #     str = self.txtsendcommand.get(0.0, tkinter.END)
    #     str = str.split()
    #     str = str[command_count]
    #     self.sendCommandtoDSP(str)
    #     self.listbox.insert(30000 - command_count, str)
    #     self.listbox.see(30000 - command_count)
    #     command_count += 1

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

    def snapshot(self):
         ret, frame = self.vid.get_frame()
         if ret:
             cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def getPerpCoord(self, aX, aY, bX, bY, length):
        vX = bX - aX
        vY = bY - aY
        # print(str(vX)+" "+str(vY))
        if (vX == 0 or vY == 0):
            return 0, 0, 0, 0
        mag = math.sqrt(vX * vX + vY * vY)
        vX = vX / mag
        vY = vY / mag
        temp = vX
        vX = 0 - vY
        vY = temp
        cX = bX + vX * length
        cY = bY + vY * length
        dX = bX - vX * length
        dY = bY - vY * length
        return int(cX), int(cY), int(dX), int(dY)


    def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
         # print(self.vid.height)
         # print(self.vid.width)


         #self.Outframe
         if ret:
            frame=cv2.copyMakeBorder(frame,80,80,0,0,cv2.BORDER_CONSTANT,value=0)
            height, width, channel = frame.shape
            matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 90, 1)
            frame = cv2.warpAffine(frame, matrix, (width, height))
            frame = frame[:,80:560]
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            self.imgproc(frame)
            self.Outframe = cv2.cvtColor(self.Outframe, cv2.COLOR_HSV2RGB)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.Outframe))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

         self.after(self.delay, self.update)
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


        if not ((self.Run_end_x == 0 and self.Run_end_y == 0 ) or (self.Run_start_x == 0 and self.Run_start_y == 0 )):
            cv2.line(self.Outframe, (self.Run_start_x, self.Run_start_y), (self.Run_end_x, self.Run_end_y), (80, 180, 200), 10)

        if self.Start_flag:
            mid_x = int((self.Red.max_x + self.Red.max_width / 2) * 0.5 + (self.Blue.max_x + self.Blue.max_width / 2) * 0.5)
            mid_y = int((self.Red.max_y + self.Red.max_height / 2) * 0.5 + (self.Blue.max_y + self.Blue.max_height / 2) * 0.5)

            self.CenterPoints_x.append(mid_x)
            self.CenterPoints_y.append(mid_y)


            cv2.line(self.Outframe, (self.Run_start_x, self.Run_start_y), (self.Run_start_x + int(500*math.cos(self.Run_start_inclination + math.pi/2)), self.Run_start_y - int(500*math.sin(self.Run_start_inclination + math.pi/2))),(80,180,200), 5, cv2.LINE_8)#수직선 그리기

            #self.Run_start_inclination

            print(self.calcDistanceLineNdot(self.Run_start_x,self.Run_start_y,self.Run_start_x + int(500*math.cos(self.Run_start_inclination + math.pi/2)), self.Run_start_y - int(500*math.sin(self.Run_start_inclination + math.pi/2)),mid_x,mid_y))
            self.Distributions.append(self.calcDistanceLineNdot(self.Run_start_x,self.Run_start_y,self.Run_start_x + int(500*math.cos(self.Run_start_inclination + math.pi/2)), self.Run_start_y - int(500*math.sin(self.Run_start_inclination + math.pi/2)),mid_x,mid_y))
            for i in range(len(self.CenterPoints_x)):
                cv2.circle(self.Outframe, (self.CenterPoints_x[i], self.CenterPoints_y[i]), 3, (0, 255, 255), thickness=-1)


        elif self.End_flag:
            self.CenterPoints_x.clear()
            self.CenterPoints_y.clear()
            self.Distributions.clear()
    def calcDistanceLineNdot(self,x1,y1,x2,y2,x,y):
        if x1-x2 == 0:
            return abs(x1-x)
        a = float((y1 - y2)/(x1- x2))
        return abs(a*(x - x1) - y + y1) / math.sqrt(a*a + 1)
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

    def OpenRPparameterwindow(self):
        RP_parameter=RPwindow()
        RP_parameter.mainloop()

    def Start_RP_move(self):
        global Run_start_x, Run_start_y, Run_end_x, Run_end_y, Run_start_inclination,RP0,RP1,RP2,RP3,RP4,RP5,RP6,RP7,RP8,RP9,RPA,RPB,RPC,RPD,RPE,RPF,RPG
        self.Run_start_x = int((self.Red.max_x + self.Red.max_width / 2)*0.5 + (self.Blue.max_x + self.Blue.max_width / 2)*0.5)
        self.Run_start_y = int((self.Red.max_y + self.Red.max_height / 2)*0.5 + (self.Blue.max_y + self.Blue.max_height / 2)*0.5)
        self.Run_start_inclination = math.atan(abs(self.Red.max_y - self.Blue.max_y) / abs(self.Red.max_x - self.Blue.max_x))

        self.Run_end_x=0
        self.Run_end_y=0
        self.try_count += 1
        print("=============")
        print("기울기"+ str(self.Run_start_inclination*180/math.pi))
        print(self.Run_start_x)
        print(self.Run_start_y)
        RP_list = re.findall("\d+", self.txtRVvalue.get(0.0, tkinter.END))
        RP_value = int(RP_list[0])
        RPStep_list = re.findall("\d+", self.txtRVsteps.get(0.0, tkinter.END))
        RP_Step_value = int(RPStep_list[0])

        if self.try_count!=1:
            if self.RP_Change_flag == True:
                sending_message = ""
                if self.RandChoice == 0:
                    RP0 = self.Penalty_Min_RP_value
                    sending_message = ("RP0," + str(RP0) + ";")
                elif self.RandChoice == 1:
                    RP1 = self.Penalty_Min_RP_value
                    sending_message = ("RP1," + str(RP1) + ";")
                elif self.RandChoice == 2:
                    RP2 = self.Penalty_Min_RP_value
                    sending_message = ("RP2," + str(RP2) + ";")
                elif self.RandChoice == 3:
                    RP3 = self.Penalty_Min_RP_value
                    sending_message = ("RP3," + str(RP3) + ";")
                elif self.RandChoice == 4:
                    RP4 = self.Penalty_Min_RP_value
                    sending_message = ("RP4," + str(RP4) + ";")
                elif self.RandChoice == 5:
                    RP5 = self.Penalty_Min_RP_value
                    sending_message = ("RP5," + str(RP5) + ";")
                elif self.RandChoice == 6:
                    RP6 = self.Penalty_Min_RP_value
                    sending_message = ("RP6," + str(RP6) + ";")
                elif self.RandChoice == 7:
                    RP7 = self.Penalty_Min_RP_value
                    sending_message = ("RP7," + str(RP7) + ";")
                elif self.RandChoice == 8:
                    RP8 = self.Penalty_Min_RP_value
                    sending_message = ("RP8," + str(RP8) + ";")
                elif self.RandChoice == 9:
                    RP9 = self.Penalty_Min_RP_value
                    sending_message = ("RP9," + str(RP9) + ";")
                elif self.RandChoice == 10:
                    RPA = self.Penalty_Min_RP_value
                    sending_message = ("RPA," + str(RPA) + ";")
                elif self.RandChoice == 11:
                    RPB = self.Penalty_Min_RP_value
                    sending_message = ("RPB," + str(RPB) + ";")
                elif self.RandChoice == 12:
                    RPC = self.Penalty_Min_RP_value
                    sending_message = ("RPC," + str(RPC) + ";")
                elif self.RandChoice == 13:
                    RPD = self.Penalty_Min_RP_value
                    sending_message = ("RPD," + str(RPD) + ";")
                elif self.RandChoice == 14:
                    RPE = self.Penalty_Min_RP_value
                    sending_message = ("RPE," + str(RPE) + ";")
                elif self.RandChoice == 15:
                    RPF = self.Penalty_Min_RP_value
                    sending_message = ("RPF," + str(RPF) + ";")
                elif self.RandChoice == 16:
                    RPG = self.Penalty_Min_RP_value
                    sending_message = ("RPG," + str(RPG) + ";")

                s.write(sending_message.encode())
                time.sleep(0.1)
                #////////////////////////////////////////////////////////

                
                
                
                while True:
                    self.RandChoice = random.randint(0, 4)  # Choice 선택 원래 17
                    self.RP_Change_flag = False
                    if self.RandChoice == 2:
                        self.RandChoice = 3
                    elif self.RandChoice == 3:
                        self.RandChoice = 7
                    elif self.RandChoice == 4:
                        self.RandChoice = 11
                    if RP_ischanged[self.RandChoice] == False:
                        break
                if self.RP_Change_order == 0:
                    self.RandChoice = 0
                    self.RP_Change_order = 1
                elif self.RP_Change_order == 1:
                    self.RandChoice = 1
                    self.RP_Change_order = 2
                elif self.RP_Change_order == 2:
                    self.RandChoice = 11
                    self.RP_Change_order = 3
                elif self.RP_Change_order == 3:
                    self.RandChoice = 3
                    self.RP_Change_order = 4
                elif self.RP_Change_order == 4:
                    self.RandChoice = 7

                self.RP_Change_count = 10
                self.Current_delta_value = (RP_mapping_max[self.RandChoice]-RP_mapping_min[self.RandChoice])/2

                if self.RandChoice == 0:
                    self.Current_delta_value = 10
                self.txt_Deep.insert(tkinter.END, "=========================\n")
                self.Penalty_Min = 10000
                self.Penalty_Min_RP_value = 0
                Templist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]
                RP_ischanged[self.RandChoice] = True
                self.combobox_Changing_RP.set("RP"+Templist[self.RandChoice])


            else:
                self.Current_delta_value /= 2
                if self.RandChoice == 0:
                    self.Current_delta_value = 10
            Rand_value=random.random()

            print(self.RandChoice)
            self.delta_value = round(self.Current_delta_value)
            sending_message = ""
            if self.RandChoice==0:
                RP0 += RP_sign_type[0] * self.delta_value
                if RP0 > RP_mapping_max[0]:
                    RP0=RP_mapping_max[0]
                elif RP0 < RP_mapping_min[0]:
                    RP0 = RP_mapping_min[0]
               # s.write(("RP" + str(self.RandChoice) + "," + str(RP0) + ";").encode())
                sending_message= ("RP0," + str(RP0) + ";")
            elif self.RandChoice == 1:
                RP1 += RP_sign_type[1] * self.delta_value
                if RP1 > RP_mapping_max[1]:
                    RP1=RP_mapping_max[1]
                elif RP1 < RP_mapping_min[1]:
                    RP1 = RP_mapping_min[1]
                sending_message= ("RP1," + str(RP1) + ";")
            elif self.RandChoice == 2:
                RP2 += RP_sign_type[2] * self.delta_value
                if RP2 > RP_mapping_max[2]:
                    RP2=RP_mapping_max[2]
                elif RP2 < RP_mapping_min[2]:
                    RP2 = RP_mapping_min[2]
                sending_message= ("RP2," + str(RP2) + ";")
            elif self.RandChoice == 3:
                RP3 += RP_sign_type[3] * self.delta_value
                if RP3 > RP_mapping_max[3]:
                    RP3=RP_mapping_max[3]
                elif RP3 < RP_mapping_min[3]:
                    RP3 = RP_mapping_min[3]
                sending_message= ("RP3," + str(RP3) + ";")
            elif self.RandChoice == 4:
                RP4 += RP_sign_type[4] * self.delta_value
                if RP4 > RP_mapping_max[4]:
                    RP4=RP_mapping_max[4]
                elif RP4 < RP_mapping_min[4]:
                    RP4 = RP_mapping_min[4]
                sending_message= ("RP4," + str(RP4) + ";")
            elif self.RandChoice == 5:
                RP5 += RP_sign_type[5] * self.delta_value
                if RP5 > RP_mapping_max[5]:
                    RP5 = RP_mapping_max[5]
                elif RP5 < RP_mapping_min[5]:
                    RP5 = RP_mapping_min[5]
                sending_message= ("RP5," + str(RP5) + ";")
            elif self.RandChoice == 6:
                RP6 += RP_sign_type[6] * self.delta_value
                if RP6 > RP_mapping_max[6]:
                    RP6=RP_mapping_max[6]
                elif RP6 < RP_mapping_min[6]:
                    RP6 = RP_mapping_min[6]
                sending_message= ("RP6," + str(RP6) + ";")
            elif self.RandChoice == 7:
                RP7 += RP_sign_type[7] * self.delta_value
                if RP7 > RP_mapping_max[7]:
                    RP7=RP_mapping_max[7]
                elif RP7 < RP_mapping_min[7]:
                    RP7 = RP_mapping_min[7]
                sending_message= ("RP7," + str(RP7) + ";")
            elif self.RandChoice == 8:
                RP8 += RP_sign_type[8] * self.delta_value
                if RP8 > RP_mapping_max[8]:
                    RP8=RP_mapping_max[8]
                elif RP8 < RP_mapping_min[8]:
                    RP8 = RP_mapping_min[8]
                sending_message= ("RP8," + str(RP8) + ";")
            elif self.RandChoice == 9:
                RP9 += RP_sign_type[9] * self.delta_value
                if RP9 > RP_mapping_max[9]:
                    RP9=RP_mapping_max[9]
                elif RP9 < RP_mapping_min[9]:
                    RP9 = RP_mapping_min[9]
                sending_message= ("RP9," + str(RP9) + ";")
            elif self.RandChoice == 10:
                RPA += RP_sign_type[10] * self.delta_value
                if RPA > RP_mapping_max[10]:
                    RPA=RP_mapping_max[10]
                elif RPA < RP_mapping_min[10]:
                    RPA = RP_mapping_min[10]
                sending_message= ("RPA," + str(RPA) + ";")
            elif self.RandChoice == 11:
                RPB += RP_sign_type[11] * self.delta_value
                if RPB > RP_mapping_max[11]:
                    RPB=RP_mapping_max[11]
                elif RPB < RP_mapping_min[11]:
                    RPB = RP_mapping_min[11]
                sending_message= ("RPB," + str(RPB) + ";")
            elif self.RandChoice == 12:
                RPC += RP_sign_type[12] * self.delta_value
                if RPC > RP_mapping_max[12]:
                    RPC=RP_mapping_max[12]
                elif RPC < RP_mapping_min[12]:
                    RPC = RP_mapping_min[12]
                sending_message= ("RPC," + str(RPC) + ";")
            elif self.RandChoice == 13:
                RPD += RP_sign_type[13] * self.delta_value
                if RPD > RP_mapping_max[13]:
                    RPD = RP_mapping_max[13]
                elif RPD < RP_mapping_min[13]:
                    RPD = RP_mapping_min[13]
                sending_message = ("RPD," + str(RPD) + ";")
            elif self.RandChoice == 14:
                RPE += RP_sign_type[14] * self.delta_value
                if RPE > RP_mapping_max[14]:
                    RPE=RP_mapping_max[14]
                elif RPE < RP_mapping_min[14]:
                    RPE = RP_mapping_min[14]
                sending_message= ("RPE," + str(RPE) + ";")
            elif self.RandChoice == 15:
                RPF += RP_sign_type[15] * self.delta_value
                if RPF > RP_mapping_max[15]:
                    RPF=RP_mapping_max[15]
                elif RPF < RP_mapping_min[15]:
                    RPF = RP_mapping_min[15]
                sending_message= ("RPF," + str(RPF) + ";")
            elif self.RandChoice == 16:
                RPG += RP_sign_type[16] * self.delta_value
                if RPG > RP_mapping_max[16]:
                    RPG=RP_mapping_max[16]
                elif RPG < RP_mapping_min[16]:
                    RPG = RP_mapping_min[16]
                sending_message= ("RPG," + str(RPG) + ";")

            s.write(sending_message.encode())
            time.sleep(0.1)
            self.txt_Deep.insert(tkinter.END, "변경 RP"+str(self.RandChoice)+"\n변경량 : "+str(self.delta_value)+"\n")

            if self.RandChoice == 0:
                self.txt_Deep.insert(tkinter.END, "RP0:" + str(RP0) + "\n")
            elif self.RandChoice == 1:
                self.txt_Deep.insert(tkinter.END, "RP1:" + str(RP1) + "\n")
            elif self.RandChoice == 2:
                self.txt_Deep.insert(tkinter.END, "RP2:" + str(RP2) + "\n")
            elif self.RandChoice == 3:
                self.txt_Deep.insert(tkinter.END, "RP3:" + str(RP3) + "\n")
            elif self.RandChoice == 4:
                self.txt_Deep.insert(tkinter.END, "RP4:" + str(RP4) + "\n")
            elif self.RandChoice == 5:
                self.txt_Deep.insert(tkinter.END, "RP5:" + str(RP5) + "\n")
            elif self.RandChoice == 6:
                self.txt_Deep.insert(tkinter.END, "RP6:" + str(RP6) + "\n")
            elif self.RandChoice == 7:
                self.txt_Deep.insert(tkinter.END, "RP7:" + str(RP7) + "\n")
            elif self.RandChoice == 8:
                self.txt_Deep.insert(tkinter.END, "RP8:" + str(RP8) + "\n")
            elif self.RandChoice == 9:
                self.txt_Deep.insert(tkinter.END, "RP9:" + str(RP9) + "\n")
            elif self.RandChoice == 10:
                self.txt_Deep.insert(tkinter.END, "RPA:" + str(RPA) + "\n")
            elif self.RandChoice == 11:
                self.txt_Deep.insert(tkinter.END, "RPB:" + str(RPB) + "\n")
            elif self.RandChoice == 12:
                self.txt_Deep.insert(tkinter.END, "RPC:" + str(RPC) + "\n")
            elif self.RandChoice == 13:
                self.txt_Deep.insert(tkinter.END, "RPD:" + str(RPD) + "\n")
            elif self.RandChoice == 14:
                self.txt_Deep.insert(tkinter.END, "RPE:" + str(RPE) + "\n")
            elif self.RandChoice == 15:
                self.txt_Deep.insert(tkinter.END, "RPF:" + str(RPF) + "\n")
            elif self.RandChoice == 16:
                self.txt_Deep.insert(tkinter.END, "RPG:" + str(RPG) + "\n")

            self.txt_Deep.see(tkinter.END)

            self.prev_Penalty = self.current_Peanalty
            self.RP_Change_count -= 1
        self.Start_flag = True
        self.End_flag = False
        s.write(("RV" + str(RP_value) + "," + str(RP_Step_value) + ";").encode())
        RP_ischanged[self.RandChoice] = True

    def End_RP_move(self):
        global Run_end_x, Run_end_y, Run_end_inclination
        self.Run_end_x = int((self.Red.max_x + self.Red.max_width / 2) * 0.5 + (self.Blue.max_x + self.Blue.max_width / 2) * 0.5)
        self.Run_end_y = int((self.Red.max_y + self.Red.max_height / 2) * 0.5 + (self.Blue.max_y + self.Blue.max_height / 2) * 0.5)

        self.Run_end_inclination = math.atan((self.Red.max_y - self.Blue.max_y) / (self.Red.max_x - self.Blue.max_x))


        print("=============")
        print(self.Run_end_x)
        print(self.Run_end_y)
        # twisted_value = (self.Run_start_y - self.Run_end_y) / (self.Run_start_x - self.Run_end_x)
        twisted_value = abs(self.Run_end_inclination - self.Run_start_inclination)*180/math.pi
        X_axis_twisted_value = abs(self.Run_end_x - self.Run_start_x)
        Run_Distance = abs(self.Run_start_y - self.Run_end_y)

        print(twisted_value)
        self.txtTwisted_value.delete(0.0,tkinter.END)
        self.txtTwisted_value.insert(0.0, str(twisted_value))
        self.txtX_axis_twisted_value.delete(0.0,tkinter.END)
        self.txtX_axis_twisted_value.insert(0.0, str(X_axis_twisted_value))

        AvgMid_points_x = sum(self.CenterPoints_x, 0.0) / len(self.CenterPoints_x)
        AvgMid_points_y = sum(self.CenterPoints_y, 0.0) / len(self.CenterPoints_y)
        total_distribution = 0
        for i in range(len(self.Distributions)):
            #self.CenterPoints_x[i] = abs(self.CenterPoints_x[i] - AvgMid_points_x)
            #self.CenterPoints_y[i] = abs(self.CenterPoints_y[i] - AvgMid_points_y)
            #total_distribution +=self.CenterPoints_x[i] + self.CenterPoints_y[i]
            total_distribution+= self.Distributions[i]
        print("편차는 : "+ str(total_distribution/len(self.Distributions)))
        avg_distribution = round(total_distribution/len(self.Distributions),4)
        self.Start_flag = False
        self.End_flag = True
        #X_axis_twisted_value일단 생략
        self.current_Peanalty = round(5 * twisted_value  + avg_distribution - Run_Distance + 600, 4)
        print("틀어진 정도(x20):"+ str(twisted_value) + "도")
        print("전진 거리 :" + str(Run_Distance))
        print("표준편차 :"+str(avg_distribution))
        print("현재 패널티:" + str(self.current_Peanalty))
        self.txt_Deep.insert(tkinter.END, "현재 패널티:" + str(self.current_Peanalty) + "\n")


        if self.try_count != 1:
            self.txt_Deep.insert(tkinter.END, "이전 패널티:" + str(self.prev_Penalty) + "\n")

            if self.current_Peanalty < self.Penalty_Min:
                self.Penalty_Min = self.current_Peanalty
                Min_value = 0
                if self.RandChoice == 0:
                    Min_value = RP0
                elif self.RandChoice == 1:
                    Min_value = RP1
                elif self.RandChoice == 2:
                    Min_value = RP2
                elif self.RandChoice == 3:
                    Min_value = RP3
                elif self.RandChoice == 4:
                    Min_value = RP4
                elif self.RandChoice == 5:
                    Min_value = RP5
                elif self.RandChoice == 6:
                    Min_value = RP6
                elif self.RandChoice == 7:
                    Min_value = RP7
                elif self.RandChoice == 8:
                    Min_value = RP8
                elif self.RandChoice == 9:
                    Min_value = RP9
                elif self.RandChoice == 10:
                    Min_value = RPA
                elif self.RandChoice == 11:
                    Min_value = RPB
                elif self.RandChoice == 12:
                    Min_value = RPC
                elif self.RandChoice == 13:
                    Min_value = RPD
                elif self.RandChoice == 14:
                    Min_value = RPE
                elif self.RandChoice == 15:
                    Min_value = RPF
                elif self.RandChoice == 16:
                    Min_value = RPG
                self.Penalty_Min_RP_value = Min_value
                self.RP_value_min.delete(0.0, tkinter.END)
                self.RP_value_min.insert(0.0, str(self.Penalty_Min_RP_value))

            if self.current_Peanalty> self.prev_Penalty:
                global RP_sign_type
                #self.delta_sign *= -1
                RP_sign_type[self.RandChoice] *= -1
        self.txt_Deep.insert(tkinter.END, "-------------------------\n")
        self.txt_Deep.see(tkinter.END)

        if self.RP_Change_count == 0 or self.current_Peanalty < self.RP_Change_threshold_twisted_value or self.delta_value < 4:
            self.RP_Change_flag = True
            self.txt_Deep.insert(tkinter.END, "**********************\n")

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
         #self.vid.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
         #self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
         self.vid.set(cv2.CAP_PROP_AUTOFOCUS, False)
         self.vid.set(cv2.CAP_PROP_SETTINGS, True)
     def get_frame(self):

         if self.vid.isOpened():
             ret, frame = self.vid.read()
             height, width, channel = frame.shape
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


app = App()
app.mainloop()