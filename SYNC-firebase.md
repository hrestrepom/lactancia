# Sincronización entre teléfonos — configuración de Firebase

Objetivo: que el iPhone de mamá y el de papá compartan el mismo historial en
tiempo real. Cada uno inicia sesión con su cuenta de Google y solo ustedes dos
ven los datos del bebé.

El trabajo se divide en dos: lo que haces tú **una sola vez** (crear el proyecto,
Paso 1) y lo que programo yo (toda la integración en la app, Paso 2). Cuando
termines el Paso 1, me pasas la configuración y yo continúo.

---

## Paso 1 — Crear el proyecto de Firebase (lo haces tú, ~10 min)

### 1.1 Crear el proyecto
1. Entra a <https://console.firebase.google.com> con tu cuenta de Google.
2. **Agregar proyecto** → nombre: `lactancia` (o el que quieras) → Continuar.
3. Puedes **desactivar Google Analytics** (no hace falta) → Crear proyecto.

### 1.2 Registrar la app web
1. En la pantalla del proyecto, toca el ícono **`</>`** (Web).
2. Apodo de la app: `lactancia-web`. **No** marques "Firebase Hosting".
3. Registrar app. Firebase te muestra un bloque de código con un objeto
   `firebaseConfig = { apiKey: "...", authDomain: "...", ... }`.
   **Ese objeto completo es lo que me tienes que pasar.** (Es público, no es secreto.)

### 1.3 Activar el inicio de sesión con Google
1. Menú izquierdo → **Compilación (Build) → Authentication** → Comenzar.
2. Pestaña **Sign-in method** → **Google** → Habilitar.
3. Elige tu correo como "correo de asistencia del proyecto" → Guardar.

### 1.4 Crear la base de datos
1. Menú izquierdo → **Compilación (Build) → Firestore Database** → Crear base de datos.
2. Modo: **Producción** (yo te doy las reglas de seguridad en el Paso 2).
3. Ubicación: la que te sugiera (ej. `nam5` / us-central) → Habilitar.

### 1.5 Autorizar el dominio de la app
1. En **Authentication → Settings → Authorized domains** (Dominios autorizados).
2. Agrega: `hrestrepom.github.io`
   (Si más adelante usas otro dominio, se agrega aquí también.)

### 1.6 Pasarme la configuración
Cópiame el objeto `firebaseConfig` del punto 1.2. Se ve así:

```js
const firebaseConfig = {
  apiKey: "AIza............",
  authDomain: "lactancia-xxxx.firebaseapp.com",
  projectId: "lactancia-xxxx",
  storageBucket: "lactancia-xxxx.appspot.com",
  messagingSenderId: "0000000000",
  appId: "1:0000000000:web:abcdef......"
};
```

---

## Paso 1-bis — Pegar las reglas de seguridad (lo haces tú)

Las reglas definen que solo los miembros de la familia (los dos teléfonos que
inician sesión) puedan ver el historial. El texto está en el archivo
`firestore.rules` de este proyecto.

1. En la consola de Firebase → **Firestore Database** → pestaña **Reglas (Rules)**.
2. Borra lo que haya y **pega el contenido completo de `firestore.rules`**.
3. **Publicar (Publish)**.

---

## Paso 2 — Integración en la app (¡ya está hecha!)

Ya está programado en la app (`index.html` + `firebase-config.js`):

- **Inicio de sesión con Google** (botón "Entrar con Google" en Ajustes).
- **Familia compartida:** el primero toca *Crear familia nueva* y obtiene un
  *código*; el segundo lo escribe en *Unirme con código* una sola vez. A partir de
  ahí ambos comparten historial y datos del bebé.
- **Sincronización en tiempo real:** lo que registra uno aparece en el otro en
  segundos. Como cada registro tiene identificador único, se combinan sin duplicar.
- **Sigue funcionando sin señal:** lo que registres sin internet se guarda local
  y se sincroniza al reconectar.
- Los temporizadores en curso siguen siendo de cada teléfono; se comparten los
  registros terminados y el perfil del bebé.

### Cómo lo usan (una vez publicado y con Firebase configurado)

1. Los dos abren la app (en `hrestrepom.github.io/lactancia/`) y tocan
   **Ajustes → Entrar con Google**, cada uno con su cuenta.
2. **Tú** (o tu esposa) toca **Crear familia nueva**. Aparece un **código** de 6
   caracteres.
3. **El otro teléfono** escribe ese código en **Unirme con código**.
4. Listo: desde ese momento el historial es el mismo en ambos y se actualiza solo.

---

## Notas

- El plan gratuito de Firebase (Spark) cubre de sobra el uso de una familia.
- Los datos quedan en **tu** proyecto de Firebase, bajo tu cuenta.
- Esto NO reemplaza los respaldos: sigue siendo buena idea exportar de vez en
  cuando desde Ajustes.
