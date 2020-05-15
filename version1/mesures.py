from machine import Pin, I2C
from bmp280 import BMP280
from time import sleep_us ,ticks_us, ticks_ms
sens = Pin(19, Pin.IN)
bus = I2C(sda = Pin(18),scl = Pin(22))
bmp = BMP280(bus)
# Fonctions
def start():
    if sens.value() == 1:
        Time = ticks_us()
        while sens.value() == 1:
            sleep_us(10)
        pulse = ticks_us() - Time
        if pulse >= 400 and pulse < 550:
            Time = ticks_us()
            while sens.value() == 0:
                sleep_us(10)
            pulse = ticks_us() - Time
            if pulse >= 3700 and pulse < 4100:
                return (True)
            
            else:
                return (False)
def trame():
    Time = 0
    pulse = 0
    Result = []
    while (pulse < 3000):
        while sens.value() == 1:
            sleep_us(10)
        Time = ticks_us()
        while sens.value() == 0:
            sleep_us(10)
        pulse = ticks_us() - Time

        if pulse > 600 and pulse <= 1200:
             Result.append(0)

        if pulse > 1200 and pulse <= 2100:
            Result.append(1)
    return(Result)
    Result = []
def String_to_int(chaine):
    value = 0
    for i in range(len(chaine)):
        value = value * 2
        if chaine[i] == 1:
            value = value + 1
    return (value)
    chaine =[]
def temp_hum(chaine):
    hum = String_to_int(chaine[28:])
    temp = String_to_int(chaine[14:24])
    if chaine[13:14] == [1,1]:
        temp = -(1024 - temp)
    return (round(temp/10,1),hum)
    chaine =[]
def Sondes():
    if start() is True:
        #print('start')
        Trame_bin = trame()
        #print(Trame_bin)
        #print(len(Trame_bin))
        
        if len(Trame_bin) == 36:
            if Trame_bin[24:28] == [1,1,1,1]:
                temp,hum = temp_hum(Trame_bin)
                
                #identification du canal
                if Trame_bin[10:12] == [0,0]:
                    canal = 1
                    
                elif Trame_bin[10:12] == [0,1]:
                    canal = 2
                    
                elif Trame_bin[10:12] == [1,0]:
                    canal = 3
                else:
                    canal = None
                print('--------------------------')
                print('Trame = ',Trame_bin)
                print('Numero du canal:',canal)
                print('Humidite = ', hum,' %')
                print('T = ', round(temp,1),'°C')
                print('--------------------------')
                return(canal,temp,hum)
            else:
                return(None)
        else:
            return(None)
    else:
        return(None)
    Trame_bin = []
def bmp280_mes():
    P = int(bmp.pressure/100)
    T = bmp.temperature
    print('----------')
    print('BMP 280')
    print('T = ',round(T,1), '°C')
    print('P = ',P, 'hPa')
    print('----------')
    return(round(T,1),P)       