import utime

def distance(oled,setImage,sensor_hc):
    bandera_distancia=True
    distance=0
    while bandera_distancia:
        distance = sensor_hc.distance_cm()
        utime.sleep(1)
        oled.fill(0)
        oled.blit(setImage("../img/pultemsoft.pbm"), 0, 0) 
        oled.text("Acercate:",40,0) 
        oled.text(f"{str(round(distance,2))} cm",40,10)
        oled.show()
        if distance>20:
            oled.fill(0)
            oled.blit(setImage("../img/pultemsoft.pbm"), 0, 0) 
            oled.text("Acercate:",40,0) 
            oled.text(f"{str(round(distance,2))} cm",40,10)
            oled.show()
        if distance<20 and distance>0:
            bandera_distancia=False
    return distance