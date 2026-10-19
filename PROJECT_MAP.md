# PROJECT_MAP — MisApps (catálogo multi-repo + Temporales + Páginas + Skills, Firebase Hosting)

## Qué es
App web estática (sin build, sin backend) que arma sola su catálogo desde los
**Releases de N repos GitHub**. Visitantes descargan **sin login** vía links directos
`releases/download/...`. Hosting: **Firebase Hosting → https://appsdeocta.web.app**.

## Repos (modelo corregido 2026-09-23)
- **`Owning01/mis-apps`** (código de la página + releases de apps SIN repo propio:
  vistamd, cinegbro, derecho-informatico, temporales `temp-*`).
- **`Owning01/Openher`** (existente, solo lectura): sus releases también salen en la página.
- Regla: app con repo propio → release en SU repo (+ agregarlo a `config.json`);
  app suelta → release en `mis-apps`.

## Estructura
```
mis-apps/  (repo git → Owning01/mis-apps, branch main)
├── index.html                  # UI + lógica (tabs Apps/Temporales/Páginas/Skills)
├── manifest.json               # PWA (nombre, iconos, standalone, theme)
├── sw.js                       # service worker (cache v3: shell + skills.json; API con red primero)
├── icons/                      # icon-192/512, maskable-512, apple-touch-icon
├── bg-abisal.jpg               # fondo abisal generado con Qwen (1920x1080)
├── config.json                 # {repos:[...], siteName, categories} de producción
├── apps.json                   # fallback curado (vacío: solo estructura)
├── pages.json                  # sitios Firebase (sección Páginas: nombre, url, icon)
├── skills.json                 # 36 skills: categoría, explicación y diagrama de uso
├── skills/                     # un .zip por skill (~4.8 MB total)
├── tools/build-skills.py       # regenera skills.json + skills/*.zip (no se deploya)
├── firebase.json               # config de Firebase Hosting (public: .)
├── desktop-update.json         # feed de actualización de LeonSys POS (escritorio)
├── DESIGN.md                   # dirección de estilo de la tienda
├── SUBIR-APPS.md               # guía para agentes: cómo publicar releases
├── README.md                   # setup, publicación, deploy
├── .gitignore                  # preview*.png, .firebaserc, .firebase/, Logo.jpg, .taste-skill/
├── PROJECT_MAP.md              # este archivo
└── PROJECT_MEMORY.md
```

## Cómo corre
- Local: `python -m http.server 8010` en la carpeta → `http://localhost:8010`
  (8000 ocupado por otro server). No usar doble clic: `file://` rompe los fetch.
- Preview con repo ajeno: `?owner=cli&repo=cli` o `?repos=owner/a,owner/b`.
- Deploy (manual, no hay CI): `firebase deploy --only hosting --project appsdeocta`.
- Skills: si cambian las carpetas de `~/.agents/skills` → `python tools/build-skills.py`
  (regenera `skills.json` + zips), commit, push y deploy.

## Stack / dependencias
- Vanilla JS + CSS, sin frameworks ni node_modules en runtime.
- Externa (runtime): API pública de GitHub (`api.github.com/repos/{o}/{r}/releases`).
- Generador de skills: Python 3 (solo stdlib).
- Deploy: firebase-tools 15.30.

## Funciones vivas
- Tabs Aplicaciones / Temporales / Páginas / Skills, con conteos en vivo.
- Catálogo multi-repo con agrupación por app (última versión en la fila; modal Historial).
- Categorías configurables (`config.json: categories`, primera coincidencia gana) + chips.
- Búsqueda global: filtra apps, temporales, sitios y skills a la vez.
- **Skills**: 36 skills agrupadas en 7 categorías, con explicación, diagrama de uso de
  3 nodos (Cuándo usarla → Qué hace → Qué entrega), chips de categoría y descarga
  `.zip` por skill (`./skills/<id>.zip`). Link de acceso en el footer.
- PWA instalable (manifest + sw + iconos). Avatares-letra deterministas, iconos SVG.
- Sin fotos en la página (a pedido); esquinas cuadradas; fondo abisal.
- Múltiples assets por release: filas individuales; 1 asset = botón grande;
  sin assets = etiqueta, nunca botón muerto.
- Prioridad de config: `config.json` → query `?repos=` / `?owner=&repo=` override.
- Fallback: caché del catálogo en localStorage y `apps.json` si GitHub falla.

## Trampas conocidas
- Rate limit anónimo GitHub: 60 req/h por IP → error visible + fallback a caché.
- `.reveal` con threshold 0.15: no dispara en elementos más altos que ~6.7× el
  viewport. Los paneles de sección NO llevan `.reveal`; al cambiar de pestaña
  `setView` re-observa los `.reveal` internos del panel activo.
- Puerto 8000 ocupado en esta máquina por otro servidor (APKs); usar 8010.
- `G:\Proyectos\mi-tienda-apps\` es un clon viejo y divergente: la fuente es esta carpeta.
- El deploy es manual (se eliminó el workflow de GitHub que no funcionaba).
