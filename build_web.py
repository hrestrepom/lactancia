# -*- coding: utf-8 -*-
"""Genera la version instalable (PWA) a partir de index.html.

index.html esta escrito como artifact (sin <html>/<head>/<body>); aqui se envuelve
en un documento completo con manifest, iconos y service worker para poder alojarlo
en GitHub Pages, Netlify o cualquier servidor estatico.

Uso:  python build_web.py
"""
import os
import re
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
# GitHub Pages solo publica desde la raiz o desde /docs
OUT_DIR = "docs"
WEB = os.path.join(BASE, OUT_DIR)

HEAD_EXTRA = """  <meta charset="utf-8">
  <meta name="theme-color" content="#B25E6E" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#221C1E" media="(prefers-color-scheme: dark)">
  <meta name="description" content="Registro de lactancia: tomas por seno, extracciones, temporizador de gases y estadisticas.">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="apple-touch-icon" href="icon-180.png">
  <link rel="icon" type="image/png" href="icon-192.png">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="Lactancia">
  <!-- Firebase (sincronizacion entre telefonos). Solo en la version alojada. -->
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-auth-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js"></script>
  <script src="firebase-config.js"></script>
"""

SW_REGISTER = """
<script>
  // Service worker: permite abrir la app sin conexion y ayuda a que iOS
  // trate el almacenamiento como permanente.
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('sw.js').catch(function () {});
    });
  }
</script>
"""


def build():
    src = os.path.join(BASE, "index.html")
    with open(src, encoding="utf-8") as fh:
        content = fh.read()

    # separar la cabecera (title/meta/style) del cuerpo (markup + script)
    m = re.search(r"</style>", content)
    if not m:
        raise SystemExit("No se encontro </style> en index.html")
    head, body = content[: m.end()], content[m.end():]

    doc = (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n"
        + HEAD_EXTRA
        + head.strip()
        + "\n</head>\n<body>\n"
        + body.strip()
        + "\n"
        + SW_REGISTER
        + "</body>\n</html>\n"
    )

    os.makedirs(WEB, exist_ok=True)
    with open(os.path.join(WEB, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)

    for extra in ("icon-180.png", "icon-192.png", "icon-512.png", "firebase-config.js"):
        srcp = os.path.join(BASE, extra)
        if os.path.exists(srcp):
            shutil.copy2(srcp, os.path.join(WEB, extra))

    print("Generado:", os.path.join(WEB, "index.html"))
    print("Tamano:", os.path.getsize(os.path.join(WEB, "index.html")), "bytes")


if __name__ == "__main__":
    build()
