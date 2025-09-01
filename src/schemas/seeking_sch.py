from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional


class SchemaOnlyId(BaseModel):
    id: int


class SeekerSchema(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str] = None
    work_exp: int = Field(ge=0)
    age: int = Field(ge=0)


class SeekerSchemaWid(SeekerSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ResumeSchema(BaseModel):
    seeker_id: int
    description: str
    stack: str
    education: str | None = None


class ResumeSchemaWid(ResumeSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class JudgeSchemaOnlyVerdict(BaseModel):
    verdict: Literal['seen', 'approved', 'disapproved'] = Field(default_factory='seen')


class JudgeSchema(JudgeSchemaOnlyVerdict):
    resume_id: int
    hr_id: int


class JudgeSchemaOnlyVerdictWid(JudgeSchemaOnlyVerdict):
    id: int

    model_config = ConfigDict(from_attributes=True)


class JudgeSchemaWid(JudgeSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class HRSchema(BaseModel):
    company: str


class HRSchemaWid(HRSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
