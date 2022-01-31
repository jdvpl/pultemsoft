
import utime

def temperature(sensor_temperatura):
    temperatura=0
    bandera_bool_temperatura=True
    while bandera_bool_temperatura:
        temperatura=sensor_temperatura.read_object_temp()
        print(temperatura)
        if temperatura >35.9 and temperatura <50:
            bandera_bool_temperatura=False
        utime.sleep(1)
    return temperatura