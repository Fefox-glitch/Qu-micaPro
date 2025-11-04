# QuímicaPro - Aplicación Educativa de Química

![Python CI](https://github.com/Fefox-glitch/Qu-micaPro/actions/workflows/python-ci.yml/badge.svg)
![Integration](https://github.com/Fefox-glitch/Qu-micaPro/actions/workflows/integration.yml/badge.svg)

## CI y ejecución manual
- Unit tests: `/.github/workflows/python-ci.yml` se ejecuta en `push/PR`.
- Integración: `/.github/workflows/integration.yml` requiere secretos (`SUPABASE_URL`, `SUPABASE_KEY`, opcional `DATABASE_URL`).
- Disparo manual: en GitHub → Actions → Integration → Run workflow (elige rama, p.ej. `main`).

Una aplicación de escritorio educativa interactiva diseñada para estudiantes de enseñanza media (13-18 años) que enseña química desde conceptos básicos hasta temas avanzados.

## 🧪 Características

### Sistema Modular de Aprendizaje
- **Nivel 1: Conceptos Básicos** - Átomo, moléculas, estados de la materia, tabla periódica
- **Nivel 2: Enlaces y Compuestos** - Enlaces químicos, compuestos, formulación básica
- **Nivel 3: Reacciones Químicas** - Reacciones, balanceo, estequiometría
- **Nivel 4: Química Avanzada** - Termoquímica, soluciones, pH, química orgánica

### Funcionalidades
- ✅ Sistema de inicio de sesión local (sin conexión a internet después de configuración inicial)
- 📚 Lecciones interactivas con contenido educativo detallado
- 📝 Cuestionarios con retroalimentación automática
- 🏆 Sistema de logros y reconocimientos
- 📊 Seguimiento de progreso por módulo
- 🎨 Interfaz moderna con diseño temático de química
- ⭐ Puntuación y estadísticas personalizadas

## 🛠️ Tecnologías

- **Lenguaje:** Python 3.11 recomendado (3.7+ compatible)
- **Framework GUI:** PyQt5
- **Base de Datos:** Supabase (PostgreSQL)
- **Gestión de configuración:** python-dotenv
- **Pruebas y CI:** Pytest + GitHub Actions

## 📋 Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Supabase (gratuita)

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd quimica-pro
```

### 2. Crear entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r project/requirements.txt
```

### 4. Configurar Supabase

#### 4.1 Crear cuenta en Supabase
1. Ve a [https://supabase.com](https://supabase.com)
2. Crea una cuenta gratuita
3. Crea un nuevo proyecto

#### 4.2 Obtener credenciales
1. En tu proyecto de Supabase, ve a **Settings** → **API**
2. Copia tu **Project URL**
3. Copia tu **anon/public key**

#### 4.3 Configurar archivo .env
1. Crea un archivo `.env` en la carpeta `project/` (o copia `.env.example`)
2. Agrega tus credenciales:

```env
SUPABASE_URL=https://YOUR_REF.supabase.co
SUPABASE_KEY=YOUR_ANON_KEY

# (Opcional) Conexión directa a PostgreSQL para scripts
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_REF.supabase.co:5432/postgres?sslmode=require
```

#### 4.4 La base de datos ya está configurada
Las tablas y el contenido inicial ya fueron creados automáticamente mediante migración. No necesitas hacer nada más.

## ▶️ Ejecución

### Ejecutar la aplicación

```bash
python project/main.py
```

### Primera vez
1. La aplicación mostrará la pantalla de inicio de sesión
2. Haz clic en "¿No tienes cuenta? Regístrate"
3. Ingresa un nombre de usuario y nombre para mostrar
4. ¡Comienza a aprender química!

## 📱 Uso de la Aplicación

### Navegación Principal

#### 🏠 Inicio
- Resumen de tu progreso general
- Estadísticas de lecciones completadas
- Vista rápida de todos los módulos

#### 📚 Módulos
- Explora los 4 módulos de química
- Accede a lecciones individuales
- Realiza cuestionarios interactivos

#### 📊 Mi Progreso
- Visualiza tu avance por módulo
- Revisa estadísticas detalladas
- Seguimiento de lecciones completadas

#### 🏆 Logros
- Desbloquea logros completando lecciones
- Obtén reconocimientos por puntuaciones perfectas
- Colecciona insignias especiales

### Flujo de Aprendizaje

1. **Selecciona un módulo** desde la vista de Inicio o Módulos
2. **Elige una lección** del módulo
3. **Lee el contenido** educativo
4. **Completa el cuestionario** al final de la lección
5. **Revisa tus respuestas** y aprende de los errores
6. **Desbloquea logros** según tu desempeño

## 🎓 Contenido Educativo

### Módulo 1: Conceptos Básicos
- El Átomo
- Moléculas
- Estados de la Materia
- La Tabla Periódica

### Módulo 2: Enlaces y Compuestos
- Enlaces Iónicos
- Enlaces Covalentes
- Formulación Química

### Módulo 3: Reacciones Químicas
- Tipos de Reacciones
- Balanceo de Ecuaciones
- Estequiometría

### Módulo 4: Química Avanzada
- Termoquímica
- Soluciones y Concentración
- pH y Ácidos-Bases
- Química Orgánica Básica

## 🏆 Sistema de Logros

- **Primer Paso:** Completa tu primera lección
- **Estudiante Dedicado:** Completa el Módulo 1
- **Químico Junior:** Completa el Módulo 2
- **Experto en Reacciones:** Completa el Módulo 3
- **Maestro de Química:** Completa el Módulo 4
- **Perfeccionista:** Obtén 100% en cualquier quiz
- **Racha de Aprendizaje:** Completa 5 lecciones seguidas

## 🔧 Estructura del Proyecto

```
QuímicaPro/
│
├── .github/workflows/python-ci.yml    # CI con Pytest
├── pytest.ini                         # Configuración de Pytest
├── project/
│   ├── main.py                        # Punto de entrada de la aplicación
│   ├── requirements.txt               # Dependencias del proyecto
│   ├── .env                           # Configuración (no subir a git)
│   ├── .env.example                   # Plantilla de configuración
│   ├── scripts/                       # Utilidades (DB y migraciones)
│   │   ├── apply_migration.py
│   │   └── test_db_connection.py
│   ├── src/
│   │   ├── database.py                # Gestión de base de datos
│   │   ├── auth.py                    # Sistema de autenticación
│   │   └── ui/                        # Vistas y componentes
│   └── tests/
│       ├── test_auth.py
│       └── test_theme.py
│
└── supabase/migrations/               # Migraciones SQL adicionales
```

## 🎨 Personalización

### Agregar nuevo contenido

#### Agregar lecciones
Puedes agregar nuevas lecciones directamente en la base de datos de Supabase:
1. Ve a tu proyecto en Supabase
2. Accede al **Table Editor**
3. Selecciona la tabla `lessons`
4. Inserta nuevas filas con el contenido

#### Agregar preguntas de quiz
1. En Supabase, ve a la tabla `quizzes`
2. Agrega nuevas preguntas vinculadas a una lección (usando `lesson_id`)
3. Define el tipo de pregunta, opciones, respuesta correcta y explicación

#### Agregar logros
1. Ve a la tabla `achievements`
2. Crea nuevos logros con requisitos personalizados
3. Los logros se desbloquean automáticamente según los criterios

## 🐛 Solución de Problemas

### Error de conexión a Supabase
- Verifica que tu archivo `.env` tenga las credenciales correctas
- Asegúrate de tener conexión a internet
- Comprueba que tu proyecto de Supabase esté activo

### Error al instalar PyQt5
En Linux, puede ser necesario instalar dependencias adicionales:
```bash
sudo apt-get install python3-pyqt5
```

### La aplicación no inicia
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Comprueba que estés usando Python 3.7 o superior: `python --version`

## 🚀 Futuras Mejoras

- Simulaciones interactivas (pH, modelos atómicos, mezclas)
- Más contenido educativo y niveles avanzados
- Modo de práctica sin límite de tiempo
- Exportación de progreso a PDF
- Modo oscuro
- Soporte multiidioma

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👨‍💻 Desarrollo

Desarrollado con ❤️ para estudiantes que quieren aprender química de forma interactiva.

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor crea un issue en el repositorio del proyecto.

---

**¡Disfruta aprendiendo química! 🧪**
## 🧪 Pruebas

- Ejecutar prueba con Pytest:
  ```bash
  python -m pytest -q
  ```
- Descubrimiento con unittest (respaldo):
  ```bash
  python -m unittest discover -s project/tests -p "test_*.py" -v
  ```

Incluye:
- `test_auth.py`: login con base de datos simulada
- `test_theme.py`: funciones de tema (`lighten_color`, `set_mode`)

## 🔄 CI y Job de Integración (GitHub Actions)

- Workflow: `/.github/workflows/python-ci.yml`
- Jobs:
  - `tests`: instala dependencias y ejecuta Pytest + unittest
  - `integration`: se ejecuta solo si hay secretos configurados

### Secretos Requeridos
Configura en GitHub → Repo → Settings → Secrets and variables → Actions:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `DATABASE_URL` (opcional, para test de conexión PostgreSQL)

### Qué hace el job de integración
- Crea `project/.env` a partir de secretos
- Prueba conexión a PostgreSQL si hay `DATABASE_URL`
- Inicializa el cliente de Supabase como verificación

## 🧰 Migraciones

Aplicar una migración:
```bash
python project/scripts/apply_migration.py project/supabase/migrations/ARCHIVO.sql
```

Probar conexión a DB:
```bash
python project/scripts/test_db_connection.py
```
