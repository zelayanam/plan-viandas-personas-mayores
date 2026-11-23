# -*- coding: utf-8 -*-
"""Genera app/datos.js y plan.json desde el modelo."""

import json
import os

import colectar

D = colectar.datos


def main():
    D["generado"] = "2026-11-12"

    os.makedirs("app", exist_ok=True)
    with open("plan.json", "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False, indent=1)
    with open(os.path.join("app", "datos.js"), "w", encoding="utf-8") as f:
        f.write("/* Generado automaticamente desde datos_plan.py - no editar a mano */\n")
        f.write("window.DATOS = ")
        json.dump(D, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    print(f"Recetas: {len(D['recetas'])}")
    for k, temps in D["resumen"].items():
        print(f"\nMenú {k}:")
        for est, filas in temps.items():
            prom = lambda key: sum(x[key] for x in filas) / len(filas)
            print(f"  -- {est}: {prom('kcal'):.0f} kcal | P {prom('prot'):.1f} g | "
                  f"Ca {prom('calcio'):.0f} mg | Fibra {prom('fibra'):.1f} g")


if __name__ == "__main__":
    main()
