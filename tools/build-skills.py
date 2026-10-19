#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye skills.json + skills/<id>.zip para Apps de Octa.

Lee las skills reales del disco, arma un zip por skill y un skills.json con la
explicacion y el diagrama de uso de cada una. Los textos de cada skill viven en
la tabla SKILLS de este archivo.

Uso:  python tools/build-skills.py
"""
import json
import os
import zipfile
from datetime import date

HOME = os.path.expanduser("~")
ROOTS = [
    (os.path.join(HOME, ".agents", "skills"), ".agents/skills"),
    (os.path.join(HOME, ".config", "opencode", "skills"), ".config/opencode/skills"),
]
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIPDIR = os.path.join(SITE, "skills")
JSONP = os.path.join(SITE, "skills.json")

EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".taste-skill", "dist"}
EXCLUDE_FILES = {".DS_Store"}

# id, root (0=.agents, 1=.config), subruta, categoria, summary, when, does, out
SKILLS = [
    # ---------- Diseno y UI ----------
    ("design-taste-frontend", 0, "design-taste-frontend", "Diseño y UI",
     "Dirección de arte anti-slop para páginas web, destilada de 247 sitios de galería (tasteskill v2): idea, composición, tipografía, paleta y fotos.",
     "Diseñás, rediseñás o pulís una landing, portafolio o página pública.",
     "Resuelve la dirección y corre un look-and-fix sobre capturas reales del navegador.",
     "Página lista con dirección propia y gate superado."),
    ("antislop", 0, "antislop", "Diseño y UI",
     "Filtro anti-slop para agentes que escriben interfaces: reglas R-01 a R-38, patrones prohibidos, diales de vivacidad y gate de entrega.",
     "Construís o revisás UI y querés evitar el look genérico de IA.",
     "Aplica el playbook del tipo de superficie y bloquea los patrones de slop.",
     "Interfaz sin slop y gate de entrega superado."),
    ("apple-design", 0, "apple-design", "Diseño y UI",
     "El enfoque de Apple para interfaces, traducido a la web: resortes, gestos, inercia, materiales translúcidos, tipografía y sobriedad.",
     "Construís UI con gestos, arrastre, hojas o transiciones interrumpibles.",
     "Guía feedback, consistencia espacial y movimiento físico.",
     "Interacciones con fundamento Apple."),
    ("diagram-design", 0, "diagram-design", "Diseño y UI",
     "Crea diagramas de arquitectura, flujos, secuencia, ER, timeline, kanban, UML y más como HTML/SVG/PNG con la marca puesta.",
     "Necesitás un diagrama presentable o redibujar un drawio/Mermaid.",
     "Compone el diagrama con patrones semánticos y estilo de marca.",
     "Diagrama standalone listo para publicar."),
    ("apuntes", 0, "apuntes", "Diseño y UI",
     "Crea apuntes bonitos en HTML: carpeta con portada, divisorias, índice y hojas con títulos a mano, cajas de definición y doodles SVG.",
     "Pedís 'armar unos apuntes' o pasar notas a un cuaderno visual.",
     "Genera la carpeta con 18 estilos de título y 10 bloques de apunte.",
     "Carpeta de apuntes HTML lista para abrir."),
    ("prototype", 0, "prototype", "Diseño y UI",
     "Construye varias versiones realmente diferentes de un elemento de UI, detrás de un selector visual para recorrerlas en vivo y promover la que se siente bien.",
     "No sabés qué variante conviene y querés compararlas juntas.",
     "Renderiza las variantes y promueve la elegida.",
     "La variante ganadora puesta en el código."),
    ("editar-pagina", 0, "editar-pagina", "Diseño y UI",
     "Cambia cómo se ve o se comporta una página abierta en el navegador: ocultar, mover, borrar o agregar elementos sobre el DOM vivo.",
     "Mirás una pestaña y decís 'sacá este banner' o 'arreglá este estilo'.",
     "Edita el HTML/CSS del DOM en vivo que entrega Chrome.",
     "Página cambiada al instante, sin tocar archivos del disco."),
    # ---------- Animacion ----------
    ("animate", 0, "animate", "Animación",
     "Construye una animación web desde cero, decidiendo en orden: si debe animarse, con qué propósito, qué herramienta, qué propiedades, qué curva y duración, y cómo se interrumpe.",
     "Te piden animar algo o hacer que un componente se sienta vivo.",
     "Recorre las decisiones del movimiento y escribe la implementación.",
     "Código de animación listo para usar."),
    ("animate-expo", 0, "animate/animate-expo", "Animación",
     "Como animate, pero para React Native y Expo: hilo de ejecución, resortes o timing, gestos que entregan el control, degradación y háptics.",
     "Animás una app Expo: gestos, hojas, transiciones o feedback.",
     "Elige dónde corre cada animación y usa Reanimated + Gesture Handler.",
     "Animación fluida en el dispositivo."),
    ("animation-vocabulary", 0, "animate/animation-vocabulary", "Animación",
     "Glosario inverso: convierte una descripción vaga ('la cosa que rebota al abrir un popover') en el término exacto (Pop in, Rubber-banding).",
     "No sabés cómo se llama un efecto de movimiento.",
     "Busca el nombre correcto por descripción o por ejemplo.",
     "El término exacto para pedirlo a una IA o a un diseñador."),
    ("find-animation-opportunities", 0, "animate/find-animation-opportunities", "Animación",
     "Busca en una codebase o UI los lugares que no se animan pero deberían, y rechaza todo lo que no debería animarse. Solo lectura.",
     "Preguntás '¿qué se podría animar acá?'.",
     "Detecta oportunidades y propone movimiento con valores exactos.",
     "Lista priorizada de oportunidades (no implementa)."),
    ("improve-animations", 0, "improve-animations", "Animación",
     "Audita el motion de un codebase con ojo de asesor senior y produce una auditoría priorizada con planes autocontenidos para otros agentes.",
     "Querés 'mejorar las animaciones' de una base entera.",
     "Revisa en solo-lectura y planifica mejoras por tarea.",
     "Auditoría de motion + planes de implementación."),
    ("remotion-best-practices", 0, "remotion-best-practices", "Animación",
     "Punto de entrada a las skills de Remotion (video con React): enruta cada caso a su referencia (crear video, markup, mapas, multimedia).",
     "Vas a construir o editar video con Remotion.",
     "Enruta al workflow correcto y aplica las prácticas de Remotion.",
     "Composición de video encaminada."),
    # ---------- Codigo y calidad ----------
    ("code-review", 0, "code-review", "Código y calidad",
     "Motor de auditoría: bugs ocultos, flujos reales de usuario, desincronización full-stack, resiliencia (Chaos Monkey) y zero data loss, con auto-fix supervisado.",
     "Querés auditar un código o cazar bugs antes de publicar.",
     "Corre más de 50 reglas por stack y scripts deterministas.",
     "Scorecard (JSON/markdown/SARIF) y tests de regresión."),
    ("optimize-code", 0, "optimize-code", "Código y calidad",
     "Optimización para cualquier lenguaje: algoritmos, estructuras de datos, I/O, memoria, concurrencia, bases y redes.",
     "Pedís 'hacelo más rápido' o 'optimizá esto'.",
     "Audita y arregla cuellos de botella; sin archivo puntual revisa todo el repo.",
     "Código más rápido con cambios justificados."),
    ("test-audit", 0, "test-audit", "Código y calidad",
     "Gate para escribir tests y auditar los existentes: detecta los de bajo valor, acoplados a implementación o duplicados.",
     "Escribís, cambiás o revisás tests.",
     "Aplica el protocolo de autoría y el workflow de auditoría.",
     "Suite sólida, sin tests de relleno."),
    ("reverse-engineer-anything", 0, "reverse-engineer-anything", "Código y calidad",
     "Ingeniería inversa de binarios nativos, Electron/JS, firmware y navegador con evidencia del artefacto real (REA).",
     "Querés entender un artefacto sin código fuente.",
     "Decompila y reconstruye desde el runtime o artefacto entregado.",
     "Explicación o reconstrucción con evidencia."),
    ("flutter-pro", 0, "flutter-pro", "Código y calidad",
     "Orquestadora Flutter: arquitectura por capas (MVVM, Riverpod, BLoC), 60/120fps y networking robusto.",
     "Estructurás un proyecto Flutter o diagnosticás errores de layout.",
     "Cubre Dart 3, GoRouter, Dio, constraints y formularios accesibles.",
     "App Flutter ordenada y optimizada."),
    ("firebase-optimization", 0, "firebase-optimization", "Código y calidad",
     "Optimización extrema de Firebase: cuota gratuita, cache-first, agregaciones nativas y reglas de costo cero.",
     "Tu app usa Firebase y querés bajar lecturas y escrituras.",
     "Aplica arquitectura cache-first y testea con el Emulator Suite.",
     "Consumo mínimo y costos controlados."),
    # ---------- Investigacion ----------
    ("boost", 0, "boost", "Investigación",
     "Modo de razonamiento profundo: debate adversarial multi-agente, exploración dialéctica de hipótesis y verificación empírica rigurosa.",
     "El problema es difícil y querés agotar hipótesis antes de decidir.",
     "Corre debate y verificación con perspectivas opuestas.",
     "Decisión con evidencia y objeciones resueltas."),
    ("debate", 0, "debate", "Investigación",
     "Debate deliberativo entre especialistas con roles opuestos y síntesis arbitral central, sin invalidar el caché de contexto.",
     "Tenés que evaluar alternativas, arquitecturas o trade-offs.",
     "Abre roles (arquitecto, pragmático, adversario) y arbitra.",
     "Decisión razonada con posturas enfrentadas."),
    ("deep-investigator", 0, "deep-investigator", "Investigación",
     "Investigación técnica profunda: auditoría adversarial, benchmarking de repos, diagnóstico forense y arquitectura de soluciones.",
     "Querés investigar a fondo una tecnología o comparar tu código contra referencias.",
     "Diagnostica con evidencia empírica y código ejecutable verificado.",
     "Informe con hallazgos y arquitectura propuesta."),
    ("deep-research", 0, "deep-research", "Investigación",
     "Meta-investigación para una pregunta o decisión: búsqueda web, verificación de fuentes y reporte Q&A con citas.",
     "Necesitás research serio o validar una hipótesis.",
     "Busca, verifica fuentes y arma el reporte citado.",
     "Reporte Q&A con citas por archivo."),
    # ---------- Agentes y OpenCode ----------
    ("teamwork", 0, "teamwork", "Agentes y OpenCode",
     "Equipos de agentes: entrevista de alcance más swarm autónomo con verificación adversarial y ownership de archivos por worker.",
     "El trabajo es grande y conviene paralelizar con varios agentes.",
     "Orquesta sentinel, exploradores y workers con gates de verificación.",
     "Tarea grande terminada y auditada."),
    ("opencode-api", 0, "opencode-api", "Agentes y OpenCode",
     "Guía para consumir la API de OpenCode por HTTP: Go y Zen, endpoints por modelo, tool calling, streaming, precios y límites.",
     "Integrás o debugueás una app o agente contra OpenCode.",
     "Elige endpoint y arma el request/response con el header de sesión.",
     "Integración funcionando con el request correcto."),
    ("opencode-architecture", 0, "opencode-architecture", "Agentes y OpenCode",
     "Arquitectura interna de OpenCode: sesiones, runtime Effect-TS, contratos de plugins, hooks y tools.",
     "Vas a escribir un plugin o entender OpenCode por dentro.",
     "Explica ciclo de vida, context y extensiones sin romper el caché.",
     "Plugin o decisión de arquitectura fundada."),
    ("skill-creator", 0, "skill-creator", "Agentes y OpenCode",
     "Crea, mejora y mide skills: autoría desde cero, evals de rendimiento y optimización del trigger.",
     "Querés una skill nueva o que una existente dispare mejor.",
     "Escribe la skill, corre evals y ajusta la descripción.",
     "Skill medida y lista para usar."),
    ("mi-entorno", 0, "mi-entorno", "Agentes y OpenCode",
     "Perfil de desarrollo personal: convenciones para iniciar proyectos, herramientas, dependencias, documentación, commits y despliegue.",
     "Arranca un proyecto nuevo o hay que configurar el entorno.",
     "Fija tus convenciones de trabajo y despliegue.",
     "Setup alineado a tu forma de trabajar."),
    # ---------- Aprendizaje ----------
    ("estudio-profundo", 0, "estudio-profundo", "Aprendizaje",
     "Aprendizaje profundo en español: entrevista de nivel, plan de lectura y 21 técnicas pedagógicas integradas.",
     "Querés aprender un tema a fondo o preparar un examen.",
     "Arma el plan con puentes a lo que ya sabés y activa recall, flashcards y quizzes.",
     "Plan de estudio personalizado con materiales."),
    ("html-plan", 0, "html-plan", "Aprendizaje",
     "Escribe un plan de implementación como página HTML interactiva: árbol de claims (por qué › qué › cómo › dónde) con las decisiones marcadas.",
     "Necesitás un plan o RFC antes de tocar varios archivos.",
     "Prueba cada claim con una exhibición: mockup, máquina de estados, esquema o código.",
     "Página HTML interactiva con el plan."),
    # ---------- Automatizacion ----------
    ("computer-use", 0, "computer-use", "Automatización",
     "Control nativo de Windows: 63 herramientas, clics semánticos, formularios atómicos y evasión anti-bot.",
     "Hay que operar una app de escritorio que no tiene API.",
     "Ejecuta con aceleración C# DesktopBridge, sin tokens visuales UIA.",
     "Tarea de escritorio hecha y verificada."),
    ("qwen-image", 0, "qwen-image", "Automatización",
     "Genera o edita imágenes por IA en local (Qwen-Image-2.1, RTX 3090): logos, fondos, keyframes y PNG con alfa.",
     "Pedís crear o editar una imagen o un keyframe.",
     "Corre el modelo local, sin servicios externos.",
     "Imagen generada o editada en disco."),
    ("x-scrape", 0, "x-scrape", "Automatización",
     "Lee y busca en Twitter/X automatizando Brave con Playwright, con la sesión real del perfil.",
     "Querés scrapear X, buscar opiniones o leer un timeline.",
     "Navega con tu sesión ya iniciada, sin credenciales extra.",
     "Posts, búsquedas o trends extraídos."),
    ("subir-a-misapps", 0, "subir-a-misapps", "Automatización",
     "Publica apps o archivos en la tienda Apps de Octa: releases en Owning01/mis-apps, temporales y limpieza.",
     "Pedís subir algo a la página o pasar un archivo al celu.",
     "Crea o borra releases y deja el archivo accesible por URL.",
     "Archivo publicado con link para compartir."),
    ("flow-images", 1, "flow-images", "Automatización",
     "Genera imágenes en Google Flow con tu cuenta, manejando tu Chrome real, sin API key.",
     "Querés crear imágenes con Flow o Nano Banana.",
     "Elige modelo y relación de aspecto y maneja la interfaz real.",
     "Imagen generada en Flow."),
    ("generador-fotos", 1, "generador-fotos", "Automatización",
     "Genera y edita imágenes con tu cuenta (Flow / Nano Banana y Gemini) sin API key, y las deja en disco.",
     "Pedís una imagen, un fondo o editar una foto.",
     "Maneja tu Chrome real con un solo comando o una llamada HTTP.",
     "Imágenes nuevas listas en disco."),
]


def iter_files(base):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if f in EXCLUDE_FILES or f.endswith(".pyc"):
                continue
            full = os.path.join(dirpath, f)
            yield full, os.path.relpath(full, base).replace("\\", "/")


def main():
    os.makedirs(ZIPDIR, exist_ok=True)
    out = []
    for sid, root_i, sub, cat, summary, when, does, outtxt in SKILLS:
        base_root = ROOTS[root_i][0]
        src = os.path.join(base_root, sub.replace("/", os.sep))
        if not os.path.isdir(src):
            print("FALTA:", src)
            continue
        files = list(iter_files(src))
        zpath = os.path.join(ZIPDIR, sid + ".zip")
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for full, rel in files:
                z.write(full, sid + "/" + rel)
        kb = max(1, round(os.path.getsize(zpath) / 1024))
        out.append({
            "id": sid,
            "name": sid,
            "cat": cat,
            "summary": summary,
            "when": when,
            "does": does,
            "out": outtxt,
            "files": len(files),
            "kb": kb,
            "src": ROOTS[root_i][1],
        })
        print(f"{sid:28} {len(files):4} archivos  {kb:6} KB")

    doc = {"generated": date.today().isoformat(), "count": len(out), "skills": out}
    with open(JSONP, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(f"\nOK: {len(out)} skills -> skills.json + {ZIPDIR}")


if __name__ == "__main__":
    main()
