# -*- coding: utf-8 -*-
"""Reune todos los textos del plan en una estructura para procesarlos."""

import datos_plan as D
import recetas_a as RA
import recetas_b as RB
import menus as M

ALIMENTOS = dict(D.ALIMENTOS)
ALIMENTOS.update({
    "infusion": dict(kcal=0, p=0, ca=0, fb=0, fe=0, cat="almacen"),
    "leche": dict(kcal=62, p=3.3, ca=120, fb=0, fe=0.05, cat="lacteos"),
    "hojas verdes": dict(kcal=20, p=1.8, ca=45, fb=2.0, fe=1.5, cat="verduleria"),
    "verduras de estacion": dict(kcal=35, p=1.8, ca=30, fb=2.5, fe=0.8, cat="verduleria"),
    "aceitunas": dict(kcal=145, p=1.0, ca=60, fb=3.0, fe=3.3, cat="almacen"),
})


def calcular(receta):
    tot = dict(kcal=0.0, p=0.0, ca=0.0, fb=0.0, fe=0.0)
    ings = []
    porciones = receta.get("porciones", 1)
    for ing in receta["ingredientes"]:
        base = ALIMENTOS[ing["n"]]
        q = ing["q"]
        tot["kcal"] += base["kcal"] * q / 100.0 / porciones
        tot["p"] += base["p"] * q / 100.0 / porciones
        tot["ca"] += base["ca"] * q / 100.0 / porciones
        tot["fb"] += base["fb"] * q / 100.0 / porciones
        tot["fe"] += base["fe"] * q / 100.0 / porciones
        ings.append(dict(n=ing["n"], q=q, t=ing["t"], est=ing.get("est"), cat=base.get("cat", "otros")))
    out = dict(receta)
    out["ingredientes"] = ings
    out["porciones"] = porciones
    out["nutricion"] = dict(
        kcal=round(tot["kcal"]), prot=round(tot["p"], 1), calcio=round(tot["ca"]),
        fibra=round(tot["fb"], 1), hierro=round(tot["fe"], 1),
    )
    return out


RECETAS = [calcular(r) for r in (RA.RECETAS + RB.RECETAS_B)]
REC = {r["id"]: r for r in RECETAS}

resumen = {}
for k, menu in M.MENUS.items():
    filas = []
    for d in menu["dias"]:
        acc = dict(kcal=0, prot=0.0, calcio=0.0, fibra=0.0, hierro=0.0)
        for t, _n, _h in M.TOMAS:
            n = REC[d[t]]["nutricion"]
            acc["kcal"] += n["kcal"]
            acc["prot"] += n["prot"]
            acc["calcio"] += n["calcio"]
            acc["fibra"] += n["fibra"]
            acc["hierro"] += n["hierro"]
        filas.append(dict(dia=d["dia"], **{k2: round(v) for k2, v in acc.items()}))
    resumen[k] = filas

datos = dict(
    meta=D.META,
    estaciones=D.ESTACIONES,
    estacional=D.ESTACIONAL,
    tomas=[dict(id=a, nombre=b, hora=c) for a, b, c in M.TOMAS],
    menus=M.MENUS,
    recetas=RECETAS,
    guia=M.GUIA_VIANDAS,
    nutricion=M.NUTRICION,
    gapa=M.GAPA,
    tips=M.TIPS_VIANDA,
    resumen=resumen,
    cats={
        "verduleria": "Verdulería y frutería",
        "carniceria": "Carnicería y pescadería",
        "lacteos": "Lácteos y huevos",
        "almacen": "Almacén",
        "panaderia": "Panadería",
        "congelados": "Congelados",
        "otros": "Otros",
    },
    etiquetas_est={
        "fruta": "Fruta de estación",
        "fruta2": "Fruta de estación",
        "hojas": "Hojas verdes",
        "hojas2": "Hojas verdes",
        "verdura_horno": "Verduras para horno",
        "verdura_salteado": "Verduras para salteado",
        "verdura_sopa": "Verduras para sopa",
    },
)

from acentuar import acentuar_datos  # noqa: E402

datos = acentuar_datos(datos)
RECETAS = datos["recetas"]
REC = {r["id"]: r for r in RECETAS}
