# micropython-connected-weather-station
Connected weather station with: ESP32, micropython, tft spi ili9341 screen, RF 433 Mhz RXB6 reciever, RF 433 Mhz temperature an humidity sensor, Blynk.io, OpenWeathermap, BMP280 ...

![](carte_english.png)

## Start up:
- Copy all files in'version1' folder to the ESP32 board.

- Paste your OpenWeatherMap API key, Blynk API key, SSID name and Wifi key into data_wifi.py file when you see "..."

- For RF sensor, the code in 'mesure.py' has to be adapt to your sensor model.


## My sensor Rf signal:

 ![](Rf_signal.PNG)
  ![](binary_code.PNG)
  
  ## Display on screen and smartphone:
  
  ![](Result.png)
