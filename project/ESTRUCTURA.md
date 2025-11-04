# Estructura del Proyecto QuímicaPro

## Arquitectura General

QuímicaPro sigue una arquitectura modular basada en el patrón MVC (Modelo-Vista-Controlador) adaptado para aplicaciones de escritorio:

- **Modelo:** Gestión de datos con Supabase (PostgreSQL)
- **Vista:** Interfaz gráfica con PyQt5
- **Controlador:** Lógica de negocio y coordinación

## Estructura de Carpetas

```
quimica-pro/
│
├── main.py                      # Punto de entrada principal
├── requirements.txt             # Dependencias del proyecto
├── .env                        # Configuración (NO incluir en repositorio)
├── .env.example                # Plantilla de configuración
├── README.md                   # Documentación principal
├── INSTALACION.md              # Guía de instalación
├── ESTRUCTURA.md               # Este archivo
│
└── src/                        # Código fuente principal
    ├── __init__.py            # Inicialización del paquete
    ├── database.py            # Capa de acceso a datos
    ├── auth.py                # Sistema de autenticación
    │
    └── ui/                    # Componentes de interfaz
        ├── __init__.py
        ├── login_window.py     # Ventana de login/registro
        ├── main_window.py      # Ventana principal con navegación
        ├── home_view.py        # Vista de inicio/dashboard
        ├── modules_view.py     # Vista de módulos y lecciones
        ├── lesson_view.py      # Vista de contenido de lección
        ├── quiz_view.py        # Vista de cuestionarios
        ├── progress_view.py    # Vista de progreso del usuario
        └── achievements_view.py # Vista de logros
```

## Descripción de Módulos

### main.py

**Responsabilidad:** Inicialización de la aplicación

- Crea la instancia de QApplication
- Inicializa Database y AuthManager
- Gestiona el flujo de login → aplicación principal
- Maneja el ciclo de vida de las ventanas

**Flujo:**
1. Inicia con LoginWindow
2. Al autenticarse exitosamente → MainWindow
3. Al cerrar sesión → vuelve a LoginWindow

### src/database.py

**Responsabilidad:** Interacción con Supabase (capa de datos)

**Métodos principales:**

```python
create_user(username, display_name)           # Crear nuevo usuario
get_user_by_username(username)                # Obtener usuario por nombre
update_last_login(user_id)                    # Actualizar último login

get_all_modules()                             # Obtener todos los módulos
get_lessons_by_module(module_id)              # Obtener lecciones de un módulo
get_lesson_by_id(lesson_id)                   # Obtener lección específica

get_quizzes_by_lesson(lesson_id)              # Obtener preguntas de quiz

get_user_progress(user_id)                    # Obtener progreso del usuario
save_lesson_progress(user_id, lesson_id, ...) # Guardar progreso de lección
get_module_completion(user_id, module_id)     # Calcular completitud de módulo

get_all_achievements()                        # Obtener todos los logros
get_user_achievements(user_id)                # Obtener logros del usuario
award_achievement(user_id, achievement_id)    # Otorgar logro a usuario
```

**Características:**
- Maneja todas las operaciones CRUD
- Gestiona relaciones entre tablas
- Implementa lógica de cálculos (porcentajes, estadísticas)
- Manejo de errores con try/except

### src/auth.py

**Responsabilidad:** Gestión de autenticación local

**Métodos principales:**

```python
login(username)                    # Iniciar sesión
register(username, display_name)   # Registrar nuevo usuario
logout()                          # Cerrar sesión
is_authenticated()                # Verificar si está autenticado
get_current_user()                # Obtener datos del usuario actual
get_current_user_id()             # Obtener ID del usuario actual
```

**Características:**
- Validación de credenciales
- Gestión de sesión actual
- Mensajes de error descriptivos

## Componentes de Interfaz (UI)

### src/ui/login_window.py

**Responsabilidad:** Ventana de autenticación

**Características:**
- Dos páginas: Login y Registro
- Navegación entre páginas con botones
- Validación de campos
- Señal `login_successful` al autenticarse
- Diseño con gradiente azul

**Estructura:**
```
LoginWindow (QWidget)
├── QStackedWidget
│   ├── Login Page
│   │   ├── Username input
│   │   ├── Login button
│   │   └── Switch to register button
│   └── Register Page
│       ├── Username input
│       ├── Display name input
│       ├── Register button
│       └── Switch to login button
```

### src/ui/main_window.py

**Responsabilidad:** Ventana principal con navegación

**Componentes:**
1. **Sidebar (250px):**
   - Logo y nombre de usuario
   - Botones de navegación
   - Botón de cerrar sesión

2. **Content Area:**
   - QStackedWidget con 4 vistas
   - Cambio dinámico según navegación

**Vistas incluidas:**
- HomeView (index 0)
- ModulesView (index 1)
- ProgressView (index 2)
- AchievementsView (index 3)

### src/ui/home_view.py

**Responsabilidad:** Dashboard principal

**Elementos:**
1. **Estadísticas generales:**
   - Lecciones completadas
   - Logros obtenidos
   - Puntuación promedio

2. **Vista rápida de módulos:**
   - Grid 2x2 con los 4 módulos
   - Progreso visual por módulo
   - Colores temáticos

**Método clave:**
- `refresh()`: Actualiza datos al mostrar la vista

### src/ui/modules_view.py

**Responsabilidad:** Navegación de módulos y lecciones

**Estructura:**
```
ModulesView
├── Sidebar (300px)
│   └── Lista de módulos
└── Content Area
    ├── Module Content (vista de lecciones)
    └── Lesson View (contenido de lección)
```

**Flujo:**
1. Usuario selecciona módulo → muestra lecciones
2. Usuario selecciona lección → muestra contenido
3. Usuario inicia quiz → muestra cuestionario

### src/ui/lesson_view.py

**Responsabilidad:** Mostrar contenido de lección

**Componentes:**
1. **Header:**
   - Botón "Volver"
   - Título de la lección

2. **Content:**
   - QTextBrowser con HTML de la lección
   - Soporte para formato HTML

3. **Quiz Card:**
   - Información sobre el quiz
   - Botón para iniciar cuestionario

### src/ui/quiz_view.py

**Responsabilidad:** Sistema de cuestionarios interactivos

**Flujo:**
1. **Mostrar pregunta:**
   - Una pregunta a la vez
   - Opciones con radio buttons
   - Navegación anterior/siguiente

2. **Recopilar respuestas:**
   - Almacena respuestas en diccionario
   - Permite navegar entre preguntas

3. **Mostrar resultados:**
   - Calcula puntuación
   - Muestra revisión con explicaciones
   - Guarda progreso en base de datos
   - Verifica y otorga logros

**Características especiales:**
- Retroalimentación visual (verde/rojo)
- Explicaciones detalladas
- Sistema de logros automático

### src/ui/progress_view.py

**Responsabilidad:** Visualización de progreso del estudiante

**Componentes:**
1. **Estadísticas globales:**
   - Módulos completados
   - Lecciones completadas
   - Puntuación promedio

2. **Progreso por módulo:**
   - Cards con barras de progreso
   - Porcentajes visuales
   - Estado de completitud

### src/ui/achievements_view.py

**Responsabilidad:** Sistema de logros y reconocimientos

**Componentes:**
- Grid 3 columnas de achievement cards
- Logros bloqueados (grises) vs desbloqueados (dorados)
- Íconos emoji según tipo
- Descripción de requisitos

**Tipos de logros:**
- `lesson_complete`: Por número de lecciones
- `module_complete`: Por módulos completos
- `perfect_score`: Por puntuación perfecta
- `streak`: Por rachas de estudio

## Base de Datos (Supabase)

### Tablas

#### app_users
```sql
id              uuid PRIMARY KEY
username        text UNIQUE NOT NULL
display_name    text NOT NULL
created_at      timestamptz DEFAULT now()
last_login      timestamptz DEFAULT now()
```

#### modules
```sql
id              integer PRIMARY KEY
level           integer NOT NULL
title           text NOT NULL
description     text NOT NULL
icon            text NOT NULL
color           text NOT NULL (hex color)
order_index     integer NOT NULL
```

#### lessons
```sql
id                  uuid PRIMARY KEY
module_id           integer → modules(id)
title               text NOT NULL
content             text NOT NULL (HTML)
order_index         integer NOT NULL
estimated_minutes   integer DEFAULT 10
```

#### quizzes
```sql
id              uuid PRIMARY KEY
lesson_id       uuid → lessons(id)
question        text NOT NULL
question_type   text NOT NULL (multiple_choice, true_false)
options         jsonb (array de opciones)
correct_answer  text NOT NULL
explanation     text NOT NULL
points          integer DEFAULT 10
order_index     integer NOT NULL
```

#### user_progress
```sql
id              uuid PRIMARY KEY
user_id         uuid → app_users(id)
lesson_id       uuid → lessons(id)
completed       boolean DEFAULT false
score           integer DEFAULT 0
completed_at    timestamptz DEFAULT now()
UNIQUE(user_id, lesson_id)
```

#### achievements
```sql
id                  uuid PRIMARY KEY
title               text NOT NULL
description         text NOT NULL
icon                text NOT NULL
requirement_type    text NOT NULL
requirement_value   integer NOT NULL
```

#### user_achievements
```sql
id              uuid PRIMARY KEY
user_id         uuid → app_users(id)
achievement_id  uuid → achievements(id)
earned_at       timestamptz DEFAULT now()
UNIQUE(user_id, achievement_id)
```

## Flujo de Datos

### Flujo de Autenticación

```
Usuario ingresa credenciales
    ↓
AuthManager.login(username)
    ↓
Database.get_user_by_username(username)
    ↓
Supabase Query
    ↓
Si existe: AuthManager guarda sesión
    ↓
LoginWindow emite señal login_successful
    ↓
main.py crea y muestra MainWindow
```

### Flujo de Lección

```
Usuario selecciona módulo
    ↓
ModulesView.load_module_content(module)
    ↓
Database.get_lessons_by_module(module_id)
    ↓
Usuario hace clic en "Comenzar lección"
    ↓
LessonView muestra contenido HTML
    ↓
Usuario hace clic en "Iniciar Cuestionario"
    ↓
QuizView.show_question()
    ↓
Usuario responde todas las preguntas
    ↓
QuizView.show_results()
    ↓
Database.save_lesson_progress()
    ↓
QuizView.check_achievements()
    ↓
Database.award_achievement() (si aplica)
```

## Estilos y Diseño

### Paleta de Colores

- **Primario:** Azul (#1e3c72, #2196F3)
- **Secundario:** Verde (#4CAF50)
- **Acentos:** Naranja (#FF9800), Morado (#9C27B0)
- **Neutros:** Grises (#f5f5f5, #e0e0e0, #666)

### Tipografía

- **Fuente:** Arial
- **Títulos grandes:** 28-32px Bold
- **Títulos medianos:** 18-20px Bold
- **Títulos pequeños:** 14-16px Bold
- **Texto normal:** 12-14px Regular

### Componentes Reutilizables

1. **Cards:**
   - Border radius: 10-15px
   - Padding: 20-25px
   - Border: 2px solid #e0e0e0

2. **Botones:**
   - Border radius: 8px
   - Padding: 10-15px
   - Hover: Color más oscuro

3. **Gradientes:**
   - Login: Azul vertical
   - Módulos: Colores específicos por tema

## Extensibilidad

### Agregar nuevo módulo

1. Insertar en tabla `modules`
2. Crear lecciones en tabla `lessons`
3. Agregar quizzes en tabla `quizzes`
4. La UI se actualiza automáticamente

### Agregar nueva vista

1. Crear archivo en `src/ui/nueva_vista.py`
2. Heredar de `QWidget`
3. Implementar método `refresh()`
4. Agregar a `MainWindow.content_stack`
5. Crear botón de navegación en sidebar

### Personalizar estilos

- Todos los estilos están inline con `setStyleSheet()`
- Usar QSS (Qt Style Sheets) similar a CSS
- Modificar colores, tamaños y efectos en cada componente

## Buenas Prácticas Implementadas

✅ Separación de responsabilidades (UI, Lógica, Datos)
✅ Manejo de errores con try/except
✅ Señales y slots de PyQt5 para comunicación
✅ Uso de `.maybeSingle()` en lugar de `.single()`
✅ Documentación inline en código
✅ Naming conventions claros
✅ Validación de entrada de usuario
✅ Feedback visual inmediato
✅ Arquitectura escalable y modular

---

Esta estructura permite un mantenimiento fácil y la extensión futura del proyecto.
