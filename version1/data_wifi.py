import json
import urequests
import time
from  machine import RTC
import network
from time import ticks_ms

#Paramètres connexion WIFI
ssid = "HOME"
password = "14e0040820jtt"
wifi = network.WLAN(network.STA_IF)  # création client d'accès WiFi
rtc = RTC()
url_openweathermap = 'http://api.openweathermap.org/data/2.5/weather?q=laval,fr&units=metric&APPID=1f0dcfa859a381bd96bd7f57f7481ec8'
url_worldtimeapi = "http://worldtimeapi.org/api/timezone/Europe/Paris"
url_blynk = "http://blynk-cloud.com/C-fiYmEf0PagfdS3eaFIsw260rsgwZKP/update/"

def connect_wifi():
    delay = 6000
    prevtime = ticks_ms()
    print("Connexion au réseau WIFI '{}'".format(ssid) + "...")
    wifi.active(True)  # activation du client d'accès WiFi   
    wifi.connect(ssid, password)
    while  ticks_ms() - prevtime < delay:
        while not wifi.isconnected():  # connexion au point d'accès WiFi
            pass
    if wifi.isconnected():
        print("WIFI connecté")
        print('WiFi IP:', wifi.ifconfig()[0])
        return True
    else:
        print("!! Pas de connexion WIFI")
        return False

def traite_date_heure():
    reponse = urequests.get(url_worldtimeapi)
    if reponse.status_code == 200:  # requête ok
        data = json.loads(reponse.text)
        temps_unix = int(data.get("unixtime"))
        annee, mois, date,heure, minute, seconde,semaine,jour = time.localtime(temps_unix - 946684800 )
        heure_offset = data.get("utc_offset") 
        operation_offset = heure_offset[0]
        heure_offset = int(heure_offset[2:3])
        if operation_offset == "+":
            heure += heure_offset
        if operation_offset == "-":
            heure -= heure_offset
        rtc.datetime((annee, mois, date, 0, heure, minute, seconde, 0))
              
def traite_openweathermap():
    print("Récupération des données météo...")
    reponse = urequests.get(url_openweathermap)
    if reponse.status_code == 200:
        print("Réception OK")
        data = json.loads(reponse.text)
        temperature = data.get("main").get("temp")
        weather = data.get("weather")
        icon_meteo = data["weather"][0]["icon"]
        icon_meteo = icon_meteo[:2]
        t_res = data.get("main").get("feels_like")
        vent_vitesse = data.get("wind").get("speed")
        vent_vitesse = (3.6 * vent_vitesse)
        vent_orientation = data.get("wind").get("deg")
        print("Température : " + str(temperature))    
        print("Vitesse du vent : " + str(vent_vitesse) + " Km/h, Orientation : " + str(vent_orientation) + "°")
              
        if vent_orientation > 22.5 and vent_orientation <= 67.5:
            icon_vent = 'NE.txt'
        elif vent_orientation > 67.5 and vent_orientation <= 112.5:
            icon_vent = 'E.txt'
        elif vent_orientation > 112.5 and vent_orientation <= 157.5:
            icon_vent = 'SE.txt'
        elif vent_orientation > 157.5 and vent_orientation <= 202.5:
            icon_vent = 'S.txt'
        elif vent_orientation > 202.5 and vent_orientation <= 237.5:
            icon_vent = 'SO.txt'
        elif vent_orientation > 237.5 and vent_orientation <= 292.5:
            icon_vent = 'O.txt'
        elif vent_orientation > 292.5 and vent_orientation <= 337.5:
            icon_vent = 'NO.txt'
        else :
            icon_vent = 'N.txt'
        temperature = str(int(round(temperature,0)))
        t_res = str(int(round(t_res,0)))
        vent_vitesse= str(int(round(vent_vitesse,0)))
        return(icon_meteo,temperature,t_res,icon_vent,str(vent_vitesse))
    else:
        print("Problème ...")
        
def send_Blynk(t,t1,t2,hr1):
    print("connexion à Blynk...")
    url = url_blynk + "v0?value=" + str(t)
    reponse = urequests.get(url)
    if reponse.status_code == 200:  # requête ok
        print("Send T: OK")
    else:
        print("T Error!")
    reponse.close()
    url = url_blynk + "v1?value=" + str(t1)
    reponse = urequests.get(url)
    if reponse.status_code == 200:  # requête ok
        print("Send T1: OK")
    else:
        print("T1 Error!")
    reponse.close()
    url = url_blynk + "v2?value=" + str(t2)
    reponse = urequests.get(url)
    if reponse.status_code == 200:  # requête ok
        print("Send T2: OK")
    else:
        print("T2 Error!")
    reponse.close()
    url = url_blynk + "v3?value=" + str(hr1)
    reponse = urequests.get(url)
    if reponse.status_code == 200:  # requête ok
        print("Send HR1: OK")
    else:
        print("HR1 Error!")
    reponse.close()