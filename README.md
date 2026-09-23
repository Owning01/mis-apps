# MisApps — tienda personal de aplicaciones

Código en **un solo repo de GitHub** · página servida por **Firebase Hosting** ·
archivos descargables en **GitHub Releases** (descarga directa, sin login).

## Arquitectura

```
┌──────────────┐   push a main    ┌──────────────────┐
│  GitHub repo │ ───────────────▶ │ Firebase Hosting │ ◀── visitantes (página)
│  (este código)│  (deploy auto   │  tu-sitio.web.app │
└──────┬───────┘   vía Action)    └──────────────────┘
       │ Releases con .exe/.zip/.apk
       ▼
┌──────────────┐   click Descargar (directo, sin login)
│ gh release   │ ────────────────────────────────────▶ visitantes (archivos)
└──────────────┘
```

La página **no tiene backend**: al abrirse lee los Releases del repo vía API pública
de GitHub y arma el catálogo sola. Publicar una app = crear un Release con el archivo
adjunto. Sin tocar código, sin redeploy.

## Puesta en marcha local

```powershell
cd G:\proyectos\mi-tienda-apps
python -m http.server 8010
# abrir http://localhost:8010
# (el puerto 8000 está ocupado en esta máquina por otro servidor)
```

Vista previa con cualquier repo público (útil para probar sin configurar nada):

```
http://localhost:8010/?owner=cli&repo=cli
```

## Conectar tu repo (2 lugares)

1. **`config.json`** → `owner`, `repo`, `siteName`. Es lo que ven todos los visitantes
   (producción). Cambiar + deploy.
2. **⚙️ Ajustes en la página** → vista previa solo en tu navegador (no afecta a otros).

## Cómo publicar una app

1. En GitHub: repo → **Releases → Draft a new release**.
2. Tag (ej `v1.0.0`), título, descripción y **adjuntar el archivo** (.exe, .zip, .apk…).
3. Publicar. La página lo muestra en segundos con botón **Descargar** directo:
   `https://github.com/<owner>/<repo>/releases/download/<tag>/<archivo>`

Alternativa por terminal: `gh release create v1.0.0 app.zip --title "Mi App 1.0" --notes "..."`

## Deploy a Firebase Hosting

Requisitos: proyecto en [console.firebase.google.com](https://console.firebase.google.com)
(crear uno es gratis) y estar logueado:

```powershell
cd G:\proyectos\mi-tienda-apps
firebase login
firebase use --add        # elegir tu proyecto (reescribe .firebaserc)
firebase deploy --only hosting
```

Deploy automático en cada push a `main` (opcional, recomendado):
1. Repo → Settings → Secrets → agregar `FIREBASE_SERVICE_ACCOUNT`
   (contenido: `firebase init hosting:github` te da el JSON, o generarlo en
   IAM de Google Cloud con rol *Firebase Hosting Admin*).
2. Repo → Settings → Variables → agregar `FIREBASE_PROJECT_ID`.
3. Listo: el workflow `.github/workflows/firebase-hosting.yml` despliega solo.

## Notas y límites

- API de GitHub sin autenticar: **60 consultas/hora por IP** (alcanza para un catálogo;
  si se agota, la página muestra error y usa el caché). Con token en ⚙️ Ajustes: 5000/h.
- Releases tipo **draft** o sin archivos adjuntos no aparecen.
- El badge "NUEVA" = publicado en los últimos 14 días; "BETA" = prerelease.
- Los links `releases/download/...` descargan directo, **sin cuenta Google ni GitHub**.
