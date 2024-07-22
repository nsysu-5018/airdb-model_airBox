from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import airBox


class InputData(BaseModel):
    address: str


app = FastAPI()


@app.post("/run")
def run(data: InputData):
    output = airBox.run(data)
    return [output]

@app.get("/fig_one")
def fig_one():
    return FileResponse('fig_one.jpg')

@app.get("/fig_two")
def fig_two():
    return FileResponse('fig_two.jpg')