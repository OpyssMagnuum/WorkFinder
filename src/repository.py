from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, update
from src.database import new_a_session
from src.models.seeking import SeekerModel, ResumeModel, HRModel, JudgeModel
from src.schemas.seeking_sch import SeekerSchema, ResumeSchema, SeekerSchemaWid, ResumeSchemaWid, HRSchema, HRSchemaWid, \
    JudgeSchema, JudgeSchemaWid, JudgeSchemaOnlyVerdictWid


async def validate_query(session, query, schema):
    result = await session.execute(query)
    object_models = result.scalars().all()
    object_schemas = [schema.model_validate(obj) for obj in object_models]
    return object_schemas


def db_transaction(func):
    async def wrapper(*args, **kwargs):
        async with new_a_session() as session:
            try:
                result = await func(session=session, *args, **kwargs)
                await session.commit()
                return result
            except Exception as e:
                await session.rollback()
                raise HTTPException(500, f'Database error: {str(e)}')
    return wrapper


@db_transaction
async def add_to_db(session, data, model) -> int:
    dictionary = data.model_dump()

    res = model(**dictionary)
    session.add(res)
    await session.flush()
    return res.id

T = TypeVar('T', bound=BaseModel)
M = TypeVar('M')


class BaseRepository:
    model: type[M]
    schema: type[T]

    @classmethod
    async def get_all(cls) -> list[T]:
        async with new_a_session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return [cls.schema.model_validate(obj) for obj in result.scalars().all()]


class SeekerRepository(BaseRepository):
    model = SeekerModel
    schema = SeekerSchemaWid

    @classmethod
    async def add_seeker(
            cls,
            data: SeekerSchema
    ) -> int:
        return await add_to_db(data=data, model=cls.model)

    # @classmethod
    # async def find_seekers(
    #         cls,
    # ) -> list[SeekerSchemaWid]:
    #     return await cls.get_all()


class ResumeRepository(BaseRepository):
    model = ResumeModel
    schema = ResumeSchemaWid

    @classmethod
    async def add_resume(
            cls,
            data: ResumeSchema
    ) -> int:
        return await add_to_db(data=data, model=cls.model)

    # @classmethod
    # async def find_resumes(
    #         cls,
    # ) -> list[ResumeSchemaWid]:
    #     return await cls.get_all()

    @classmethod
    async def find_resumes_for_seeker(cls, seeker_id) -> list[ResumeSchemaWid]:
        async with new_a_session() as session:
            query = select(cls.model).filter(cls.model.seeker_id == seeker_id)
            return await validate_query(session, query, cls.schema)


class HRRepository(BaseRepository):
    model = HRModel
    schema = HRSchemaWid

    @classmethod
    async def add_hr(
            cls,
            data: HRSchema,
    ) -> int:
        return await add_to_db(data=data, model=cls.model)

    # @classmethod
    # async def find_hrs(
    #         cls,
    # ) -> list[HRSchemaWid]:
    #     return await cls.get_all()


class JudgeRepository(BaseRepository):
    model = JudgeModel
    schema = JudgeSchemaWid

    @classmethod
    async def add_judge(
            cls,
            data: JudgeSchema
    ) -> int:
        return await add_to_db(data=data, model=cls.model)

    # @classmethod
    # async def find_judges(
    #         cls,
    # ) -> list[JudgeSchemaWid]:
    #     return await cls.get_all()

    @classmethod
    async def change_judge_status(
            cls,
            data: JudgeSchemaOnlyVerdictWid,
    ) -> dict:
        async with new_a_session() as session:
            judge_dump = data.model_dump()

            change = {'id': judge_dump.get('id'), 'verdict': judge_dump.get('verdict')}
            stmt = (
                update(JudgeModel)
                .where(JudgeModel.id == change.get('id'))
                .values(verdict=change.get('verdict'))
            )
            await session.execute(stmt)
            await session.commit()
            return change

