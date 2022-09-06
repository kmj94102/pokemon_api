from cgitb import reset
from inspect import Attribute
import logging
from operator import attrgetter, index
from unittest import result

from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import aliased
from itertools import combinations

from db import session
from model import PokemonTable, Pokemon, EvolutionTable, Evolution, EvolutionTypeTable, EvolutionType, CharacteristicTable, Characteristic, SearchInfo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return "개인 서버 생성"