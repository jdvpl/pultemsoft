# gps
from lib.micropyGPS import MicropyGPS
import lib.nmea as nmea
import utime
from machine import UART

def gps(oled,setImage,gpsBandera=False):
    uart = UART(2, 9600)
    now = utime.ticks_ms()
    my_nmea = nmea.nmea(debug=1)

    latitude=4.60971
    longitude=-74.08175
    lat=0
    lng=0
    while gpsBandera:
            oled.fill(0)
            oled.blit(setImage("../img/gps.pbm"), 50, 0)  
            oled.text(f"Conectando...",12,40)
            oled.show()
            while uart.any():
                b = uart.read()
                my_nmea.parse(b)
            if utime.ticks_diff(utime.ticks_ms(), now) > 1000:
                    now = utime.ticks_ms()
                    print('{} {}'.format(my_nmea.latitude, my_nmea.longitude))
                    lat = my_nmea.latitude
                    lng = my_nmea.longitude
                    if lat != 0 and lng !=0:
                        gpsBandera=False
                        oled.fill(0)
                        oled.blit(setImage("../img/gps.pbm"), 50, 0) 
                        oled.text("Lat:{}".format(my_nmea.latitude),  0, 45)
                        oled.text("Lng:{}".format(my_nmea.longitude),  0, 55)
                        oled.show()

    #es por si la latitud y longitud es 0 ya que aveces el gps no es muy estable con la señal
    if lat==0 and lng==0:
        lat=latitude
        lng=longitude
    
    return lat,lng