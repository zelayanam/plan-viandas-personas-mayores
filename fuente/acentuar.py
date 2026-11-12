# -*- coding: utf-8 -*-
"""Acentuación y ñ para los textos del plan.

Se aplica solo a los valores de texto (nunca a las claves internas), y usa
reemplazos de frase para los casos ambiguos (esta/está, este/esté, te/té).
"""

import re

# Casos ambiguos: se resuelven por contexto antes del diccionario.
FRASES = [
    ("Si esta muy espeso", "Si está muy espeso"),
    ("hasta que el pollo este", "hasta que el pollo esté"),
    ("hasta que este jugoso", "hasta que esté jugoso"),
    ("hasta que todo este tierno", "hasta que todo esté tierno"),
    ("hasta que este tierna", "hasta que esté tierna"),
    ("hasta que este bien caliente", "hasta que esté bien caliente"),
    ("centro este bien caliente", "centro esté bien caliente"),
    ("densidad osea", "densidad ósea"),
    ("masa osea", "masa ósea"),
    ("1 taza de te o cafe", "1 taza de té o café"),
    ("Evitar te y cafe", "Evitar té y café"),
    ("cuanto mas colorido", "cuánto más colorido"),
    ("Que necesita el cuerpo", "Qué necesita el cuerpo"),
    ("65 anos", "65 años"),
    ("los anos cambian", "los años cambian"),
    ("al ano y", "al año y"),
]

# Palabras inequívocas.
DICC = {
    "facil": "fácil", "faciles": "fáciles", "limon": "limón", "musculo": "músculo",
    "musculos": "músculos", "mas": "más", "dia": "día", "dias": "días",
    "energia": "energía", "carniceria": "carnicería", "brocoli": "brócoli",
    "corazon": "corazón", "morron": "morrón", "proteina": "proteína",
    "proteinas": "proteínas", "pure": "puré", "purees": "purés",
    "estacion": "estación", "albondigas": "albóndigas", "azucar": "azúcar",
    "colacion": "colación", "budin": "budín", "chia": "chía", "oregano": "orégano",
    "sarten": "sartén", "acompanar": "acompañar", "atun": "atún",
    "citrico": "cítrico", "citricos": "cítricos", "mediterranea": "mediterránea",
    "porcion": "porción", "miercoles": "miércoles", "sabado": "sábado",
    "rucula": "rúcula", "sandia": "sandía", "absorcion": "absorción",
    "cafe": "café", "frio": "frío", "fria": "fría", "frias": "frías",
    "hidratacion": "hidratación", "masticacion": "masticación",
    "medico": "médico", "medica": "médica", "melon": "melón", "menu": "menú",
    "menus": "menús", "segun": "según", "presion": "presión", "rinon": "riñón",
    "funcion": "función", "digestion": "digestión", "deficit": "déficit",
    "epoca": "época", "esparrago": "espárrago", "esparragos": "espárragos",
    "higado": "hígado", "hipertension": "hipertensión", "maximo": "máximo",
    "neurologica": "neurológica", "otono": "otoño", "pequena": "pequeña",
    "pequeno": "pequeño", "pimenton": "pimentón", "practico": "práctico",
    "prevencion": "prevención", "rapido": "rápido", "sensacion": "sensación",
    "tamano": "tamaño", "tambien": "también", "tuberculos": "tubérculos",
    "unico": "único", "coccion": "cocción", "deshidratacion": "deshidratación",
    "elaboracion": "elaboración", "formacion": "formación",
    "guarnicion": "guarnición", "guia": "guía", "liberacion": "liberación",
    "perdida": "pérdida", "anos": "años", "ano": "año", "manana": "mañana",
    "despues": "después", "cuanto": "cuánto", "osea": "ósea", "criticos": "críticos",
    "hermetico": "hermético", "plasticos": "plásticos", "economica": "económica",
    "economicas": "económicas", "economicos": "económicos", "fisica": "física",
    "cascara": "cáscara", "globulos": "glóbulos", "lacteos": "lácteos",
    "verduleria": "verdulería", "panaderia": "panadería", "almacen": "almacén",
    "jamon": "jamón", "pelon": "pelón", "util": "útil", "esten": "estén",
    "animo": "ánimo", "aromatico": "aromático", "caidas": "caídas",
    "cartilagos": "cartílagos", "combinacion": "combinación",
    "hinchazon": "hinchazón", "humeda": "húmeda", "humedo": "húmedo",
    "humedos": "húmedos", "proximo": "próximo", "ultimo": "último",
    "pelicula": "película", "azucares": "azúcares", "cancer": "cáncer",
    "acompanado": "acompañado", "transito": "tránsito", "acompanada": "acompañada",
}

PATRON = re.compile(r"\b(" + "|".join(sorted(DICC, key=len, reverse=True)) + r")\b", re.IGNORECASE)


def _match_case(original, reemplazo):
    if original.isupper():
        return reemplazo.upper()
    if original[:1].isupper():
        return reemplazo[:1].upper() + reemplazo[1:]
    return reemplazo


def acentuar_texto(s):
    for a, b in FRASES:
        s = s.replace(a, b)
    s = PATRON.sub(lambda m: _match_case(m.group(0), DICC[m.group(0).lower()]), s)
    s = re.sub(r"(\d+)\s*C\b", r"\1 °C", s)
    return s


# Campos que son códigos internos: no se acentúan nunca.
EXCLUIR = {"id", "tipo", "cat", "est", "beneficios", "emoji"}


def acentuar_datos(obj):
    if isinstance(obj, str):
        return acentuar_texto(obj)
    if isinstance(obj, dict):
        return {k: (v if k in EXCLUIR else acentuar_datos(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [acentuar_datos(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(acentuar_datos(v) for v in obj)
    return obj
