import data_wifi
import mesures
from time import sleep_us, ticks_ms
import screen
from machine import Pin

#BME280
delay1 = 30000
prevtime1 = ticks_ms()
#Variables globales
T = 0
P = 0
T1= 0
HR1 = 0
T2 = 0
HR2 = 0
Text = 0
T_RES = 0
vit_vent = 0
#Données météo
prevtime2 = ticks_ms()
#Affichage
prevtime3 = ticks_ms()
Led = Pin (21,Pin.OUT)
Sens = Pin(16,Pin.IN)
#éclairage LCD
prevtime4 = ticks_ms()
#blynk
prevtime5 = ticks_ms() 
def eclairage():
    global prevtime4
    if Sens.value() == 0:
        prevtime4 = ticks_ms()
        Led.value(1)
    if ticks_ms() - prevtime4 > 30000:
        Led.value(0)
#Programme principal
Led.value(1)
print('---')
print('Ca demarre !!!!!')
screen.Screen_init()
if data_wifi.connect_wifi() is True:
    print('Récupération de données: date,heure ')
    data_wifi.traite_date_heure()
    print('Connect OpenWeatherMap ... ')
    icon_meteo,Text,T_RES,icon_vent,vit_vent = data_wifi.traite_openweathermap()
screen.Screen_write(T,P,T1,HR1,T2,HR2,Text,T_RES,vit_vent,icon_vent,icon_meteo)              
while True:
    eclairage()   
    sleep_us(2)
    Data = mesures.Sondes()
    if  Data is not None:
        if Data[0] == 1:
            T1 = Data[1]
            HR1 = Data[2]
        if Data[0] == 2:
            T2 = Data[1]
            HR2 = Data[2]        
    if  ticks_ms() - prevtime1 > 30000:#BMP280
        T,P = mesures.bmp280_mes()
        prevtime1 = ticks_ms()    
    if  ticks_ms() - prevtime3 > 47890: #Affichage
        screen.Screen_write(T,P,T1,HR1,T2,HR2,Text,T_RES,vit_vent,icon_vent,icon_meteo)
        prevtime3 = ticks_ms()    
    if  ticks_ms() - prevtime2 > 1800595: #OpenWeatherMap
        if  data_wifi.connect_wifi() is True:
            print('Connect OpenWeatherMap ... ')
            icon_meteo,Text,T_RES,icon_vent,vit_vent = data_wifi.traite_openweathermap()
        else:
            print(" Pas de connection Wifi ...")
        prevtime2 = ticks_ms()
    if  ticks_ms() - prevtime5 > 905879:  # Envoi des données à Blynk
        if  data_wifi.connect_wifi() is True:
            print("WIFI connecté ... Send Blynk")
            data_wifi.send_Blynk(T,T1,T2,HR1)
        else:
            print(" Pas de connection Wifi ...")
        prevtime5 = ticks_ms()