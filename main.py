from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# class Calc(BaseModel):

#     num1: int
#     num2: int


@app.get("/")
async def into_file():
    return FileResponse("public/index.html")

@app.get("/info")
async def get_info():
    return {"message": "Это мой первый проект FastAPI!"}

@app.post("/calculate")
async def calc(num1, num2):
    sum = num1 + num2
    return {"message": "Сумма " + num1 + " и " + num2 + " равна " + sum}
