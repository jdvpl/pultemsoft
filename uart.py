from machine import UART,Pin
import utime

uartRitmo = UART(2, 115200)                        
uartRitmo.init(baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=21)


data=None;
red=0
ir=0
Hr=0
HrValid=0
SPO2=0
SPO2Valid=0
Pultem_bool=True
while Pultem_bool:
    data=uartRitmo.read()
    print(data)
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
            if SPO2Valid==1 and HrValid==1:
                if SPO2>40 and SPO2<=100:
                    if Hr>30 and Hr<=200:
                        Pultem_bool=False
            print(cadena)
    utime.sleep(1)
