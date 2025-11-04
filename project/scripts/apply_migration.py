import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


def ensure_ssl_in_url(db_url: str) -> str:
    if "sslmode=" in db_url:
        return db_url
    sep = "?" if "?" not in db_url else "&"
    return f"{db_url}{sep}sslmode=require"


def get_connection_from_env():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        db_url = ensure_ssl_in_url(db_url)
        return psycopg2.connect(db_url)

    user = os.getenv("DB_USER") or os.getenv("user")
    password = os.getenv("DB_PASSWORD") or os.getenv("password")
    host = os.getenv("DB_HOST") or os.getenv("host")
    port = os.getenv("DB_PORT") or os.getenv("port")
    dbname = os.getenv("DB_NAME") or os.getenv("dbname")

    if not all([user, password, host, port, dbname]):
        raise RuntimeError(
            "Faltan variables de entorno para conexión: DATABASE_URL o DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME"
        )

    return psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        dbname=dbname,
        sslmode="require",
    )


def main():
    # Permite pasar el nombre de archivo de migración como argumento
    default_path = Path(__file__).resolve().parents[1] / "supabase" / "migrations" / "20251104184500_insert_quizzes_atom_basics.sql"
    arg_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else default_path
    migration_path = arg_path
    if not migration_path.exists():
        print(f"No se encontró el archivo de migración: {migration_path}")
        sys.exit(1)

    sql = migration_path.read_text(encoding="utf-8")

    try:
        conn = get_connection_from_env()
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.close()
        print("Migración aplicada correctamente.")
    except Exception as e:
        print(f"Error aplicando migración: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()