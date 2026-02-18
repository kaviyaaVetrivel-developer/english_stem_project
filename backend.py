from fastapi import FastAPI
from pydantic import BaseModel
from nltk.corpus import wordnet as wn
import nltk
from nltk import pos_tag
from nltk.corpus import cmudict

app = FastAPI()

# Pronunciation dictionary
d = cmudict.dict()

class WordRequest(BaseModel):
    word: str

# Get pronunciation
def get_pronunciation(word):
    word = word.lower()
    if word in d:
        return " ".join(d[word][0])
    return "Not found"

# Generate terminology using WordNet
def generate_terminology(word):
    synsets = wn.synsets(word)

    if not synsets:
        return []

    results = []

    for syn in synsets:

        pos_map = {
        "n": "Noun",
        "v": "Verb",
        "a": "Adjective",
        "r": "Adverb"
    }

    pos_name = pos_map.get(syn.pos(), "Other")

    terminology.append({
        "part_of_speech": pos_name,   # ✅ ADD THIS
        "definition": syn.definition(),
        "examples": syn.examples(),
        "synonyms": syn.lemma_names(),
        "hypernyms": [h.name() for h in syn.hypernyms()],
        "hyponyms": [h.name() for h in syn.hyponyms()]
    })


    return results


@app.post("/generate")
def generate(request: WordRequest):

    word = request.word.lower()

    pronunciation = "Not found"
    if word in d:
        pronunciation = " ".join(d[word][0])

    synsets = wn.synsets(word)

    terminology = []

    for syn in synsets:

        pos_map = {
            "n": "Noun",
            "v": "Verb",
            "a": "Adjective",
            "r": "Adverb"
        }

        pos_name = pos_map.get(syn.pos(), "Other")

        terminology.append({
            "part_of_speech": pos_name,
            "definition": syn.definition(),
            "examples": syn.examples(),
            "synonyms": syn.lemma_names(),
            "hypernyms": [h.name().split('.')[0] for h in syn.hypernyms()],
            "hyponyms": [h.name().split('.')[0] for h in syn.hyponyms()]

        })

    return {
        "word": word,
        "pronunciation": pronunciation,
        "terminology": terminology
    }
