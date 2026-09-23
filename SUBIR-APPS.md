# Cómo subir apps/archivos a Apps de Octa (para agentes IA)

La tienda https://appsdeocta.web.app se alimenta sola de **GitHub Releases**.
Publicar = crear un release con el archivo adjunto. Sin tocar código.

## Destino
- App/archivo **sin repo propio** → releases de `Owning01/mis-apps`.
- App **con repo propio** → release en SU repo. Si no está en `config.json` (`repos[]`),
  agregarlo (+ patrón en `categories`, si no cae en "Otras"), commit+push y
  `firebase deploy --only hosting`.

## Cuenta de GitHub (hay 2)
1. `gh auth status` → ver usuario activo.
2. `gh repo view <DUEÑO/REPO> --json name` → si falla, es la cuenta equivocada:
   `gh auth switch --hostname github.com --user <OTRO_USUARIO>` (o `gh auth login`).
3. Sin acceso al repo: FRENAR y avisar al usuario.

## Comandos
- Permanente: `gh release create <app>-vX.Y.Z <archivo> --repo <DUEÑO/REPO> --title "<App> vX.Y.Z" --notes "<qué es>"`
  (ej: `gh release create vistamd-v1.0.0 vistamd.exe --repo Owning01/mis-apps --title "VistaMD v1.0.0" --notes "App de escritorio (Windows)"`).
  Tag único; versión nueva = tag nuevo.
- Temporal: `gh release create temp-<slug>-AAAAMMDD <archivo> --repo Owning01/mis-apps --prerelease --title "[TEMP] <nombre>" --notes "Se borra a los 7 días"`.
- Limpieza (+7 días): `gh release list -R Owning01/mis-apps`; borrar cada `temp-*` viejo con
  `gh release delete <tag> -y -R Owning01/mis-apps` + `gh api -X DELETE repos/Owning01/mis-apps/git/refs/tags/<tag>`.

## Reglas
- El archivo debe quedar **ADJUNTO**: drafts o releases sin archivos NO se muestran.
- Verificar: `gh release view <tag> -R <DUEÑO/REPO> --json tagName,assets` (assets>0).
- Límite 2 GB por archivo. La descarga es directa, sin logins.
- Responder al usuario solo con el link directo
  (`https://github.com/<DUEÑO>/<REPO>/releases/download/<tag>/<archivo>`) + la página.
