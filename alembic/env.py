from __future__ import annotations

import asyncio
import re
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import settings
from app.infra.db.base import Base
import app.domain.models  
# Alembic's Config object, populated from alembic.ini.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

_ASYNC_DRIVER = "asyncpg"


def _get_database_url() -> str:
    url = settings.DATABASE_URL
    return re.sub(
        r"^postgresql(?:\+\w+)?://",
        f"postgresql+{_ASYNC_DRIVER}://",
        url,
        count=1,
    )


# Inject the resolved async URL before Alembic reads it anywhere else.
config.set_main_option("sqlalchemy.url", _get_database_url())

# All tables live on this metadata object.
target_metadata = Base.metadata


def _configure_context(connection: Connection | str) -> None:
    """Shared context.configure() used by both online and offline paths.

    Online mode receives a live Connection; offline mode receives the URL
    string and must be configured with ``url=`` instead.
    """
    kwargs: dict[str, object] = {"target_metadata": target_metadata}
    if isinstance(connection, str):
        kwargs["url"] = connection
        kwargs["literal_binds"] = True
        kwargs["dialect_opts"] = {"paramstyle": "named"}
    else:
        kwargs["connection"] = connection
    context.configure(
        **kwargs,
        # Detect column type changes (e.g. String(50) -> String(255)).
        compare_type=config.get_section_option("alembic", "compare_type", "false")
        == "true",
        render_as_batch=False,  # no SQLite batch-mode aliasing needed
    )


def run_migrations_offline() -> None:
    """Offline mode: emit SQL for the target database without a connection."""
    _configure_context(config.get_main_option("sqlalchemy.url"))
    with context.begin_transaction():
        context.run_migrations()


def _do_run_migrations(connection: Connection) -> None:
    """Synchronous bridge called by the async engine via run_sync()."""
    _configure_context(connection)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Build an AsyncEngine from the same config used by the app and migrate."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        # NullPool avoids keeping pooled connections alive during short
        # migration runs (standard Alembic async recommendation).
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # SQLAlchemy async connections must be driven from a sync function.
        await connection.run_sync(_do_run_migrations)

    # Ensure the engine and its loop-bound resources are fully released.
    await connectable.dispose()


def run_migrations_online() -> None:
    """Online mode: run inside a fresh asyncio event loop."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
