import os
import sys
import subprocess


def build_exe(mode: str = "onefile", name: str = "QuimicaPro", icon: str = "project/assets/icons/app.ico", windowed: bool = True):
    entry = "project/main.py"
    if not os.path.isfile(entry):
        print(f"[error] No se encuentra el entry point: {entry}")
        sys.exit(1)

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name", name,
    ]

    cmd += ["--windowed"] if windowed else ["--console"]
    cmd += ["--onefile"] if mode == "onefile" else ["--onedir"]

    # Recolección y imports necesarios para PyQt5
    cmd += ["--collect-all", "PyQt5", "--hidden-import", "PyQt5.sip"]

    # Icono (opcional)
    if icon and os.path.isfile(icon):
        cmd += ["--icon", icon]
    else:
        print(f"[warn] Icono no encontrado en '{icon}', se omite.")

    # Incluir assets si existen (se accederán vía ruta relativa 'assets/')
    assets_src = "project/assets"
    if os.path.isdir(assets_src):
        # Formato SRC;DEST en Windows
        cmd += ["--add-data", f"{assets_src};assets"]

    # Archivo principal
    cmd += [entry]

    print("[info] Ejecutando:")
    print(" ", " ".join(cmd))
    subprocess.check_call(cmd)
    print("[info] Build completado. Revisa la carpeta 'dist/'.")


def parse_args(argv):
    mode = "onefile"
    name = "QuimicaPro"
    icon = "project/assets/icons/app.ico"
    windowed = True

    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--mode", "-m") and i + 1 < len(argv):
            mode = argv[i + 1]
            i += 1
        elif a.startswith("--name="):
            name = a.split("=", 1)[1]
        elif a.startswith("--icon="):
            icon = a.split("=", 1)[1]
        elif a == "--console":
            windowed = False
        elif a == "--windowed":
            windowed = True
        i += 1

    return mode, name, icon, windowed


if __name__ == "__main__":
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("[error] PyInstaller no está instalado.")
        print("        Instálalo con: python -m pip install pyinstaller")
        sys.exit(1)

    mode, name, icon, windowed = parse_args(sys.argv[1:])
    build_exe(mode=mode, name=name, icon=icon, windowed=windowed)