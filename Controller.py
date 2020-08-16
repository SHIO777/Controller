#-*- coding:utf-8-*-
import webiopi
import time
import pigpio
import subprocess as proc
import datetime

path = "/home/pi/work/0816/"   #自分で指定する
filename = "kakikae.txt"       #予めテキストファイル作っておく
filename2 = "rangemax.txt"

webiopi.setDebug()
pi=pigpio.pi()

#ピン指定
SV_1 = 12  #THROTTLE and BRAKE
SV_2 = 19  #BRAKE
SV_3 = 21  #STEARING

def setup():
 pi.set_mode(SV_1, pigpio.OUTPUT) #THROTTLE
 pi.set_mode(SV_2, pigpio.OUTPUT) #BRAKE
 pi.set_mode(SV_3, pigpio.OUTPUT) #STEARING

# def loop():
#  webiopi.sleep(5)

#****************サーボ動作***************************
@webiopi.macro
def GET1(val):
    val2=int(val)
    if val2 >= 1501:           
        pi.set_servo_pulsewidth(SV_1, int(val2))
    elif val2 <= 1500:
            pi.set_servo_pulsewidth(SV_2, int(val2))
    else: 
        pass

#STEARING
@webiopi.macro
def GET2(val):
 pi.set_servo_pulsewidth(SV_3, int(val))
#*****************************************************


#*****************テキストの値書き換え*******************
@webiopi.macro
def SaveNUMBER(val):
    file=open(path + filename, "w")
    file.write(val)
    file.close()
    
@webiopi.macro
def LoadNUMBER(val):
    file=open(path + filename, "r")
    value=int(file.read())     #java scriptは文字型でないと受け取れない？？
    file.close()
    #webiopi.debug(str(value))    #デバッグしたらvalueが表示される
    return "%d"%(value)   #10進数表記にする(%dはvalueをデシマルに変換)
#******************************************************

@webiopi.macro
def Currentvalue(val):
    file=open(path + filename2, "r")
    value=int(file.read())
    webiopi.debug(value)
    file.close()
    return "%d"%(value)



#シャットダウン実行関数
@webiopi.macro
def ShutCmd():
    proc.call("sudo killall sudo", shell=True)
    proc.call("sudo /sbin/shutdown -h now", shell=True)