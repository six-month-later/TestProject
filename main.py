from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def get_info():
    return FileResponse("public/index.html")


@app.post("/calculate")
async def calc(num1, num2):
    sum = sum(num1 + num2)
    return {"message": "Сумма " + num1 + " и " + num2 + " равна " + sum}
