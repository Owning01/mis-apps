# MisApps — tienda personal de aplicaciones y archivos

Código en **`Owning01/mis-apps`** · página servida por **Firebase Hosting** ·
archivos en **GitHub Releases** (descarga directa, sin login).

## Arquitectura

```
Repos fuente (la página lee los Releases de todos):
├── Owning01/mis-apps   ← código de ESTA página + releases de apps sin repo propio
└── Owning01/Openher    ← releases de OpenHer (solo lectura, no se toca)

Publicar = crear un Release con el archivo adjunto → aparece solo en la página.
Tags temp-* → sección 📁 Temporales (se borran a los 7 días).
```

La página **no tiene backend**: al abrirse lee los Releases vía API pública
de GitHub y arma el catálogo sola. Sin tocar código, sin redeploy.

## Puesta en marcha local

```powershell
cd G:\proyectos\mi-tienda-apps
python -m http.server 8010
# abrir http://localhost:8010
# (el puerto 8000 está ocupado en esta máquina por otro servidor)
```

Vista previa con otros repos (útil para probar sin configurar nada):

```
http://localhost:8010/?repos=cli/cli,octocat/Hello-World
```

## La página (qué ve el visitante)

- **Tabs**: Aplicaciones (permanentes) y Temporales (`temp-*`, se borran a los 7 días).
- **Agrupada por app**: cada card muestra la ÚLTIMA versión; el botón **Historial**
  abre el modal con todas las versiones anteriores, cada una descargable.
- **Categorías**: chips de filtro configurados en `config.json` → `categories`
  (primera coincidencia gana; el orden importa). Se matchea contra repo-corto/tag,
  nombre y archivos. Lo que no matchea va a "Otras".
- **Sin panel de dueño**: no hay login ni botones de admin en la página.
  Todo se configura en `config.json` + Releases de GitHub.

## Cómo publicar

**No hacerlo a mano**: pedirle a cualquier IA *"subime X a la página"* — el skill
`subir-a-misapps` (`~/.agents/skills/`) le enseña el procedimiento:
- App permanente sin repo → release en `Owning01/mis-apps`, tag `<app>-vX.Y.Z`.
- App con repo propio → release en su repo (agregarlo a `config.json` si es nuevo).
- Temporal → release `temp-<slug>-AAAAMMDD` con `--prerelease` (sale en Temporales).
- Limpieza: borrar `temp-*` de +7 días (release + tag).

Manual (si hace falta): `gh release create v1.0.0 app.zip --repo DUEÑO/REPO --title "..." --notes "..."`

## Deploy a Firebase Hosting

Requisitos: proyecto en [console.firebase.google.com](https://console.firebase.google.com)
y estar logueado. **Falta el ID del proyecto** (bloquea el deploy).

```powershell
cd G:\proyectos\mi-tienda-apps
firebase login
firebase use --add        # elegir tu proyecto (reescribe .firebaserc)
firebase deploy --only hosting
```

Deploy automático en cada push a `main` (opcional, recomendado):
1. Repo → Settings → Secrets → `FIREBASE_SERVICE_ACCOUNT` (rol *Firebase Hosting Admin*).
2. Repo → Settings → Variables → `FIREBASE_PROJECT_ID`.
3. El workflow `.github/workflows/firebase-hosting.yml` despliega solo.

## Notas y límites

- API de GitHub sin autenticar: **60 consultas/hora por IP** (la página usa `no-store`;
  si se agota, muestra error y usa el caché).
- Releases **draft** o sin archivos adjuntos no aparecen.
- "NUEVA" = publicado en los últimos 14 días; "BETA" = prerelease no-temporal.
- Los links `releases/download/...` descargan directo, **sin cuenta**.
- Máximo 2 GB por archivo en Releases.
