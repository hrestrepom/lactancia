# Lactancia · Mi bebé

App web para registrar la lactancia: tomas por seno con temporizador, extracciones en
onzas, temporizador de gases de 30 minutos con alarma, historial y estadísticas según
la edad del bebé.

## Por qué hay que alojarla

Los datos se guardan **en el propio teléfono** (localStorage + IndexedDB). Para que iOS
los conserve de forma permanente, la app tiene que cumplir dos condiciones:

1. Estar servida desde **un dominio propio** (`https://…`), no dentro del visor de otra
   aplicación ni como archivo local.
2. Estar **instalada en la pantalla de inicio** (Compartir → Agregar a pantalla de inicio).

Cumplidas ambas, Safari le concede almacenamiento persistente y el historial sobrevive
a cerrar la app y reiniciar el teléfono. En Ajustes, la app muestra un indicador verde
cuando el almacenamiento permanente está activo.

## Estructura

| Archivo | Para qué sirve |
| --- | --- |
| `index.html` | Código fuente único de la app. Editar solo aquí. |
| `build_web.py` | Genera `docs/` a partir de `index.html`. |
| `docs/` | **Carpeta que publica GitHub Pages.** Generada, no editar a mano. |
| `docs/manifest.webmanifest` | Nombre, ícono y colores de la app instalada. |
| `docs/sw.js` | Permite abrirla sin conexión. |
| `icon-*.png` | Íconos de la app. |

Tras editar `index.html`, regenerar la versión publicada:

```
python build_web.py
```

La carpeta se llama `docs` porque GitHub Pages solo publica desde la raíz del
repositorio o desde `/docs`; no acepta otros nombres.

## Publicar en GitHub Pages

1. Crear un repositorio vacío en <https://github.com/new> llamado `lactancia`
   (sin README ni .gitignore, para que quede limpio).
2. Desde esta carpeta:

```bash
git push -u origin main
```

3. En GitHub: **Settings → Pages → Source: Deploy from a branch**,
   rama `main`, carpeta **`/docs`** → Save.
4. Esperar un par de minutos. La app queda en
   <https://hrestrepom.github.io/lactancia/>.
5. Abrir esa dirección **en Safari** en el iPhone → Compartir →
   **Agregar a pantalla de inicio**.
6. Abrir la app desde el ícono nuevo y confirmar en Ajustes el indicador verde
   de almacenamiento permanente.

Para publicar cambios posteriores:

```bash
python build_web.py
git add -A
git commit -m "Descripción del cambio"
git push
```

## Probar en el computador

```
python -m http.server 8777 --directory docs
```

y abrir <http://localhost:8777>.

## Respaldos

En **Ajustes → Datos** están *Exportar respaldo* (descarga un `.json`) e *Importar*.
Conviene exportar de vez en cuando: es la única copia fuera del teléfono.
