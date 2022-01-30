# ultrasonico
from hcsr04 import HCSR04
from machine import Pin,SoftI2C,UART, Pin
# pantalla
from lib.sh1106 import SH1106_I2C

from functions.seticon import setImage
from functions.conexionWifi import conectaWifi
# api
import urequests as requests
import json
import utime

# termometro
from lib.mlx90614 import MLX90614
from functions.data_conection import red_wifi, wifi_password

from functions.keypad import initKeypad,scanKeys,teclas,tecla_Abajo
from functions.setDataOledOfKeyPad import setDataOledOfKeyPad
from functions.gps import gps
from functions.distance import distance
from functions.data_oled import dataOled
# pantalla oled
ancho=128
alto=64
i2c=SoftI2C(scl=Pin(4),sda=Pin(15),freq=100000)
oled =SH1106_I2C(ancho, alto, i2c)
# termometro
i2cTer =SoftI2C(scl=Pin(2), sda=Pin(23),freq = 100000)
sensor_temperatura = MLX90614(i2cTer)
# hcrso4
sensor_hc = HCSR04(trigger_pin=5, echo_pin=18,echo_timeout_us=1000000)

def oledStatusIcon():
    oled.fill(0)
    oled.blit(setImage("img/wifi.pbm"), 50, 0)
    oled.text(f'Conectando {red_wifi}...',0,35)
    oled.show()
    utime.sleep(3)

def oledMenu(data):
    oled.fill(0)
    oled.text(f"Escribe {data}",0,0)
    oled.text(f"Opciones: ",20,10)
    oled.text(f"A. Anular ",0,20)
    oled.text(f"B. Borrar ",0,30)
    oled.text(f"C. Confirmar ",0,40)
    oled.show()

def oledSintomas():
    oled.fill(0)
    oled.text(f"Sintomas:1Vomito",0,0)
    oled.text(f"2.Diarrea.3Gripa",0,10)
    oled.text(f"4.Dolor cabeza ",0,20)
    oled.text(f"5.Malestar.6ojos",0,30)
    oled.text(f"7.Asma.8.covid ",0,40)
    oled.text(f"9.Corazon. ",0,50)
    oled.show()



def main():
    bienvenido=[
        {
            "text":"Pultemsoft",
            "x":35, 
            "y":10
        },
        {
            "image":"img/pultemsoft.pbm",
            "x":0,
            "y":0
        }
    ]
    dataOled(oled,setImage,bienvenido)

    utime.sleep(10)
    if conectaWifi (red_wifi,wifi_password,oledStatusIcon):
        print ("Conexión exitosa!")
        # llamar funcion para leer las teclas
        initKeypad();
        # mostrar menu de la cedula
        oledMenu("Cedula") 
        # guarda lo que escribio del teclado
        cedula=setDataOledOfKeyPad(oled,scanKeys,tecla_Abajo,teclas)
        # menu del celular
        oledMenu("Celular") 
        celular=setDataOledOfKeyPad(oled,scanKeys,tecla_Abajo,teclas)
        # menu de los sintomas
        oledSintomas()
        sintomas=setDataOledOfKeyPad(oled,scanKeys,tecla_Abajo,teclas,True)
        print(sintomas,cedula,celular)
        data=gps(oled,setImage,False);
        lat=data[0]
        lng=data[1]
        print(lat,lng)
        
        distancia=distance(oled,setImage,sensor_hc)

        print(distancia)

        oled.fill(0)                    
        oled.text(f"Acercate al",0,0)
        oled.text(f"Termometro : ",0,10)
        oled.show() 
        utime.sleep(3)

        temperatura=0
        bandera_bool_temperatura=True
        while bandera_bool_temperatura:
            temperatura=sensor_temperatura.read_object_temp()
            print(temperatura)
            if temperatura >35.9 and temperatura <50:
                bandera_bool_temperatura=False
            utime.sleep(1) 

        oled.fill(0)
        oled.blit(setImage("img/termometro.pbm"), 0, 0)  
        oled.text(f"Temperatura",40,0)
        oled.text(f"{temperatura}",45,10)
        oled.show()
        utime.sleep(5)

        oled.fill(0)
        oled.blit(setImage("img/pulso.pbm"), 0, 0)  
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
                    oled.blit(setImage("img/heart.pbm"), 0, 0)  
                    oled.blit(setImage("img/oxigeno.pbm"), 98, 34)  
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
        url = f"http://us-central1-pultemsoft.cloudfunctions.net/app/api/document/{cedula}"

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
            oled.blit(setImage("img/pultemsoft.pbm"), 0, 0)  
            oled.text(f"Hola: {nombre}",40,0)
            oled.text(f"Actualizando",40,10)
            oled.show()
            utime.sleep(4)
            urlUpdate=f"http://us-central1-pultemsoft.cloudfunctions.net/app/update/document/{cedula}"
            dataInfo = {
            "lat":lat,
            "lng":lng,
            "phone":celular,
            "temp":temperatura,
            "distance":distancia,
            "Ir":ir,
            "Hr":Hr,
            "SPO2":SPO2,
            "illnesses":sintomas
            }
            headers = {"Content-Type": "application/json"}
            r = requests.put(urlUpdate,data=json.dumps(dataInfo),headers=headers)
            print(r.status_code)
        if r.status_code==500:
            urlUpdate=f"http://us-central1-pultemsoft.cloudfunctions.net/app/api/users"
            dataInfo = {
            "lat":lat,
            "lng":lng,
            "phone":celular,
            "temp":temperatura,
            "distance":distancia,
            "Ir":ir,
            "Hr":Hr,
            "SPO2":SPO2,
            "illnesses":sintomas,
            "name":cedula,
            "document":cedula
            }
            headers = {"Content-Type": "application/json"}
            r = requests.post(urlUpdate,data=json.dumps(dataInfo),headers=headers)
            oled.fill(0)
            oled.blit(setImage("img/pultemsoft.pbm"), 0, 0)  
            oled.text(f"Data enviada",40,10)
            oled.show()

    else:
        oled.fill(0)
        oled.blit(setImage("img/wifi_failed.pbm"), 50, 0)
        oled.text(f'Error en la red.',0,35)
        oled.show()


if __name__ == '__main__':
    main()
    









