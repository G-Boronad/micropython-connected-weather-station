from ili934xnew import ILI9341, color565
from machine import Pin, SPI,RTC
import tt14
import tt24
spi = SPI(1,baudrate=19000000,miso=Pin(12),mosi=Pin(13),sck=Pin(14))
display = ILI9341(spi,cs=15,dc=32,rst=25,w=320,h=240,r=2)
rtc = RTC()
def text_to_list(file):
    with open (file, "r") as f:
        data = [line for line in f.readlines()]
        f.close()
    data_F =[]
    for line in data:
        line = line[:-2]
        data_line = []
        for char in line:
            if char == '0':
                data_line.append(0)
            else:
                data_line.append(1)
        data_F.append(data_line)
    data = []    
    return(data_F)
    data_F =[]      
def Screen_init():
    display.erase()
    display.set_pos(60,100)
    display.set_font(tt24)
    display.print('ATTENDS')
    display.set_pos(60,200)
    display.set_font(tt24)
    display.print('je demarre !!!')
def Screen_write(t,p,t1,hr1,t2,hr2,text,t_res,vit_vent, icon_vent,icon_meteo):
    if icon_vent == None:
        icon_vent = 'interrogation.txt'
    if icon_meteo == None:
        icon_meteo = 'interrogation'
    icon_vent = "ICONS/" +icon_vent
    icon_meteo = "ICONS/"+icon_meteo + ".txt"
    clock = rtc.datetime()
    display.erase()
    #Date
    display.set_pos(85,5)
    display.set_font(tt14)
    display.print(str(clock[2])+" / "+str(clock[1])+" / "+str(clock[0]))
    # heure
    display.set_pos(100,30)
    display.set_font(tt24)
    display.print(str(clock[4])+":"+str(clock[5]))
    display.fill_rectangle(0, 60, 340, 2, color=color565(0,255,255))
    display.fill_rectangle(0, 200, 340, 2, color=color565(0,255,255))
    #icone_vent
    X0 = 150
    Y0 = 90
    data = text_to_list(icon_vent)
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 1:
                display.pixel(X0+x,Y0+y,color=color565(0,255,255))
    data = []
    X0 = 15 #icone_meteo
    Y0 = 70
    data = text_to_list(icon_meteo)
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] == 1:
                display.pixel(X0+x,Y0+y,color=color565(0,255,255))
    data = []
    display.set_pos(185,110)#vitesse vent
    display.set_font(tt14)
    display.print(vit_vent + ' km/h')
    display.set_pos(90,205)#Affichage T,P
    display.set_font(tt14)
    display.print (" STATION")
    display.set_pos(30,220)
    display.set_font(tt24)
    display.print(str(t)+" C")
    display.set_pos(130,220)
    display.print(str(p)+" hPa")
    display.fill_rectangle(0, 250, 340, 2, color=color565(0,255,255))
    display.fill_rectangle(115, 250, 2, 70, color=color565(0,255,255))
    display.set_pos(130,160)#t_res
    display.set_font(tt14)
    display.print("T RESSENTIE: ")
    display.set_pos(170,175)
    display.set_font(tt24)
    display.print(t_res)    
    display.set_pos(5,160)#Text
    display.set_font(tt14)
    display.print("T EXTERIEURE:")
    display.set_pos(45,175)
    display.set_font(tt24)
    display.print(text)
    display.set_pos(5,255)#Affichage T1,HR1,T2,HR2
    display.set_font(tt14)
    display.print("SONDE 1:")
    display.set_pos(30,270)
    display.set_font(tt24)
    display.print(str(t1)+" C")
    display.set_pos(30,295)
    display.print(str(hr1)+" %")        
    display.set_pos(127,255)
    display.set_font(tt14)
    display.print("SONDE 2:")
    display.set_font(tt24)
    display.set_pos(150,270)
    display.print(str(t2)+" C")
    display.set_pos(150,295)
    display.print(str(hr2)+" %")