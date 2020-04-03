# micropython-connected-weather-station
Connected weather station with: ESP32, micropython, tft spi ili9341 screen, RF 433 Mhz RXB6 reciever, RF 433 Mhz temperature an humidity sensor, Blynk.io, OpenWeathermap, BMP280 ...

![](carte_english.png)

Copy all the files in the 'version1' folder to the ESP32 board.

Paste your: OpenWeatherMap API key, Blynk API key, SSID name and Wifi key into data_wifi.py file

For RF sensor, the code in 'mesure.py' have to be adapt to your model.

My sensor's Rf signal is here:

 ![](Rf_signal.PNG)
 
 ![](binary_code.PNG)
