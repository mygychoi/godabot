import asyncio
from contextlib import asynccontextmanager

from asyncpg import Connection, Pool, create_pool
from fastapi import FastAPI

from app.configs import settings

from .exceptions import DatabaseError


class PoolManager:
    _pool: Pool

    @classmethod
    async def start(cls):
        cls._pool = await create_pool(  # pyright: ignore
            dsn=settings.DATABASE_URL,
            min_size=8,
            max_size=8,
            command_timeout=3,
        )

    @classmethod
    async def close(cls):
        try:
            await asyncio.wait_for(cls._pool.close(), timeout=1)
        except (Exception, asyncio.TimeoutError) as error:
            raise DatabaseError("Pool was abort") from error

    @classmethod
    async def acquire(cls) -> Connection:
        return await cls._pool.acquire(timeout=10)

    @classmethod
    async def release(cls, *, connection: Connection):
        await cls._pool.release(connection, timeout=10)

    @classmethod
    @asynccontextmanager
    async def initiate(cls, app: FastAPI | None = None):  # noqa
        try:
            await cls.start()
            yield {"pool": cls}
        finally:
            await cls.close()

    @classmethod
    async def __aenter__(cls):
        await cls.start()

    @classmethod
    async def __aexit__(cls, exc_type, exc_val, exc_tb):
        await cls.close()

    @classmethod
    def pool(cls) -> Pool:
        if not hasattr(cls, "_pool"):
            raise DatabaseError("There is no pool")
        return cls._pool
