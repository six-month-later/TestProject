from pydantic import BaseModel, ConfigDict


class Calculator(BaseModel):
    num1: int
    num2: int


class STaskAdd(BaseModel):
    name: str
    description: str | None = None


class STask(STaskAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class STaskID(BaseModel):
    id: int


class User(BaseModel):
    name: str
    age: int
