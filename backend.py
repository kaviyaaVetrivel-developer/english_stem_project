from fastapi import FastAPI
from pydantic import BaseModel
from nltk.corpus import wordnet as wn

app = FastAPI()

class WordRequest(BaseModel):
    word: str

def generate_terminology(word):
    synsets = wn.synsets(word)

    if not synsets:
        return {"error": "No terminology found"}

    results = []

    for syn in synsets:
        terminology = {
            "definition": syn.definition(),
            "examples": syn.examples(),
            "synonyms": list(set(lemma.name() for lemma in syn.lemmas())),
            "hypernyms": [h.name().split('.')[0] for h in syn.hypernyms()],
            "hyponyms": [h.name().split('.')[0] for h in syn.hyponyms()]
        }
        results.append(terminology)

    return results


@app.post("/generate")
def generate(data: WordRequest):
    return {"word": data.word, "terminology": generate_terminology(data.word)}