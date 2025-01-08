from typing import List

from pydantic import BaseModel
from pydantic.v1 import NotNoneError


class Location(BaseModel):
    latitude: float
    longitude: float

class Image(BaseModel):
    url: str
    name: str

class ArtworkModel(BaseModel):
    MONA_id: int
    Wikidata_id: int | None
    title_fr: str
    title_en: str | None
    year: int
    location: Location
    urls: List[str] = []
    categories: List[str] = []
    producer: int | None
    source: int | None
    owner: int | None
    artists: List[int] = []

class ArtistModel(BaseModel):
    MONA_id: int
    label: str
    Wikidata_id: int | None
    ULAN_id: int | None
    is_collective: bool

class SPARQLModel(BaseModel):
    item: str
    title: str | None
    creator: str | None
    genre: str | None
    place: str | None
    arrondissement: str
    image: Image | None
    #TODO fix data type to point
    coordinates: str