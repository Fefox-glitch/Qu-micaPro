# QuímicaPro

![Python CI](https://github.com/Fefox-glitch/Qu-micaPro/actions/workflows/python-ci.yml/badge.svg)
![Integration](https://github.com/Fefox-glitch/Qu-micaPro/actions/workflows/integration.yml/badge.svg)

Aplicación de escritorio educativa de química para estudiantes de secundaria y bachillerato. Incluye módulos de aprendizaje, lecciones, cuestionarios, progreso y logros, con persistencia en Supabase.

## Características
- Módulos y lecciones con contenido estructurado.
- Cuestionarios con corrección y explicación.
- Progreso y logros por usuario.
- Modo claro/oscuro y UI moderna en PyQt5.
- Pruebas unitarias y CI en GitHub Actions.

## Estructura del proyecto

```
QuímicaPro/
├── .github/workflows/python-ci.yml     # CI (pytest + unittest)
├── pytest.ini                          # Configuración de Pytest
├── project/                            # Código principal de la app
│   ├── main.py                         # Punto de entrada
│   ├── requirements.txt                # Dependencias
│   ├── .env.example                    # Plantilla de variables de entorno
│   ├── scripts/                        # Utilidades (migraciones y tests DB)
│   │   ├── apply_migration.py
│   │   └── test_db_connection.py
│   ├── src/                            # Código de aplicación
│   │   ├── database.py                 # Capa de datos (Supabase)
│   │   ├── auth.py                     # Autenticación local
│   │   └── ui/                         # Vistas y componentes PyQt5
│   └── tests/                          # Pruebas unitarias
│       ├── test_auth.py
│       └── test_theme.py
└── supabase/migrations/                # (Opcional) migraciones SQL adicionales
```

Nota: El proyecto vive dentro de `project/`. El README raíz facilita el onboarding, CI y comandos.

## Requisitos
- Python 3.11 (recomendado) o superior.
- Cuenta y proyecto en Supabase.

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/Fefox-glitch/Qu-micaPro.git
   cd QuímicaPro
   ```
2. (Opcional) Crea y activa un entorno virtual.
3. Instala dependencias:
   ```bash
   python -m pip install -r project/requirements.txt
   ```

## Configuración (.env)
1. Copia la plantilla:
   ```bash
   copy project\.env.example project\.env
   ```
2. Completa al menos:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

   Opcional (para conexión directa PostgreSQL / scripts):
   - `DATABASE_URL` (recomendado) o
   - `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`

## Ejecutar la aplicación
```bash
python project/main.py
```

## Pruebas
- Ejecuta la suite con Pytest:
  ```bash
  python -m pytest -q
  ```
- Descubrimiento por unittest (respaldo):
  ```bash
  python -m unittest discover -s project/tests -p "test_*.py" -v
  ```

Pruebas incluidas:
- `test_auth.py`: flujo de login con base de datos simulada.
- `test_theme.py`: funciones puras de tema (`lighten_color`, `set_mode`).

## CI/CD (GitHub Actions)
- Workflows:
  - `/.github/workflows/python-ci.yml` (unit tests con Pytest/Unittest)
  - `/.github/workflows/integration.yml` (integración con Supabase y DB, requiere secretos; se ejecuta solo cuando cambian migraciones)
- Se ejecutan en cada `push`/`PR` contra `main`.
 - Disparo manual: GitHub → Actions → Integration → Run workflow → selecciona rama (p.ej. `main`).
   - Requiere tener configurados `SUPABASE_URL`, `SUPABASE_KEY` y opcional `DATABASE_URL` en `Settings → Secrets and variables → Actions`.

## Empaquetado (.exe)
- Instala PyInstaller:
  ```bash
  python -m pip install pyinstaller
  ```
- Genera ejecutable (modo `onefile`):
  ```bash
  python project/scripts/build_exe.py --mode onefile
  ```
- Resultado: `dist/QuimicaPro.exe` (o carpeta `dist/QuimicaPro/` si usas `--mode onedir`).
- Icono (opcional): coloca `project/assets/icons/app.ico` para que se incluya automáticamente.
- Variables de entorno: pon `project/.env` junto al `.exe` o configura variables del sistema.

### Release Build (tags)
- Al crear un tag `v*` y hacer push, el workflow `/.github/workflows/release-build.yml` construye el `.exe` y sube un artefacto.
- También puedes ejecutarlo manualmente desde `Actions → Release Build → Run workflow`.
- Artefacto esperado: `QuimicaPro-<tag>-windows` con `dist/QuimicaPro.exe`.

## Migraciones de Supabase
- Ubicación principal: `project/supabase/migrations/`.
- Aplicar una migración:
  ```bash
  python project/scripts/apply_migration.py project/supabase/migrations/ARCHIVO.sql
  ```
- Probar conexión PostgreSQL (usando `.env`):
  ```bash
  python project/scripts/test_db_connection.py
  ```

Consejos:
- Prefiere `DATABASE_URL` con `sslmode=require` para scripts.
- El script añade `sslmode=require` si falta.

## Resolución de problemas
- “`pytest` no se reconoce”: usa `python -m pytest -q`.
- Faltan variables Supabase: revisa `project/.env`.
- Error `pg_config` al instalar `psycopg2`: ya usamos `psycopg2-binary`; si persiste, actualiza `pip` y reinstala.
- Ventana de login no aparece en foreground: ya está forzado el foco tras logout y en inicio.

## Contribuir
1. Crea una rama desde `main`.
2. Añade tests para nuevas funciones.
3. Abre un Pull Request describiendo cambios.

## Licencia
Pendiente de definir.