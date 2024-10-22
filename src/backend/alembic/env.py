from __future__ import absolute_import
import sys
import os

from alembic import context
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlmodel import SQLModel
from app.models.user_models import User  # Cambia esto a la ubicación correcta de tu modelo

# Agrega el directorio de tu proyecto a la ruta para que pueda importar los modelos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

# Obtenemos la URL de la base de datos de la configuración
config = context.config
target_metadata = SQLModel.metadata

# La configuración de la URL de la base de datos
def run_migrations_online():
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
