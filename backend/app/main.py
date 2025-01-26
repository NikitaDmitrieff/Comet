import os

from comet_helper.main import GuidanceCounselor
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float


class Question(BaseModel):
    text: str


app = FastAPI()


@app.get("/")
async def read_item():
    return {"message": "Welcome to our app"}


@app.get("/hello/{name}")
async def read_item(name):
    return {"message": f"Hello {name}, how are you?"}


@app.post("/items/")
async def create_item(item: Item):
    return {"message": f"{item.name} is priced at £{item.price}"}


@app.post("/question/")
async def fetch_answer(question: Question):

    guidance_counselor = GuidanceCounselor(
        pdf_directory=os.getenv("COMET_HELPER_DATA_PATH"),
    )

    output = guidance_counselor.generate_answer(user_question=question.text)

    return {"Question": question.text, "Answer": output["answer"]}
