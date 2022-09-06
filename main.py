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


# ----------API 정의------------
# 포켓몬 리스트 조회
@app.get("/pokemons/{generation}")
async def read_pokemons(generation: str):
    session.commit()
    if(generation == "all") :
        pokemons = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage).all()
    else :
        pokemons = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage).filter(PokemonTable.generation == generation).all()

    # pokemons = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage).order_by(PokemonTable.number.desc()).all()
    # pokemons = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage).all()
    return pokemons

@app.post("/pokemons/search")
async def read_search_pokemons(item: SearchInfo):
    # generationTuple = tuple(item.generations)

    query = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage, PokemonTable.attribute)\
        .filter(PokemonTable.generation.in_(item.generations), PokemonTable.name.like(f"%{item.searchText}%"))

    pokemons = query.all()
    return pokemons


# 포켓몬 등록
@app.post("/pokemon")
async def create_pokemon(item: Pokemon):

    pokemon = PokemonTable()
    pokemon.number = item.number
    pokemon.name = item.name
    pokemon.status = item.status
    pokemon.classification = item.classification
    pokemon.characteristic = item.characteristic
    pokemon.attribute = item.attribute
    pokemon.dotImage = item.dotImage
    pokemon.dotShinyImage = item.dotShinyImage
    pokemon.image = item.image
    pokemon.shinyImage = item.shinyImage
    pokemon.description = item.description
    pokemon.generation = item.generation

    session.add(pokemon)
    session.commit()

    return f"{item.name} 추가 완료"

# 특정 포켓몬 정보 조회 (번호)
@app.get("/pokemon/number/{number}")
def read_pokemon(number: str):
    pokemon = session.query(PokemonTable).filter(PokemonTable.number == number).first()
    beforInfo = read_pokemon_dot_image(pokemon.index -1)
    after = read_pokemon_dot_image(pokemon.index + 1)
    pokemon1 = aliased(PokemonTable)
    pokemon2 = aliased(PokemonTable)
    evolution = session.query(pokemon1.dotImage.label('beforeDot'), pokemon1.dotShinyImage.label('beforeShinyDot'), pokemon2.dotImage.label('afterDot'), pokemon2.dotShinyImage.label('afterShinyDot'), EvolutionTypeTable.image.label('evolutionImage'), EvolutionTable.evolutionConditions)\
        .filter(EvolutionTable.numbers.like(f"%{number}%"), EvolutionTable.beforeNum == pokemon1.number, EvolutionTable.afterNum == pokemon2.number, EvolutionTypeTable.name == EvolutionTable.evolutionType).all()

    return {"info": pokemon, "before": beforInfo, "after": after, "evolution": evolution}

# 특정 포켓몬 이미지 정보 조회 (인덱스)
@app.get("/pokemon/number/image/index/{index}")
def read_pokemon_dot_image(index: int):
    pokemon = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage, PokemonTable.attribute).filter(PokemonTable.index == index).first()

    return pokemon

# 특정 포켓몬 이미지 정보 조회 (번호)
@app.get("/pokemon/number/image/{number}")
def read_pokemon_dot_image_to_nußmber(number: str):
    pokemon = session.query(PokemonTable.number, PokemonTable.name, PokemonTable.dotImage, PokemonTable.dotShinyImage, PokemonTable.attribute).filter(PokemonTable.number == number).first()

    return pokemon

# 특성 등록
@app.post("/char")
async def create_characteristic(item: Characteristic):
    result = item.name
    char = session.query(CharacteristicTable).filter(CharacteristicTable.name == item.name).first()
    if(char is None):
        charTable = CharacteristicTable()
        charTable.name = item.name
        charTable.description = item.description
        session.add(charTable)
        session.commit()
        result = f"{item.name} 추가완료"
    else:
        result = f"{item.name} 이미 추가된 특성입니다."
    return result

# 진화 타입 등록
@app.post("/evolution/type")
async def create_evolution_type(item: EvolutionType):
    type = EvolutionTypeTable()
    type.name = item.name
    type.image = item.image
    
    result = ""
    before = session.query(EvolutionTypeTable).filter(EvolutionTypeTable.name == item.name).first()
    if(before is None):
        session.add(type)
        session.commit()
        result = f"{item.name} 추가완료"
    else:
        result = f"{item.name}은 이미 등록되어있습니다."

    return result

# 진화 타입 조회
@app.get("/evolution/type")
async def read_evolution_types():
    session.commit()
    return session.query(EvolutionTypeTable.name).order_by(EvolutionTypeTable.name).all()

# 진화 등록
@app.post("/evolution")
def create_evolution(item: Evolution, index: int):
    evolution = EvolutionTable()
    evolution.numbers = item.numbers
    evolution.beforeNum = item.beforeNum
    evolution.afterNum = item.afterNum
    evolution.evolutionType = item.evolutionType
    evolution.evolutionConditions = item.evolutionConditions

    result = ""
    before = session.query(EvolutionTable).filter(EvolutionTable.afterNum == item.afterNum and EvolutionTable.beforeNum == item.beforeNum).first()
    if(before is None):
        session.add(evolution)
        session.commit()
        result = f"{index} 등록에 성공하였습니다.\n"
    else:
        result = f"{index} 등록에 실패하였습니다.\n"

    return result

@app.post("/evolutions")
async def create_evolution_list(items: List[Evolution]):
    result = ""
    for index, item in enumerate(items):
        result += create_evolution(item, index)

    return result

@app.post("/test")
async def test():

    return result   