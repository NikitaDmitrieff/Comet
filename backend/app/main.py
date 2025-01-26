import os

from fastapi import FastAPI
from pydantic import BaseModel

from comet_helper.main import GuidanceCounselor


class Profile(BaseModel):
    name: str = "Nikit"
    section_1: str
    section_2: str
    subjects_1: list
    subjects_2: list
    subjects_3: list
    relative_overall_average: float
    absolute_value: float
    overall_average: float
    french_grade: float
    math_level: float


class Question(BaseModel):
    text: str


app = FastAPI()


@app.post("/items/")
async def fetch_wishes(profile: Profile):
    profile_dict = profile.model_dump()
    return {"message": f"{profile.name} has {profile_dict.items()}"}


@app.post("/question/")
async def ask(question: Question):

    guidance_counselor = GuidanceCounselor(
        pdf_directory=os.getenv("COMET_HELPER_DATA_PATH"),
    )

    output = guidance_counselor.generate_answer(user_question=question.text)

    return {"Question": question.text, "Answer": output["answer"]}
