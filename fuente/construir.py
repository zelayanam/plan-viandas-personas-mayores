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
    for k, filas in D["resumen"].items():
        print(f"\nMenú {k}:")
        for f in filas:
            print(f"  {f['dia']:<10} {f['kcal']:>5} kcal | P {f['prot']:>5} g | "
                  f"Ca {f['calcio']:>5} mg | Fibra {f['fibra']:>4} g | Fe {f['hierro']:>4} mg")
        print(f"  PROMEDIO   {sum(x['kcal'] for x in filas)/7:>5.0f} kcal | "
              f"P {sum(x['prot'] for x in filas)/7:>5.1f} g | "
              f"Ca {sum(x['calcio'] for x in filas)/7:>5.0f} mg | "
              f"Fibra {sum(x['fibra'] for x in filas)/7:>4.1f} g")


if __name__ == "__main__":
    main()
