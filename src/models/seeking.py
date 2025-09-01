from sqlalchemy import ForeignKey, Table, Column

from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class SeekerModel(Model):
    __tablename__ = 'seeker'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    work_exp: Mapped[int]
    age: Mapped[int]


class ResumeModel(Model):
    __tablename__ = 'resume'

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    stack: Mapped[str]
    education: Mapped[str | None]

    seeker_id: Mapped[int] = mapped_column(ForeignKey('seeker.id'))


class JudgeModel(Model):
    __tablename__ = 'judge'

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey('resume.id'))
    hr_id: Mapped[int] = mapped_column(ForeignKey('hr.id'))
    verdict: Mapped[str]


class HRModel(Model):
    __tablename__ = 'hr'

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str]

