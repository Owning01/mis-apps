# PROJECT_MAP — MisApps (catálogo multi-repo + Temporales, Firebase Hosting)

## Qué es
App web estática (sin build, sin backend) que arma sola su catálogo desde los
**Releases de N repos GitHub**. Visitantes descargan **sin login** vía links directos
`releases/download/...`. Hosting: **Firebase Hosting → https://appsdeocta.web.app**.

## Repos (modelo corregido 2026-09-23)
- **`Owning01/mis-apps`** (nuevo, creado por el agente): código de la página + releases
  de apps SIN repo propio (vistamd, cinegbro, temporales `temp-*`).
- **`Owning01/Openher`** (existente, solo lectura): sus releases también salen en la página.
- Regla: app con repo propio → release en SU repo (+ agregarlo a `config.json`);
  app suelta → release en `mis-apps`.

## Estructura
```
mi-tienda-apps/  (repo git → Owning01/mis-apps, branch main)
├── index.html                  # UI + lógica (fetch multi-repo, secciones Apps/Temporales)
├── config.json                 # {repos:[...], siteName, categories} de producción
├── apps.json                   # entradas curadas/manual (extra, opcional)
├── pages.json                  # sitios Firebase (sección Páginas: nombre, url, icon)
├── firebase.json               # config de Firebase Hosting (public: .)
├── .firebaserc                 # IGNORADO en git (tiene placeholder local)
├── .gitignore                  # preview*.png + .firebaserc
├── .github/workflows/firebase-hosting.yml  # deploy auto en push a main
├── README.md                   # setup, publicación, deploy
├── preview*.png                # screenshots (no van al repo)
├── PROJECT_MAP.md              # este archivo
└── PROJECT_MEMORY.md
```

## Cómo corre
- Local: `python -m http.server 8010` → `http://localhost:8010` (8000 ocupado por otro server).
- No funciona con doble clic (file:// rompe los fetch de `config.json`/`apps.json`).
- Preview con repo ajeno: `?owner=cli&repo=cli`.
- Prod: `firebase deploy --only hosting` (requiere `firebase login` + proyecto en `.firebaserc`).

## Stack / dependencias
- Vanilla JS + CSS, sin frameworks ni node_modules.
- Externa (runtime): API pública de GitHub (`api.github.com/repos/{o}/{r}/releases`).
- Deploy: firebase-tools 15.30 verificado instalado (2026-09-23).
- Verificado 2026-09-23 con repo real `cli/cli`: 51 cards, links directos OK,
  búsqueda OK, modal dueño OK, 0 errores de consola. Fix: sin botones muertos (`href="#"`).
- Screenshots: `preview.png` (vista anterior), `preview-gh.png` (catálogo real).

## Funciones vivas
- Tabs Aplicaciones / Temporales con conteos; sin botones de dueño/ajustes en la UI.
- Tab Páginas: `pages.json` con sitios Firebase (favicon a la izquierda, abrir en pestaña nueva).
- Agrupación por app (última versión en card; modal Historial con versiones anteriores).
- Categorías configurables (`config.json: categories`, primera coincidencia gana).
- Avatares-letra deterministas, iconos SVG (cero emojis UI), tabs con teclado.
- Fetch a la API con `cache:'no-store'` (la API cachea 60s y mostraba datos viejos).
- Múltiples assets por release: filas individuales; 1 asset = botón Descargar grande;
  sin assets descargables = etiqueta, nunca botón muerto.
- Búsqueda, stats (apps / nuevas 14d / última fecha), chips versión/fecha/BETA/NUEVA.
- Fallback: `apps.json` curado + caché localStorage si GitHub falla o no hay repo.
- Prioridad de config: `?owner=&repo=` > localStorage (Ajustes) > `config.json`.
- Panel dueño: guía de publicación (link a `/releases/new`), alta manual por enlace,
  Ajustes (owner/repo/nombre/token local), exportar `apps.json`.
- Token GitHub opcional solo en el navegador (sube rate limit 60→5000/h).

## Trampas conocidas
- Rate limit anónimo GitHub: 60 req/h por IP → error visible + fallback a caché.
- `.firebaserc` tiene placeholder `TU-PROYECTO-FIREBASE`; deploy bloqueado hasta definirlo.
- Puerto 8000 ocupado en esta máquina por otro servidor (APKs); usar 8010.

## Pendiente
- Secrets del workflow (`FIREBASE_SERVICE_ACCOUNT`, var `FIREBASE_PROJECT_ID`) para deploy automático.
