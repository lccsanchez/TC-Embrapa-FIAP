import os
from logging.config import fileConfig
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context
from app.model.model import Base

# Carrega variáveis do .env
load_dotenv()

driver = os.getenv('DB_DRIVER', 'mysql+pymysql')  # pymysql é o driver mais comum
user = os.getenv('DB_USER')
password = quote_plus(os.getenv('DB_PASSWORD'))  # Codifica a senha
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT', '3306')  # Porta padrão do MySQL
db_name = os.getenv('DB_NAME')
ssl_cert = os.getenv('SSL_CERT')

SQLALCHEMY_DATABASE_URI =f"{driver}://{user}:{password}@{host}:{port}/{db_name}?ssl_ca={ssl_cert}"

print("url: " + SQLALCHEMY_DATABASE_URI)
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = SQLALCHEMY_DATABASE_URI

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=SQLALCHEMY_DATABASE_URI,  # Passa a URL diretamente aqui
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
