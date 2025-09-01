from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from secretstuff import db_conn, db_conn_async

a_engine = create_async_engine(db_conn_async)

new_a_session = async_sessionmaker(a_engine)


class Model(DeclarativeBase):
    pass


async def get_async_session():
    async with new_a_session() as session:
        yield session
