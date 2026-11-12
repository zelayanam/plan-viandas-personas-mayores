/* ============================================================
   Viandas Mayores · lógica de la aplicación
   Sin dependencias. Funciona abriendo index.html (file://).
   ============================================================ */
(function () {
  "use strict";

  const D = window.DATOS;
  if (!D) { document.body.innerHTML = "<p style='padding:40px'>No se encontró datos.js</p>"; return; }

  const $ = (s, c) => (c || document).querySelector(s);
  const $$ = (s, c) => Array.from((c || document).querySelectorAll(s));
  const REC = {};
  D.recetas.forEach(r => { REC[r.id] = r; });

  const TIPO_ICONO = {
    desayuno: "☕", colacion: "🍎", almuerzo: "🍲", merienda: "🍵", cena: "🌙"
  };
  const TIPO_NOMBRE = {
    desayuno: "Desayuno", colacion: "Colación", almuerzo: "Almuerzo", merienda: "Merienda", cena: "Cena"
  };
  const BEN_NOMBRE = {
    musculo: "Músculo", huesos: "Huesos", energia: "Energía", digestivo: "Digestión",
    inmune: "Defensas", corazon: "Corazón", hidrata: "Hidratación", hierro: "Hierro"
  };
  const CAT_ICONO = {
    verduleria: "🥬", carniceria: "🥩", lacteos: "🥛", almacen: "🫙",
    panaderia: "🍞", congelados: "❄️", otros: "🧾"
  };
  const CAT_ORDEN = ["verduleria", "carniceria", "lacteos", "panaderia", "almacen", "congelados", "otros"];

  /* ---------------- estado ---------------- */
  const CLAVE = "viandas-mayores-v1";
  const estadoGuardado = leerEstado();
  const state = {
    estacion: estadoGuardado.estacion || estacionPorFecha(),
    menu: estadoGuardado.menu || "A",
    porciones: Number(estadoGuardado.porciones) || 1,
    vista: "menu",
    semanaCompras: estadoGuardado.semanaCompras || "A",
    checks: estadoGuardado.checks || {},
    filtroTipo: "todas",
    filtroBen: "todos",
    busqueda: ""
  };

  function leerEstado() {
    try { return JSON.parse(localStorage.getItem(CLAVE)) || {}; } catch (e) { return {}; }
  }
  function guardarEstado() {
    try {
      localStorage.setItem(CLAVE, JSON.stringify({
        estacion: state.estacion, menu: state.menu, porciones: state.porciones,
        semanaCompras: state.semanaCompras, checks: state.checks
      }));
    } catch (e) { /* modo privado */ }
  }
  function estacionPorFecha() {
    const m = new Date().getMonth() + 1;
    if (m >= 9 && m <= 11) return "primavera";
    if (m === 12 || m <= 2) return "verano";
    if (m >= 3 && m <= 5) return "otono";
    return "invierno";
  }

  /* ---------------- utilidades ---------------- */
  function num(n, dec) {
    if (dec === undefined) dec = 0;
    return n.toLocaleString("es-AR", { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  function norm(s) {
    return String(s).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  function nombreIng(ing) {
    if (ing.est && D.estacional[ing.est]) {
      return D.estacional[ing.est][state.estacion] || ing.n;
    }
    return ing.n;
  }
  function factor(receta) {
    return state.porciones / (receta.porciones || 1);
  }
  function fmtCantidad(ing, receta) {
    const total = ing.q * factor(receta);
    if (ing.n === "huevo") {
      const u = total / 50;
      return `${num(u, u % 1 ? 1 : 0)} ${u === 1 ? "unidad" : "unidades"}`;
    }
    if (total >= 1000) return `${num(total / 1000, 2)} kg`;
    if (total >= 1) return `${num(Math.round(total))} g`;
    return `${num(total, 1)} g`;
  }
  function kcalTexto(n) { return `${num(n)} kcal`; }

  /* ---------------- navegación ---------------- */
  function navegar(vista, silencioso) {
    state.vista = vista;
    $$(".vista").forEach(v => v.classList.toggle("activa", v.id === "vista-" + vista));
    $$(".tab").forEach(t => {
      const on = t.dataset.vista === vista;
      t.classList.toggle("activo", on);
      t.setAttribute("aria-selected", on ? "true" : "false");
    });
    if (!silencioso) {
      history.replaceState(null, "", "#" + vista);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    if (vista === "compras") renderCompras();
  }
  document.addEventListener("click", e => {
    const el = e.target.closest("[data-vista]");
    if (el && el.dataset.vista) { navegar(el.dataset.vista); }
  });

  /* ---------------- render: selects ---------------- */
  function initControles() {
    const selEst = $("#sel-estacion");
    selEst.innerHTML = Object.keys(D.estaciones).map(k =>
      `<option value="${k}">${D.estaciones[k].emoji} ${D.estaciones[k].nombre}</option>`).join("");
    selEst.value = state.estacion;
    selEst.addEventListener("change", () => {
      state.estacion = selEst.value;
      guardarEstado();
      renderTodo();
    });

    const selMenu = $("#sel-menu");
    selMenu.value = state.menu;
    selMenu.addEventListener("change", () => {
      state.menu = selMenu.value;
      guardarEstado();
      renderTodo();
    });

    const selPor = $("#sel-porciones");
    selPor.value = String(state.porciones);
    selPor.addEventListener("change", () => {
      state.porciones = Number(selPor.value);
      guardarEstado();
      renderTodo();
    });

    $("#btn-imprimir").addEventListener("click", () => window.print());
  }

  /* ---------------- render: menú ---------------- */
  function renderMenu() {
    const est = D.estaciones[state.estacion];
    const menu = D.menus[state.menu];

    $("#hero-estacion").textContent = `${est.emoji} ${est.nombre} · ${est.meses}`;
    $("#hero-desc").textContent = menu.descripcion;
    $("#titulo-menu").textContent = `${menu.nombre} · ${menu.lema}`;

    const filas = D.resumen[state.menu];
    const prom = k => filas.reduce((a, f) => a + f[k], 0) / filas.length;
    $("#hero-resumen").innerHTML = `
      <h4>Promedio por día</h4>
      <div class="resumen-fila"><span>Energía</span><strong>${num(prom("kcal"))} kcal</strong></div>
      <div class="resumen-fila"><span>Proteínas</span><strong>${num(prom("prot"))} g</strong></div>
      <div class="resumen-fila"><span>Calcio</span><strong>${num(prom("calcio"))} mg</strong></div>
      <div class="resumen-fila"><span>Fibra</span><strong>${num(prom("fibra"))} g</strong></div>`;

    const destacados = est.destacados.join(", ");
    const nota = est.nota.charAt(0).toLowerCase() + est.nota.slice(1);
    $("#aviso-estacion").innerHTML =
      `<strong>${est.emoji} ${est.nombre}:</strong> ${esc(nota)} ` +
      `<br><span style="color:var(--suave)">Lo mejor de la estación: <em>${esc(destacados)}</em>.</span>`;

    $("#contenedor-dias").innerHTML = menu.dias.map(d => {
      const tomas = D.tomas.map(t => {
        const r = REC[d[t.id]];
        return `
          <button class="comida ${t.id}" data-receta="${r.id}" aria-label="Ver receta de ${esc(r.nombre)}">
            <span class="comida-ico" aria-hidden="true">${TIPO_ICONO[t.id]}</span>
            <span class="comida-txt">
              <span class="comida-hora">${t.nombre} · ${t.hora}</span>
              <span class="comida-nombre">${esc(r.nombre)}</span>
            </span>            <span class="comida-kcal">${num(r.nutricion.kcal)} kcal</span>
          </button>`;
      }).join("");

      const total = D.tomas.reduce((a, t) => a + REC[d[t.id]].nutricion.kcal, 0);
      const prot = D.tomas.reduce((a, t) => a + REC[d[t.id]].nutricion.prot, 0);
      const cal = D.tomas.reduce((a, t) => a + REC[d[t.id]].nutricion.calcio, 0);

      return `
        <article class="dia">
          <div class="dia-cab">
            <h3>${d.dia}</h3>
            <span class="kcal-dia">${num(total)} kcal</span>
          </div>
          <div class="comidas">${tomas}</div>
          <div class="dia-pie">
            <span>Proteína ${num(prot)} g</span>
            <span>Calcio ${num(cal)} mg</span>
          </div>
        </article>`;
    }).join("");
  }

  /* ---------------- render: recetas ---------------- */
  function renderFiltros() {
    const tipos = [["todas", "Todas"], ["desayuno", "Desayunos"], ["colacion", "Colaciones"],
      ["almuerzo", "Almuerzos"], ["merienda", "Meriendas"], ["cena", "Cenas"]];
    $("#filtros-tipo").innerHTML = tipos.map(([v, n]) =>
      `<button class="chip ${state.filtroTipo === v ? "activo" : ""}" data-tipo="${v}">${n}</button>`).join("");

    const bens = [["todos", "Todos"], ["musculo", "Masa muscular"], ["huesos", "Huesos"],
      ["corazon", "Corazón"], ["digestivo", "Digestión"], ["hierro", "Hierro"], ["inmune", "Defensas"]];
    $("#filtros-beneficio").innerHTML = bens.map(([v, n]) =>
      `<button class="chip ${state.filtroBen === v ? "activo" : ""}" data-ben="${v}">${n}</button>`).join("");

    $$("#filtros-tipo .chip").forEach(b => b.addEventListener("click", () => {
      state.filtroTipo = b.dataset.tipo; renderFiltros(); renderRecetas();
    }));
    $$("#filtros-beneficio .chip").forEach(b => b.addEventListener("click", () => {
      state.filtroBen = b.dataset.ben; renderFiltros(); renderRecetas();
    }));
  }

  function recetasFiltradas() {
    const q = norm(state.busqueda.trim());
    return D.recetas.filter(r => {
      if (state.filtroTipo !== "todas" && r.tipo !== state.filtroTipo) return false;
      if (state.filtroBen !== "todos" && !(r.beneficios || []).includes(state.filtroBen)) return false;
      if (!q) return true;
      const texto = norm([r.nombre, r.tipo,
        (r.ingredientes || []).map(i => i.n + " " + (i.est ? Object.values(D.estacional[i.est]).join(" ") : "")).join(" "),
        (r.pasos || []).join(" ")].join(" "));
      return texto.includes(q);
    });
  }

  function renderRecetas() {
    const lista = recetasFiltradas();
    $("#grid-recetas").innerHTML = lista.map(r => {
      const n = r.nutricion;
      return `
        <button class="receta-card" data-receta="${r.id}">
          <div class="receta-top">
            <span class="etiqueta ${r.tipo}">${TIPO_NOMBRE[r.tipo] || r.tipo}</span>
            <span class="receta-meta">⏱ ${r.tiempo} min</span>
          </div>
          <h3>${esc(r.nombre)}</h3>
          <div class="receta-meta">
            <span>${r.apto_vianda ? "🥡 Apta vianda" : "🍽 Para servir"}</span>
            ${r.porciones > 1 ? `<span>Rinde ${r.porciones} porciones</span>` : ""}
          </div>
          <div class="receta-nutri">
            <span class="pill">${num(n.kcal)} kcal</span>
            <span class="pill">${num(n.prot)} g proteína</span>
            <span class="pill">${num(n.calcio)} mg calcio</span>
          </div>
          <div class="beneficios">${(r.beneficios || []).slice(0, 3).map(b =>
            `<span class="benef">${BEN_NOMBRE[b] || b}</span>`).join("")}</div>
        </button>`;
    }).join("");
    $("#sin-resultados").hidden = lista.length > 0;
  }

  /* ---------------- modal receta ---------------- */
  let ultimoFoco = null;
  function abrirReceta(id) {
    const r = REC[id];
    if (!r) return;
    ultimoFoco = document.activeElement;
    const n = r.nutricion;

    const estacionales = [...new Set((r.ingredientes || []).filter(i => i.est).map(i => i.est))];
    const notaEst = estacionales.length ? `
      <div class="modal-estacion">
        <strong>Versión de ${D.estaciones[state.estacion].nombre.toLowerCase()}:</strong>
        ${estacionales.map(k => `${k === "hojas" ? "hojas verdes" : k === "fruta" ? "fruta" : k === "verdura_salteado" ? "verduras" : k === "verdura_horno" ? "verduras" : k === "verdura_sopa" ? "verduras" : k === "fruta2" ? "fruta" : k === "citrico" ? "cítrico" : k} → <em>${esc(D.estacional[k][state.estacion])}</em>`).join(" · ")}
      </div>` : "";

    const contenido = `
      <span class="etiqueta ${r.tipo}">${TIPO_NOMBRE[r.tipo] || r.tipo}</span>
      <h2 id="modal-titulo">${esc(r.nombre)}</h2>
      <div class="modal-meta">
        <span class="pill">⏱ ${r.tiempo} min</span>
        <span class="pill">${esc(r.dificultad)}</span>
        <span class="pill">${r.apto_vianda ? "🥡 Apta vianda" : "🍽 Para servir en el momento"}</span>
        <span class="pill">${state.porciones} ${state.porciones === 1 ? "porción" : "porciones"}</span>
        ${r.porciones > 1 ? `<span class="pill">La receta rinde ${r.porciones}</span>` : ""}
      </div>

      <h3>Ingredientes</h3>
      <ul class="modal-ingredientes">
        ${(r.ingredientes || []).map(i => `
          <li>
            <span>${esc(nombreIng(i))}${i.est ? "" : ""}</span>
            <span class="c">${fmtCantidad(i, r)}</span>
          </li>`).join("")}
      </ul>
      ${notaEst}

      <h3>Preparación</h3>
      <ol class="modal-pasos">${(r.pasos || []).map(p => `<li>${esc(p)}</li>`).join("")}</ol>

      ${(r.tips || []).length ? `<h3>Consejos</h3>${r.tips.map(t =>
        `<div class="modal-tip">💡 ${esc(t)}</div>`).join("")}` : ""}

      <h3>Por porción</h3>
      <div class="modal-nutri">
        <div><b>${num(n.kcal)}</b><small>kcal</small></div>
        <div><b>${num(n.prot)} g</b><small>proteína</small></div>
        <div><b>${num(n.calcio)} mg</b><small>calcio</small></div>
        <div><b>${num(n.fibra)} g</b><small>fibra</small></div>
      </div>
      <p style="font-size:.72rem;color:var(--suave);margin-top:10px">
        Valores estimados con tablas de composición de alimentos. Pueden variar según marca y tamaño de la porción.
      </p>`;

    $("#modal-contenido").innerHTML = contenido;
    $("#modal").hidden = false;
    document.body.style.overflow = "hidden";
    $(".modal-cerrar").focus();
    try {
      const url = new URL(location.href);
      url.searchParams.set("receta", id);
      history.replaceState(null, "", url);
    } catch (e) { /* file:// sin soporte */ }
  }
  function cerrarModal() {
    $("#modal").hidden = true;
    document.body.style.overflow = "";
    if (ultimoFoco) ultimoFoco.focus();
    try {
      const url = new URL(location.href);
      url.searchParams.delete("receta");
      history.replaceState(null, "", url);
    } catch (e) { /* file:// sin soporte */ }
  }
  document.addEventListener("click", e => {
    const r = e.target.closest("[data-receta]");
    if (r) { e.preventDefault(); abrirReceta(r.dataset.receta); }
    if (e.target.closest("[data-cerrar]")) cerrarModal();
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !$("#modal").hidden) cerrarModal();
    if (e.key === "Tab" && !$("#modal").hidden) {
      const foco = $$("button, [href], input, select, textarea", $("#modal")).filter(el => el.offsetParent !== null);
      if (!foco.length) return;
      const primero = foco[0], ultimo = foco[foco.length - 1];
      if (e.shiftKey && document.activeElement === primero) { e.preventDefault(); ultimo.focus(); }
      else if (!e.shiftKey && document.activeElement === ultimo) { e.preventDefault(); primero.focus(); }
    }
  });

  /* ---------------- lista de compras ---------------- */
  function construirCompras(semanas) {
    const mapa = new Map();
    semanas.forEach(sem => {
      D.menus[sem].dias.forEach(d => {
        D.tomas.forEach(t => {
          const r = REC[d[t.id]];
          const f = factor(r);
          (r.ingredientes || []).forEach(i => {
            if (i.n === "infusion" || i.n === "agua") return;
            let nombre = nombreIng(i);
            if (i.est && D.etiquetas_est && D.etiquetas_est[i.est]) {
              nombre = `${D.etiquetas_est[i.est]}: ${nombre}`;
            }
            const clave = norm(nombre) + "|" + i.cat;
            const prev = mapa.get(clave) || {
              nombre, cat: i.cat, g: 0, unidad: i.n === "huevo" ? "u" : "g"
            };
            prev.g += i.q * f;
            mapa.set(clave, prev);
          });
        });
      });
    });
    return Array.from(mapa.values()).sort((a, b) => {
      const ca = CAT_ORDEN.indexOf(a.cat), cb = CAT_ORDEN.indexOf(b.cat);
      if (ca !== cb) return ca - cb;
      return a.nombre.localeCompare(b.nombre, "es");
    });
  }

  function formatoCompra(p) {
    if (p.unidad === "u") {
      const u = Math.ceil(p.g / 50);
      return `${num(u)} ${u === 1 ? "unidad" : "unidades"}`;
    }
    if (p.g >= 1000) {
      const v = Math.round(p.g / 100) / 10;
      return `${num(v, v % 1 ? 1 : 0)} kg`;
    }
    if (p.g >= 1) return `${num(Math.round(p.g))} g`;
    return `${num(p.g, 1)} g`;
  }

  function renderCompras() {
    const semanas = state.semanaCompras === "AB" ? ["A", "B"] : [state.semanaCompras];
    const productos = construirCompras(semanas);

    const porCat = {};
    productos.forEach(p => { (porCat[p.cat] = porCat[p.cat] || []).push(p); });

    $("#contenedor-compras").innerHTML = CAT_ORDEN.filter(c => porCat[c]).map(c => {
      const items = porCat[c];
      return `
        <div class="categoria">
          <h3>${CAT_ICONO[c] || "🧾"} ${D.cats[c] || c} <span class="cuenta">${items.length}</span></h3>
          <div class="items">
            ${items.map(p => {
              const key = norm(p.nombre) + "|" + p.cat;
              const on = !!state.checks[key];
              return `
                <label class="item ${on ? "tildado" : ""}" data-key="${esc(key)}">
                  <input type="checkbox" ${on ? "checked" : ""} data-check="${esc(key)}">
                  <span class="nombre">${esc(p.nombre)}</span>
                  <span class="cant">${formatoCompra(p)}</span>
                </label>`;
            }).join("")}
          </div>
        </div>`;
    }).join("");

    actualizarProgreso(productos.length);
    $$("[data-check]").forEach(ch => ch.addEventListener("change", e => {
      const key = e.target.dataset.check;
      if (e.target.checked) state.checks[key] = true; else delete state.checks[key];
      e.target.closest(".item").classList.toggle("tildado", e.target.checked);
      guardarEstado();
      actualizarProgreso(productos.length);
    }));

    $("#seg-compras").querySelectorAll("button").forEach(b => {
      b.classList.toggle("activo", b.dataset.semana === state.semanaCompras);
      b.onclick = () => {
        state.semanaCompras = b.dataset.semana;
        guardarEstado();
        renderCompras();
      };
    });

    $("#btn-copiar").onclick = () => {
      const texto = CAT_ORDEN.filter(c => porCat[c]).map(c =>
        `${D.cats[c]}\n` + porCat[c].map(p => `- ${p.nombre}: ${formatoCompra(p)}`).join("\n")
      ).join("\n\n");
      copiar(texto).then(() => toast("Lista copiada al portapapeles")).catch(() => toast("No se pudo copiar"));
    };

    $("#btn-csv").onclick = () => {
      const filas = [["Categoria", "Producto", "Cantidad"]];
      CAT_ORDEN.filter(c => porCat[c]).forEach(c => {
        porCat[c].forEach(p => filas.push([D.cats[c], p.nombre, formatoCompra(p)]));
      });
      const csv = "\ufeff" + filas.map(f => f.map(x => `"${String(x).replace(/"/g, '""')}"`).join(";")).join("\r\n");
      descargar(csv, "lista-de-compras.csv", "text/csv;charset=utf-8");
      toast("Lista descargada");
    };

    $("#btn-reset-checks").onclick = () => {
      state.checks = {};
      guardarEstado();
      renderCompras();
      toast("Se destildaron todos los productos");
    };
  }

  function actualizarProgreso(total) {
    const tildados = Object.keys(state.checks).length;
    const pct = total ? Math.min(100, (tildados / total) * 100) : 0;
    $("#barra-compras").style.width = pct + "%";
    $("#texto-progreso").textContent = `${tildados} de ${total} productos`;
  }

  function copiar(texto) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(texto);
    return new Promise((res, rej) => {
      const ta = document.createElement("textarea");
      ta.value = texto; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy") ? res() : rej(); } catch (e) { rej(e); }
      document.body.removeChild(ta);
    });
  }
  function descargar(contenido, nombre, tipo) {
    const blob = new Blob([contenido], { type: tipo });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = nombre; document.body.appendChild(a); a.click();
    document.body.removeChild(a); setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  let toastTimer;
  function toast(msg) {
    const t = $("#toast");
    t.textContent = msg; t.classList.add("visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove("visible"), 2600);
  }

  /* ---------------- guía ---------------- */
  function renderGuia() {
    $("#grid-guia").innerHTML = D.guia.secciones.map(s => `
      <article class="guia-card">
        <h3><span aria-hidden="true">${s.icono}</span> ${esc(s.titulo)}</h3>
        <ul>${s.items.map(i => `<li>${esc(i)}</li>`).join("")}</ul>
      </article>`).join("");

    $("#tabla-freezer").querySelector("tbody").innerHTML = D.guia.congelado.map(f =>
      `<tr><td>${esc(f[0])}</td><td>${esc(f[1])}</td><td>${esc(f[2])}</td></tr>`).join("");

    $("#grid-tips").innerHTML = D.tips.map(t => `
      <div class="tip"><h4>${esc(t.titulo)}</h4><p>${esc(t.texto)}</p></div>`).join("");
  }

  /* ---------------- nutrición ---------------- */
  function renderNutricion() {
    $("#destacado-nutricion").innerHTML =
      `<p><strong>${esc(D.nutricion.titulo)}.</strong> ${esc(D.nutricion.intro)}</p>`;

    $("#grid-nutrientes").innerHTML = D.nutricion.claves.map(c => `
      <article class="nutri-card">
        <h3>${esc(c.nutriente)}</h3>
        <span class="nutri-meta">${esc(c.meta)}</span>
        <dl>
          <dt>Para qué</dt><dd>${esc(c.para)}</dd>
          <dt>Dónde está</dt><dd>${esc(c.fuentes)}</dd>
          <dt>Cómo lo resuelve el plan</dt><dd>${esc(c.como)}</dd>
        </dl>
      </article>`).join("");

    $("#plato-lista").innerHTML = D.nutricion.plato.items.map(it =>
      `<li><strong>${esc(it[0])}</strong><span>${esc(it[1])}<br><small style="color:var(--suave)">${esc(it[2])}</small></span></li>`).join("");

    const filas = D.resumen[state.menu];
    const prom = k => filas.reduce((a, f) => a + f[k], 0) / filas.length;
    const objetivos = [
      { k: "kcal", t: "Energía", obj: 1800, u: "kcal", dec: 0 },
      { k: "prot", t: "Proteínas", obj: 85, u: "g", dec: 0 },
      { k: "calcio", t: "Calcio", obj: 1100, u: "mg", dec: 0 },
      { k: "fibra", t: "Fibra", obj: 28, u: "g", dec: 0 },
      { k: "hierro", t: "Hierro", obj: 12, u: "mg", dec: 0 },
    ];
    $("#grid-cobertura").innerHTML = objetivos.map(o => {
      const val = prom(o.k);
      const pct = Math.round((val / o.obj) * 100);
      return `
        <div class="cob">
          <div class="cab"><span>${o.t}</span><span>${num(val, o.dec)} ${o.u}</span></div>
          <div class="barra"><span class="${pct < 80 ? "bajo" : ""}" style="width:${Math.min(100, pct)}%"></span></div>
          <small>${pct}% del objetivo diario (${num(o.obj)} ${o.u}) · Menú ${state.menu}</small>
        </div>`;
    }).join("");

    $("#lista-gapa").innerHTML = D.gapa.map(g => `<li>${esc(g)}</li>`).join("");
  }

  /* ---------------- render general ---------------- */
  function renderTodo() {
    renderMenu();
    renderFiltros();
    renderRecetas();
    renderGuia();
    renderNutricion();
    if (state.vista === "compras") renderCompras();
    const est = D.estaciones[state.estacion];
    $("#pie-estacion").textContent = `${est.emoji} ${est.nombre} · ${est.meses}`;
  }

  /* ---------------- inicio ---------------- */
  function init() {
    // Enlaces directos: ?estacion=invierno&menu=B&porciones=4
    try {
      const params = new URLSearchParams(location.search);
      const est = params.get("estacion");
      if (est && D.estaciones[est]) state.estacion = est;
      const men = params.get("menu");
      if (men && D.menus[men]) state.menu = men;
      const por = Number(params.get("porciones"));
      if ([1, 2, 4, 6].includes(por)) state.porciones = por;
    } catch (e) { /* sin soporte */ }

    initControles();
    renderTodo();
    if (state.vista === "compras") renderCompras();

    const hash = location.hash.replace("#", "");
    if (["menu", "recetas", "compras", "viandas", "nutricion"].includes(hash)) navegar(hash, true);

    const params = new URLSearchParams(location.search);
    if (params.get("receta") && REC[params.get("receta")]) {
      abrirReceta(params.get("receta"));
    }

    $("#buscar").addEventListener("input", e => {
      state.busqueda = e.target.value;
      renderRecetas();
    });
    window.addEventListener("hashchange", () => {
      const h = location.hash.replace("#", "");
      if (["menu", "recetas", "compras", "viandas", "nutricion"].includes(h)) navegar(h, true);
    });
    window.addEventListener("beforeprint", () => {
      if (state.vista === "compras") renderCompras();
    });
  }

  init();
})();
