import os
import sys
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

import psycopg2
from dotenv import load_dotenv


def ensure_ssl_in_url(db_url: str) -> str:
    """Append sslmode=require to a PostgreSQL URL if not present."""
    parsed = urlparse(db_url)
    query = parse_qs(parsed.query)
    if "sslmode" not in query:
        query["sslmode"] = ["require"]
    new_query = urlencode({k: v[0] for k, v in query.items()})
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


def main():
    load_dotenv()

    # Prefer DATABASE_URL if available
    db_url = os.getenv("DATABASE_URL")

    try:
        if db_url:
            db_url = ensure_ssl_in_url(db_url)
            conn = psycopg2.connect(db_url)
        else:
            user = os.getenv("DB_USER") or os.getenv("user")
            password = os.getenv("DB_PASSWORD") or os.getenv("password")
            host = os.getenv("DB_HOST") or os.getenv("host")
            port = os.getenv("DB_PORT") or os.getenv("port")
            dbname = os.getenv("DB_NAME") or os.getenv("dbname")

            if not all([user, password, host, port, dbname]):
                raise RuntimeError(
                    "Faltan variables de entorno para conexión: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME (o sus equivalentes en minúscula)."
                )

            conn = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                dbname=dbname,
                sslmode="require",
            )

        print("Conexión exitosa a PostgreSQL.")
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        now = cur.fetchone()
        print("Hora actual:", now)
        cur.close()
        conn.close()
        print("Conexión cerrada.")
    except Exception as e:
        print(f"Error de conexión: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()