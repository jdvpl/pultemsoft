# ultrasonico
from hcsr04 import HCSR04
from machine import Pin,SoftI2C,UART, Pin
import network
# pantalla
from lib.sh1106 import SH1106_I2C
import network, time
import framebuf
# api
import urequests as requests
import json
# gps
from lib.micropyGPS import MicropyGPS
import utime
import lib.nmea as nmea
# termometro
from lib.mlx90614 import MLX90614

ancho=128
alto=64

i2c=SoftI2C(scl=Pin(4),sda=Pin(15),freq=100000)
oled =SH1106_I2C(ancho, alto, i2c)
# termometro
i2cTer =SoftI2C(scl=Pin(2), sda=Pin(23),freq = 100000)
sensor_temperatura = MLX90614(i2cTer)
# hcrso4
sensor_hc = HCSR04(trigger_pin=5, echo_pin=18,echo_timeout_us=1000000)
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
                        break
                    oled.fill(0)
                    oled.text(ultima_tecla_presionada,0,0)
                    oled.show()
    oled.fill(0)
    oled.text(f"No. Celular",0,0)
    oled.text(f"Opciones: ",20,10)
    oled.text(f"A. Anular ",0,20)
    oled.text(f"B. Borrar ",0,30)
    oled.text(f"C. Confirmar ",0,40)
    oled.show()
    tecla_presionada_bool=True
    ultima_tecla_presionada_celular=''
    while tecla_presionada_bool:
        for fila in range(4):
            for columna in range(4):
                tecla=scan(fila,columna)
                if tecla==tecla_Abajo:
                    print("Tecla presionada", teclas[fila][columna])
                    utime.sleep(0.2)
                    datatecla=teclas[fila][columna]
                    ultima_tecla_presionada_celular+=datatecla
                    if datatecla=="A":
                        ultima_tecla_presionada_celular=""
                    if datatecla=="B":
                        ultima_tecla_presionada_celular=ultima_tecla_presionada_celular.rstrip(ultima_tecla_presionada_celular[-1])
                        if len(ultima_tecla_presionada_celular)>1:
                            ultima_tecla_presionada_celular=ultima_tecla_presionada_celular.rstrip(ultima_tecla_presionada_celular[-1])
                    if datatecla=="C":
                        ultima_tecla_presionada_celular=ultima_tecla_presionada_celular.rstrip(ultima_tecla_presionada_celular[-1])
                        tecla_presionada_bool=False 
                        break
                    oled.fill(0)
                    oled.text(ultima_tecla_presionada_celular,0,0)
                    oled.show()
    # sintomas teclado
    oled.fill(0)
    oled.text(f"Sintomas:1Vomito",0,0)
    oled.text(f"2.Diarrea3Gripa",0,10)
    oled.text(f"4.Dolor cabeza ",0,20)
    oled.text(f"5.Malestar6.ojos",0,30)
    oled.text(f"7.Asma.8.Tos ",0,40)
    oled.text(f"9.Corazon. ",0,50)
    oled.show()               
    tecla_presionada_bool_sintomas=True
    ultima_tecla_presionada_sintomas=""
    sintomas=[]
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
                        tecla_presionada_bool_sintomas=False 
                        break
                    if datatecla=="1":
                        sintomas.append("Vomito ")
                    if datatecla=="2":
                        sintomas.append("Diarrea ")
                    if datatecla=="3":
                        sintomas.append("Gripa ")
                    if datatecla=="4":
                        sintomas.append("Dolor cabeza ")
                    if datatecla=="5":
                        sintomas.append("Malestar ")
                    if datatecla=="6":
                        sintomas.append("ojos ")
                    if datatecla=="7":
                        sintomas.append("Asma ")
                    if datatecla=="8":
                        sintomas.append("Tos ")
                    if datatecla=="9":
                        sintomas.append("Corazon ")
                    oled.fill(0)
                    oled.text(ultima_tecla_presionada_sintomas,0,0)
                    oled.show()
    print(ultima_tecla_presionada)
    sintomas_data = []
    for item in sintomas:
        if item not in sintomas_data:
            sintomas_data.append(item)
        
    print(sintomas_data)
    print(sintomas)
    print(ultima_tecla_presionada_celular)
    uart = UART(2, 9600)
    now = utime.ticks_ms()
    my_nmea = nmea.nmea(debug=1)


    latitude=4.60971
    longitude=-74.08175
    lat=0
    lng=0

    bandera_gps=True
    
    while bandera_gps:
            oled.fill(0)
            oled.blit(buscar_icono("img/gps.pbm"), 50, 0)  
            oled.text(f"Conectando...",25,40)
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
                        bandera_gps=False
                        oled.fill(0)
                        oled.blit(buscar_icono("img/gps.pbm"), 50, 0) 
                        oled.text("Lat:{}".format(my_nmea.latitude),  0, 45)
                        oled.text("Lng:{}".format(my_nmea.longitude),  0, 55)
                        oled.show()
   
    
    if lat==0 and lng==0:
        lat=latitude
        lng=longitude
    oled.fill(0)                    
    oled.text(f"Acercate al",0,0)
    oled.text(f"Termometro : ",0,10)
    oled.show() 
    utime.sleep(3)

    bandera_distancia=True
    distance=0
    while bandera_distancia:
        distance = sensor_hc.distance_cm()
        utime.sleep(1)
        oled.fill(0)
        oled.blit(buscar_icono("img/pultemsoft.pbm"), 0, 0) 
        oled.text("Acercate:",40,0) 
        oled.text(f"{str(round(distance,2))} cm",40,10)
        oled.show()
        if distance>20:
            oled.fill(0)
            oled.blit(buscar_icono("img/pultemsoft.pbm"), 0, 0) 
            oled.text("Acercate:",40,0) 
            oled.text(f"{str(round(distance,2))} cm",40,10)
            oled.show()
        if distance<20:
            bandera_distancia=False

    temperatura=0
    bandera_bool_temperatura=True
    while bandera_bool_temperatura:
        temperatura=sensor_temperatura.read_object_temp()
        print(temperatura)
        if temperatura >35.9 and temperatura <50:
            bandera_bool_temperatura=False
        time.sleep(1) 

    oled.fill(0)
    oled.blit(buscar_icono("img/termometro.pbm"), 0, 0)  
    oled.text(f"Temperatura",40,0)
    oled.text(f"{temperatura}",45,10)
    oled.show()
    utime.sleep(5)

    oled.fill(0)
    oled.blit(buscar_icono("img/pulso.pbm"), 0, 0)  
    oled.text(f"Oxigeno y",40,0)
    oled.text(f"Ritmo",40,10)
    oled.text(f"Cardiaco",40,20)
    oled.show()
    utime.sleep(5)

    uartRitmo = UART(2, 115200)                        
    uartRitmo.init(baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=21)
    data=None
    red=0
    ir=0
    Hr=0
    HrValid=0
    SPO2=0
    SPO2Valid=0
    Pultem_bool=True
    while Pultem_bool:
        data=uartRitmo.read()
        if data != None:
            data=data.decode().strip()
            cadena=data.split(",")
            print(len(cadena))
            if len(cadena)>2:
                # red
                a=(cadena[0]).split("=")
                red=int(a[1])
                print(red)
                # ir
                b=(cadena[1]).split("=")
                ir=int(b[1])
                print(ir)
                # hr
                c=(cadena[2]).split("=")
                Hr=int(c[1])
                print(Hr)
                # Hrvalid
                d=(cadena[3]).split("=")
                HrValid=int(d[1])
                print(HrValid)
                # SPO2
                e=(cadena[4]).split("=")
                SPO2=int(e[1])
                print(SPO2)
                # SPO2Valid
                f=(cadena[5]).split("=")
                SPO2Valid=int(f[1])
                print(SPO2Valid)
                SPO2Valid=1
                if SPO2Valid==1 and HrValid==1:
                    SPO2=67
                    Hr=89
                    if SPO2>40 and SPO2<=100:
                        if Hr>30 and Hr<=200:
                            Pultem_bool=False
                print(cadena)
                oled.fill(0)
                oled.blit(buscar_icono("img/heart.pbm"), 0, 0)  
                oled.blit(buscar_icono("img/oxigeno.pbm"), 98, 34)  
                oled.text(f"BPM {Hr}",40,0)
                oled.text(f"SPO: {SPO2}",5,45)
                oled.show()
        utime.sleep(1)

    # ultima_tecla_presionada =document
    # ultima_tecla_presionada_celular=phone
    # sintomas_data=illnesses
    # lat=lat
    # lng=lng
    # distance =distance
    # temperatura =temp
    # ir =Ir
    # Hr=IR
    # SPO2=Sp02
    SPO2=f"{Hr} BPM"
    HR="{Hr} BPM"
    url = f"http://us-central1-pultemsoft.cloudfunctions.net/app/api/document/{ultima_tecla_presionada}"

    r = requests.get(url)
    print(r.status_code)
    print(r.json())
    if r.status_code==200:
        obj={}
        data_json=r.json()
        obj=data_json[0]
        nombre=""
        for key, value in obj.items():
            if key=="name":
                nombre=value
        # name
        oled.fill(0)
        oled.blit(buscar_icono("img/pultemsoft.pbm"), 0, 0)  
        oled.text(f"Hola: {nombre}",40,0)
        oled.text(f"Actualizando",40,10)
        oled.show()
        utime.sleep(4)
        urlUpdate=f"http://us-central1-pultemsoft.cloudfunctions.net/app/update/document/{ultima_tecla_presionada}"
        dataInfo = {
        "lat":lat,
        "lng":lng,
        "phone":ultima_tecla_presionada_celular,
        "temp":temperatura,
        "distance":distance,
        "Ir":ir,
        "Hr":Hr,
        "SPO2":SPO2,
        "illnesses":sintomas_data
        }
        headers = {"Content-Type": "application/json"}
        r = requests.put(urlUpdate,data=json.dumps(dataInfo),headers=headers)
        print(r.status_code)
    if r.status_code==500:
        urlUpdate=f"http://us-central1-pultemsoft.cloudfunctions.net/app/api/users"
        dataInfo = {
        "lat":lat,
        "lng":lng,
        "phone":ultima_tecla_presionada_celular,
        "temp":temperatura,
        "distance":distance,
        "Ir":ir,
        "Hr":Hr,
        "SPO2":SPO2,
        "illnesses":sintomas_data,
        "name":ultima_tecla_presionada,
        "document":ultima_tecla_presionada
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(urlUpdate,data=json.dumps(dataInfo),headers=headers)
        oled.fill(0)
        oled.blit(buscar_icono("img/pultemsoft.pbm"), 0, 0)  
        oled.text(f"Data enviada",40,10)
        oled.show()

else:
    print ("Imposible conectar")

    miRed.active (False)
    oled.fill(0)
    oled.blit(buscar_icono("img/wifi_failed.pbm"), 50, 0)
    oled.text(f'Error en la red.',0,35)
    oled.show()








