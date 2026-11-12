# -*- coding: utf-8 -*-
"""Genera el documento Word del plan de viandas."""

import math

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import colectar

D = colectar.datos
REC = {r["id"]: r for r in D["recetas"]}

VERDE = RGBColor(0x2B, 0x4D, 0x38)
VERDE2 = RGBColor(0x3D, 0x6B, 0x50)
TERRA = RGBColor(0xBD, 0x62, 0x39)
GRIS = RGBColor(0x6D, 0x6A, 0x5E)
NEGRO = RGBColor(0x2B, 0x2A, 0x24)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

CREMA = "FAF6EE"
ARENA = "F0E6D6"
VERDE_CLARO = "E7EFE4"
TERRA_CLARO = "F7E4D8"


# ----------------------------------------------------------------- utilidades
def sombrear(celda, hex_color):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def bordes_tabla(tabla, color="D8CDBB", sz="4"):
    tbl = tabla._tbl
    tblPr = tbl.tblPr
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
    tbl = tabla._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for borde in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{borde}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)


def ancho_columnas(tabla, anchos_cm):
    tabla.autofit = False
    tabla.allow_autofit = False
    for i, ancho in enumerate(anchos_cm):
        for celda in tabla.columns[i].cells:
            celda.width = Cm(ancho)


def celda_texto(celda, texto, bold=False, size=9, color=NEGRO, align=None, italic=False):
    celda.text = ""
    p = celda.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    if align:
        p.alignment = align
    r = p.add_run(texto)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    r.font.color.rgb = color
    celda.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def parrafo(texto="", size=10.5, color=NEGRO, bold=False, italic=False,
            espacio_despues=4, espacio_antes=0, align=None, sangria=0, francesa=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(espacio_despues)
    pf.space_before = Pt(espacio_antes)
    pf.line_spacing = 1.12
    if align:
        p.alignment = align
    if sangria:
        pf.left_indent = Cm(sangria)
    if francesa:
        pf.first_line_indent = Cm(-francesa)
    if texto:
        r = p.add_run(texto)
        r.bold = bold
        r.italic = italic
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return p


def h1(texto, salto=True):
    if salto:
        doc.add_page_break()
    p = doc.add_heading(texto, level=1)
    for r in p.runs:
        r.font.color.rgb = VERDE
        r.font.size = Pt(21)
        r.font.name = "Calibri"
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(10)
    # linea inferior
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "8")
    bottom.set(qn("w:space"), "6")
    bottom.set(qn("w:color"), "BD6239")
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


def h2(texto):
    p = doc.add_heading(texto, level=2)
    for r in p.runs:
        r.font.color.rgb = VERDE2
        r.font.size = Pt(14)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    return p


def h3(texto):
    p = doc.add_heading(texto, level=3)
    for r in p.runs:
        r.font.color.rgb = TERRA
        r.font.size = Pt(11)
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    return p


def banda(texto):
    """Separador de grupo, visualmente distinto de los títulos de receta."""
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    sin_bordes(t)
    c = t.cell(0, 0)
    sombrear(c, VERDE_CLARO)
    c.text = ""
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(texto.upper())
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = VERDE
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def paso(n, texto):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.65)
    pf.first_line_indent = Cm(-0.65)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.1
    r = p.add_run(f"{n}.  ")
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = TERRA
    r2 = p.add_run(texto)
    r2.font.size = Pt(10)
    r2.font.color.rgb = NEGRO


def vineta(texto, size=10):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.55)
    pf.first_line_indent = Cm(-0.45)
    pf.space_after = Pt(2)
    pf.line_spacing = 1.1
    r = p.add_run("•  ")
    r.font.size = Pt(size)
    r.font.color.rgb = TERRA
    r2 = p.add_run(texto)
    r2.font.size = Pt(size)
    r2.font.color.rgb = NEGRO


def campo(p, instr):
    r = p.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {instr} "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t")
    t.text = "1"
    fld3 = OxmlElement("w:fldChar")
    fld3.set(qn("w:fldCharType"), "end")
    r._r.append(fld1)
    r._r.append(it)
    r._r.append(fld2)
    r._r.append(t)
    r._r.append(fld3)


def fmt_g(q):
    if q >= 1000:
        v = round(q / 100) / 10
        s = f"{v:.1f}".replace(".", ",")
        return s.replace(",0", "") + " kg"
    if q >= 1:
        return f"{round(q)} g"
    return f"{q:.1f}".replace(".", ",") + " g"


LIQUIDOS = {"leche entera", "leche descremada", "leche", "infusion",
            "caldo de verduras", "agua"}


def fmt_ing(ing):
    q = ing["q"]
    if ing["n"] in LIQUIDOS:
        if q >= 1000:
            return f"{q / 1000:.2f}".replace(".", ",") + " l"
        return f"{round(q)} ml"
    return fmt_g(q)


def nombre_ing(ing):
    base = ing["n"].capitalize()
    est = ing.get("est")
    if not est:
        return base
    if est in ("fruta", "fruta2"):
        return f"{base} o fruta de estación"
    if est in ("hojas", "hojas2"):
        return f"{base} (hojas de estación)"
    if est == "citrico":
        return f"{base} o cítrico de estación"
    return f"{base} (de estación)"


def mantener_tabla_junta(tabla):
    """Evita que la tabla de ingredientes se corte entre páginas."""
    for i, fila in enumerate(tabla.rows):
        trPr = fila._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
        if i < len(tabla.rows) - 1:
            for cell in fila.cells:
                for p_ in cell.paragraphs:
                    p_.paragraph_format.keep_with_next = True


def f1(v):
    return f"{v:.1f}".replace(".", ",")


# ----------------------------------------------------------------- documento
doc = Document()

sec = doc.sections[0]
sec.page_width = Cm(21)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.0)
sec.bottom_margin = Cm(1.9)
sec.left_margin = Cm(1.9)
sec.right_margin = Cm(1.9)
sec.header_distance = Cm(1.0)
sec.footer_distance = Cm(1.0)

est = doc.styles["Normal"]
est.font.name = "Calibri"
est.font.size = Pt(10.5)
est.font.color.rgb = NEGRO
est.paragraph_format.space_after = Pt(4)
est.paragraph_format.line_spacing = 1.12

for nombre in ("Heading 1", "Heading 2", "Heading 3"):
    st = doc.styles[nombre]
    st.font.name = "Calibri"
    st.font.bold = True

# encabezado y pie
hdr = sec.header.paragraphs[0]
hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = hdr.add_run("Plan de viandas para personas mayores  ·  Argentina")
r.font.size = Pt(7.5)
r.font.color.rgb = GRIS

ftr = sec.footer.paragraphs[0]
ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = ftr.add_run("Página ")
r.font.size = Pt(8)
r.font.color.rgb = GRIS
campo(ftr, "PAGE")
r = ftr.add_run(" de ")
r.font.size = Pt(8)
r.font.color.rgb = GRIS
campo(ftr, "NUMPAGES")
for run in ftr.runs:
    run.font.size = Pt(8)
    run.font.color.rgb = GRIS

# ============================================================== PORTADA
for _ in range(6):
    doc.add_paragraph()

t = doc.add_table(rows=1, cols=1)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
sin_bordes(t)
c = t.cell(0, 0)
sombrear(c, "2B4D38")
c.width = Cm(17.2)
c.text = ""
p = c.paragraphs[0]
p.paragraph_format.space_before = Pt(26)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("PLAN DE VIANDAS  ·  ARGENTINA")
r.font.size = Pt(9)
r.font.bold = True
r.font.color.rgb = RGBColor(0xF3, 0xC8, 0x77)

p2 = c.add_paragraph()
p2.paragraph_format.space_before = Pt(4)
p2.paragraph_format.space_after = Pt(6)
r = p2.add_run("Comer bien\ndespués de los 65")
r.font.size = Pt(34)
r.font.bold = True
r.font.color.rgb = BLANCO

p3 = c.add_paragraph()
p3.paragraph_format.space_after = Pt(24)
r = p3.add_run("Dos menús semanales, recetas y cantidades para cocinar,\nenvasar y mantener la fuerza, los huesos y la energía.")
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(0xDB, 0xE5, 0xD3)

doc.add_paragraph()
parrafo("Una guía práctica para familias, cuidadores y personas mayores que quieren "
        "comer mejor sin complicarse. Con productos de estación de todo el año.",
        size=11, color=GRIS, align=WD_ALIGN_PARAGRAPH.CENTER, espacio_despues=18)

# recuadro de datos
t = doc.add_table(rows=3, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
bordes_tabla(t, "E2D8C8", "6")
ancho_columnas(t, [5.2, 11.6])
datos_portada = [
    ("Para quién", "Adultos mayores de 65 años, con o sin dentadura completa, actividad física liviana."),
    ("Cobertura diaria", f"{D['meta']['energia_objetivo']} · {D['meta']['proteina_objetivo']} · "
                         f"{D['meta']['calcio_objetivo']} de calcio"),
    ("Cómo está armado", "7 días × 5 comidas × 2 menús (A y B), con 44 recetas y lista de compras."),
]
for i, (k, v) in enumerate(datos_portada):
    celda_texto(t.cell(i, 0), k, bold=True, size=9, color=VERDE)
    sombrear(t.cell(i, 0), CREMA)
    celda_texto(t.cell(i, 1), v, size=9, color=NEGRO)
    sombrear(t.cell(i, 1), "FFFDF9")

doc.add_paragraph()
parrafo("Actualizado en noviembre de 2026  ·  Versión 1.0", size=9, color=GRIS,
        align=WD_ALIGN_PARAGRAPH.CENTER)

# ============================================================== CONTENIDO
h1("Contenido")
contenido = [
    ("1", "Cómo usar este plan", "Porciones, organización de la semana y qué tener en la alacena."),
    ("2", "Qué necesita el cuerpo después de los 65", "Proteínas, calcio, vitamina D, fibra, hierro, agua y sodio."),
    ("3", "El plato saludable y las 10 recomendaciones", "La guía argentina aplicada a la vida diaria."),
    ("4", "Productos de estación", "Qué comprar en primavera, verano, otoño e invierno."),
    ("5", "Recetas base", "Desayunos, colaciones y meriendas que se repiten en los dos menús."),
    ("6", "Menú A · Sabores de casa", "La semana completa y las 14 recetas principales."),
    ("7", "Menú B · Cocina mediterránea", "La semana completa y las 14 recetas principales."),
    ("8", "Guía de viandas", "Envases, frío, recalentado, texturas y seguridad alimentaria."),
    ("9", "Lista de compras", "Todo lo necesario para cada semana, por rubro."),
    ("10", "Anexo", "Medidas caseras, equivalencias y preguntas frecuentes."),
]
for num, titulo, desc in contenido:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Cm(0.9)
    p.paragraph_format.first_line_indent = Cm(-0.9)
    r = p.add_run(f"{num}.  ")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = TERRA
    r = p.add_run(titulo)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = VERDE
    r = p.add_run(f"\n      {desc}")
    r.font.size = Pt(9.5)
    r.font.color.rgb = GRIS

parrafo("")
parrafo("Este documento se complementa con la aplicación web «Viandas Mayores», donde se puede "
        "elegir la estación del año, el menú y la cantidad de porciones, y obtener la lista de "
        "compras actualizada automáticamente.", size=9.5, color=GRIS, italic=True)

# ============================================================== 1. COMO USAR
h1("1. Cómo usar este plan")
parrafo("El plan resuelve la pregunta más difícil de la semana: qué cocinar. Está pensado para "
        "cocinar en tandas, envasar en porciones y comer bien de lunes a domingo, con platos "
        "tiernos, sabrosos y fáciles de recalentar.")

h2("La semana en cinco comidas")
parrafo("Cada día tiene cinco tomas: desayuno, colación de la mañana, almuerzo, merienda y cena. "
        "Las dos comidas principales (almuerzo y cena) son las que se preparan como vianda. "
        "Las otras tres se resuelven en pocos minutos.")
for t in D["tomas"]:
    vineta(f"{t['nombre']} · {t['hora']}")

h2("Las reglas que ordenan todo")
reglas = [
    ("Una porción de proteína en cada comida principal.", "Pollo, carne magra, pescado, huevo o legumbres. "
     "Es lo que sostiene el músculo y da saciedad."),
    ("La mitad del plato, verduras.", "De estación, crudas o cocidas, con aceite de oliva crudo."),
    ("Un lácteo en el desayuno y otro en la merienda.", "Es la forma más simple de llegar al calcio del día."),
    ("Legumbres dos veces por semana y pescado dos veces.", "Aportan hierro, fibra y omega 3."),
    ("Agua cada dos horas, aunque no haya sed.", "La sed disminuye con la edad: hay que ofrecerla."),
    ("Sal, azúcar y ultraprocesados, lo menos posible.", "El sabor se construye con limón, ajo, hierbas y especias."),
]
for i, (titulo, texto) in enumerate(reglas, 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    r = p.add_run(f"{i}.  ")
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = TERRA
    r = p.add_run(titulo + " ")
    r.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = VERDE
    r = p.add_run(texto)
    r.font.size = Pt(10)

h2("Cómo organizar la cocina en dos horas")
parrafo("Cocinar todo el domingo no es necesario ni conveniente: las verduras pierden textura y "
        "las ensaladas se marchitan. La propuesta es cocinar tres preparaciones base y completar "
        "el resto en el día.")
pasos_cocina = [
    "Hervir legumbres para dos comidas y guardarlas en frascos con su caldo.",
    "Cocinar una fuente grande de pollo al horno o estofado y porcionarlo.",
    "Preparar una tarta o budín que rinda dos porciones.",
    "Lavar y secar las hojas verdes; guardarlas con papel de cocina en un recipiente hermético.",
    "Cortar y blanquear las verduras de estación que se van a usar en salteados.",
    "Rotular cada envase con el plato y la fecha antes de guardarlo.",
]
for i, texto in enumerate(pasos_cocina, 1):
    paso(i, texto)

h2("Las cantidades de este plan")
parrafo("Todas las cantidades son por persona y por comida. Una porción de carne o pescado ronda "
        "los 130 gramos crudos (unos 100 gramos cocidos), la guarnición de cereales o tubérculos "
        "unos 150 a 200 gramos cocidos, y las verduras 200 gramos o más. Para cocinar para más "
        "personas, multiplicar por el número de comensales.")
parrafo("Las recetas indican cuando rinden más de una porción (por ejemplo, un budín que rinde dos). "
        "En ese caso, los ingredientes de la receta alcanzan para esas porciones y no para una sola.",
        color=GRIS, size=10)

# ============================================================== 2. NUTRICION
h1("2. Qué necesita el cuerpo después de los 65")
parrafo(D["nutricion"]["intro"])

h2("Los nutrientes que hay que cuidar")
t = doc.add_table(rows=1, cols=4)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
bordes_tabla(t)
ancho_columnas(t, [3.0, 3.2, 5.4, 5.6])
cabeceras = ["Nutriente", "Meta diaria", "Para qué sirve", "Dónde encontrarlo"]
for i, h in enumerate(cabeceras):
    celda_texto(t.cell(0, i), h, bold=True, size=8.5, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")

for c in D["nutricion"]["claves"]:
    fila = t.add_row()
    celda_texto(fila.cells[0], c["nutriente"], bold=True, size=8.5, color=VERDE)
    celda_texto(fila.cells[1], c["meta"], size=8, color=TERRA)
    celda_texto(fila.cells[2], c["para"], size=8)
    celda_texto(fila.cells[3], c["fuentes"], size=8)

parrafo("")
parrafo("Cómo lo resuelve el plan", size=9, bold=True, color=VERDE2)
for c in D["nutricion"]["claves"]:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(0.3)
    r = p.add_run(f"{c['nutriente']}: ")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = VERDE
    r = p.add_run(c["como"])
    r.font.size = Pt(9)

# ============================================================== 3. PLATO
h1("3. El plato saludable y las 10 recomendaciones")
parrafo("No hace falta pesar cada alimento: alcanza con mirar el plato. Esta es la proporción "
        "que recomiendan las guías alimentarias y que se repite en todas las recetas del plan.")

h2("Cómo armar el plato")
t = doc.add_table(rows=1, cols=3)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
bordes_tabla(t)
ancho_columnas(t, [3.4, 8.2, 5.6])
for i, h in enumerate(["Proporción", "Qué poner", "Qué aporta"]):
    celda_texto(t.cell(0, i), h, bold=True, size=8.5, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
for fila in D["nutricion"]["plato"]["items"]:
    f = t.add_row()
    celda_texto(f.cells[0], fila[0], bold=True, size=9, color=VERDE)
    celda_texto(f.cells[1], fila[1], size=9)
    celda_texto(f.cells[2], fila[2], size=8.5, color=GRIS)

h2("Las 10 recomendaciones de las Guías Alimentarias Argentinas")
for i, g in enumerate(D["gapa"], 1):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.first_line_indent = Cm(-0.8)
    r = p.add_run(f"{i}.  ")
    r.bold = True
    r.font.size = Pt(10)
    r.font.color.rgb = TERRA
    r = p.add_run(g)
    r.font.size = Pt(10)

# ============================================================== 4. ESTACIONES
h1("4. Productos de estación")
parrafo("Comprar lo que da la tierra en cada momento es más barato, más sabroso y más nutritivo. "
        "Las recetas del plan cambian sus verduras y frutas según la estación: la aplicación lo "
        "hace automáticamente y en este documento se indican las opciones.")

t = doc.add_table(rows=1, cols=4)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
bordes_tabla(t)
ancho_columnas(t, [4.3, 4.3, 4.3, 4.3])
for i, k in enumerate(["primavera", "verano", "otono", "invierno"]):
    e = D["estaciones"][k]
    celda_texto(t.cell(0, i), e["nombre"], bold=True, size=10, color=BLANCO,
                align=WD_ALIGN_PARAGRAPH.CENTER)
    sombrear(t.cell(0, i), "3D6B50")

fila = t.add_row()
for i, k in enumerate(["primavera", "verano", "otono", "invierno"]):
    e = D["estaciones"][k]
    c = fila.cells[i]
    c.text = ""
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("FRUTAS")
    r.bold = True
    r.font.size = Pt(7.5)
    r.font.color.rgb = TERRA
    p2 = c.add_paragraph()
    p2.paragraph_format.space_after = Pt(6)
    r = p2.add_run(", ".join(e["frutas"]).capitalize() + ".")
    r.font.size = Pt(8)
    r.font.color.rgb = NEGRO
    p3 = c.add_paragraph()
    p3.paragraph_format.space_after = Pt(2)
    r = p3.add_run("VERDURAS")
    r.bold = True
    r.font.size = Pt(7.5)
    r.font.color.rgb = TERRA
    p4 = c.add_paragraph()
    r = p4.add_run(", ".join(e["verduras"]).capitalize() + ".")
    r.font.size = Pt(8)
    r.font.color.rgb = NEGRO

parrafo("")
h2("Qué conviene aprovechar en cada estación")
for k in ["primavera", "verano", "otono", "invierno"]:
    e = D["estaciones"][k]
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(f"{e['nombre']} ({e['meses']}): ")
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = VERDE
    r = p.add_run("Lo mejor: " + ", ".join(e["destacados"]) + ". " + e["nota"])
    r.font.size = Pt(9.5)

# ============================================================== RECETAS base
def ficha_receta(r, con_estacional=True):
    h2(r["nombre"])
    # metadatos
    partes = [f"{r['tiempo']} min", r["dificultad"]]
    partes.append("Apta para vianda" if r["apto_vianda"] else "Para servir en el momento")
    if r["porciones"] > 1:
        partes.append(f"Rinde {r['porciones']} porciones")
    else:
        partes.append("1 porción")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r0 = p.add_run("  ·  ".join(partes))
    r0.font.size = Pt(8.5)
    r0.font.color.rgb = GRIS
    r0.italic = True

    # ingredientes
    h3("Ingredientes")
    t = doc.add_table(rows=0, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordes_tabla(t, "E8DFCE", "4")
    ancho_columnas(t, [9.6, 7.6])
    for ing in r["ingredientes"]:
        f = t.add_row()
        celda_texto(f.cells[0], nombre_ing(ing), size=8.5)
        if ing["n"] == "infusion":
            cant = ing["t"]
        else:
            cant = f"{fmt_ing(ing)}  ·  {ing['t']}"
        celda_texto(f.cells[1], cant, size=8.5, color=VERDE, align=WD_ALIGN_PARAGRAPH.RIGHT)

    mantener_tabla_junta(t)

    # preparacion
    h3("Preparación")
    for i, p_ in enumerate(r["pasos"], 1):
        paso(i, p_)

    # tips
    if r.get("tips"):
        h3("Consejos")
        for tip in r["tips"]:
            vineta(tip, size=9)

    # nutri
    n = r["nutricion"]
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"Por porción: {n['kcal']} kcal · {f1(n['prot'])} g de proteína · "
                   f"{n['calcio']} mg de calcio · {f1(n['fibra'])} g de fibra · "
                   f"{f1(n['hierro'])} mg de hierro")
    r1.font.size = Pt(8)
    r1.font.color.rgb = GRIS
    r1.italic = True


h1("5. Recetas base")
parrafo("Estas preparaciones se repiten en los dos menús. Son rápidas, económicas y se adaptan a "
        "la estación. Las cantidades son por persona; si se cocina para más, multiplicar.")

for tipo, titulo in [("desayuno", "Desayunos"), ("colacion", "Colaciones"), ("merienda", "Meriendas")]:
    banda(titulo)
    for r in D["recetas"]:
        if r["tipo"] == tipo:
            ficha_receta(r)


# ============================================================== MENUS
def tabla_menu(semana):
    menu = D["menus"][semana]
    t = doc.add_table(rows=1, cols=6)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordes_tabla(t)
    ancho_columnas(t, [1.9, 3.1, 3.1, 3.1, 3.1, 3.1])
    cab = ["Día", "Desayuno", "Colación", "Almuerzo", "Merienda", "Cena"]
    for i, h in enumerate(cab):
        celda_texto(t.cell(0, i), h, bold=True, size=8, color=BLANCO,
                    align=WD_ALIGN_PARAGRAPH.CENTER)
        sombrear(t.cell(0, i), "3D6B50")
    for d in menu["dias"]:
        f = t.add_row()
        celda_texto(f.cells[0], d["dia"], bold=True, size=7.5, color=VERDE)
        for j, toma in enumerate(["desayuno", "colacion", "almuerzo", "merienda", "cena"], 1):
            celda_texto(f.cells[j], REC[d[toma]]["nombre"], size=7.5)


def tabla_nutricion(semana):
    filas = D["resumen"][semana]
    t = doc.add_table(rows=1, cols=6)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordes_tabla(t)
    ancho_columnas(t, [3.4, 2.9, 3.0, 2.9, 2.5, 2.5])
    cab = ["Día", "Energía (kcal)", "Proteína (g)", "Calcio (mg)", "Fibra (g)", "Hierro (mg)"]
    for i, h in enumerate(cab):
        celda_texto(t.cell(0, i), h, bold=True, size=8, color=BLANCO,
                    align=WD_ALIGN_PARAGRAPH.CENTER)
        sombrear(t.cell(0, i), "3D6B50")
    for f_ in filas:
        f = t.add_row()
        celda_texto(f.cells[0], f_["dia"], bold=True, size=8, color=VERDE)
        for j, k in enumerate(["kcal", "prot", "calcio", "fibra", "hierro"], 1):
            celda_texto(f.cells[j], str(f_[k]), size=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    f = t.add_row()
    celda_texto(f.cells[0], "Promedio", bold=True, size=8, color=TERRA)
    for j, k in enumerate(["kcal", "prot", "calcio", "fibra", "hierro"], 1):
        prom = sum(x[k] for x in filas) / len(filas)
        celda_texto(f.cells[j], f"{prom:.0f}", bold=True, size=8, color=TERRA,
                    align=WD_ALIGN_PARAGRAPH.CENTER)
    for c in f.cells:
        sombrear(c, CREMA)


def principales(semana):
    ids, vistos = [], set()
    for d in D["menus"][semana]["dias"]:
        for toma in ("almuerzo", "cena"):
            rid = d[toma]
            if rid not in vistos:
                vistos.add(rid)
                ids.append(rid)
    return ids


for semana, titulo in [
    ("A", "6. Menú A · Sabores de casa"),
    ("B", "7. Menú B · Cocina mediterránea"),
]:
    h1(titulo)
    parrafo(D["menus"][semana]["descripcion"])

    h2("La semana completa")
    tabla_menu(semana)

    parrafo("")
    h2("Cobertura nutricional estimada")
    parrafo("Valores calculados con tablas de composición de alimentos, por día y por persona. "
            "Son estimaciones: varían según la marca, el tamaño de la porción y la forma de cocción.",
            size=9, color=GRIS)
    tabla_nutricion(semana)

    h2("Las recetas de la semana")
    parrafo("Se listan las 14 preparaciones principales (almuerzos y cenas). Los desayunos, "
            "colaciones y meriendas están en el capítulo 5.", size=9.5, color=GRIS)
    for rid in principales(semana):
        ficha_receta(REC[rid])

# ============================================================== VIANDAS
h1("8. Guía de viandas")
parrafo("La comida casera guardada bien dura más, conserva mejor sus nutrientes y evita "
        "infecciones. Estas son las reglas que usa una cocina de viandas.")

for s in D["guia"]["secciones"]:
    h2(s["titulo"].split(". ", 1)[-1] if ". " in s["titulo"] else s["titulo"])
    for item in s["items"]:
        vineta(item, size=9.5)

h2("Cuánto dura cada preparación en el freezer")
t = doc.add_table(rows=1, cols=3)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
bordes_tabla(t)
ancho_columnas(t, [5.4, 3.4, 8.4])
for i, h in enumerate(["Preparación", "Duración", "Consejo"]):
    celda_texto(t.cell(0, i), h, bold=True, size=8.5, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
for f_ in D["guia"]["congelado"]:
    f = t.add_row()
    celda_texto(f.cells[0], f_[0], bold=True, size=8.5, color=VERDE)
    celda_texto(f.cells[1], f_[1], size=8.5)
    celda_texto(f.cells[2], f_[2], size=8.5)

h2("Seis trucos que hacen la diferencia")
for tip in D["tips"]:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(tip["titulo"] + ". ")
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = VERDE
    r = p.add_run(tip["texto"])
    r.font.size = Pt(9.5)

# ============================================================== COMPRAS
def compras(semana, estacion="primavera"):
    mapa = {}
    for d in D["menus"][semana]["dias"]:
        for t in D["tomas"]:
            r = REC[d[t["id"]]]
            for ing in r["ingredientes"]:
                if ing["n"] in ("infusion", "agua"):
                    continue
                nombre = ing["n"]
                if ing.get("est"):
                    v = D["estacional"][ing["est"]].get(estacion)
                    if v:
                        nombre = v
                    et = D["etiquetas_est"].get(ing["est"])
                    if et:
                        nombre = f"{et}: {nombre}"
                clave = (nombre.lower(), ing["cat"])
                prev = mapa.get(clave)
                if prev is None:
                    mapa[clave] = dict(nombre=nombre, cat=ing["cat"], g=ing["q"],
                                       u=(ing["n"] == "huevo"))
                else:
                    prev["g"] += ing["q"]
    orden = ["verduleria", "carniceria", "lacteos", "panaderia", "almacen", "congelados", "otros"]
    res = {}
    for v in mapa.values():
        res.setdefault(v["cat"], []).append(v)
    for k in res:
        res[k].sort(key=lambda x: x["nombre"].lower())
    return [(k, res[k]) for k in orden if k in res]


h1("9. Lista de compras")
parrafo("Calculada para una persona y una semana, en primavera. Al cambiar la estación, cambian "
        "las frutas y verduras: la aplicación web genera la lista actualizada. Para más comensales, "
        "multiplicar las cantidades por el número de personas.")
parrafo("Los huevos se indican en unidades; el resto, en gramos o kilos. Las cantidades incluyen "
        "lo necesario para las cinco comidas de los siete días.", size=9, color=GRIS)

for semana, titulo in [("A", "Semana A"), ("B", "Semana B")]:
    h2(titulo)
    for cat, items in compras(semana):
        h3(D["cats"][cat])
        t = doc.add_table(rows=0, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        bordes_tabla(t, "E8DFCE", "4")
        ancho_columnas(t, [12.4, 4.8])
        for it in items:
            f = t.add_row()
            celda_texto(f.cells[0], it["nombre"], size=8.5)
            if it["u"]:
                u = math.ceil(it["g"] / 50)
                cant = f"{u} {'unidad' if u == 1 else 'unidades'}"
            else:
                cant = fmt_g(it["g"])
            celda_texto(f.cells[1], cant, size=8.5, color=VERDE, align=WD_ALIGN_PARAGRAPH.RIGHT)

# ============================================================== ANEXO
h1("10. Anexo")
h2("Medidas caseras")
medidas = [
    ("1 taza", "240 ml", "1 vaso", "200 ml"),
    ("1 cucharada (cda)", "15 g", "1 cucharadita (cdta)", "5 g"),
    ("1 puñado", "30 g", "1 feta de queso", "40 g"),
    ("1 huevo", "50 g", "1 rodaja de pan", "25 g"),
    ("1 papa mediana", "150 g", "1 banana", "100 g"),
]
t = doc.add_table(rows=1, cols=4)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
bordes_tabla(t)
ancho_columnas(t, [4.6, 3.6, 4.6, 4.4])
for i, h in enumerate(["Medida", "Equivale", "Medida", "Equivale"]):
    celda_texto(t.cell(0, i), h, bold=True, size=8.5, color=BLANCO)
    sombrear(t.cell(0, i), "3D6B50")
for fila in medidas:
    f = t.add_row()
    for i, v in enumerate(fila):
        celda_texto(f.cells[i], v, size=8.5, bold=(i % 2 == 0), color=(VERDE if i % 2 == 0 else NEGRO))

h2("Preguntas frecuentes")
faq = [
    ("¿Puedo repetir el mismo menú la semana siguiente?",
     "Sí. Los dos menús están pensados para alternarse: una semana A, una semana B. También se "
     "puede repetir el que más le guste y cambiar solo las frutas y verduras de estación."),
    ("¿Qué hago si la persona no tiene dientes o le cuesta masticar?",
     "Todas las recetas se pueden adaptar: cocinar más las verduras, desmenuzar las carnes, "
     "humedecer con salsa o caldo y licuar las sopas. La guía de viandas tiene una sección de texturas."),
    ("¿Sirve si hay diabetes?",
     "El plan es bajo en azúcares agregados y prioriza cereales integrales, pero las porciones de "
     "hidratos (papa, batata, arroz, pan) deben ajustarse con el médico o nutricionista."),
    ("¿Y si hay hipertensión?",
     "El plan usa poca sal y condimenta con limón, ajo, hierbas y especias. Hay que evitar los "
     "caldos concentrados, los embutidos y los quesos duros en exceso."),
    ("¿Se puede congelar todo?",
     "Casi todo. Las ensaladas crudas y los lácteos no se congelan. Las tartas, guisos, sopas y "
     "carnes cocidas se congelan muy bien en porciones individuales."),
    ("¿Cuánta agua hay que tomar?",
     "Entre 6 y 8 vasos por día (1,5 a 2 litros), aunque no haya sed, y más en verano. Las sopas, "
     "infusiones y frutas también cuentan."),
]
for preg, resp in faq:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(preg)
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = VERDE
    parrafo(resp, size=9.5, espacio_despues=8)

h2("Una nota sobre las porciones")
parrafo("Las porciones de este plan cubren a una persona mayor con actividad liviana. Si hay "
        "pérdida de peso no buscada, poco apetito o alguna enfermedad que aumente los "
        "requerimientos, las cantidades deben ajustarse con el equipo de salud. Comer bien no es "
        "comer mucho: es comer lo necesario, con variedad y en compañía.", size=9.5)

h2("Descargo de responsabilidad")
parrafo("Este material es una guía educativa general y no reemplaza la consulta médica ni la "
        "indicación de un nutricionista. Antes de cambiar la alimentación de una persona mayor, "
        "especialmente si tiene diabetes, enfermedad renal, hipertensión, disfagia, alergias "
        "alimentarias o toma medicación, conviene consultar con el equipo de salud.", size=9,
        color=GRIS)

doc.save("Plan_Alimentario_Adultos_Mayores.docx")
print("DOCX generado")
