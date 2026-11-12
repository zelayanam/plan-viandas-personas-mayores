# -*- coding: utf-8 -*-
"""
Base de datos del Plan de Viandas para Personas Mayores (Argentina).
Fuente unica: se usa para generar la app web, el DOCX y el XLSX.
"""

META = {
    "titulo": "Plan de Viandas para Personas Mayores",
    "subtitulo": "Dos menus semanales, recetas y cantidades para cocinar y envasar",
    "pais": "Argentina",
    "version": "1.0",
    "actualizado": "noviembre 2026",
    "perfil": "Adulto/a mayor de 65 anos, con o sin dentadura completa, actividad fisica liviana.",
    "energia_objetivo": "1.700 - 1.900 kcal/dia",
    "proteina_objetivo": "75 - 95 g/dia (1,0 a 1,2 g por kg de peso)",
    "calcio_objetivo": "1.000 - 1.200 mg/dia",
    "fibra_objetivo": "25 - 30 g/dia",
    "agua_objetivo": "6 a 8 vasos (1,5 a 2 litros) por dia, aunque no tenga sed",
}

# ---------------------------------------------------------------------------
# ESTACIONES Y PRODUCTOS DE ESTACION (hemisferio sur, Argentina)
# ---------------------------------------------------------------------------
ESTACIONES = {
    "primavera": {
        "nombre": "Primavera",
        "meses": "21 de septiembre al 20 de diciembre",
        "emoji": "🌱",
        "frutas": ["frutilla", "cereza", "durazno temprano", "pelon", "banana",
                   "naranja", "mandarina", "limon", "palta", "manzana", "pera", "kiwi"],
        "verduras": ["lechuga", "radicheta", "rucula", "espinaca", "acelga", "arvejas",
                     "habas", "alcaucil", "esparrago", "zapallito", "brocoli", "coliflor",
                     "zanahoria", "remolacha", "cebolla de verdeo", "rabanito", "papa nueva"],
        "destacados": ["arvejas frescas", "habas", "alcaucil", "esparragos", "frutillas"],
        "nota": "Temporada ideal para sumar hojas verdes y legumbres frescas. Aprovechar "
                "arvejas y habas para congelar y usar en invierno.",
    },
    "verano": {
        "nombre": "Verano",
        "meses": "21 de diciembre al 20 de marzo",
        "emoji": "☀️",
        "frutas": ["durazno", "damasco", "ciruela", "nectarina", "sandia", "melon",
                   "uva", "higo", "frutilla", "banana", "manzana", "pera"],
        "verduras": ["tomate", "berenjena", "morron", "zapallito", "zucchini", "choclo",
                     "chaucha", "pepino", "lechuga", "rucula", "albahaca", "cebolla",
                     "papa", "batata"],
        "destacados": ["tomate", "durazno", "sandia", "melon", "choclo", "zapallito"],
        "nota": "Epoca de mucha agua y fruta fresca: ayuda a la hidratacion. Cuidar la "
                "cadena de frio de las viandas mas que nunca.",
    },
    "otono": {
        "nombre": "Otono",
        "meses": "21 de marzo al 20 de junio",
        "emoji": "🍂",
        "frutas": ["manzana", "pera", "uva", "membrillo", "higo", "banana", "naranja",
                   "mandarina", "limon", "palta", "granada", "kiwi"],
        "verduras": ["zapallo", "calabaza", "batata", "papa", "choclo", "acelga",
                     "espinaca", "brocoli", "coliflor", "repollo", "zanahoria", "remolacha",
                     "puerro", "cebolla", "hongos", "berenjena"],
        "destacados": ["zapallo", "manzana", "pera", "uva", "membrillo", "hongos"],
        "nota": "Temporada de zapallos y frutas de guarda. Buen momento para sopas, "
                "purees y platos al horno, que son faciles de masticar.",
    },
    "invierno": {
        "nombre": "Invierno",
        "meses": "21 de junio al 20 de septiembre",
        "emoji": "❄️",
        "frutas": ["naranja", "mandarina", "pomelo", "limon", "kiwi", "manzana",
                   "pera", "banana", "palta"],
        "verduras": ["acelga", "espinaca", "repollo", "coliflor", "brocoli", "puerro",
                     "zapallo", "calabaza", "batata", "papa", "zanahoria", "remolacha",
                     "cebolla", "hongos", "chaucha", "arvejas"],
        "destacados": ["naranja", "mandarina", "kiwi", "puerro", "repollo", "zapallo"],
        "nota": "Los citricos aportan vitamina C, que ayuda a absorber el hierro. "
                "Sopas, guisos y purees: platos calientes, tiernos y economicos.",
    },
}

# Estacionalidad por ingrediente: reemplazo del nombre segun la estacion.
# Se usa en la app y en los documentos para mostrar la version de cada estacion.
ESTACIONAL = {
    "fruta": {
        "primavera": "frutillas y durazno",
        "verano": "durazno y sandia",
        "otono": "manzana y pera",
        "invierno": "naranja y mandarina",
    },
    "fruta2": {
        "primavera": "banana o frutillas",
        "verano": "melon o ciruela",
        "otono": "pera o uva",
        "invierno": "kiwi o mandarina",
    },
    "hojas": {
        "primavera": "lechuga, radicheta y rucula",
        "verano": "lechuga y albahaca",
        "otono": "espinaca y acelga",
        "invierno": "repollo y espinaca",
    },
    "hojas2": {
        "primavera": "espinaca fresca",
        "verano": "lechuga y rucula",
        "otono": "acelga",
        "invierno": "repollo colorado",
    },
    "verdura_horno": {
        "primavera": "zapallito y zanahoria",
        "verano": "berenjena y morron",
        "otono": "zapallo y batata",
        "invierno": "calabaza y puerro",
    },
    "verdura_salteado": {
        "primavera": "arvejas, zanahoria y cebolla de verdeo",
        "verano": "morron, zapallito y choclo",
        "otono": "brocoli, zanahoria y cebolla",
        "invierno": "repollo, zanahoria y puerro",
    },
    "verdura_sopa": {
        "primavera": "espinaca, arvejas y papa",
        "verano": "zapallito, choclo y tomate",
        "otono": "zapallo, zanahoria y puerro",
        "invierno": "calabaza, acelga y papa",
    },
    "tomate": {
        "primavera": "tomate",
        "verano": "tomate",
        "otono": "tomate",
        "invierno": "tomate (o morron asado)",
    },
    "citrico": {
        "primavera": "limon",
        "verano": "limon",
        "otono": "naranja",
        "invierno": "naranja",
    },
}

# ---------------------------------------------------------------------------
# TABLA DE COMPOSICION (por 100 g de alimento crudo, salvo indicacion)
# kcal, proteinas g, calcio mg, fibra g, hierro mg, categoria de compra, unidad
# ---------------------------------------------------------------------------
ALIMENTOS = {
    # Carnes y pescados
    "pechuga de pollo":        dict(kcal=120, p=22.5, ca=11, fb=0, fe=0.7, cat="carniceria"),
    "muslo de pollo":          dict(kcal=145, p=19.0, ca=11, fb=0, fe=0.8, cat="carniceria"),
    "carne vacuna magra":      dict(kcal=130, p=21.0, ca=12, fb=0, fe=2.5, cat="carniceria"),
    "carne picada magra":      dict(kcal=155, p=20.0, ca=12, fb=0, fe=2.4, cat="carniceria"),
    "merluza":                 dict(kcal=90,  p=18.0, ca=25, fb=0, fe=0.4, cat="carniceria"),
    "atun al natural":         dict(kcal=110, p=24.0, ca=10, fb=0, fe=1.0, cat="almacen"),
    "huevo":                   dict(kcal=143, p=12.6, ca=56, fb=0, fe=1.8, cat="lacteos", ud="u", g_ud=50),
    "jamon cocido":            dict(kcal=145, p=18.0, ca=10, fb=0, fe=0.9, cat="carniceria"),
    # Lacteos
    "leche entera":            dict(kcal=62,  p=3.3, ca=120, fb=0, fe=0.05, cat="lacteos"),
    "leche descremada":        dict(kcal=35,  p=3.4, ca=125, fb=0, fe=0.05, cat="lacteos"),
    "yogur natural":           dict(kcal=65,  p=3.5, ca=120, fb=0, fe=0.05, cat="lacteos"),
    "yogur descremado":        dict(kcal=45,  p=4.0, ca=130, fb=0, fe=0.05, cat="lacteos"),
    "queso fresco":            dict(kcal=250, p=17.0, ca=400, fb=0, fe=0.3, cat="lacteos"),
    "queso untable":           dict(kcal=240, p=6.0,  ca=100, fb=0, fe=0.1, cat="lacteos"),
    "ricota":                  dict(kcal=175, p=11.0, ca=200, fb=0, fe=0.4, cat="lacteos"),
    "queso port salut":        dict(kcal=250, p=25.0, ca=700, fb=0, fe=0.3, cat="lacteos"),
    "queso rallado":           dict(kcal=400, p=25.0, ca=1100, fb=0, fe=0.5, cat="lacteos"),
    "leche en polvo":          dict(kcal=500, p=35.0, ca=1200, fb=0, fe=0.5, cat="lacteos"),
    # Legumbres y cereales
    "lentejas secas":          dict(kcal=350, p=25.0, ca=56,  fb=11, fe=7.5, cat="almacen"),
    "garbanzos secos":         dict(kcal=360, p=20.0, ca=105, fb=12, fe=6.0, cat="almacen"),
    "arroz blanco":            dict(kcal=360, p=7.0,  ca=10,  fb=1,  fe=0.8, cat="almacen"),
    "arroz integral":          dict(kcal=350, p=7.5,  ca=15,  fb=3,  fe=2.0, cat="almacen"),
    "fideos secos":            dict(kcal=360, p=12.0, ca=20,  fb=2,  fe=1.5, cat="almacen"),
    "fideos integrales":       dict(kcal=350, p=13.0, ca=30,  fb=6,  fe=2.5, cat="almacen"),
    "pan integral":            dict(kcal=250, p=9.0,  ca=40,  fb=6,  fe=2.5, cat="panaderia"),
    "pan rallado":             dict(kcal=350, p=10.0, ca=50,  fb=3,  fe=1.5, cat="almacen"),
    "avena":                   dict(kcal=380, p=13.0, ca=54,  fb=10, fe=4.0, cat="almacen"),
    "quinoa":                  dict(kcal=370, p=14.0, ca=60,  fb=7,  fe=4.5, cat="almacen"),
    "harina integral":         dict(kcal=340, p=13.0, ca=34,  fb=10, fe=3.5, cat="almacen"),
    # Verduras
    "papa":         dict(kcal=77,  p=2.0,  ca=12,  fb=2, fe=0.8, cat="verduleria"),
    "batata":       dict(kcal=90,  p=1.6,  ca=30,  fb=3, fe=0.6, cat="verduleria"),
    "zapallo":      dict(kcal=26,  p=1.0,  ca=20,  fb=2, fe=0.8, cat="verduleria"),
    "calabaza":     dict(kcal=26,  p=1.0,  ca=20,  fb=2, fe=0.8, cat="verduleria"),
    "zanahoria":    dict(kcal=41,  p=0.9,  ca=33,  fb=3, fe=0.3, cat="verduleria"),
    "remolacha":    dict(kcal=43,  p=1.6,  ca=16,  fb=3, fe=0.7, cat="verduleria"),
    "tomate":       dict(kcal=18,  p=0.9,  ca=10,  fb=1, fe=0.3, cat="verduleria"),
    "lechuga":      dict(kcal=15,  p=1.4,  ca=36,  fb=1, fe=1.2, cat="verduleria"),
    "acelga":       dict(kcal=19,  p=1.8,  ca=51,  fb=2, fe=1.8, cat="verduleria"),
    "espinaca":     dict(kcal=23,  p=2.9,  ca=99,  fb=2, fe=2.7, cat="verduleria"),
    "brocoli":      dict(kcal=34,  p=2.8,  ca=47,  fb=3, fe=0.7, cat="verduleria"),
    "coliflor":     dict(kcal=25,  p=1.9,  ca=22,  fb=2, fe=0.4, cat="verduleria"),
    "zapallito":    dict(kcal=17,  p=1.2,  ca=16,  fb=1, fe=0.4, cat="verduleria"),
    "berenjena":    dict(kcal=25,  p=1.0,  ca=9,   fb=3, fe=0.2, cat="verduleria"),
    "morron":       dict(kcal=26,  p=1.0,  ca=7,   fb=2, fe=0.4, cat="verduleria"),
    "cebolla":      dict(kcal=40,  p=1.1,  ca=23,  fb=2, fe=0.2, cat="verduleria"),
    "puerro":       dict(kcal=61,  p=1.5,  ca=59,  fb=2, fe=2.1, cat="verduleria"),
    "arvejas":      dict(kcal=81,  p=5.4,  ca=25,  fb=5, fe=1.5, cat="verduleria"),
    "choclo":       dict(kcal=86,  p=3.3,  ca=2,   fb=3, fe=0.5, cat="verduleria"),
    "repollo":      dict(kcal=25,  p=1.3,  ca=40,  fb=3, fe=0.5, cat="verduleria"),
    "palta":        dict(kcal=160, p=2.0,  ca=12,  fb=7, fe=0.6, cat="verduleria"),
    "pepino":       dict(kcal=15,  p=0.7,  ca=16,  fb=1, fe=0.3, cat="verduleria"),
    "hongos":       dict(kcal=22,  p=3.1,  ca=3,   fb=1, fe=0.5, cat="verduleria"),
    "ajo":          dict(kcal=149, p=6.0,  ca=180, fb=2, fe=1.7, cat="verduleria"),
    "perejil":      dict(kcal=36,  p=3.0,  ca=138, fb=3, fe=6.2, cat="verduleria"),
    # Frutas
    "banana":    dict(kcal=89, p=1.1, ca=5,  fb=3, fe=0.3, cat="verduleria"),
    "manzana":   dict(kcal=52, p=0.3, ca=6,  fb=2, fe=0.1, cat="verduleria"),
    "pera":      dict(kcal=57, p=0.4, ca=9,  fb=3, fe=0.2, cat="verduleria"),
    "naranja":   dict(kcal=47, p=0.9, ca=40, fb=2, fe=0.1, cat="verduleria"),
    "mandarina": dict(kcal=53, p=0.8, ca=37, fb=2, fe=0.2, cat="verduleria"),
    "frutilla":  dict(kcal=32, p=0.7, ca=16, fb=2, fe=0.4, cat="verduleria"),
    "durazno":   dict(kcal=39, p=0.9, ca=6,  fb=2, fe=0.3, cat="verduleria"),
    "kiwi":      dict(kcal=61, p=1.1, ca=34, fb=3, fe=0.3, cat="verduleria"),
    "uva":       dict(kcal=69, p=0.7, ca=10, fb=1, fe=0.4, cat="verduleria"),
    "sandia":    dict(kcal=30, p=0.6, ca=7,  fb=0, fe=0.2, cat="verduleria"),
    "melon":     dict(kcal=34, p=0.8, ca=9,  fb=1, fe=0.2, cat="verduleria"),
    "ciruela":   dict(kcal=46, p=0.7, ca=6,  fb=1, fe=0.2, cat="verduleria"),
    "limon":     dict(kcal=29, p=1.1, ca=26, fb=3, fe=0.6, cat="verduleria"),
    # Otros
    "aceite de oliva": dict(kcal=884, p=0,   ca=0,   fb=0, fe=0, cat="almacen"),
    "aceite":          dict(kcal=884, p=0,   ca=0,   fb=0, fe=0, cat="almacen"),
    "nueces":          dict(kcal=654, p=15.0, ca=98,  fb=7, fe=2.9, cat="almacen"),
    "almendras":       dict(kcal=579, p=21.0, ca=269, fb=13, fe=3.7, cat="almacen"),
    "chia":            dict(kcal=486, p=17.0, ca=631, fb=34, fe=7.7, cat="almacen"),
    "miel":            dict(kcal=304, p=0.3, ca=6,   fb=0, fe=0.4, cat="almacen"),
    "mermelada":       dict(kcal=250, p=0.4, ca=20,  fb=1, fe=0.3, cat="almacen"),
    "caldo de verduras": dict(kcal=10, p=0.5, ca=5,  fb=0, fe=0.1, cat="almacen"),
    "sal":             dict(kcal=0, p=0, ca=0, fb=0, fe=0, cat="almacen"),
    "pimienta":        dict(kcal=251, p=10, ca=440, fb=25, fe=9.7, cat="almacen"),
    "oregano":         dict(kcal=265, p=9, ca=1600, fb=43, fe=36.8, cat="almacen"),
    "comino":          dict(kcal=375, p=18, ca=931, fb=11, fe=66.4, cat="almacen"),
    "canela":          dict(kcal=247, p=4, ca=1002, fb=53, fe=8.3, cat="almacen"),
    "curry":           dict(kcal=325, p=14, ca=525, fb=33, fe=19.1, cat="almacen"),
    "vainillas":       dict(kcal=400, p=7, ca=30, fb=1, fe=2, cat="almacen"),
    "masa para tarta": dict(kcal=330, p=8, ca=30, fb=2, fe=1.5, cat="almacen"),
    "levadura":        dict(kcal=105, p=12, ca=30, fb=6, fe=2, cat="almacen"),
    "azucar":          dict(kcal=400, p=0, ca=0, fb=0, fe=0, cat="almacen"),
}

# Ingredientes que se compran por unidad (huevos)
UNIDADES = {"huevo": ("unidad", 50)}
