# -*- coding: utf-8 -*-
"""Genera un EPUB 3 navegable con el plan completo."""

import html
import os
import sys
import uuid
import zipfile
from datetime import date

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import colectar  # noqa: E402

D = colectar.datos
REC = {r["id"]: r for r in D["recetas"]}
TOMAS = ["desayuno", "colacion", "almuerzo", "merienda", "cena"]
TIPOS = [("desayuno", "Desayunos"), ("colacion", "Colaciones"), ("almuerzo", "Almuerzos"),
         ("merienda", "Meriendas"), ("cena", "Cenas"), ("postre", "Postres")]
ESTACIONES = ["invierno", "otono", "primavera", "verano"]
FONT = r"C:\Windows\Fonts"

CSS = """
@charset "utf-8";
body { font-family: Georgia, "Times New Roman", serif; line-height: 1.6; color: #2b2a24;
       background: #faf6ee; margin: 0 6%; }
h1 { color: #2b4d38; font-size: 1.55em; border-bottom: 2px solid #bd6239;
     padding-bottom: 0.25em; margin-top: 1.2em; }
h2 { color: #3d6b50; font-size: 1.2em; margin-top: 1.4em; }
h3 { color: #bd6239; font-size: 1.02em; margin-bottom: 0.2em; }
p { margin: 0.55em 0; }
a { color: #8f4626; text-decoration: none; }
.meta { color: #6d6a5e; font-size: 0.85em; font-style: italic; }
.etiqueta { display: inline-block; background: #e7efe4; color: #2b4d38; font-size: 0.72em;
            text-transform: uppercase; letter-spacing: 0.06em; padding: 0.12em 0.6em;
            border-radius: 0.6em; }
table { width: 100%; border-collapse: collapse; font-size: 0.82em; margin: 0.8em 0; }
th { background: #3d6b50; color: #fffdf9; text-align: left; padding: 0.4em; }
td { border: 1px solid #e2d8c8; padding: 0.35em; vertical-align: top; }
tr:nth-child(even) td { background: #fdfaf4; }
.box { background: #fffdf9; border: 1px solid #e2d8c8; border-left: 5px solid #bd6239;
       padding: 0.8em 1em; margin: 1em 0; }
.dia { font-weight: bold; color: #2b4d38; }
.volver { margin-top: 2em; font-size: 0.85em; }
.nutri { background: #e7efe4; padding: 0.6em; border-radius: 0.4em; font-size: 0.85em; }
.portada { text-align: center; margin-top: 18%; }
.portada img { max-width: 100%; }
"""


def e(t):
    return html.escape(str(t), quote=True)


def pagina(titulo, cuerpo, extra=""):
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="es">
<head><meta charset="utf-8"/><title>{e(titulo)}</title>
<link rel="stylesheet" href="../styles.css" type="text/css"/></head>
<body>
{cuerpo}
{extra}
</body></html>"""


def portada():
    img = Image.new("RGB", (1600, 2400), (43, 77, 56))
    d = ImageDraw.Draw(img)
    for y in range(0, 2400, 8):
        c = int(43 + (77 - 43) * y / 2400)
        d.line((0, y, 1600, y), fill=(c, int(77 + (107 - 77) * y / 2400), int(56 + (80 - 56) * y / 2400)))
    d.rectangle((0, 0, 1600, 16), fill=(243, 200, 119))
    f1 = ImageFont.truetype(os.path.join(FONT, "segoeuib.ttf"), 34)
    f2 = ImageFont.truetype(os.path.join(FONT, "segoeuib.ttf"), 104)
    f3 = ImageFont.truetype(os.path.join(FONT, "segoeui.ttf"), 40)
    f4 = ImageFont.truetype(os.path.join(FONT, "segoeuib.ttf"), 30)
    d.text((110, 250), "PLAN DE VIANDAS  ·  ARGENTINA", font=f1, fill=(243, 200, 119))
    d.text((110, 340), "Comer bien", font=f2, fill=(255, 253, 249))
    d.text((110, 460), "después de", font=f2, fill=(255, 253, 249))
    d.text((110, 580), "los 65", font=f2, fill=(255, 253, 249))
    d.text((110, 780), "8 semanas de menús, 66 recetas y lista", font=f3, fill=(219, 229, 211))
    d.text((110, 835), "de compras para cada estación.", font=f3, fill=(219, 229, 211))
    d.line((110, 960, 700, 960), fill=(243, 200, 119), width=5)
    d.text((110, 1010), "2 MENÚS  ·  4 ESTACIONES  ·  66 RECETAS", font=f4, fill=(243, 200, 119))
    d.text((110, 2190), "Viandas Mayores · 2026", font=f3, fill=(230, 225, 210))
    os.makedirs("epub-build", exist_ok=True)
    img.save("epub-build/cover.jpg", "JPEG", quality=90)


def link_receta(rid):
    return f"receta_{rid}.xhtml"


def seccion_intro():
    c = ["<h1>Cómo usar este libro</h1>",
         "<p>Este ebook es el plan de viandas para personas mayores, pensado para cocinar una vez "
         "y comer bien toda la semana. Todo está enlazado: desde el menú podés ir a cada receta y "
         "desde la receta volver al menú.</p>",
         "<h2>Qué vas a encontrar</h2>",
         "<ul>",
         "<li><strong>Cuatro estaciones</strong>, cada una con dos menús semanales (A y B).</li>",
         "<li><strong>66 recetas</strong> con ingredientes, cantidades, preparación y consejos.</li>",
         "<li><strong>Listas de compras</strong> por estación y por menú.</li>",
         "<li><strong>Guía de viandas</strong>: envases, frío, recalentado y texturas.</li>",
         "<li><strong>Nutrición</strong>: qué necesita el cuerpo después de los 65.</li>",
         "</ul>",
         "<div class='box'><strong>Importante.</strong> Este plan es una guía educativa y no "
         "reemplaza la consulta médica ni la indicación de un nutricionista. Si hay diabetes, "
         "enfermedad renal, hipertensión o dificultades para tragar, consultá con el equipo de salud.</div>",
         "<h2>Cómo navegar</h2>",
         "<p>Usá el índice del lector o tocá los nombres de los platos en los menús. Cada receta "
         "tiene un enlace para volver al menú de donde salió.</p>"]
    return pagina("Cómo usar este libro", "\n".join(c))


def seccion_menus():
    c = ["<h1>Menús por estación</h1>",
         "<p>Cada estación tiene dos semanas completas. Los platos cambian según el clima: en verano "
         "no se usa el horno, en invierno sí. Tocá un plato para ver la receta.</p>"]
    for est in ESTACIONES:
        e_ = D["estaciones"][est]
        c.append(f"<h2 id='{est}'>{e(e_['nombre'])}</h2>")
        c.append(f"<p class='meta'>{e(e_['meses'])}. Lo mejor: {e(', '.join(e_['destacados']))}.</p>")
        for sem in ["A", "B"]:
            menu = D["menus"][sem]
            temp = menu["temporadas"][est]
            c.append(f"<h3 id='{est}-{sem}'>{e(menu['nombre'])} · {e(menu['lema'])}</h3>")
            c.append(f"<p class='meta'>{e(temp['descripcion'])}</p>")
            c.append("<table><tr><th>Día</th><th>Desayuno</th><th>Colación</th>"
                     "<th>Almuerzo</th><th>Merienda</th><th>Cena</th></tr>")
            for dia in temp["dias"]:
                c.append("<tr>")
                c.append(f"<td class='dia'>{e(dia['dia'])}</td>")
                for t in TOMAS:
                    r = REC[dia[t]]
                    c.append(f"<td><a href='{link_receta(r['id'])}'>{e(r['nombre'])}</a></td>")
                c.append("</tr>")
            c.append("</table>")
            filas = D["resumen"][sem][est]
            prom = lambda k: sum(x[k] for x in filas) / len(filas)
            c.append(f"<p class='meta'>Promedio por día: {prom('kcal'):.0f} kcal · "
                     f"{prom('prot'):.0f} g de proteína · {prom('calcio'):.0f} mg de calcio · "
                     f"{prom('fibra'):.0f} g de fibra.</p>")
    return pagina("Menús por estación", "\n".join(c))


def seccion_indice_recetas():
    c = ["<h1>Índice de recetas</h1>",
         "<p>66 recetas agrupadas por tipo de comida.</p>"]
    for tipo, nombre in TIPOS:
        recs = [r for r in D["recetas"] if r["tipo"] == tipo]
        if not recs:
            continue
        c.append(f"<h2>{e(nombre)}</h2><ul>")
        for r in sorted(recs, key=lambda x: x["nombre"]):
            c.append(f"<li><a href='{link_receta(r['id'])}'>{e(r['nombre'])}</a> "
                     f"<span class='meta'>· {r['nutricion']['kcal']} kcal</span></li>")
        c.append("</ul>")
    return pagina("Índice de recetas", "\n".join(c))


def pagina_receta(r):
    n = r["nutricion"]
    tipo = {"desayuno": "Desayuno", "colacion": "Colación", "almuerzo": "Almuerzo",
            "merienda": "Merienda", "cena": "Cena"}.get(r["tipo"], r["tipo"])
    c = [f"<h1>{e(r['nombre'])}</h1>",
         f"<p class='meta'>{e(tipo)} · {r['tiempo']} min · {e(r['dificultad'])} · "
         f"{'Apta para vianda' if r['apto_vianda'] else 'Para servir en el momento'}"
         f"{' · Rinde ' + str(r['porciones']) + ' porciones' if r['porciones'] > 1 else ' · 1 porción'}</p>",
         "<h2>Ingredientes</h2>", "<table><tr><th>Ingrediente</th><th>Cantidad</th></tr>"]
    for i in r["ingredientes"]:
        nombre = i["n"]
        if i.get("est"):
            nombre += " (según estación)"
        c.append(f"<tr><td>{e(nombre.capitalize())}</td><td>{e(i['t'])}</td></tr>")
    c.append("</table>")
    c.append("<h2>Preparación</h2><ol>")
    for p in r["pasos"]:
        c.append(f"<li>{e(p)}</li>")
    c.append("</ol>")
    if r.get("tips"):
        c.append("<h2>Consejos</h2><div class='box'>")
        for t in r["tips"]:
            c.append(f"<p>💡 {e(t)}</p>")
        c.append("</div>")
    c.append(f"<p class='nutri'>Por porción: {n['kcal']} kcal · {n['prot']} g de proteína · "
             f"{n['calcio']} mg de calcio · {n['fibra']} g de fibra · {n['hierro']} mg de hierro.</p>")
    # enlaces de vuelta
    estaciones = []
    for est in ESTACIONES:
        for sem in ["A", "B"]:
            for dia in D["menus"][sem]["temporadas"][est]["dias"]:
                if r["id"] in [dia[t] for t in TOMAS] and est not in estaciones:
                    estaciones.append(est)
    c.append("<p class='volver'>Volver a: " +
             " · ".join(f"<a href='menus.xhtml#{est}'>menú de {e(D['estaciones'][est]['nombre'].lower())}</a>"
                        for est in estaciones) +
             " · <a href='recetas.xhtml'>índice de recetas</a></p>")
    return pagina(r["nombre"], "\n".join(c))


def compras(semana, estacion):
    mapa = {}
    for dia in D["menus"][semana]["temporadas"][estacion]["dias"]:
        for t in TOMAS:
            r = REC[dia[t]]
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
    res = []
    for k in orden:
        items = sorted([v for v in mapa.values() if v["cat"] == k], key=lambda x: x["nombre"].lower())
        res.extend(items)
    return res


def fmt_g(q):
    if q >= 1000:
        v = round(q / 100) / 10
        return f"{v:.1f}".replace(".", ",") + " kg"
    if q >= 1:
        return f"{round(q)} g"
    return f"{q:.1f}".replace(".", ",") + " g"


def seccion_compras():
    c = ["<h1>Listas de compras</h1>",
         "<p>Calculadas para una persona y una semana. Multiplicá por el número de comensales.</p>"]
    for est in ESTACIONES:
        e_ = D["estaciones"][est]
        c.append(f"<h2>{e(e_['nombre'])}</h2>")
        for sem in ["A", "B"]:
            c.append(f"<h3>Menú {sem}</h3>")
            cat_actual = None
            abierta = False
            for it in compras(sem, est):
                if it["cat"] != cat_actual:
                    if abierta:
                        c.append("</table>")
                    cat_actual = it["cat"]
                    c.append(f"<p><strong>{e(D['cats'][cat_actual])}</strong></p>")
                    c.append("<table><tr><th>Producto</th><th>Cantidad</th></tr>")
                    abierta = True
                cant = (f"{__import__('math').ceil(it['g'] / 50)} unidades" if it["u"]
                        else fmt_g(it["g"]))
                c.append(f"<tr><td>{e(it['nombre'])}</td><td>{e(cant)}</td></tr>")
            if abierta:
                c.append("</table>")
    return pagina("Listas de compras", "\n".join(c))


def seccion_viandas():
    c = ["<h1>Guía de viandas</h1>",
         "<p>Cocinar una vez, comer bien toda la semana. Envases, frío, recalentado y texturas.</p>"]
    for s in D["guia"]["secciones"]:
        c.append(f"<h2>{e(s['titulo'])}</h2><ul>")
        for i in s["items"]:
            c.append(f"<li>{e(i)}</li>")
        c.append("</ul>")
    c.append("<h2>Cuánto dura en el freezer</h2><table><tr><th>Preparación</th><th>Duración</th>"
             "<th>Consejo</th></tr>")
    for f in D["guia"]["congelado"]:
        c.append(f"<tr><td>{e(f[0])}</td><td>{e(f[1])}</td><td>{e(f[2])}</td></tr>")
    c.append("</table>")
    return pagina("Guía de viandas", "\n".join(c))


def seccion_nutricion():
    c = ["<h1>Nutrición</h1>", f"<p>{e(D['nutricion']['intro'])}</p>"]
    c.append("<h2>Nutrientes clave</h2>")
    for n in D["nutricion"]["claves"]:
        c.append(f"<h3>{e(n['nutriente'])} <span class='meta'>· {e(n['meta'])}</span></h3>")
        c.append(f"<p>{e(n['para'])}</p>")
        c.append(f"<p class='meta'>Dónde: {e(n['fuentes'])}</p>")
        c.append(f"<p>{e(n['como'])}</p>")
    c.append("<h2>El plato saludable</h2><table><tr><th>Proporción</th><th>Qué poner</th>"
             "<th>Qué aporta</th></tr>")
    for it in D["nutricion"]["plato"]["items"]:
        c.append(f"<tr><td>{e(it[0])}</td><td>{e(it[1])}</td><td>{e(it[2])}</td></tr>")
    c.append("</table>")
    c.append("<h2>Cobertura por estación</h2><table><tr><th>Menú</th><th>Estación</th>"
             "<th>kcal</th><th>Proteína</th><th>Calcio</th></tr>")
    for sem in ["A", "B"]:
        for est in ESTACIONES:
            filas = D["resumen"][sem][est]
            prom = lambda k: sum(x[k] for x in filas) / len(filas)
            c.append(f"<tr><td>{sem}</td><td>{e(D['estaciones'][est]['nombre'])}</td>"
                     f"<td>{prom('kcal'):.0f}</td><td>{prom('prot'):.0f} g</td>"
                     f"<td>{prom('calcio'):.0f} mg</td></tr>")
    c.append("</table>")
    c.append("<h2>Las 10 recomendaciones</h2><ol>")
    for g in D["gapa"]:
        c.append(f"<li>{e(g)}</li>")
    c.append("</ol>")
    return pagina("Nutrición", "\n".join(c))


def construir():
    portada()
    docs = {
        "intro.xhtml": seccion_intro(),
        "menus.xhtml": seccion_menus(),
        "recetas.xhtml": seccion_indice_recetas(),
        "compras.xhtml": seccion_compras(),
        "viandas.xhtml": seccion_viandas(),
        "nutricion.xhtml": seccion_nutricion(),
    }
    for r in D["recetas"]:
        docs[f"receta_{r['id']}.xhtml"] = pagina_receta(r)

    nav = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="es">
<head><meta charset="utf-8"/><title>Índice</title></head>
<body>
<nav epub:type="toc" id="toc"><h1>Contenido</h1><ol>
<li><a href="text/intro.xhtml">Cómo usar este libro</a></li>
<li><a href="text/menus.xhtml">Menús por estación</a>
  <ol>
    <li><a href="text/menus.xhtml#invierno">Invierno</a></li>
    <li><a href="text/menus.xhtml#otono">Otoño</a></li>
    <li><a href="text/menus.xhtml#primavera">Primavera</a></li>
    <li><a href="text/menus.xhtml#verano">Verano</a></li>
  </ol></li>
<li><a href="text/recetas.xhtml">Índice de recetas</a></li>
<li><a href="text/compras.xhtml">Listas de compras</a></li>
<li><a href="text/viandas.xhtml">Guía de viandas</a></li>
<li><a href="text/nutricion.xhtml">Nutrición</a></li>
</ol></nav>
</body></html>"""

    items = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
             '<item id="css" href="styles.css" media-type="text/css"/>',
             '<item id="cover" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
             '<item id="portada" href="text/portada.xhtml" media-type="application/xhtml+xml"/>']
    spine = ['<itemref idref="portada"/>']
    for i, (nombre, _) in enumerate(docs.items()):
        items.append(f'<item id="d{i}" href="text/{nombre}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="d{i}"/>')

    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="es">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'viandas-mayores')}</dc:identifier>
<dc:title>Viandas Mayores · Plan de comidas para personas mayores</dc:title>
<dc:creator>Viandas Mayores</dc:creator>
<dc:language>es</dc:language>
<dc:date>{date.today().isoformat()}</dc:date>
<dc:description>8 semanas de menús, 66 recetas, listas de compras y guía de viandas para personas mayores.</dc:description>
<meta property="dcterms:modified">2026-11-28T00:00:00Z</meta>
<meta name="cover" content="cover"/>
</metadata>
<manifest>
{chr(10).join(items)}
</manifest>
<spine>
{chr(10).join(spine)}
</spine>
</package>"""

    portada_xhtml = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head><meta charset="utf-8"/><title>Portada</title>
<link rel="stylesheet" href="../styles.css" type="text/css"/></head>
<body class="portada">
<img src="../cover.jpg" alt="Viandas Mayores"/>
</body></html>"""

    out = "Viandas_Mayores.epub"
    if os.path.exists(out):
        os.remove(out)
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>""", compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/styles.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        z.write("epub-build/cover.jpg", "OEBPS/cover.jpg", compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/text/portada.xhtml", portada_xhtml, compress_type=zipfile.ZIP_DEFLATED)
        for nombre, contenido in docs.items():
            z.writestr(f"OEBPS/text/{nombre}", contenido, compress_type=zipfile.ZIP_DEFLATED)
    print(f"EPUB generado: {out} ({len(docs)+5} documentos)")


if __name__ == "__main__":
    construir()
