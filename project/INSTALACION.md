# Guía de Instalación - QuímicaPro

## Paso 1: Requisitos del Sistema

Antes de comenzar, asegúrate de tener:
- ✅ Python 3.7 o superior instalado
- ✅ Conexión a internet (solo para configuración inicial)
- ✅ Aproximadamente 100 MB de espacio en disco

### Verificar Python

Abre una terminal o símbolo del sistema y ejecuta:

```bash
python --version
```

o

```bash
python3 --version
```

Deberías ver algo como `Python 3.7.x` o superior.

## Paso 2: Descargar el Proyecto

Descarga y extrae el proyecto en una carpeta de tu computadora.

## Paso 3: Configurar Entorno Virtual (Recomendado)

### En Windows:

```bash
cd ruta\a\quimica-pro
python -m venv venv
venv\Scripts\activate
```

### En Linux/Mac:

```bash
cd ruta/a/quimica-pro
python3 -m venv venv
source venv/bin/activate
```

Verás `(venv)` al inicio de tu línea de comando cuando el entorno esté activado.

## Paso 4: Instalar Dependencias

Con el entorno virtual activado, ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:
- PyQt5 (interfaz gráfica)
- supabase (base de datos)
- python-dotenv (configuración)

## Paso 5: Configurar Supabase

### 5.1 Crear cuenta en Supabase

1. Ve a [https://supabase.com](https://supabase.com)
2. Haz clic en **"Start your project"**
3. Crea una cuenta con tu email
4. Verifica tu correo electrónico

### 5.2 Crear un nuevo proyecto

1. Una vez dentro, haz clic en **"New project"**
2. Elige una organización o crea una nueva
3. Completa los datos:
   - **Name:** QuimicaPro (o el nombre que prefieras)
   - **Database Password:** Crea una contraseña segura (guárdala)
   - **Region:** Elige el más cercano a tu ubicación
   - **Pricing Plan:** Free (Plan gratuito)
4. Haz clic en **"Create new project"**
5. Espera 1-2 minutos mientras se crea el proyecto

### 5.3 Obtener credenciales

1. En el panel de tu proyecto, ve al menú lateral izquierdo
2. Haz clic en **⚙️ Settings** (Configuración)
3. Selecciona **API** en el submenú
4. Verás dos valores importantes:

   - **Project URL:** Algo como `https://xxxxx.supabase.co`
   - **anon public:** Una clave larga que empieza con `eyJ...`

5. Copia estos dos valores

### 5.4 Crear archivo .env

1. En la carpeta raíz del proyecto, crea un archivo llamado `.env`
2. Abre el archivo con un editor de texto
3. Pega lo siguiente, reemplazando con tus valores:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

4. Guarda el archivo

### 5.5 Inicializar la base de datos

**IMPORTANTE:** La base de datos se inicializó automáticamente durante la configuración. Ya contiene:
- Todas las tablas necesarias
- Los 4 módulos de química
- 13 lecciones con contenido
- Preguntas de cuestionario
- Sistema de logros

No necesitas hacer nada más.

## Paso 6: Ejecutar la Aplicación

Con todo configurado, ejecuta:

```bash
python main.py
```

## Paso 7: Primera Ejecución

1. Verás la pantalla de inicio de sesión
2. Haz clic en **"¿No tienes cuenta? Regístrate"**
3. Ingresa:
   - **Nombre de usuario:** Un nombre único (ej: "juan_perez")
   - **Nombre para mostrar:** Tu nombre real (ej: "Juan Pérez")
4. Haz clic en **"Registrarse"**
5. ¡Listo! Ya estás dentro de QuímicaPro

## Verificación de Instalación

Si todo está correcto, deberías ver:
- ✅ La ventana principal de QuímicaPro
- ✅ Un menú lateral con: Inicio, Módulos, Mi Progreso, Logros
- ✅ 4 módulos de química disponibles
- ✅ Tu nombre de usuario en la parte superior del menú

## Problemas Comunes

### Error: "No module named 'PyQt5'"

**Solución:** Instala PyQt5 manualmente

```bash
pip install PyQt5
```

### Error: "No module named 'supabase'"

**Solución:** Instala supabase manualmente

```bash
pip install supabase
```

### Error: "SUPABASE_URL not found"

**Solución:**
- Verifica que el archivo `.env` esté en la carpeta raíz del proyecto
- Asegúrate de que las variables estén correctamente escritas (sin espacios)

### Error de conexión a Supabase

**Solución:**
- Verifica tu conexión a internet
- Comprueba que las credenciales en `.env` sean correctas
- Asegúrate de que tu proyecto de Supabase esté activo

### En Linux: Error al instalar PyQt5

**Solución:** Instala las dependencias del sistema

```bash
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine
```

## Desactivar Entorno Virtual

Cuando termines de usar la aplicación, puedes desactivar el entorno virtual:

```bash
deactivate
```

## Próximos Pasos

Una vez instalado correctamente:

1. **Explora los módulos** de química
2. **Completa lecciones** para aprender
3. **Realiza cuestionarios** para evaluar tu conocimiento
4. **Desbloquea logros** según tu progreso

## Ayuda Adicional

Si sigues teniendo problemas:

1. Revisa que Python esté correctamente instalado
2. Verifica que todas las dependencias estén instaladas
3. Comprueba los logs de error en la consola
4. Asegúrate de que Supabase esté configurado correctamente

---

**¡Feliz aprendizaje! 🧪**
