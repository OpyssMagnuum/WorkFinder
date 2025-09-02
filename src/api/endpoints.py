from typing import Annotated
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.dependencies import a_session_dep
from src.repository import SeekerRepository, ResumeRepository, HRRepository, JudgeRepository
from src.schemas.seeking_sch import SeekerSchema, ResumeSchema, ResumeSchemaWid, HRSchemaWid, HRSchema, JudgeSchemaWid, \
    JudgeSchema, JudgeSchemaOnlyVerdict, JudgeSchemaOnlyVerdictWid, SeekerSchemaWid

router = APIRouter()


@router.get('/seekers', tags=['Искатель работы 🔍'], summary='Вывести всех искателей 🧑🏻‍👩🏻‍👦🏻')
async def get_seekers() -> list[SeekerSchemaWid]:
    seekers = await SeekerRepository.get_all()
    return seekers


@router.post('/seekers', tags=['Искатель работы 🔍'], summary='Добавить искателя 🧑')
async def add_seeker(seeker: SeekerSchema) -> dict:
    seeker_id = await SeekerRepository.add_seeker(seeker)
    return {"ok": True, "seeker_id": seeker_id}


# RESUMES
@router.post('/resumes', tags=['Резюме 🧐'], summary='Добавить резюме 📃')
async def add_resume(resume: ResumeSchema) -> dict:
    resume_id = await ResumeRepository.add_resume(resume)
    return {"ok": True, "resume_id": resume_id}


@router.get('/resumes', tags=['Резюме 🧐'], summary='Посмотреть все резюме 📖')
async def get_resumes() -> list[ResumeSchemaWid]:
    resumes = await ResumeRepository.get_all()
    return resumes


@router.get('/resumes/{seeker_id}', tags=['Резюме 🧐'], summary='Найти все резюме искателя 📘')
async def get_resumes(seeker_id: int) -> list[ResumeSchemaWid]:
    resumes = await ResumeRepository.find_resumes_for_seeker(seeker_id)
    return resumes


# HR
@router.get('/hrs', tags=['HR 💼'], summary='Посмотреть на всех HR 📧')
async def get_hrs() -> list[HRSchemaWid]:
    hrs = await HRRepository.get_all()
    return hrs


@router.post('/hrs', tags=['HR 💼'], summary='Добавить HR 🤝')
async def add_hr(hr: HRSchema) -> dict:
    hr_id = await HRRepository.add_hr(hr)
    return {"ok": True, "hr_id": hr_id}


# JUDGEMENT
@router.get('/judges', tags=['Рассмотр 🔨'], summary='Посмотреть на все рассмотры 🤔')
async def get_judges() -> list[JudgeSchemaWid]:
    judges = await JudgeRepository.get_all()
    return judges


@router.post('/judges', tags=['Рассмотр 🔨'], summary='Добавить рассмотрение ⁉️')
async def add_judge(judge: JudgeSchema) -> dict:
    judge_id = await JudgeRepository.add_judge(judge)
    return {"ok": True, "judge_id": judge_id}


@router.patch('/judges', tags=['Рассмотр 🔨'], summary='Изменить статус рассмотрения  🔍️')
async def change_judge(data: JudgeSchemaOnlyVerdictWid) -> dict:
    changed = await JudgeRepository.change_judge_status(data)
    return {"ok": True, "changed_id": changed.get("id"), "changed_verdict": changed.get("verdict")}
