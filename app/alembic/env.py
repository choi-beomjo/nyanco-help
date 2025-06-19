from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from sqlalchemy import text 
from model.base import Base
# ❗ 여기서 모델들 import
import os, glob, importlib.util
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_GLOB = BASE_DIR / "api" / "domain" / "*" / "models.py"

for model_path in glob.glob(str(MODEL_GLOB)):
    module_name = (
        Path(model_path).with_suffix("").relative_to(BASE_DIR).as_posix().replace("/", ".")
    )
    importlib.import_module(module_name)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

import os
# 🔥 핵심: 환경변수 강제 적용
db_url = os.getenv("DB_URL", "sqlite:///./myapi.db")
print(f"🔥 DB_URL = {db_url}")  # 확인용
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)
else:
    raise ValueError("환경변수 DB_URL이 설정되지 않았습니다.")


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
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
    url = config.get_main_option("sqlalchemy.url")
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
    )

    with connectable.connect() as connection:
        # ✅ DB 종류가 mysql/mariadb인 경우에만 외래키 체크 해제
        if connection.dialect.name in ("mysql", "mariadb"):
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=(connection.dialect.name == "sqlite")  # 🔥 핵심!
        )

        with context.begin_transaction():
            context.run_migrations()

        # ✅ 마찬가지로 다시 외래키 체크 활성화 (MySQL/MariaDB일 때만)
        if connection.dialect.name in ("mysql", "mariadb"):
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
