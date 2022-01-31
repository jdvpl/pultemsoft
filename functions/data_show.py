# bienvenida
bienvenido=[
        {
            "text":"Pultemsoft",
            "x":35, 
            "y":8
        },
        {
            "image":"img/pultemsoft.pbm",
            "x":0,
            "y":0
        },
        {
            "text":"Bienvenido",
            "x":35, 
            "y":16
        },
    ]

def statusIconWifi(red_wifi):
    statusIconWifi=[
        {
                "text":f"Conectando {red_wifi}...",
                "x":0, 
                "y":35
        },
        {
                "image":"img/wifi.pbm",
                "x":50, 
                "y":0
            },
    ]
    return statusIconWifi

def menuSImple(data):
    menuSImple=[
        {
                "text":f"Escribe {data}",
                "x":0, 
                "y":0
        },
        {
                "text":"Opciones:",
                "x":20, 
                "y":8
        },
        {
                "text":"A. Anular",
                "x":0, 
                "y":18
        },
        {
                "text":"B. Borrar ",
                "x":0, 
                "y":26
        },
        {
                "text":"C. Confirmar ",
                "x":0, 
                "y":34
        },
 
    ]
    return menuSImple


sintomasDataMenu=[
    {
        "text":"Sintomas:1Vomito",
        "x":0,
        "y":0
    },
    {
        "text":"2.Diarrea.3Gripa",
        "x":0,
        "y":8
    },
    {
        "text":"4.Dolor cabeza",
        "x":0,
        "y":16
    },
    {
        "text":"5.Malestar ",
        "x":0,
        "y":24
    },
    {
        "text":"6.Dolor huesos",
        "x":0,
        "y":32
    },
    {
        "text":"7.Asma.8.covid",
        "x":0,
        "y":40
    },
    {
        "text":"9.Corazon.0.Tos",
        "x":0,
        "y":48
    },
    {
        "text":"*.cancer#.Ebola",
        "x":0,
        "y":56
    },
]

acercate_termoemtro=[
    {
        "image":"img/distance.pbm",
        "x":0,
        "y":0
    },
    {
        "text":"Acercate al",
        "x":40,
        "y":8
    },
    {
        "text":"termometro",
        "x":40,
        "y":16
    },
]

def show_data_temperature(temperatura):
    show_data_temperature=[
        {
            "image":"img/termometro.pbm",
            "x":0,
            "y":0
        },
        {
            "text":"Temperatura",
            "x":40,
            "y":8
        },
        {
            "text":f"{temperatura}",
            "x":45,
            "y":16
        },
    ]
    return show_data_temperature

ritmo_cardiaco=[
    
    {
        "image":"img/pulso.pbm",
        "x":0,
        "y":0
    },
    {
        "text":"Oxigeno y",
        "x":40,
        "y":8
    },
    {
        "text":"Ritmo",
        "x":40,
        "y":16
    },
    {
        "text":"Cardiaco",
        "x":40,
        "y":24
    },
    
]

