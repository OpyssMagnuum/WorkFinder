from typing import Annotated

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database import new_a_session
from src.models.seeking import SeekerModel, ResumeModel, HRModel, JudgeModel
from src.schemas.seeking_sch import SeekerSchema, ResumeSchema, SeekerSchemaWid, ResumeSchemaWid, HRSchema, HRSchemaWid, \
    JudgeSchema, JudgeSchemaWid, JudgeSchemaOnlyVerdictWid


async def validate_query(session, query, schema):
    result = await session.execute(query)
    object_models = result.scalars().all()
    object_schemas = [schema.model_validate(object) for object in object_models]
    return object_schemas


async def add_to_db(session, data, Model):
    dictionary = data.model_dump()

    res = Model(**dictionary)
    session.add(res)
    await session.flush()

    res_id = res.id

    return res_id


class SeekerRepository:
    @classmethod
    async def add_seeker(cls, data: SeekerSchema) -> int:
        async with new_a_session() as session:
            res = await add_to_db(session, data, SeekerModel)
            await session.commit()
            return res

    @classmethod
    async def find_seekers(
            cls,
    ) -> list[SeekerSchemaWid]:
        async with new_a_session() as session:
            query = select(SeekerModel)
            return await validate_query(session, query, SeekerSchemaWid)


class ResumeRepository:
    @classmethod
    async def add_resume(cls, data: ResumeSchema) -> int:
        async with new_a_session() as session:
            res = await add_to_db(session, data, ResumeModel)
            await session.commit()
            return res

    @classmethod
    async def find_resumes(
            cls,
    ) -> list[ResumeSchemaWid]:
        async with new_a_session() as session:
            query = select(ResumeModel)
            return await validate_query(session, query, ResumeSchemaWid)

    @classmethod
    async def find_resumes_for_seeker(cls, seeker_id) -> list[ResumeSchemaWid]:
        async with new_a_session() as session:
            query = select(ResumeModel).filter(ResumeModel.seeker_id == seeker_id)
            return await validate_query(session, query, ResumeSchemaWid)


class HRRepository:
    @classmethod
    async def add_hr(cls, data: HRSchema) -> int:
        async with new_a_session() as session:
            res = await add_to_db(session, data, HRModel)
            await session.commit()
            return res

    @classmethod
    async def find_hrs(
            cls,
    ) -> list[HRSchemaWid]:
        async with new_a_session() as session:
            query = select(HRModel)
            return await validate_query(session, query, HRSchemaWid)


class JudgeRepository:
    @classmethod
    async def add_judge(cls, data: JudgeSchema) -> int:
        async with new_a_session() as session:
            res = await add_to_db(session, data, JudgeModel)
            await session.commit()
            return res

    @classmethod
    async def find_judges(
            cls,
    ) -> list[JudgeSchemaWid]:
        async with new_a_session() as session:
            query = select(JudgeModel)
            return await validate_query(session, query, JudgeSchemaWid)

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

