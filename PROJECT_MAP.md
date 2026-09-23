# PROJECT_MAP — MisApps (catálogo sobre GitHub Releases + Firebase Hosting)

## Qué es
App web estática (sin build, sin backend) que arma sola su catálogo desde los
**Releases de un repo GitHub**. Visitantes descargan **sin login** vía links directos
`releases/download/...`. Hosting de la página: **Firebase Hosting**.

## Estructura
```
mi-tienda-apps/
├── index.html                  # UI + lógica completa (fetch a API de GitHub)
├── config.json                 # {owner, repo, siteName} de producción
├── apps.json                   # entradas curadas/manual (extra, opcional)
├── firebase.json               # config de Firebase Hosting (public: .)
├── .firebaserc                 # proyecto Firebase (PENDIENTE: poner ID real)
├── .github/workflows/firebase-hosting.yml  # deploy auto en push a main
├── README.md                   # setup, publicación, deploy
├── preview.png / preview-gh.png # screenshots de referencia
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
- Catálogo automático desde Releases (filtra drafts y releases sin assets).
- Múltiples assets por release: filas individuales con tamaño y contador de descargas;
  1 asset = botón Descargar grande.
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
- Nombre del repo GitHub (owner/repo) + crearlo y subir este código.
- ID del proyecto Firebase + `firebase login` + primer deploy.
- Secrets del workflow (`FIREBASE_SERVICE_ACCOUNT`, var `FIREBASE_PROJECT_ID`).
- Quitar Drive de la historia (ya eliminado del código; queda mención en memoria vieja).
