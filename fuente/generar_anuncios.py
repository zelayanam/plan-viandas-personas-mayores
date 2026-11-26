# -*- coding: utf-8 -*-
"""Genera el documento de anuncios para Facebook (DOCX + Markdown)."""

import os

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

VERDE = RGBColor(0x2B, 0x4D, 0x38)
VERDE2 = RGBColor(0x3D, 0x6B, 0x50)
TERRA = RGBColor(0xBD, 0x62, 0x39)
GRIS = RGBColor(0x6D, 0x6A, 0x5E)
NEGRO = RGBColor(0x2B, 0x2A, 0x24)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
CREMA = "FAF6EE"
ARENA = "F0E6D6"
VERDE_CLARO = "E7EFE4"

ANUNCIOS = [
    dict(
        id="A1", nombre="La semana resuelta",
        dolor="Todos los días la misma pregunta: ¿qué le cocino?",
        copy=(
            "Son las 7 de la tarde y otra vez la misma pregunta: ¿qué le cocino?\n\n"
            "No es falta de ganas. Es falta de un plan.\n\n"
            "Viandas Mayores te da 8 semanas de menús pensados para personas mayores: "
            "con proteína para mantener el músculo, calcio para los huesos y platos fáciles "
            "de masticar.\n\n"
            "Elegís la estación, el menú y cuántas porciones. La app arma la lista de compras.\n\n"
            "Esta semana, no decidas más."
        ),
        titular="La semana resuelta, en una app",
        desc="Menús, recetas y lista de compras para personas mayores.",
        cta="Probar la app",
        visual="Mano sosteniendo el celular con la app abierta; al lado, un plato servido. "
               "Formato 4:5, texto grande: «La semana, resuelta».",
        nota="Anuncio de entrada. Ideal para frío y para el público de 35-60 que cuida a sus padres.",
    ),
    dict(
        id="A2", nombre="Mi mamá come siempre lo mismo",
        dolor="Monotonía y poco apetito en la persona mayor.",
        copy=(
            "Mi mamá tiene 78 años y come lo mismo desde que enviudó: sopa, galletitas y un té.\n\n"
            "Un día le pregunté qué quería comer y me dijo: «lo que sea, hijo».\n\n"
            "El problema no era el apetito. Era que nadie le había armado un plan.\n\n"
            "Le armé una semana con Viandas Mayores: comidas ricas, porciones chicas, todo fácil "
            "de masticar. La app arma la lista de compras y yo se la llevo el domingo.\n\n"
            "Ahora me pregunta qué hay de almorzar."
        ),
        titular="Para el que cocina para sus viejos",
        desc="8 semanas de menús para adultos mayores. Elegís, cocinás y envasás.",
        cta="Ver el plan",
        visual="Plano subjetivo: heladera abierta con viandas rotuladas. Texto en pantalla: "
               "«Lo que come mi mamá». Foto cálida, sin dramatismo.",
        nota="El comprador es el hijo/a. Habla de culpa y de solución, no de enfermedad.",
    ),
    dict(
        id="A3", nombre="Que no pierda fuerza",
        dolor="Miedo a la fragilidad, las caídas y la pérdida de independencia.",
        copy=(
            "Después de los 65, el cuerpo empieza a perder músculo. No es solo estética: "
            "es fuerza para levantarse de una silla, para caminar, para no caerse.\n\n"
            "La proteína no puede faltar en ninguna comida. Y no alcanza con un huevo a la mañana.\n\n"
            "Viandas Mayores reparte proteína en las 5 comidas del día, con platos que se cocinan "
            "una vez y duran toda la semana.\n\n"
            "No es una dieta. Es una forma de comer para seguir siendo independiente."
        ),
        titular="Que no pierda fuerza por no comer bien",
        desc="Menús con proteína, calcio y vitamina D para mayores de 65.",
        cta="Conocer el plan",
        visual="Persona mayor levantándose de una silla con seguridad, luz natural. "
               "Texto: «Fuerza para seguir haciendo». Evitar imágenes de caídas.",
        nota="Ángulo emocional fuerte. No prometer revertir la pérdida de masa muscular: "
             "hablar de «mantener» y «acompañar».",
    ),
    dict(
        id="A4", nombre="Verano sin horno",
        dolor="El calor y la resistencia a prender el horno.",
        copy=(
            "35 grados. Y la receta dice «hornear 45 minutos».\n\n"
            "No.\n\n"
            "Para el verano armamos una semana entera sin horno: ensaladas completas, pollo al "
            "vapor, gazpacho, wrap de pollo y platos fríos que se preparan en 15 minutos.\n\n"
            "La cocina queda fresca y la persona mayor come igual de bien.\n\n"
            "Cambiá la estación en la app y cambia el menú completo."
        ),
        titular="Verano sin prender el horno",
        desc="Menús frescos para personas mayores. Sin horno, con proteína.",
        cta="Ver menú de verano",
        visual="Horno apagado con un cartel de «cerrado» y, al lado, una ensalada colorida. "
               "Colores frescos, mucho verde y rojo.",
        nota="Estacional: programar de diciembre a febrero. Es el gancho más concreto del verano.",
    ),
    dict(
        id="A5", nombre="La lista de compras se arma sola",
        dolor="Comprar de más, olvidarse cosas, no saber cuánto calcular.",
        copy=(
            "¿Cuántas veces volviste del supermercado y te diste cuenta de que te faltaba lo principal?\n\n"
            "El plan te dice qué comprar, cuánto y para qué día. La app arma la lista sola, por rubro, "
            "para la cantidad de personas que elijas.\n\n"
            "Verdulería, carnicería, lácteos, almacén. Todo junto y en las cantidades justas.\n\n"
            "Se terminó comprar de más y tirar comida."
        ),
        titular="La lista de compras se arma sola",
        desc="Elegís el menú y las porciones; la app hace el resto.",
        cta="Probar la app",
        visual="Captura de la lista de compras en el celular, con los rubros y los tildes. "
               "Texto: «Comprá una vez, comé toda la semana».",
        nota="Anuncio racional. Bueno para retargeting de gente que ya vio el video.",
    ),
    dict(
        id="A6", nombre="Cocinar para uno",
        dolor="Soledad y desgano: cocinar para una sola persona no vale la pena.",
        copy=(
            "Cuando cocinás para uno, parece que no vale la pena.\n\n"
            "Pero comer bien solo también es un acto de cariño propio.\n\n"
            "Con Viandas Mayores cocinás dos o tres preparaciones y comés bien toda la semana. "
            "Porciones individuales, fáciles de recalentar.\n\n"
            "Y si un día no tenés ganas, la comida ya está lista en la heladera."
        ),
        titular="Cocinar para uno, comer como si fueran varios",
        desc="Viandas porcionadas para toda la semana.",
        cta="Ver cómo funciona",
        visual="Una mesa chica, bien puesta, con un plato lindo y una vianda al lado. "
               "Luz cálida. Sin tristeza: dignidad.",
        nota="Tono de cuidado, nunca de lástima. Evitar imágenes de soledad dramática.",
    ),
    dict(
        id="A7", nombre="No es otra dieta",
        dolor="Hartazgo de dietas que no duran y de prohibiciones.",
        copy=(
            "Ya probó la dieta de la sopa, la de los batidos y la que le recomendó la vecina.\n\n"
            "Ninguna le duró.\n\n"
            "Viandas Mayores no prohíbe: organiza. Platos argentinos, con las cosas que le gustan, "
            "en porciones que le hacen bien.\n\n"
            "Sin contar calorías. Sin pasar hambre. Sin cocinar distinto para ella y para el resto."
        ),
        titular="No es una dieta. Es la semana organizada.",
        desc="Comida real, porciones justas, sin prohibiciones.",
        cta="Conocer el plan",
        visual="Plato de comida casera abundante y colorido, con tenedor. "
               "Texto tachado: «dieta»; al lado: «plan».",
        nota="Funciona muy bien con público de 55-70 que ya está cansado de restricciones.",
    ),
    dict(
        id="A8", nombre="De «coma mejor» a un plan concreto",
        dolor="La indicación médica vaga, sin instrucciones claras.",
        copy=(
            "El médico le dijo: «tiene que comer mejor».\n\n"
            "Y salió del consultorio sin saber qué hacer con eso.\n\n"
            "¿Más verduras? ¿Menos sal? ¿Cuánta carne? ¿Qué desayuno?\n\n"
            "Viandas Mayores traduce esa indicación en un plan concreto: 8 semanas, 66 recetas, "
            "porciones y lista de compras.\n\n"
            "Para que «comer mejor» no sea una frase suelta."
        ),
        titular="De «coma mejor» a un plan concreto",
        desc="Menús para mayores de 65, con cantidades y recetas.",
        cta="Ver el plan",
        visual="Receta médica escrita a mano con la frase «coma mejor» y, al lado, el plan impreso. "
               "Texto: «¿Y ahora qué cocino?».",
        nota="Cuidado con las políticas de Meta: no mencionar enfermedades ni medicamentos. "
             "Hablar de «indicación» en general.",
    ),
]

VIDEOS = [
    dict(
        id="V1", nombre="Domingo de viandas", dur="30 s", formato="9:16 (Reels/Stories)",
        idea="Mostrar el trabajo de dos horas que resuelve la semana. El premio es la heladera llena.",
        escenas=[
            ("0-3 s", "Heladera abierta con envases rotulados.", "Domingo, 2 horas.", "«Dos horas de cocina y la semana resuelta.»"),
            ("3-8 s", "Manos cocinando pollo y verduras.", "Una sola cocción.", "«Cocinás tres preparaciones y listo.»"),
            ("8-15 s", "Envasando y rotulando porciones.", "Todo porcionado.", "«Cada vianda es una comida completa.»"),
            ("15-22 s", "Persona mayor comiendo y sonriendo.", "Come rico, come bien.", "«Con la proteína y el calcio que necesita.»"),
            ("22-27 s", "Pantalla de la app: estación, menú, porciones.", "La app arma la lista.", "«Elegís y la lista de compras se arma sola.»"),
            ("27-30 s", "Logo y botón.", "Probala hoy.", "«Viandas Mayores. La semana, resuelta.»"),
        ],
        hooks=["«Domingo, 2 horas. Comida para toda la semana.»",
               "«Si cocinás para tus viejos, mirá esto.»",
               "«La heladera de mi mamá ahora se ve así.»"],
        cta="Probá la app",
    ),
    dict(
        id="V2", nombre="Lo que come mi mamá", dur="25 s", formato="9:16, cámara en mano",
        idea="POV del hijo/a. Antes y después sin mostrar cuerpos, solo la heladera y el plato.",
        escenas=[
            ("0-3 s", "Heladera con sopa instantánea y galletitas.", "Lo que come mi mamá.", "«Sopa, galletitas y un té. Todos los días.»"),
            ("3-8 s", "Plato vacío en la mesa.", "Hace tres meses.", "«Le pregunté qué quería y me dijo: lo que sea.»"),
            ("8-15 s", "Viandas nuevas, coloridas, rotuladas.", "Ahora.", "«Le armé una semana. Cinco comidas por día.»"),
            ("15-20 s", "Madre comiendo, plano de manos.", "Come sola, come bien.", "«No era falta de apetito. Era falta de plan.»"),
            ("20-25 s", "App en el celular.", "La lista la hace la app.", "«Y yo solo paso el domingo a dejársela.»"),
        ],
        hooks=["«Mi mamá comía lo mismo desde que enviudó.»",
               "«Le pregunté qué quería comer y me dijo: lo que sea.»",
               "«Esto no es una dieta. Es lo que come mi mamá ahora.»"],
        cta="Ver el plan",
    ),
    dict(
        id="V3", nombre="El horno apagado", dur="20 s", formato="9:16",
        idea="Verano. El enemigo es el horno. La solución son los platos fríos.",
        escenas=[
            ("0-3 s", "Termómetro marcando 35° y horno apagado.", "35 grados.", "«Y la receta dice: hornear 45 minutos.»"),
            ("3-8 s", "Manos cortando tomate y palta, sin fuego.", "Sin horno.", "«En verano, cero horno.»"),
            ("8-14 s", "Platos fríos: gazpacho, ensalada, wrap.", "Todo fresco.", "«Ensaladas completas, pollo al vapor, gazpacho.»"),
            ("14-20 s", "App con la estación en «Verano».", "Cambiá la estación.", "«El menú cambia solo. Y la cocina queda fresca.»"),
        ],
        hooks=["«35 grados y la receta dice hornear 45 minutos.»",
               "«En verano, el horno se apaga.»",
               "«Comida rica sin prender el horno.»"],
        cta="Ver menú de verano",
    ),
    dict(
        id="V4", nombre="La app en 15 segundos", dur="15 s", formato="9:16, screen recording",
        idea="Demo pura. Sin rostros. Para retargeting.",
        escenas=[
            ("0-3 s", "Pantalla: selector de estación.", "Elegís la estación.", "«Primavera, verano, otoño o invierno.»"),
            ("3-6 s", "El menú cambia completo.", "Cambia el menú.", "«No solo los ingredientes: cambian los platos.»"),
            ("6-10 s", "Selector de porciones.", "Elegís porciones.", "«Para una, dos o cuatro personas.»"),
            ("10-13 s", "Lista de compras por rubro.", "La lista se arma.", "«Y la lista de compras aparece sola.»"),
            ("13-15 s", "Logo.", "Probala.", "«Viandas Mayores.»"),
        ],
        hooks=["«La app en 15 segundos.»",
               "«Mirá cómo cambia el menú según la estación.»",
               "«Esto hace la app por vos.»"],
        cta="Probar la app",
    ),
]

DOLORES = [
    ("Decidir todos los días", "«¿Qué le cocino hoy?»", "A1"),
    ("Monotonía y poco apetito", "«Come siempre lo mismo»", "A2"),
    ("Fragilidad y caídas", "«Se le nota la debilidad»", "A3"),
    ("Calor y horno", "«No quiero prender el horno»", "A4"),
    ("Compras y cantidades", "«Compro de más o me olvido»", "A5"),
    ("Soledad", "«Cocinar para uno no vale la pena»", "A6"),
    ("Dietas que no duran", "«Ya probó de todo»", "A7"),
    ("Indicación médica vaga", "«Le dijeron: coma mejor»", "A8"),
]

SEGMENTACION = [
    ("Frío A · Cuidadores", "Argentina, 35-60", "Cuidado de adultos mayores, nutrición, cocina saludable, "
     "hijos de padres mayores", "A2, A1, V2"),
    ("Frío B · Mayores activos", "Argentina, 60-75", "Recetas fáciles, comida saludable, jardinería, "
     "caminatas", "A1, A4, A6"),
    ("Frío C · Interés en fuerza", "Argentina, 55-70", "Ejercicio para adultos mayores, osteoporosis, "
     "caminar, yoga suave", "A3, A8"),
    ("Retargeting · Video", "Quienes vieron el 50% de V1 o V2", "—", "A5, V4"),
    ("Retargeting · App", "Visitantes de la app o del link", "—", "A7, V4"),
]

CALENDARIO = [
    ("Semana 1", "Test de 3 anuncios (A1, A2, A4) en 2 conjuntos", "USD 5-8 por conjunto por día",
     "Hook rate, CTR, costo por lead"),
    ("Semana 2", "Escalar el ganador y cortar el peor; sumar A3 y V2", "USD 10-15 en el ganador",
     "CPA, retención de video"),
    ("Semana 3", "Retargeting con A5 y V4; probar A6 y A8", "USD 5 en retargeting",
     "ROAS o costo por registro"),
    ("Semana 4", "Consolidar: 2 creativos ganadores + 1 nuevo hook por semana", "Según CPA",
     "Frecuencia y fatiga"),
]

COMPLIANCE = [
    "No prometer curas, reversión de enfermedades ni resultados médicos. Usar «pensado para», "
    "«acompaña», «ayuda a mantener».",
    "No nombrar enfermedades en el copy principal (diabetes, osteoporosis, sarcopenia): Meta puede "
    "rechazar el anuncio por salud. Dejarlas para la landing, con aval profesional.",
    "No usar imágenes de antes/después corporales ni de personas en situación de vulnerabilidad.",
    "Incluir el descargo: «No reemplaza la consulta médica ni la indicación de un nutricionista».",
    "Evitar el tono paternalista: la persona mayor no es un niño. El comprador es el hijo, "
    "pero el protagonista es el mayor.",
    "Revisar que las fotos tengan licencia comercial (CC BY, no BY-NC) y atribuir al autor.",
]

STORIES = [
    ("S1", "«Domingo, 2 horas. Comida para toda la semana.» → swipe up."),
    ("S2", "«Mi mamá comía sopa y galletitas. Ahora come esto.» → foto del plato."),
    ("S3", "«¿Cuánto hace que no le preguntás qué quiere comer?» → encuesta."),
    ("S4", "«Verano sin horno: 7 cenas frías.» → carrusel de 3 platos."),
]


# ---------------------------------------------------------------- DOCX
def sombrear(celda, hex_color):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def bordes_tabla(tabla, color="D8CDBB", sz="4"):
    tblPr = tabla._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{borde}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def sin_bordes(tabla):
    tblPr = tabla._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{borde}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)


def anchos(tabla, valores):
    tabla.autofit = False
    for i, v in enumerate(valores):
        for celda in tabla.columns[i].cells:
            celda.width = Cm(v)


def celda(c, texto, size=9, bold=False, color=NEGRO, align=None, italic=False):
    c.text = ""
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if align:
        p.alignment = align
    for i, linea in enumerate(str(texto).split("\n")):
        if i:
            p = c.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
        r = p.add_run(linea)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        r.font.color.rgb = color
    c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def parrafo(texto="", size=10, color=NEGRO, bold=False, italic=False, after=6, align=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.14
    if align:
        p.alignment = align
    if texto:
        r = p.add_run(texto)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return p


def h1(texto):
    doc.add_page_break()
    p = doc.add_heading(texto, level=1)
    for r in p.runs:
        r.font.color.rgb = VERDE
        r.font.size = Pt(20)
    p.paragraph_format.space_after = Pt(10)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "6")
    bottom.set(qn("w:color"), "BD6239")
    pBdr.append(bottom)
    pPr.append(pBdr)


def h2(texto):
    p = doc.add_heading(texto, level=2)
    for r in p.runs:
        r.font.color.rgb = VERDE2
        r.font.size = Pt(13)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True


def caja(texto, fill=CREMA, borde="E2D8C8"):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordes_tabla(t, borde, "6")
    c = t.cell(0, 0)
    sombrear(c, fill)
    c.width = Cm(17)
    c.text = ""
    for i, linea in enumerate(texto.split("\n")):
        p = c.paragraphs[0] if i == 0 else c.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(linea)
        r.font.size = Pt(9.5)
        r.font.color.rgb = NEGRO


doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2)
sec.bottom_margin = Cm(1.9)
sec.left_margin = Cm(2)
sec.right_margin = Cm(2)

est = doc.styles["Normal"]
est.font.name = "Calibri"
est.font.size = Pt(10)
est.font.color.rgb = NEGRO

# portada
for _ in range(5):
    doc.add_paragraph()
t = doc.add_table(rows=1, cols=1)
sin_bordes(t)
c = t.cell(0, 0)
sombrear(c, "2B4D38")
c.text = ""
p = c.paragraphs[0]
p.paragraph_format.space_before = Pt(24)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("CAMPAÑA DE ANUNCIOS  ·  META ADS")
r.font.size = Pt(9)
r.font.bold = True
r.font.color.rgb = RGBColor(0xF3, 0xC8, 0x77)

p2 = c.add_paragraph()
p2.paragraph_format.space_before = Pt(4)
p2.paragraph_format.space_after = Pt(6)
r = p2.add_run("Anuncios que\nvenden solos")
r.font.size = Pt(32)
r.font.bold = True
r.font.color.rgb = BLANCO

p3 = c.add_paragraph()
p3.paragraph_format.space_after = Pt(22)
r = p3.add_run("8 posts y 4 guiones de video para Viandas Mayores,\ncon ángulos de dolor y plan de test.")
r.font.size = Pt(11.5)
r.font.color.rgb = RGBColor(0xDB, 0xE5, 0xD3)

doc.add_paragraph()
parrafo("Noviembre de 2026  ·  Versión 1.0", size=9, color=GRIS, align=WD_ALIGN_PARAGRAPH.CENTER)

# ============================================================ ESTRATEGIA
h1("La estrategia en una página")

h2("Qué se vende")
parrafo("No se vende «un recetario». Se vende la semana resuelta: 8 semanas de menús para "
        "personas mayores, con porciones, recetas y lista de compras automática. El producto "
        "tiene tres capas: el plan (qué cocinar), la logística (qué comprar y cuánto) y la app "
        "(elegir estación, menú y porciones).")

h2("A quién le hablamos")
t = doc.add_table(rows=1, cols=3)
bordes_tabla(t)
anchos(t, [4.5, 4.5, 8.0])
for i, h in enumerate(["Quién", "Qué le duele", "Qué necesita oír"]):
    celda(t.cell(0, i), h, bold=True, size=8.5, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
filas = [
    ("El hijo/a de 40-55", "Culpa y cansancio: «no sé si come bien», «no tengo tiempo de cocinarle»",
     "«Hay un plan. No tenés que improvisar.»"),
    ("La persona mayor de 65", "Miedo a perder independencia, a caerse, a depender",
     "«Podés seguir cocinándote, con un plan que te hace bien.»"),
    ("El cuidador/a", "Sobrecarga: cocina para otro y no sabe qué",
     "«Cocinás una vez y resolvés la semana.»"),
]
for fila in filas:
    f = t.add_row()
    for i, v in enumerate(fila):
        celda(f.cells[i], v, size=8.5)

parrafo("El comprador casi siempre es el hijo o el cuidador. El protagonista del anuncio, en cambio, "
        "tiene que ser la persona mayor: dignidad, no lástima.", size=9.5, color=GRIS, italic=True)

h2("Los ocho dolores")
t = doc.add_table(rows=1, cols=3)
bordes_tabla(t)
anchos(t, [5.5, 7.5, 4.0])
for i, h in enumerate(["Dolor", "Cómo lo dice la gente", "Anuncio"]):
    celda(t.cell(0, i), h, bold=True, size=8.5, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
for d in DOLORES:
    f = t.add_row()
    celda(f.cells[0], d[0], size=8.5, bold=True, color=VERDE)
    celda(f.cells[1], d[1], size=8.5, italic=True)
    celda(f.cells[2], d[2], size=8.5, color=TERRA, align=WD_ALIGN_PARAGRAPH.CENTER)

h2("El tono")
for item in [
    "Primera persona y situaciones concretas: «mi mamá», «el domingo», «la heladera».",
    "Nada de tecnicismos: «fuerza», «huesos», «energía», no «sarcopenia» ni «densidad ósea».",
    "Sin culpa ni miedo explícito. El dolor se muestra, no se explota.",
    "Una sola idea por anuncio. Un solo pedido por anuncio.",
]:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(item)
    r.font.size = Pt(9.5)

# ============================================================ ANUNCIOS
h1("Los 8 anuncios")
parrafo("Cada anuncio está listo para pegar en el administrador de anuncios. El copy va en el "
        "campo «Texto principal», el titular en «Título» y la descripción en «Descripción». "
        "El formato sugerido es 4:5 para el feed y 9:16 para Reels y Stories.")

for a in ANUNCIOS:
    h2(f"{a['id']} · {a['nombre']}")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("DOLOR QUE TOCA  ")
    r.font.size = Pt(8)
    r.font.bold = True
    r.font.color.rgb = TERRA
    r = p.add_run(a["dolor"])
    r.font.size = Pt(9)
    r.font.italic = True
    r.font.color.rgb = GRIS

    caja(a["copy"])

    t = doc.add_table(rows=4, cols=2)
    bordes_tabla(t, "E8DFCE", "4")
    anchos(t, [3.4, 13.6])
    datos = [
        ("Titular", a["titular"]),
        ("Descripción", a["desc"]),
        ("Llamado a la acción", a["cta"]),
        ("Visual sugerido", a["visual"]),
    ]
    for i, (k, v) in enumerate(datos):
        celda(t.cell(i, 0), k, size=8, bold=True, color=VERDE)
        sombrear(t.cell(i, 0), CREMA)
        celda(t.cell(i, 1), v, size=8.5)

    parrafo("Nota: " + a["nota"], size=8.5, color=GRIS, italic=True)

# ============================================================ VIDEOS
h1("Los 4 guiones de video")
parrafo("Duración corta, un solo concepto y texto en pantalla desde el primer segundo: el 80% "
        "se mira sin sonido. Todos terminan con el mismo pedido y el mismo logo.")

for v in VIDEOS:
    h2(f"{v['id']} · {v['nombre']}")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(f"{v['dur']}  ·  {v['formato']}")
    r.font.size = Pt(8.5)
    r.font.color.rgb = GRIS
    r.italic = True
    parrafo(v["idea"], size=9.5)

    t = doc.add_table(rows=1, cols=4)
    bordes_tabla(t)
    anchos(t, [2.2, 5.2, 4.2, 5.4])
    for i, h in enumerate(["Tiempo", "Imagen", "Texto en pantalla", "Voz en off"]):
        celda(t.cell(0, i), h, bold=True, size=8, color=BLANCO)
        sombrear(t.cell(0, i), "3D6B50")
    for e in v["escenas"]:
        f = t.add_row()
        celda(f.cells[0], e[0], size=8, bold=True, color=TERRA)
        celda(f.cells[1], e[1], size=8)
        celda(f.cells[2], e[2], size=8, bold=True)
        celda(f.cells[3], e[3], size=8, italic=True)

    parrafo("Hooks alternativos (testear el mismo video con los tres):", size=8.5, bold=True, color=VERDE)
    for hk in v["hooks"]:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(hk)
        r.font.size = Pt(8.5)
    parrafo("CTA: " + v["cta"], size=8.5, bold=True, color=TERRA)

# ============================================================ MEDIOS
h1("Plan de medios")
h2("Segmentación")
t = doc.add_table(rows=1, cols=4)
bordes_tabla(t)
anchos(t, [4.2, 3.0, 6.6, 3.2])
for i, h in enumerate(["Conjunto", "Edad", "Intereses", "Creativos"]):
    celda(t.cell(0, i), h, bold=True, size=8, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
for s in SEGMENTACION:
    f = t.add_row()
    for i, val in enumerate(s):
        celda(f.cells[i], val, size=8)

h2("Calendario de test")
t = doc.add_table(rows=1, cols=4)
bordes_tabla(t)
anchos(t, [2.6, 7.4, 4.4, 2.6])
for i, h in enumerate(["Semana", "Qué se hace", "Presupuesto", "Métrica"]):
    celda(t.cell(0, i), h, bold=True, size=8, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
for c_ in CALENDARIO:
    f = t.add_row()
    for i, val in enumerate(c_):
        celda(f.cells[i], val, size=8)

h2("Métricas que importan")
for m in [
    ("Hook rate (3 s)", "Más del 25%. Si no, el hook está flojo."),
    ("CTR", "Más del 1% en frío; más del 2% en retargeting."),
    ("Retención al 50%", "Más del 15% en videos de 20-30 s."),
    ("Costo por registro", "Es la métrica de negocio. Ajustar el presupuesto a eso, no al CTR."),
    ("Frecuencia", "Cortar o rotar creativo cuando supera 2,5 en frío."),
]:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(m[0] + ": ")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = VERDE
    r = p.add_run(m[1])
    r.font.size = Pt(9)

# ============================================================ STORIES
h1("Copies cortos para Stories")
for s in STORIES:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(s[0] + "  ")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = TERRA
    r = p.add_run(s[1])
    r.font.size = Pt(9.5)

parrafo("En Stories, el texto va grande y centrado, y el sticker de link abajo. "
        "Una idea por placa: máximo 8 palabras.", size=9, color=GRIS, italic=True)

# ============================================================ COMPLIANCE
h1("Cumplimiento y cuidado")
parrafo("Los anuncios de salud son sensibles para Meta. Estas reglas evitan rechazos y, sobre todo, "
        "evitan vender humo.")
for c_ in COMPLIANCE:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(c_)
    r.font.size = Pt(9.5)

caja("«Este plan es una guía educativa y no reemplaza la consulta médica ni la indicación de un "
     "nutricionista. Si hay diabetes, enfermedad renal, hipertensión o dificultades para tragar, "
     "consultá con el equipo de salud.»\n\nEste descargo va en la landing, en el pie de la app y "
     "en el primer comentario del anuncio.", fill=ARENA)

doc.save("Anuncios_Facebook_Viandas_Mayores.docx")
print("DOCX generado")

# ============================================================ MARKDOWN
md = ["# Anuncios para Facebook · Viandas Mayores", "",
      "8 posts y 4 guiones de video, con ángulos de dolor y plan de test.", "",
      "## Estrategia", "",
      "Se vende la semana resuelta: 8 semanas de menús para personas mayores, con porciones, "
      "recetas y lista de compras automática.", "",
      "**Comprador:** hijo/a de 40-55 o cuidador. **Protagonista:** la persona mayor, con dignidad.", "",
      "## Los 8 anuncios", ""]

for a in ANUNCIOS:
    md += [f"### {a['id']} · {a['nombre']}", "",
           f"**Dolor:** {a['dolor']}", "",
           "```text", a["copy"], "```", "",
           f"**Titular:** {a['titular']}", "",
           f"**Descripción:** {a['desc']}", "",
           f"**CTA:** {a['cta']}", "",
           f"**Visual:** {a['visual']}", "",
           f"*Nota: {a['nota']}*", ""]

md += ["## Los 4 guiones de video", ""]
for v in VIDEOS:
    md += [f"### {v['id']} · {v['nombre']}", "",
           f"**Duración:** {v['dur']} · **Formato:** {v['formato']}", "",
           v["idea"], "",
           "| Tiempo | Imagen | Texto en pantalla | Voz en off |",
           "|---|---|---|---|"]
    for e in v["escenas"]:
        md.append(f"| {e[0]} | {e[1]} | {e[2]} | {e[3]} |")
    md += ["", "**Hooks alternativos:**", ""]
    md += [f"- {hk}" for hk in v["hooks"]]
    md += ["", f"**CTA:** {v['cta']}", ""]

md += ["## Segmentación", "", "| Conjunto | Edad | Intereses | Creativos |", "|---|---|---|---|"]
for s in SEGMENTACION:
    md.append(f"| {s[0]} | {s[1]} | {s[2]} | {s[3]} |")
md += ["", "## Calendario de test", "", "| Semana | Qué se hace | Presupuesto | Métrica |", "|---|---|---|---|"]
for c_ in CALENDARIO:
    md.append(f"| {c_[0]} | {c_[1]} | {c_[2]} | {c_[3]} |")
md += ["", "## Stories", ""] + [f"- **{s[0]}:** {s[1]}" for s in STORIES]
md += ["", "## Cumplimiento", ""] + [f"- {c_}" for c_ in COMPLIANCE]
md += ["", "## Descargo", "",
       "Este plan es una guía educativa y no reemplaza la consulta médica ni la indicación de un "
       "nutricionista. Si hay diabetes, enfermedad renal, hipertensión o dificultades para tragar, "
       "consultá con el equipo de salud.", ""]

with open("Anuncios_Facebook_Viandas_Mayores.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("MD generado")
