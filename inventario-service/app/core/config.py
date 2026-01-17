import os

APP_NAME = os.getenv("APP_NAME", "Microservicio Inventario - TIGO")
APP_VERSION = os.getenv("APP_VERSION", "1.0")

# SQLite por defecto (ideal para trabajo local / demo)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventario.db")
