
import utime

def setDataOledOfKeyPad(oledsh,scanKeys,tecla_Abajo,teclas,arreglo=False):
    tecla_presionada_bool=True
    data_teclado=''
    sintomas=[]
    sintomas_data = []
    while tecla_presionada_bool:
        for fila in range(4):
            for columna in range(4):
                tecla=scanKeys(fila,columna)
                if tecla==tecla_Abajo:
                    utime.sleep(0.2)
                    datatecla=teclas[fila][columna]
                    data_teclado+=datatecla
                    if datatecla=="A":
                        data_teclado=""
                    if datatecla=="B":
                        data_teclado=data_teclado.rstrip(data_teclado[-1])
                        if len(data_teclado)>1:
                            data_teclado=data_teclado.rstrip(data_teclado[-1])
                    if datatecla=="C":
                        data_teclado=data_teclado.rstrip(data_teclado[-1])
                        tecla_presionada_bool=False 
                        break
                    if arreglo:
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
                            sintomas.append("Dolor huesos ")
                        if datatecla=="7":
                            sintomas.append("Asma ")
                        if datatecla=="8":
                            sintomas.append("Covid ")
                        if datatecla=="9":
                            sintomas.append("Corazon ")
                        if datatecla=="0":
                            sintomas.append("Tos ")
                        if datatecla=="*":
                            sintomas.append("Cancer ")
                        if datatecla=="#":
                            sintomas.append("Ebola ")
                    oledsh.fill(0)
                    oledsh.text(data_teclado,0,0)
                    oledsh.show()
    if arreglo==False:
        return data_teclado
    else:
        for item in sintomas:
            if item not in sintomas_data:
                sintomas_data.append(item)
        return sintomas_data
