from machine import Pin
from time import sleep

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

print("Esperando a que pulse una tecla")

init()

while True:
    for fila in range(4):
        for columna in range(4):
            tecla=scan(fila,columna)
            if tecla==tecla_Abajo:
                print("Tecla presionada", teclas[fila][columna])
                sleep(0.5)
                ultima_tecla_presionada=teclas[fila][columna]