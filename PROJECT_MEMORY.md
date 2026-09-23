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
- Pendiente: ID proyecto Firebase + login + deploy + secrets workflow.

## 2026-09-23 — Rediseño v2: sin admin, tabs, categorías, historial, paleta verde/naranja
- Pedido: quitar "Soy el dueño"/Ajustes, separar secciones, categorizar, ver versiones
  viejas solo al hacer click, aplicar skill taste-impecable, paleta verdes+naranjas.
- Hecho: modal del dueño eliminado; tabs Aplicaciones/Temporales (con conteos y
  flechas de teclado); agrupación por app (28 releases → 4 cards) con modal Historial
  (25 versiones de OpenHer verificadas, descarga por versión); categorías por patrones
  en `config.json` + chips filtro; paleta `#0B1411/#34D399/#F97316`, Space Grotesk+Inter,
  iconos SVG, avatares-letra, focus-visible, reduced-motion, targets 44px.
- Bugs: `$` usado antes de definir (ReferenceError, fixeado); categorías no matcheaban
  por prefijo de owner (fix: match contra repo-corto/tag, nombre y archivos); chip de
  versión mostraba el tag crudo (fix: extrae `1.0.0` de `vistamd-v1.0.0`).
- Evidencia: `preview-v2.png`; 0 errores de consola.

## 2026-09-23 — Repo mis-apps + releases reales + skill + Temporales
- Modelo corregido con el usuario: Openher NO es el repo de la página. Se creó
  **`Owning01/mis-apps`** (público): código + releases de apps sin repo. Openher aporta
  sus releases como fuente de solo lectura.
- 422 "Repository is empty" al crear releases → causa: repo recién creado sin commits.
  Fix: push inicial primero, releases después.
- Releases creados: `vistamd-v1.0.0` (vistamd.exe 11.6 MB) y `bloqueador-v1.0.0`
  (app-release.apk 44.7 MB, build release, no el debug de 157 MB).
- Página: multi-repo (`repos[]`, chip de origen, orden por fecha), sección 📁 Temporales
  (tags `temp-*`), `cache:'no-store'` (la API cachea 60s y ocultaba releases nuevos).
- Skill **`subir-a-misapps`** creado en `C:/Users/perca/.agents/skills/` + fila en INDEX.md:
  cualquier agente puede subir permanente/temporal + limpieza + verificación.
- Verificación E2E: página muestra 28 apps (mis-apps + Openher), links directos OK,
  release `temp-prueba-20260923` apareció en Temporales con chip TEMPORAL y se borró
  (release + tag) con el procedimiento del skill. 0 errores de consola.
- Evidencia: commits e540f67 + c0fb94c en Owning01/mis-apps (branch main).
- Token pegado por el usuario en el chat: NO se guardó en ningún archivo; se usó la
  sesión `gh` existente (Owning01).
- Deploy manual a Firebase hecho: https://appsdeocta.web.app (proyecto `appsdeocta`).
- Pendiente: secrets del workflow para deploy automático.

## 2026-09-23 — Deploy v2 en vivo + seguridad endurecida
- Push `6d366f9` (v2: sin admin, tabs, categorías, historial, verde/naranja) y `ec7ffb9`
  (ignorar `.firebase/`) a Owning01/mis-apps; deploy a https://appsdeocta.web.app.
- Verificado en vivo: 4 cards agrupadas, categorías, tabs, modal historial, 0 errores
  de consola. Screenshot `preview-live-v2.png`.
- Seguridad (turno previo): CSP meta, `safeUrl`/`safeImg`, headers (nosniff, DENY,
  Referrer-Policy, Permissions-Policy, HSTS), fix XSS reflejado en toast vía `?repos=`,
  repo limpio de secretos, prueba de ataque con payload inerte. Commit `de2644c`.
- Resta: secrets del workflow para deploy automático.
