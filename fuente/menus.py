# -*- coding: utf-8 -*-
"""Menus semanales, guias y recomendaciones."""

# Tomas del dia
TOMAS = [
    ("desayuno", "Desayuno", "7:30"),
    ("colacion", "Colación", "10:30"),
    ("almuerzo", "Almuerzo", "12:30"),
    ("merienda", "Merienda", "16:30"),
    ("cena", "Cena", "20:00"),
]

MENUS = {
    "A": {
        "nombre": "Menu A",
        "lema": "Sabores de casa",
        "descripcion": "Cocina casera argentina, con platos de olla, horno y guisos. "
                       "Prioriza preparaciones tiernas, economicas y faciles de recalentar.",
        "temporadas": {
            "invierno": {
                "descripcion": "Platos de olla y horno, con legumbres y carnes magras. Rinde para varios dias.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_pan_queso", colacion="col_fruta_nueces",
                         almuerzo="pollo_horno_batata", merienda="mer_yogur_avena", cena="tortilla_acelga"),
                    dict(dia="Martes", desayuno="des_avena", colacion="col_yogur_avena",
                         almuerzo="guiso_lentejas", merienda="mer_tostadas_queso", cena="merluza_pure_calabaza"),
                    dict(dia="Miercoles", desayuno="des_yogur_fruta", colacion="col_pan_queso",
                         almuerzo="albondigas_arroz", merienda="mer_palta", cena="sopa_verduras_huevo"),
                    dict(dia="Jueves", desayuno="des_huevo_tomate", colacion="col_huevo_zanahoria",
                         almuerzo="milanesa_pollo_horno", merienda="mer_budin_banana", cena="revuelto_zapallitos"),
                    dict(dia="Viernes", desayuno="des_licuado", colacion="col_citrico_almendras",
                         almuerzo="tarta_acelga_ricota", merienda="mer_yogur_avena", cena="salteado_pollo_arroz"),
                    dict(dia="Sabado", desayuno="des_pan_queso", colacion="col_queso_pera",
                         almuerzo="merluza_papas_horno", merienda="mer_leche_vainillas", cena="sopa_lentejas"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="carne_horno_ensalada_papa", merienda="mer_tostadas_queso", cena="zapallitos_rellenos"),
                ],
            },
            "otono": {
                "descripcion": "Horno moderado y guisos livianos, con zapallo y manzana de la temporada.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_pan_queso", colacion="col_fruta_nueces",
                         almuerzo="pollo_horno_batata", merienda="mer_yogur_avena", cena="tortilla_acelga"),
                    dict(dia="Martes", desayuno="des_avena", colacion="col_yogur_avena",
                         almuerzo="guiso_lentejas", merienda="mer_tostadas_queso", cena="v_caprese"),
                    dict(dia="Miercoles", desayuno="des_yogur_fruta", colacion="col_pan_queso",
                         almuerzo="albondigas_arroz", merienda="mer_palta", cena="sopa_verduras_huevo"),
                    dict(dia="Jueves", desayuno="des_huevo_tomate", colacion="col_huevo_zanahoria",
                         almuerzo="milanesa_pollo_horno", merienda="mer_budin_banana", cena="v_ensalada_lentejas"),
                    dict(dia="Viernes", desayuno="des_licuado", colacion="col_citrico_almendras",
                         almuerzo="tarta_acelga_ricota", merienda="mer_yogur_avena", cena="salteado_pollo_arroz"),
                    dict(dia="Sabado", desayuno="des_pan_queso", colacion="col_queso_pera",
                         almuerzo="merluza_papas_horno", merienda="mer_leche_vainillas", cena="sopa_lentejas"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="carne_horno_ensalada_papa", merienda="mer_tostadas_queso", cena="zapallitos_rellenos"),
                ],
            },
            "primavera": {
                "descripcion": "Arvejas, esparragos y hojas tiernas, con coccion al vapor o plancha.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_pan_queso", colacion="col_fruta_nueces",
                         almuerzo="p_pollo_plancha", merienda="mer_yogur_avena", cena="p_arvejas_huevo"),
                    dict(dia="Martes", desayuno="des_avena", colacion="col_yogur_avena",
                         almuerzo="p_esparragos_huevo", merienda="mer_palta", cena="sopa_verduras_huevo"),
                    dict(dia="Miercoles", desayuno="des_yogur_fruta", colacion="col_pan_queso",
                         almuerzo="v_ensalada_pollo_quinoa", merienda="mer_tostadas_queso", cena="p_sopa_arvejas"),
                    dict(dia="Jueves", desayuno="des_huevo_tomate", colacion="col_huevo_zanahoria",
                         almuerzo="p_tarta_zapallito_fria", merienda="mer_budin_banana", cena="v_ensalada_lentejas"),
                    dict(dia="Viernes", desayuno="des_licuado", colacion="col_citrico_almendras",
                         almuerzo="v_ensalada_atun_garbanzos", merienda="mer_palta", cena="v_tortilla_zapallito_plancha"),
                    dict(dia="Sabado", desayuno="des_pan_queso", colacion="col_queso_pera",
                         almuerzo="merluza_papas_horno", merienda="mer_leche_vainillas", cena="v_gazpacho_huevo"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="pollo_horno_batata", merienda="mer_tostadas_queso", cena="v_sandwich_pollo"),
                ],
            },
            "verano": {
                "descripcion": "Ensaladas completas, platos frios y gazpacho. Nada de horno.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_yogur_fruta", colacion="col_fruta_nueces",
                         almuerzo="v_ensalada_pollo_quinoa", merienda="v_ensalada_frutas", cena="v_gazpacho_huevo"),
                    dict(dia="Martes", desayuno="des_licuado", colacion="col_yogur_avena",
                         almuerzo="v_ensalada_atun_garbanzos", merienda="mer_palta", cena="v_caprese"),
                    dict(dia="Miercoles", desayuno="des_avena", colacion="col_pan_queso",
                         almuerzo="v_wrap_pollo", merienda="v_ensalada_frutas", cena="v_ensalada_lentejas"),
                    dict(dia="Jueves", desayuno="des_huevo_tomate", colacion="col_huevo_zanahoria",
                         almuerzo="v_merluza_limon_papa", merienda="mer_yogur_avena", cena="v_tartar_tomate_palta"),
                    dict(dia="Viernes", desayuno="des_yogur_fruta", colacion="col_citrico_almendras",
                         almuerzo="v_pollo_vapor", merienda="mer_palta", cena="v_tortilla_zapallito_plancha"),
                    dict(dia="Sabado", desayuno="des_licuado", colacion="col_queso_pera",
                         almuerzo="v_ensalada_arroz_atun", merienda="mer_leche_vainillas", cena="v_sandwich_pollo"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="v_ensalada_quinoa_verduras", merienda="v_ensalada_frutas", cena="v_ensalada_papa_huevo"),
                ],
            },
        },
    },
    "B": {
        "nombre": "Menu B",
        "lema": "Cocina mediterranea",
        "descripcion": "Mas pescado, legumbres y verduras, con aceite de oliva como grasa principal. "
                       "Platos frescos y coloridos, con opciones que se adaptan a cada estacion.",
        "temporadas": {
            "invierno": {
                "descripcion": "Pescado, legumbres y horno, con mas verduras y aceite de oliva.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_yogur_fruta", colacion="col_fruta_nueces",
                         almuerzo="merluza_mediterranea", merienda="mer_palta", cena="tortilla_espinaca"),
                    dict(dia="Martes", desayuno="des_huevo_tomate", colacion="col_citrico_almendras",
                         almuerzo="pollo_curry", merienda="mer_yogur_avena", cena="sopa_zapallo"),
                    dict(dia="Miercoles", desayuno="des_avena", colacion="col_pan_queso",
                         almuerzo="ensalada_garbanzos_atun", merienda="mer_budin_banana", cena="budin_verduras"),
                    dict(dia="Jueves", desayuno="des_licuado", colacion="col_queso_pera",
                         almuerzo="carne_salteada_fideos", merienda="mer_tostadas_queso", cena="tortilla_papa_horno"),
                    dict(dia="Viernes", desayuno="des_pan_queso", colacion="col_yogur_avena",
                         almuerzo="merluza_pure_espinaca", merienda="mer_palta", cena="arroz_pollo_wok"),
                    dict(dia="Sabado", desayuno="des_yogur_fruta", colacion="col_huevo_zanahoria",
                         almuerzo="guiso_garbanzos", merienda="mer_leche_vainillas", cena="tarta_puerro"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="pollo_relleno_quinoa", merienda="mer_budin_banana", cena="sopa_calabaza"),
                ],
            },
            "otono": {
                "descripcion": "Pescado, legumbres y horno moderado, con ensaladas para los dias templados.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_yogur_fruta", colacion="col_fruta_nueces",
                         almuerzo="merluza_mediterranea", merienda="mer_palta", cena="tortilla_espinaca"),
                    dict(dia="Martes", desayuno="des_huevo_tomate", colacion="col_citrico_almendras",
                         almuerzo="pollo_curry", merienda="mer_yogur_avena", cena="sopa_zapallo"),
                    dict(dia="Miercoles", desayuno="des_avena", colacion="col_pan_queso",
                         almuerzo="ensalada_garbanzos_atun", merienda="mer_budin_banana", cena="budin_verduras"),
                    dict(dia="Jueves", desayuno="des_licuado", colacion="col_queso_pera",
                         almuerzo="carne_salteada_fideos", merienda="mer_tostadas_queso", cena="v_ensalada_papa_huevo"),
                    dict(dia="Viernes", desayuno="des_pan_queso", colacion="col_yogur_avena",
                         almuerzo="merluza_pure_espinaca", merienda="mer_palta", cena="arroz_pollo_wok"),
                    dict(dia="Sabado", desayuno="des_yogur_fruta", colacion="col_huevo_zanahoria",
                         almuerzo="guiso_garbanzos", merienda="mer_leche_vainillas", cena="tarta_puerro"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="pollo_relleno_quinoa", merienda="mer_budin_banana", cena="sopa_calabaza"),
                ],
            },
            "primavera": {
                "descripcion": "Pescado, esparragos y ensaladas completas. Coccion al vapor y plancha.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_yogur_fruta", colacion="col_fruta_nueces",
                         almuerzo="p_esparragos_huevo", merienda="mer_palta", cena="p_arvejas_huevo"),
                    dict(dia="Martes", desayuno="des_huevo_tomate", colacion="col_citrico_almendras",
                         almuerzo="v_ensalada_quinoa_verduras", merienda="mer_yogur_avena", cena="p_sopa_arvejas"),
                    dict(dia="Miercoles", desayuno="des_avena", colacion="col_pan_queso",
                         almuerzo="p_pollo_plancha", merienda="mer_budin_banana", cena="v_caprese"),
                    dict(dia="Jueves", desayuno="des_licuado", colacion="col_queso_pera",
                         almuerzo="v_wrap_pollo", merienda="mer_tostadas_queso", cena="p_tarta_zapallito_fria"),
                    dict(dia="Viernes", desayuno="des_pan_queso", colacion="col_yogur_avena",
                         almuerzo="merluza_mediterranea", merienda="mer_palta", cena="v_ensalada_papa_huevo"),
                    dict(dia="Sabado", desayuno="des_yogur_fruta", colacion="col_huevo_zanahoria",
                         almuerzo="v_ensalada_pollo_quinoa", merienda="mer_leche_vainillas", cena="v_gazpacho_huevo"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="pollo_relleno_quinoa", merienda="mer_budin_banana", cena="v_ensalada_lentejas"),
                ],
            },
            "verano": {
                "descripcion": "Pescado al vapor, ensaladas y platos frios. Sin horno.",
                "dias": [
                    dict(dia="Lunes", desayuno="des_yogur_fruta", colacion="col_fruta_nueces",
                         almuerzo="v_ensalada_atun_garbanzos", merienda="v_ensalada_frutas", cena="v_caprese"),
                    dict(dia="Martes", desayuno="des_licuado", colacion="col_yogur_avena",
                         almuerzo="v_pollo_vapor", merienda="mer_palta", cena="v_gazpacho_huevo"),
                    dict(dia="Miercoles", desayuno="des_avena", colacion="col_pan_queso",
                         almuerzo="v_ensalada_pollo_quinoa", merienda="mer_yogur_avena", cena="v_ensalada_lentejas"),
                    dict(dia="Jueves", desayuno="des_huevo_tomate", colacion="col_citrico_almendras",
                         almuerzo="v_merluza_limon_papa", merienda="mer_palta", cena="v_tartar_tomate_palta"),
                    dict(dia="Viernes", desayuno="des_yogur_fruta", colacion="col_huevo_zanahoria",
                         almuerzo="v_wrap_pollo", merienda="mer_leche_vainillas", cena="v_sopa_melon"),
                    dict(dia="Sabado", desayuno="des_licuado", colacion="col_queso_pera",
                         almuerzo="v_ensalada_arroz_atun", merienda="v_ensalada_frutas", cena="v_sandwich_pollo"),
                    dict(dia="Domingo", desayuno="des_avena", colacion="col_fruta_nueces",
                         almuerzo="v_salpicon_pollo", merienda="mer_yogur_avena", cena="v_ensalada_papa_huevo"),
                ],
            },
        },
    },
}

# ---------------------------------------------------------------------------
# RECOMENDACIONES NUTRICIONALES (marco argentino)
# ---------------------------------------------------------------------------
NUTRICION = {
    "titulo": "Que necesita el cuerpo a esta edad",
    "intro": "Con los anos cambian la masa muscular, la densidad osea, la sed, el gusto y la "
             "digestion. El plan cubre los nutrientes criticos con platos cotidianos, "
             "texturas tiernas y porciones realistas.",
    "claves": [
        dict(nutriente="Proteinas", meta="75 - 95 g por dia (1,0 a 1,2 g/kg)",
             para="Frenar la perdida de masa muscular (sarcopenia) y sostener las defensas.",
             fuentes="Huevo, pollo, carne magra, pescado, leche, yogur, queso, legumbres, quinoa.",
             como="Repartir proteina en las 5 tomas: no sirve concentrarla toda en el almuerzo. "
                   "Cada comida principal lleva 20-30 g."),
        dict(nutriente="Calcio", meta="1.000 - 1.200 mg por dia",
             para="Mantener la densidad osea y prevenir osteoporosis y fracturas.",
             fuentes="Leche, yogur, quesos, ricota, sardinas, hojas verdes, almendras, chia.",
             como="2 a 3 lacteos por dia + verduras de hoja. La vitamina D (sol) es necesaria "
                   "para absorberlo: consultar al medico si hay indicacion de suplemento."),
        dict(nutriente="Vitamina D", meta="Segun indicacion medica (habitualmente 800-1.000 UI)",
             para="Absorcion de calcio, fuerza muscular y prevencion de caidas.",
             fuentes="Sol (15-20 min al dia), pescados grasos, huevo, lacteos fortificados.",
             como="En Argentina muchas personas mayores tienen deficit: conviene controlar en "
                   "sangre una vez al ano y suplementar solo con indicacion profesional."),
        dict(nutriente="Fibra", meta="25 - 30 g por dia",
             para="Regular el intestino, controlar el colesterol y la glucemia.",
             fuentes="Verduras, frutas con cascara, legumbres, cereales integrales, avena, ciruelas.",
             como="Aumentar de a poco y acompanar con agua, para evitar hinchazon."),
        dict(nutriente="Hierro", meta="8 - 10 mg por dia",
             para="Evitar anemia y cansancio. El hierro vegetal se absorbe mejor con vitamina C.",
             fuentes="Carne magra, hígado (ocasional), legumbres, espinaca, acelga.",
             como="Legumbres con citricos o tomate en la misma comida. Evitar te y cafe justo "
                   "despues de comer: dificultan la absorcion."),
        dict(nutriente="Vitamina B12", meta="2,4 microgramos por dia",
             para="Funcion neurologica y formacion de globulos rojos.",
             fuentes="Carnes, pescado, huevo, lacteos.",
             como="Quienes comen poca carne o tienen problemas de absorcion pueden necesitar "
                   "control y suplemento indicado por el medico."),
        dict(nutriente="Omega 3", meta="2 porciones de pescado por semana",
             para="Proteger el corazon, las articulaciones y el cerebro.",
             fuentes="Merluza, caballa, sardinas, atun, nueces, chia, lino.",
             como="El plan incluye pescado 2-3 veces por semana y frutos secos en colaciones."),
        dict(nutriente="Agua", meta="1,5 a 2 litros por dia (6-8 vasos)",
             para="Evitar deshidratacion: con la edad disminuye la sensacion de sed.",
             fuentes="Agua, infusiones, sopas, frutas, verduras.",
             como="Ofrecer agua cada 2 horas, aunque no pida. En verano, mas. Evitar bebidas "
                   "azucaradas y limitar el alcohol."),
        dict(nutriente="Sodio (sal)", meta="Menos de 5 g de sal por dia",
             para="Controlar la presion arterial y cuidar el rinon y el corazon.",
             fuentes="Sal de mesa, embutidos, quesos duros, caldos, enlatados, pan.",
             como="Condimentar con limon, ajo, perejil, oregano y comino. Leer las etiquetas."),
        dict(nutriente="Potasio", meta="3.500 mg por dia (si el rinon lo permite)",
             para="Presion arterial y funcion muscular.",
             fuentes="Banana, papa, batata, zapallo, tomate, palta, naranja, hojas verdes.",
             como="Si hay enfermedad renal, consultar por las porciones de estos alimentos."),
    ],
    "plato": {
        "titulo": "El plato saludable",
        "items": [
            ("1/2 plato", "Verduras de estacion, crudas o cocidas", "Fibra, vitaminas, minerales y agua."),
            ("1/4 plato", "Proteinas: pollo, carne magra, pescado, huevo o legumbres", "Masa muscular y saciedad."),
            ("1/4 plato", "Cereales o tuberculos: arroz, fideos, papa, batata, quinoa", "Energia de liberacion lenta."),
            ("+ 1 cda", "Aceite de oliva crudo o frutos secos", "Grasas buenas para el corazon."),
            ("+ agua", "1 vaso de agua o infusion sin azucar", "Hidratacion."),
        ],
    },
}

GAPA = [
    "Comer con variedad: cuanto mas colorido el plato, mas nutrientes.",
    "Hacer 4 comidas principales y 1 o 2 colaciones; no saltear el desayuno.",
    "Incluir una porcion de proteina en cada comida principal.",
    "Consumir 5 porciones diarias entre frutas y verduras de estacion.",
    "Usar legumbres al menos 2 veces por semana y pescado 2 veces por semana.",
    "Preferir cereales integrales y aceite de oliva crudo.",
    "Tomar 6 a 8 vasos de agua por dia, aunque no haya sed.",
    "Reducir sal, azucar y productos ultraprocesados (galletitas, embutidos, gaseosas).",
    "Mantener actividad fisica adaptada: caminar, fuerza con bandas o botellas, equilibrio.",
    "Tomar sol 15-20 minutos por dia y controlar vitamina D y calcio con el medico.",
]

GUIA_VIANDAS = {
    "titulo": "Guia para preparar y conservar las viandas",
    "secciones": [
        dict(titulo="1. Organizar la semana", icono="📅", items=[
            "Elegir el menu y calcular porciones: 1 envase = 1 porcion de adulto.",
            "Cocinar 2 o 3 preparaciones base el domingo (pollo, guiso, tarta) y completar el resto fresco.",
            "Lavar y cortar verduras el mismo dia que se compran; guardarlas secas y tapadas.",
            "Rotular cada envase con el nombre del plato y la fecha de elaboracion.",
        ]),
        dict(titulo="2. Envases seguros", icono="🥡", items=[
            "Usar envases de vidrio templado o plasticos libres de BPA, con cierre hermetico.",
            "Preferir porciones individuales: se descongela solo lo que se va a comer.",
            "Evitar envases descartables finos para recalentar: pueden deformarse o liberar sustancias.",
            "Dejar 2 cm libres si se va a congelar: el alimento se expande.",
            "Separar los componentes humedos (salsa, ensalada) de los secos (arroz, pan).",
        ]),
        dict(titulo="3. Cadena de frio", icono="🧊", items=[
            "Enfriar la comida a temperatura ambiente como maximo 2 horas antes de tapar y refrigerar.",
            "Guardar en heladera a 4 C o menos; en el freezer a -18 C.",
            "Consumir las viandas refrigeradas dentro de 3 dias.",
            "Descongelar siempre en la heladera, nunca a temperatura ambiente.",
            "No recalentar dos veces el mismo plato.",
        ]),
        dict(titulo="4. Recalentar bien", icono="🔥", items=[
            "Microondas: destapar, agregar 1 cda de agua, calentar 2-3 minutos y revolver a mitad.",
            "Olla o sarten: fuego bajo con un chorrito de agua, revolviendo, hasta que este bien caliente.",
            "Horno: 15 minutos a 180 C para tartas, milanesas y platos gratinados.",
            "Verificar que el centro este bien caliente (vapor), no solo la superficie.",
            "Dejar reposar 1 minuto antes de comer para evitar quemaduras.",
        ]),
        dict(titulo="5. Texturas seguras", icono="🥄", items=[
            "Cortar carnes en tiras finas contra la fibra y eliminar huesos, espinas y cartilagos.",
            "Ofrecer verduras cocidas o ralladas si hay dificultad para masticar.",
            "Humedecer con salsa, caldo o leche los platos que quedan secos.",
            "Evitar frutos secos enteros y uvas enteras si hay riesgo de atragantamiento: picar o rallar.",
            "Cuchillo y tenedor con mango grueso, vasos livianos y platos con borde alto.",
        ]),
        dict(titulo="6. Seguridad alimentaria", icono="🧼", items=[
            "Lavarse las manos antes y despues de manipular alimentos.",
            "Cocinar completamente pollo, huevo y pescado.",
            "No descongelar y volver a congelar un plato ya descongelado.",
            "Revisar olor, color y textura antes de consumir: ante la duda, descartar.",
            "Mantener la heladera limpia y separar carnes crudas de alimentos cocidos.",
        ]),
    ],
    "congelado": [
        ("Guisos y sopas", "3 meses", "En porciones; descongelar en heladera."),
        ("Pollo cocido", "2 meses", "En su jugo o salsa para que no se seque."),
        ("Tartas y budines", "2 meses", "Cortados en porciones individuales."),
        ("Albondigas", "2 meses", "Con salsa; recalentar a fuego bajo."),
        ("Pescado cocido", "1 mes", "Mejor consumirlo fresco; no recalentar dos veces."),
        ("Pure de papa", "1 mes", "Agregar leche al recalentar."),
    ],
}

TIPS_VIANDA = [
    dict(titulo="Una comida, un envase", texto="Armar la vianda como un plato: proteina, "
         "guarnicion y verdura juntas. Si la ensalada es cruda, llevarla aparte."),
    dict(titulo="El aceite, al final", texto="Agregar el aceite de oliva crudo al servir: "
         "conserva sus propiedades y realza el sabor sin necesidad de mas sal."),
    dict(titulo="Sabor sin sal", texto="Limon, ajo, perejil, oregano, comino, pimenton y "
         "vinagre dan sabor sin subir la presion arterial."),
    dict(titulo="Comer acompanado", texto="Compartir la mesa mejora el apetito y el animo. "
         "Si se come solo, poner la mesa, la radio o una llamada."),
    dict(titulo="Porciones que se ven", texto="Servir porciones chicas y repetir si hace falta: "
         "un plato abundante desanima a quien tiene poco apetito."),
    dict(titulo="Postre con fruta", texto="Terminar con fruta de estacion o un yogur: suma "
         "calcio, fibra y agua sin azucar agregada."),
]
