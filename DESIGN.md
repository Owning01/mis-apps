# DESIGN.md - Apps de Octa

Direccion de estilo de la tienda. La pagina la aplica; `antislop.md` filtra encima.

## Identidad
Tienda personal de Octa: utilitaria, directa, sin cuentas. Tono de vecino que comparte archivos, no de startup.

## Dial
ENERGY 1 / RHYTHM 2 / MOTION 1

## Design Read
Catalogo utilitario para el dueño y su familia, en lenguaje oscuro verdoso con acento naranja de descarga, dial ENERGY 1 / RHYTHM 2 / MOTION 1.

## Paleta
- Core: verde accion #34D399 sobre tinta #06281C, fondos verdes oscuros #0B1411 / #101D17 / #132019.
- Acento unico: naranja descarga #F97316 sobre tinta #2A1503, tambien marca TEMPORAL.
- Neutros: texto #EFF6F0, apagado #A3B8AB, linea #233D31, chip #C7D4CB.
- Avatares: 3 pares dentro del sistema (menta, ambar, naranja). Sin cian, lima ni lavanda.

## Tipografia
- Titulos: Space Grotesk, geometrica que acompana al logo del pulpo.
- Cuerpo y UI: Inter, legible en listas densas y nombres de archivo.

## Motivo
Avatar-letra determinista + chips de estado (categoria, version, repo, TEMPORAL, BETA, NUEVA). El naranja aparece solo en el momento de descargar.

## Fondo
Imagen abisal generada con Qwen (`bg-abisal.jpg`, 1920x1080, 28KB): abismo verde casi
negro con tentaculos sutiles en las esquinas y particulas bioluminiscentes. El centro
queda limpio para la UI. Va bajo un overlay en gradiente (0.62 a 0.88) para que el
texto mantenga AA; el halo verde al 9% se suma encima. Motivo de marca: el pulpo.

## Botones
Escritorio compacto (36px acciones, 38px tabs, 34px chips); 44px solo en mobile
(<=640px) donde el target es el dedo.

## Decisiones (una linea cada una)
- Color: verde para accion y marca, naranja reservado a descargar y temporal.
- Layout: header fijo con buscador y tabs; grillas para apps, listado para paginas (enlaces externos, no descargas).
- Tipo: display geometrica en titulos, sans neutra en cuerpo.
- Espaciado: cards 20px con gap 16px; ritmo 2 con ruptura solo en paginas.
- Cards: uniformes porque el catalogo pesa igual; la jerarquia va en chips y version.
- Iconos: trazo 2px legible a 16px, cada glifo mapea su seccion.
- Blur: maximo 2 superficies (header y modal) para separar fijo de contenido.
- Movimiento: solo hover y apertura de modal; respeta `prefers-reduced-motion`.
- Tema: oscuro fijo por marca (verde sobre negro verdoso), sin toggle que nadie pidio.
- Halo: radial verde al 9% sobre el header como foco de marca, sin cubrir la pagina.
