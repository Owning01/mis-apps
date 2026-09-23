# PROJECT_MEMORY — bitácora (append-only)

## 2026-09-23 — Creación inicial de MisApps
- Se creó la página estática `index.html` (catálogo + panel del dueño) para subir apps a Google Drive
  y descargarlas sin login del visitante; pedido por el usuario: "entro, subo, y otros descargan con un clic".
- Por qué: el usuario preguntó si se puede almacenar en Drive y si el que descarga necesita cuenta
  Google → respuesta implementada: solo el dueño usa OAuth (`drive.file`), los archivos se publican
  con permiso `anyone/reader` y la descarga va por `uc?export=download`.
- Evidencia: archivos creados `index.html`, `apps.json`, `README.md`, `PROJECT_MAP.md`;
  servidor verificado `python -m http.server 8010` → `/` y `/apps.json` responden 200.
- Sorpresa: el puerto 8000 ya estaba ocupado por otro servidor Python (PID 28988, carpeta con
  `app-release.apk` etc.) — se documentó usar 8010 en vez de matar el proceso ajeno.
- Trampas: >100 MB dispara confirmación anti-virus de Drive; `file://` rompe el fetch del catálogo
  (hay que servir por HTTP); scope `drive.file` no ve archivos subidos por otras vías.
- Pendiente: obtener Client ID del usuario y configurar origen de JS; decidir hosting público.

## 2026-09-23 — Verificación visual y fix de favicon
- Se sirvió la página en `http://localhost:8010` y se validó en navegador: UI completa (hero, stats,
  catálogo con card demo, botones), consola con **0 errores** tras agregar favicon SVG inline.
- Evidencia: screenshot `preview.png` en la carpeta del proyecto; `browser_console_messages` → 0.
- Trampa: el puerto 8000 ya estaba tomado por otro server (APKs); se usó 8010. No matar procesos ajenos.
- Pendiente: Client ID OAuth del dueño + subir primera app real + hosting público.

## 2026-09-23 — Cambio de modelo: GitHub Releases + Firebase Hosting (adiós Drive)
- El usuario decidió: **todo el código en un mismo repo GitHub**, hosting en **Firebase**,
  descargas desde **GitHub Releases**. Se eliminó todo el código de Google Drive/OAuth.
- Cambios: `index.html` reescrito (catálogo automático vía `api.github.com/.../releases`,
  múltiples assets por release, chips NUEVA/BETA, fallback a `apps.json`+caché, config por
  `?owner=&repo=` > localStorage > `config.json`); nuevos `config.json`, `firebase.json`,
  `.firebaserc` (placeholder), `.github/workflows/firebase-hosting.yml`; README reescrito.
- Evidencia: entorno verificado (git 2.55, node 24, firebase-tools 15.30, gh 2.100).
- Pendiente: owner/repo del repo, ID proyecto Firebase, `firebase login`, primer deploy,
  secrets del workflow.

## 2026-09-23 — Verificación del modelo GitHub Releases + fix botón muerto
- Prueba con repo real `?owner=cli&repo=cli`: **51 cards** (50 releases + 1 curada), links
  `releases/download/...` correctos con tamaño y contador, búsqueda filtra bien
  ("2.100.0" → 1 resultado), modal dueño apunta a `/releases/new`. **0 errores de consola**.
- Bug encontrado y fixeado: el botón principal en releases multi-asset apuntaba a `#`
  (muerto). Ahora: 1 asset → "⬇️ Descargar" directo; N assets → "📦 Ver archivos"
  (a la página del release); sin assets → etiqueta "Sin archivo adjunto". Verificado que
  no queda ningún `href="#"` en el grid. Caso 1-asset probado con entrada inyectada.
- Evidencia: `preview-gh.png` (página completa con datos reales de cli/cli).
- Pendiente: owner/repo reales, proyecto Firebase, login, deploy, secrets del workflow.
