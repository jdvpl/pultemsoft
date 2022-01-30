
def dataOled(oled,setImage,datos):
    # tener presente que cada letra vale 8bits es decir de ancho solo caben 16 caracteres y 8 lineas de alto
    oled.fill(0)
    objeto={}
    for e in datos:
        objeto=e
        if "image" in objeto.keys():
            oled.blit(setImage(objeto["image"]),objeto["x"],objeto["y"])
        else:
            oled.text(objeto["text"],objeto["x"],objeto["y"])
            if len(objeto["text"])>16:
                print("Recuerda que por linea solo se pueden 16 caracteres")
    oled.show()