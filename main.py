from hcsr04 import HCSR04
from machine import Pin,SoftI2C,UART, Pin
from lib.sh1106 import SH1106_I2C
import network, time
import framebuf
import urequests as requests
import json

from lib.micropyGPS import MicropyGPS
import utime
import network
import lib.nmea as nmea
ancho=128
alto=64


# pines
# pin d5  es el de echo hcsr04
# pin d18 es el de triger hcsr04
i2c=SoftI2C(scl=Pin(4),sda=Pin(15),freq=100000)
oled =SH1106_I2C(ancho, alto, i2c)


# teclado
tecla_Arriba=const(0)
tecla_Abajo=const(1)

teclas=[
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D'],
    ]

# pines usado para las filas
filas=[13,12,14,27]
columnas=[26,25,33,32]

fila_pines=[Pin(nombre_pin, Pin.OUT) for nombre_pin in filas]

columna_pines=[Pin(nombre_pin, Pin.IN,Pin.PULL_DOWN) for nombre_pin in columnas]


def init():
    for fila in range(0,4):
        for columna in range(0,4):
            fila_pines[fila].on()

def scan(fila, columna):
    # Escane todo el teclado

    # define la tecla actual
    fila_pines[fila].on()
    tecla=None
    # verifica si hay teclas presionadas
    if columna_pines[columna].value()==tecla_Abajo:
        tecla=tecla_Abajo
    if columna_pines[columna].value()==tecla_Arriba:
        tecla=tecla_Arriba
    fila_pines[fila].off()
    return tecla

def buscar_icono(ruta):
    dibujo= open(ruta, "rb")  # Abrir en modo lectura de bist
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)

def conectaWifi (red, password):
    global miRed
    miRed = network.WLAN(network.STA_IF)     
    if not miRed.isconnected():              #Si no está conectado…
        miRed.active(True)                   #activa la interface
        miRed.connect(red, password)         #Intenta conectar con la red
        print('Conectando a la red', red +"…")
        oled.fill(0)
        oled.blit(buscar_icono("img/wifi.pbm"), 50, 0)
        oled.text(f'Conectando...',13,35)
        oled.show()
        utime.sleep(3)
        timeout = time.time ()
        while not miRed.isconnected():           #Mientras no se conecte..
            if (time.ticks_diff (time.time (), timeout) > 10):
                return False
    return True



if conectaWifi ("Jdvpl", "R@p1df@5t"):
    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())

    init();
    oled.fill(0)
    oled.text(f"Escribe cedula",0,0)
    oled.text(f"Opciones: ",20,10)
    oled.text(f"A. Anular ",0,20)
    oled.text(f"B. Borrar ",0,30)
    oled.text(f"C. Confirmar ",0,40)
    utime.sleep(5)
    oled.show()
    tecla_presionada_bool=True
    ultima_tecla_presionada=''
    while tecla_presionada_bool:
        for fila in range(4):
            for columna in range(4):
                tecla=scan(fila,columna)
                if tecla==tecla_Abajo:
                    print("Tecla presionada", teclas[fila][columna])
                    utime.sleep(0.2)
                    datatecla=teclas[fila][columna]
                    ultima_tecla_presionada+=datatecla
                    if datatecla=="A":
                        ultima_tecla_presionada=""
                    if datatecla=="B":
                        ultima_tecla_presionada=ultima_tecla_presionada.rstrip(ultima_tecla_presionada[-1])
                        if len(ultima_tecla_presionada)>1:
                            ultima_tecla_presionada=ultima_tecla_presionada.rstrip(ultima_tecla_presionada[-1])
                    if datatecla=="C":
                        ultima_tecla_presionada=ultima_tecla_presionada.rstrip(ultima_tecla_presionada[-1])
                        tecla_presionada_bool=False 
                    oled.fill(0)
                    oled.text(ultima_tecla_presionada,0,0)
                    oled.show()

    oled.fill(0)
    oled.text(f"Sintomas:1.Vomito",0,0)
    oled.text(f"2.Diarrea.3.Gripa",0,10)
    oled.text(f"4.Dolor cabeza ",0,20)
    oled.text(f"5.Malestar.6.ojos",0,30)
    oled.text(f"6.Asma.7.Tos ",0,40)
    oled.text(f"8.Corazon. 9.Lol ",0,50)
    oled.show()               
    tecla_presionada_bool_sintomas=True
    ultima_tecla_presionada_sintomas=[]
    while tecla_presionada_bool_sintomas:
        for fila in range(4):
            for columna in range(4):
                tecla=scan(fila,columna)
                if tecla==tecla_Abajo:
                    print("Tecla presionada", teclas[fila][columna])
                    utime.sleep(0.2)
                    datatecla=teclas[fila][columna]
                    ultima_tecla_presionada_sintomas+=datatecla
                    if datatecla=="A":
                        ultima_tecla_presionada_sintomas=""
                    if datatecla=="B":
                        ultima_tecla_presionada_sintomas=ultima_tecla_presionada_sintomas.rstrip(ultima_tecla_presionada_sintomas[-1])
                        if len(ultima_tecla_presionada_sintomas)>1:
                            ultima_tecla_presionada_sintomas=ultima_tecla_presionada_sintomas.rstrip(ultima_tecla_presionada_sintomas[-1])
                    if datatecla=="C":
                        ultima_tecla_presionada_sintomas=ultima_tecla_presionada_sintomas.rstrip(ultima_tecla_presionada_sintomas[-1])
                        tecla_presionada_bool=False 
                        pass
                    oled.fill(0)
                    oled.text(ultima_tecla_presionada_sintomas,0,0)
                    oled.show()
                    
    print(ultima_tecla_presionada)
    uart = UART(2, 9600)
    now = utime.ticks_ms()
    my_nmea = nmea.nmea(debug=1)

    # url = "http://us-central1-pultemsoft.cloudfunctions.net/app/api/users"
    # data = {
    # "name":"Daniel",
    # "lat":9.6676,
    # "lng":-74.5618,
    # "eps":"26132132lol",
    # "document":str(10111213)
    # }
    # headers = {"Content-Type": "application/json"}
    # r = requests.post(url,data=json.dumps(data),headers=headers)
    
    # print(r.status_code)
    latitude=4.60971
    longitude=-74.08175
    lat=0
    lng=0

    while 1:
            oled.fill(0)
            oled.blit(buscar_icono("img/gps.pbm"), 50, 0)  
            oled.text(f"Pultemsoft",25,40)
            oled.show()

            utime.sleep(5)
            while uart.any():
                b = uart.read()
                my_nmea.parse(b)

            if utime.ticks_diff(utime.ticks_ms(), now) > 5000:
                    now = utime.ticks_ms()
                    print('{} {}'.format(my_nmea.latitude, my_nmea.longitude))
                    lat = my_nmea.latitude
                    lng = my_nmea.longitude
                    
                    oled.fill(0)
                    oled.blit(buscar_icono("img/gps.pbm"), 50, 0) 
                    oled.text("Lat:{} Lng: {}".format(my_nmea.latitude,my_nmea.longitude),  0, 45)
                    oled.show()
                    break
                
            else:
                print("No hay gps ")
                break
    
    

    while True:
        oled.fill(0)
        oled.blit(buscar_icono("img/pultemsoft.pbm"), 0, 0)  
        oled.text(f"Pultemsoft",45,0)
        oled.show()

        

    
else:
    print ("Imposible conectar")

    miRed.active (False)
    oled.fill(0)
    oled.blit(buscar_icono("img/wifi_failed.pbm"), 50, 0)
    oled.text(f'Error en la red.',0,35)
    oled.show()








