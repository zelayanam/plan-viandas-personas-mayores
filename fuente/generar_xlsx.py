# -*- coding: utf-8 -*-
"""Genera la planilla Excel del plan de viandas."""

import math

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import colectar

D = colectar.datos
REC = {r["id"]: r for r in D["recetas"]}

VERDE = "2B4D38"
VERDE2 = "3D6B50"
CREMA = "FAF6EE"
ARENA = "F0E6D6"
TERRA = "BD6239"
GRIS = "6D6A5E"
BLANCO = "FFFFFF"

thin = Side(style="thin", color="E2D8C8")
BORDE = Border(left=thin, right=thin, top=thin, bottom=thin)


def cabecera(ws, fila, valores, ancho=None, fill=VERDE2):
    for i, v in enumerate(valores, 1):
        c = ws.cell(row=fila, column=i, value=v)
        c.font = Font(bold=True, color=BLANCO, size=10)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDE
    ws.row_dimensions[fila].height = 28
    if ancho:
        for i, w in enumerate(ancho, 1):
            ws.column_dimensions[get_column_letter(i)].width = w


def titulo(ws, texto, subtitulo=None):
    ws.merge_cells("A1:F1")
    c = ws["A1"]
    c.value = texto
    c.font = Font(bold=True, size=18, color=VERDE)
    c.alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 34
    if subtitulo:
        ws.merge_cells("A2:F2")
        c = ws["A2"]
        c.value = subtitulo
        c.font = Font(size=10, color=GRIS, italic=True)
        c.alignment = Alignment(vertical="center")
        ws.row_dimensions[2].height = 22


def estilo_datos(ws, fila_ini, fila_fin, col_ini=1, col_fin=6, zebra=True):
    for f in range(fila_ini, fila_fin + 1):
        for c in range(col_ini, col_fin + 1):
            cel = ws.cell(row=f, column=c)
            cel.border = BORDE
            cel.font = Font(size=10, color="2B2A24")
            cel.alignment = Alignment(vertical="center", wrap_text=True)
            if zebra and f % 2 == 0:
                cel.fill = PatternFill("solid", fgColor=CREMA)


def fmt_g(q):
    if q >= 1000:
        v = round(q / 100) / 10
        return f"{v:.1f}".replace(".", ",") + " kg"
    if q >= 1:
        return f"{round(q)} g"
    return f"{q:.1f}".replace(".", ",") + " g"


wb = Workbook()

# ============================================================ RESUMEN
ws = wb.active
ws.title = "Resumen"
ws.sheet_view.showGridLines = False
titulo(ws, "Plan de viandas para personas mayores",
       "Dos menús semanales · Argentina · Productos de estación · Versión 1.0 (noviembre 2026)")

ws["A4"] = "Para quién"
ws["A4"].font = Font(bold=True, color=VERDE, size=10)
ws["B4"] = D["meta"]["perfil"]
ws.merge_cells("B4:F4")

ws["A5"] = "Energía objetivo"
ws["A5"].font = Font(bold=True, color=VERDE, size=10)
ws["B5"] = D["meta"]["energia_objetivo"]
ws["D5"] = "Proteínas"
ws["D5"].font = Font(bold=True, color=VERDE, size=10)
ws["E5"] = D["meta"]["proteina_objetivo"]
ws.merge_cells("E5:F5")

ws["A6"] = "Calcio"
ws["A6"].font = Font(bold=True, color=VERDE, size=10)
ws["B6"] = D["meta"]["calcio_objetivo"]
ws["D6"] = "Fibra"
ws["D6"].font = Font(bold=True, color=VERDE, size=10)
ws["E6"] = D["meta"]["fibra_objetivo"]
ws.merge_cells("E6:F6")

ws["A7"] = "Agua"
ws["A7"].font = Font(bold=True, color=VERDE, size=10)
ws["B7"] = D["meta"]["agua_objetivo"]
ws.merge_cells("B7:F7")

cabecera(ws, 9, ["Menú", "Energía (kcal)", "Proteína (g)", "Calcio (mg)", "Fibra (g)", "Hierro (mg)"],
         [22, 16, 15, 15, 13, 13])
fila = 10
for sem, menu in D["menus"].items():
    filas = D["resumen"][sem]
    vals = [
        f"{menu['nombre']} · {menu['lema']}",
        round(sum(f["kcal"] for f in filas) / 7),
        round(sum(f["prot"] for f in filas) / 7, 1),
        round(sum(f["calcio"] for f in filas) / 7),
        round(sum(f["fibra"] for f in filas) / 7, 1),
        round(sum(f["hierro"] for f in filas) / 7, 1),
    ]
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=fila, column=i, value=v)
        c.border = BORDE
        c.font = Font(size=10, bold=(i == 1), color=(VERDE if i == 1 else "2B2A24"))
        c.alignment = Alignment(horizontal="center" if i > 1 else "left", vertical="center")
        if i > 1:
            c.number_format = "0.0" if i in (3, 5, 6) else "0"
    fila += 1

ws["A14"] = "Cómo está armado"
ws["A14"].font = Font(bold=True, color=VERDE, size=10)
ws.merge_cells("A15:F17")
ws["A15"] = ("7 días × 5 comidas por menú · 44 recetas · Lista de compras por rubro. "
             "Las cantidades son por persona y por comida. En la app se puede cambiar la estación, "
             "el menú y la cantidad de porciones.")
ws["A15"].alignment = Alignment(wrap_text=True, vertical="top")
ws["A15"].font = Font(size=10, color="2B2A24")

ws["A19"] = "Hojas de esta planilla"
ws["A19"].font = Font(bold=True, color=VERDE, size=11)
hojas = [
    ("Menú A", "La semana completa, con el detalle de cada comida y la cobertura del día."),
    ("Menú B", "La semana mediterránea, con el detalle de cada comida."),
    ("Recetas", "Las 44 recetas con tiempos, porciones y aporte nutricional por porción."),
    ("Nutrición", "Cobertura diaria de los dos menús, con promedios y objetivos."),
    ("Compras A / B", "Lista de compras por rubro para cada semana."),
    ("Estación", "Frutas y verduras de cada estación del año."),
    ("Guía de viandas", "Envases, frío, recalentado y texturas."),
]
for i, (h, d) in enumerate(hojas, 20):
    ws.cell(row=i, column=1, value=h).font = Font(bold=True, size=10, color=TERRA)
    ws.cell(row=i, column=2, value=d).font = Font(size=10, color=GRIS)
    ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)

ws.column_dimensions["A"].width = 22
for col in "BCDEF":
    ws.column_dimensions[col].width = 16

# ============================================================ MENUS
for sem in ["A", "B"]:
    ws = wb.create_sheet(f"Menú {sem}")
    ws.sheet_view.showGridLines = False
    menu = D["menus"][sem]
    titulo(ws, f"{menu['nombre']} · {menu['lema']}", menu["descripcion"])
    cabecera(ws, 4, ["Día", "Desayuno", "Colación", "Almuerzo", "Merienda", "Cena", "kcal del día"],
             [12, 30, 26, 34, 28, 34, 12])
    r = 5
    for d in menu["dias"]:
        ws.cell(row=r, column=1, value=d["dia"]).font = Font(bold=True, color=VERDE, size=10)
        for j, toma in enumerate(["desayuno", "colacion", "almuerzo", "merienda", "cena"], 2):
            ws.cell(row=r, column=j, value=REC[d[toma]]["nombre"])
        kcal = sum(REC[d[t]]["nutricion"]["kcal"] for t in ["desayuno", "colacion", "almuerzo", "merienda", "cena"])
        ws.cell(row=r, column=7, value=kcal).number_format = "0"
        ws.row_dimensions[r].height = 44
        r += 1
    estilo_datos(ws, 5, r - 1, 1, 7)
    for f in range(5, r):
        ws.cell(row=f, column=7).font = Font(bold=True, size=10, color=TERRA)
        ws.cell(row=f, column=7).alignment = Alignment(horizontal="center", vertical="center")

    # totales
    ws.cell(row=r + 1, column=1, value="Promedio semanal").font = Font(bold=True, color=VERDE, size=10)
    ws.cell(row=r + 1, column=7, value=f"=ROUND(AVERAGE(G5:G{r-1}),0)").font = Font(bold=True, color=VERDE, size=10)
    ws.cell(row=r + 1, column=7).number_format = "0"

# ============================================================ RECETAS
ws = wb.create_sheet("Recetas")
ws.sheet_view.showGridLines = False
titulo(ws, "Recetario", "44 recetas · valores por porción · estimados con tablas de composición de alimentos")
cabecera(ws, 4, ["Receta", "Tipo", "Tiempo (min)", "Dificultad", "Porciones", "Apta vianda",
                 "kcal", "Proteína (g)", "Calcio (mg)", "Fibra (g)", "Hierro (mg)"],
         [42, 12, 12, 11, 10, 11, 9, 11, 11, 10, 11])
r = 5
for rec in D["recetas"]:
    n = rec["nutricion"]
    vals = [rec["nombre"], rec["tipo"].capitalize(), rec["tiempo"], rec["dificultad"],
            rec["porciones"], "Sí" if rec["apto_vianda"] else "No",
            n["kcal"], n["prot"], n["calcio"], n["fibra"], n["hierro"]]
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v)
        c.border = BORDE
        c.font = Font(size=10)
        c.alignment = Alignment(vertical="center", wrap_text=(i == 1))
        if i == 1:
            c.font = Font(size=10, bold=True, color=VERDE)
        if i >= 7:
            c.number_format = "0.0" if i in (8, 10, 11) else "0"
            c.alignment = Alignment(horizontal="center", vertical="center")
    r += 1
ws.auto_filter.ref = f"A4:K{r-1}"
ws.freeze_panes = "A5"

# ============================================================ NUTRICION
ws = wb.create_sheet("Nutrición")
ws.sheet_view.showGridLines = False
titulo(ws, "Cobertura nutricional diaria",
       "Estimación por día y por persona. Objetivos: 1.800 kcal · 85 g de proteína · 1.100 mg de calcio · 28 g de fibra.")
cabecera(ws, 4, ["Menú", "Día", "Energía (kcal)", "Proteína (g)", "Calcio (mg)", "Fibra (g)", "Hierro (mg)"],
         [10, 13, 15, 14, 14, 13, 13])
r = 5
for sem, filas in D["resumen"].items():
    for f_ in filas:
        vals = [sem, f_["dia"], f_["kcal"], f_["prot"], f_["calcio"], f_["fibra"], f_["hierro"]]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v)
            c.border = BORDE
            c.font = Font(size=10)
            c.alignment = Alignment(horizontal="center", vertical="center")
            if i >= 3:
                c.number_format = "0.0" if i in (4, 6, 7) else "0"
        ws.cell(row=r, column=2).alignment = Alignment(horizontal="left", vertical="center")
        r += 1
    # promedio del menú
    ini = r - 7
    ws.cell(row=r, column=1, value=sem).font = Font(bold=True, color=TERRA, size=10)
    ws.cell(row=r, column=2, value="Promedio").font = Font(bold=True, color=TERRA, size=10)
    for i, col in enumerate(["C", "D", "E", "F", "G"], 3):
        c = ws.cell(row=r, column=i, value=f"=AVERAGE({col}{ini}:{col}{r-1})")
        c.number_format = "0.0" if i in (4, 6, 7) else "0"
        c.font = Font(bold=True, color=TERRA, size=10)
        c.alignment = Alignment(horizontal="center")
        c.fill = PatternFill("solid", fgColor=CREMA)
        c.border = BORDE
    r += 2

# ============================================================ COMPRAS
def compras(semana, estacion="primavera"):
    mapa = {}
    for d in D["menus"][semana]["dias"]:
        for t in D["tomas"]:
            rec = REC[d[t["id"]]]
            for ing in rec["ingredientes"]:
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
    res = []
    for k in orden:
        items = sorted([v for v in mapa.values() if v["cat"] == k], key=lambda x: x["nombre"].lower())
        res.extend(items)
    return res


for sem in ["A", "B"]:
    ws = wb.create_sheet(f"Compras {sem}")
    ws.sheet_view.showGridLines = False
    titulo(ws, f"Lista de compras · Semana {sem}",
           "Para una persona y una semana, en primavera. Cambiar la estación en la app actualiza la lista.")
    cabecera(ws, 4, ["Rubro", "Producto", "Cantidad"], [26, 46, 14])
    r = 5
    for it in compras(sem):
        if it["u"]:
            u = math.ceil(it["g"] / 50)
            cant = f"{u} {'unidad' if u == 1 else 'unidades'}"
        else:
            cant = fmt_g(it["g"])
        vals = [D["cats"][it["cat"]], it["nombre"], cant]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v)
            c.border = BORDE
            c.font = Font(size=10, bold=(i == 2))
            c.alignment = Alignment(vertical="center", horizontal="right" if i == 3 else "left")
            if i == 1:
                c.font = Font(size=9, color=GRIS)
        r += 1
    ws.auto_filter.ref = f"A4:C{r-1}"
    ws.freeze_panes = "A5"

# ============================================================ ESTACION
ws = wb.create_sheet("Estación")
ws.sheet_view.showGridLines = False
titulo(ws, "Productos de estación", "Hemisferio sur · Argentina · qué conviene comprar en cada momento del año")
cabecera(ws, 4, ["Estación", "Meses", "Frutas", "Verduras", "Lo mejor de la estación"],
         [14, 30, 46, 50, 34])
r = 5
for k in ["primavera", "verano", "otono", "invierno"]:
    e = D["estaciones"][k]
    vals = [e["nombre"], e["meses"], ", ".join(e["frutas"]), ", ".join(e["verduras"]), ", ".join(e["destacados"])]
    for i, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=i, value=v)
        c.border = BORDE
        c.font = Font(size=10, bold=(i == 1), color=(VERDE if i == 1 else "2B2A24"))
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 90
    r += 1

# ============================================================ GUIA
ws = wb.create_sheet("Guía de viandas")
ws.sheet_view.showGridLines = False
titulo(ws, "Guía de viandas", "Cómo cocinar, envasar, conservar y recalentar")
r = 4
for s in D["guia"]["secciones"]:
    ws.cell(row=r, column=1, value=s["titulo"]).font = Font(bold=True, size=11, color=VERDE)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    r += 1
    for item in s["items"]:
        c = ws.cell(row=r, column=1, value="•  " + item)
        c.font = Font(size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        ws.row_dimensions[r].height = 30
        r += 1
    r += 1
ws.column_dimensions["A"].width = 30
ws.column_dimensions["B"].width = 40
ws.column_dimensions["C"].width = 40

wb.properties.title = "Plan de viandas para personas mayores"
wb.properties.subject = "Menús, recetas y cantidades"
wb.properties.creator = "Plan de viandas"
wb.save("Plan_Alimentario_Adultos_Mayores.xlsx")
print("XLSX generado")
