import psycopg2
import logging
import os
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def create_database_if_not_exists(
    db_name: str,
    user: str,
    password: str,
    host: str = "localhost",
    port: int = 5432,
    timeout: int = 5
) -> bool:
    """
    Create a PostgreSQL database if it doesn't already exist.
    
    Args:
        db_name: Name of the database to create
        user: PostgreSQL username
        password: PostgreSQL password
        host: PostgreSQL host (default: localhost)
        port: PostgreSQL port (default: 5432)
        timeout: Connection timeout in seconds (default: 5)
    
    Returns:
        bool: True if database was created or already exists, False if error occurred
    """
    try:
        # Connect to the default 'postgres' database first
        logger.info(f"Connecting to PostgreSQL at {host}:{port}...")
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port,
            connect_timeout=timeout
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database already exists
        logger.info(f"Checking if database '{db_name}' exists...")
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if not exists:
            logger.info(f"Creating database '{db_name}'...")
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            logger.info(f"✅ Database '{db_name}' created successfully.")
        else:
            logger.info(f"✅ Database '{db_name}' already exists.")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        logger.error(f"❌ Connection failed: {e}")
        logger.error("Make sure PostgreSQL is running and credentials are correct.")
        return False
    except psycopg2.ProgrammingError as e:
        logger.error(f"❌ Database operation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


def create_database_from_config(config_path: str = "config.json") -> bool:
    """
    Create database using configuration from config.json file.
    
    Args:
        config_path: Path to config.json file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import json
        
        with open(config_path, "r") as f:
            config = json.load(f)
        
        db_config = config.get("DATABASE", {})
        
        return create_database_if_not_exists(
            db_name=db_config.get("DATABASE_NAME", "employee_db"),
            user=db_config.get("USERNAME", "postgres"),
            password=db_config.get("PASSWORD", "password"),
            host=db_config.get("HOST", "localhost"),
            port=db_config.get("PORT", 5432)
        )
    except FileNotFoundError:
        logger.error(f"❌ Config file '{config_path}' not found.")
        return False
    except json.JSONDecodeError:
        logger.error(f"❌ Invalid JSON in '{config_path}'.")
        return False


if __name__ == "__main__":
    # Load from environment or config file
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "password")
    db_name = os.getenv("DB_NAME", "employee_db")
    
    success = create_database_if_not_exists(
        db_name=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    exit(0 if success else 1)