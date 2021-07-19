from pydantic import BaseModel
from collections import Counter

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import spacy

import extract

nlp = spacy.load('ja_ginza')

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


class Item(BaseModel):
    token: str
    count: int


class Prop(BaseModel):
    text: str


@app.get('/hello')
async def hello():
    return {"message": "hello world!"}


@app.post('/tokenize')
async def tokenize(prop: Prop):
    return {prop.text: extract.tokenize(prop.text)}


@app.post('/upload')
async def extract_tokens(file: UploadFile = File(...)):
    extract.copy_file(file)
    prs = extract.get_presentation_obj(file.filename)
    extract.delete_file(file.filename)
    # text bpx reading
    tokens = []
    for slide in prs.slides:
        tokens += extract.read_text_box(slide)
    count_tokens = Counter(tokens)
    estimated_salary = extract.calculate_score(tokens)
    items = [Item(token=item[0], count=item[1]) for item in count_tokens.most_common(20)]
    return {"freq_items": items, "estimated_salary": estimated_salary}
