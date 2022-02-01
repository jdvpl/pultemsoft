# ultrasonico
from machine import Pin,SoftI2C,UART, Pin
# librerias
from lib.sh1106 import SH1106_I2C
from lib.mlx90614 import MLX90614
from hcsr04 import HCSR04
from lib.utelegram import Bot
# api
import urequests as requests
import json
import utime
# termometro
from functions.data_conection import red_wifi, wifi_password
from functions.keypad import initKeypad,scanKeys,teclas,tecla_Abajo
from functions.setDataOledOfKeyPad import setDataOledOfKeyPad
from functions.gps import gps
from functions.distance import distance
from functions.data_oled import dataOled
from functions.conexionWifi import conectaWifi
from functions.seticon import setImage
from functions.temperature import temperature
from functions.oximetro import oximetro
import _thread
# textos de la pantalla
from functions.data_show import bienvenido,statusIconWifi,menuSImple, sintomasDataMenu,acercate_termoemtro,show_data_temperature,ritmo_cardiaco
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


time_icon=3

# telegram
TOKEN = '5244470667:AAFyUIccWiW2nbF4DgKH1CoTnFOEbtfieSY'
bot = Bot(TOKEN)

def oledStatusIcon():
    dataOled(oled,setImage,statusIconWifi(red_wifi))
    utime.sleep(time_icon)

def main():
    dataOled(oled,setImage,bienvenido)
    utime.sleep(time_icon)

    if conectaWifi (red_wifi,wifi_password,oledStatusIcon):
        print ("Conexión exitosa!")

        initKeypad()
        def askCedula():
            # llamar funcion para leer las teclas
            # mostrar menu de la cedula
            dataOled(oled,setImage,menuSImple("cedula")) 
            # guarda lo que escribio del teclado
            cedula=setDataOledOfKeyPad(oled,scanKeys,tecla_Abajo,teclas)
            return cedula
        def askCelular():
            # menu del celular
            dataOled(oled,setImage,menuSImple("celular")) 
            celular=setDataOledOfKeyPad(oled,scanKeys,tecla_Abajo,teclas)
            return celular
        
        def askSintomas():
            # menu de los sintomas
            dataOled(oled,setImage,sintomasDataMenu) 
            sintomas=setDataOledOfKeyPad(oled,scanKeys,tecla_Abajo,teclas,True)
            return sintomas

        def gepData():
            data=gps(oled,setImage,False);
            return data
            
        
        def distanciaOled():
            dataOled(oled,setImage,acercate_termoemtro)
            distancia=distance(oled,setImage,sensor_hc)
            return distancia
            # texto de acercarse

        def askTemperatura():
            # temperatura
            temperatura=temperature(sensor_temperatura)
            dataOled(oled,setImage,show_data_temperature(temperatura));
            utime.sleep(time_icon)
            return temperatura
        
        def oximetroSpo2():
            # ole ritmo cardiaco
            dataOled(oled,setImage,ritmo_cardiaco);
            utime.sleep(time_icon)
            dataOxime=oximetro(oled,setImage)
            return dataOxime
        
        def telegramBot():
            @bot.add_message_handler('Start')
            def help(update):
                update.reply('Escribir las siguientes opciones:\n/Cedula\n/Celular\n/Temperatura\n/Sintomas\n/Oxigeno\n/ubicacion')

            @bot.add_message_handler('Cedula')
            def Cedula(update):
                update.reply(askCedula)

            @bot.add_message_handler('Celular')
            def Celular(update):
                update.reply(askCelular)

            @bot.add_message_handler('Temperatura')
            def Temperatura(update):
                update.reply(askTemperatura)

            @bot.add_message_handler('Sintomas')
            def Sintomas(update):
                update.reply(askSintomas)

            @bot.add_message_handler('Oxigeno')
            def Oxigeno(update):
                update.reply(askSintomas)

            @bot.add_message_handler('Ubicacion')
            def Ubicacion(update):
                update.reply(gepData)
            bot.start_loop()
        
            
        def getAllData():
            cedula=askCedula()
            celular=askCelular()
            sintomas=askSintomas()
            data=gepData()
            lat=data[0]
            lng=data[1]
            distancia=distanciaOled()
            temperatura=askTemperatura()
            dataOxime=oximetroSpo2()
            SPO2=dataOxime[0]
            Hr=dataOxime[1]
            ir=dataOxime[2]


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
            SPO2=f"{SPO2}% "
            Hr=f"{Hr} BPM"
            url = f"http://us-central1-pultemsoft.cloudfunctions.net/app/api/document/{cedula}"

            r = requests.get(url)

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
                "temp":str(temperatura),
                "distance":distancia,
                "ir":ir,
                "hr":Hr,
                "spo2":SPO2,
                "illnesses":sintomas
                }
                headers = {"Content-Type": "application/json"}
                r = requests.put(urlUpdate,data=json.dumps(dataInfo),headers=headers)
                latitud=f"{lat} | {lng}"
                oxigeno_bpm=f"{SPO2} | {Hr} | {temperatura}"
                data_doc=f"{cedula} | {celular} | {sintomas}"
                urlSheet = "https://maker.ifttt.com/trigger/pultemsodft_data/with/key/cYDCD02FxQbe-weUclU0OpIc6yi5MfmT5bOdPLt6LO3?"
                respuesta = requests.get(urlSheet+"&value1="+str(latitud)+"&value2="+str(oxigeno_bpm)+"&value3="+str(data_doc))  
                print(respuesta.text)

            if r.status_code==500:
                urlUpdate=f"http://us-central1-pultemsoft.cloudfunctions.net/app/api/users"
                dataInfo = {
                "lat":lat,
                "lng":lng,
                "phone":celular,
                "temp":str(temperatura),
                "distance":distancia,
                "ir":ir,
                "hr":Hr,
                "spo2":SPO2,
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
                latitud=f"{lat} | {lng}"
                oxigeno_bpm=f"{SPO2} | {Hr} | {temperatura}"
                data_doc=f"{cedula} | {celular} | {sintomas}"
                urlSheet = "https://maker.ifttt.com/trigger/pultemsodft_data/with/key/cYDCD02FxQbe-weUclU0OpIc6yi5MfmT5bOdPLt6LO3?"
                respuesta = requests.get(urlSheet+"&value1="+str(latitud)+"&value2="+str(oxigeno_bpm)+"&value3="+str(data_doc))  
                print(respuesta.text)

        getAllData()
        _thread.start_new_thread(telegramBot(), ())
   

    else:
        oled.fill(0)
        oled.blit(setImage("img/wifi_failed.pbm"), 50, 0)
        oled.text(f'Error en la red.',0,35)
        oled.show()


if __name__ == '__main__':
    main()
    









