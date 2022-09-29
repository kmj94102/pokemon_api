# coding: utf-8
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from db import Base
from db import ENGINE
from typing import List

class PokemonTable(Base):
    __tablename__ = 'pokemon'
    index = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(45))
    name = Column(String(45))
    status = Column(String(45))
    classification = Column(String(45))
    characteristic = Column(String(45))
    attribute = Column(String(45))
    dotImage = Column(String(500))
    dotShinyImage = Column(String(500))
    image = Column(String(500))
    shinyImage = Column(String(500))
    description = Column(String(500))
    generation = Column(Integer)

class ArecuesDexTable(Base):
    __tablename__ = 'arceusDex'
    index = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(45))
    allDexNumber = Column(String(45))
    name = Column(String(45))
    status = Column(String(45))
    classification = Column(String(45))
    characteristic = Column(String(45))
    attribute = Column(String(45))
    dotImage = Column(String(500))
    dotShinyImage = Column(String(500))
    image = Column(String(500))
    shinyImage = Column(String(500))
    description = Column(String(500))
    generation = Column(Integer)

class EvolutionTable(Base):
    __tablename__ = 'evolution'
    index = Column(Integer, primary_key=True, autoincrement=True)
    numbers = Column(String(100))
    beforeNum = Column(String(45))
    afterNum = Column(String(45))
    evolutionType = Column(String(100))
    evolutionConditions = Column(String(100))

class EvolutionTypeTable(Base):
    __tablename__ = 'evolutionType'
    index = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    image = Column(String(700))

class CharacteristicTable(Base):
    __tablename__ = 'characteristic'
    index = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    description = Column(String(45))

class Pokemon(BaseModel):
    index : int = None
    number: str = None
    name : str = None
    status : str = None
    classification : str = None
    characteristic : str = None
    attribute : str = None
    dotImage : str = None
    dotShinyImage : str = None
    image : str = None
    shinyImage : str = None
    description : str = None
    generation : int = None

class ArcuesDex(BaseModel):
    index : int = None
    number: str = None
    allDexNumber: str = None
    name : str = None
    status : str = None
    classification : str = None
    characteristic : str = None
    attribute : str = None
    dotImage : str = None
    dotShinyImage : str = None
    image : str = None
    shinyImage : str = None
    description : str = None
    generation : int = None

class Evolution(BaseModel):
    index : int = None
    numbers : str = None
    beforeNum : str = None
    afterNum : str = None
    evolutionType : str = None
    evolutionConditions : str = None

class EvolutionType(BaseModel):
    index : int = None
    name : str = None
    image : str = None
    
class Characteristic(BaseModel):
    index : int = None
    name : str = None
    description : str = None

class SearchInfo(BaseModel):
    generations: List[int] = None
    searchText: str = None

class NewDexItem(BaseModel):
    number: str = None
    allDexNumber: str = None
    type: str = None

class SelectInfo(BaseModel):
    startNum: str = None
    endNum: str = None

def main():
    # Table 없으면 생성
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main()
