from machine import Pin
# teclado
tecla_Arriba=const(0) #apagado
tecla_Abajo=const(1) #encendido
# teclado
teclas=[
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D'],
    ]

# pines usado para las filas
# config del teclado
#se conecta a estos pines para la funcionalidad del teclado
filas=[13,12,14,27]
columnas=[26,25,33,32]
fila_pines=[Pin(nombre_pin, Pin.OUT) for nombre_pin in filas]
columna_pines=[Pin(nombre_pin, Pin.IN,Pin.PULL_DOWN) for nombre_pin in columnas]


# variables

# funcion para recorrer el arreglo de los pines
def initKeypad():
    for fila in range(0,4):
        for columna in range(0,4):
            fila_pines[fila].on()

# esclanea el valor que se usa
def scanKeys(fila, columna):
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