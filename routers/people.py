from fastapi import APIRouter
from config import settings
from pydantic import BaseModel, Field
from typing import Optional, Union
import httpx

router = APIRouter()

BASE_URL = settings.BASE_URL + "people"

class person(BaseModel):
    name: str = Field(default=None)
    height: int = Field(default=None)
    mass: int = Field(default=None)
    hair_color: str = Field(default=None)
    skin_color: str = Field(default=None)
    eye_color: str = Field(default=None)
    birth_year: str = Field(default=None)
    gender: str = Field(default=None)
    homeworld: Optional[Union[str, dict]] = None
    films: Optional[list[Union[str, dict]]] = None
    species: Optional[list[Union[str, dict]]] = None
    vehicles: Optional[list[Union[str, dict]]] = None
    starships: Optional[list[Union[str, dict]]] = None
    created: str = Field(default=None)
    edited: str = Field(default=None)
    url: str = Field(default=None)

class search_people(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[list[person]] = None

async def get_detailed_data(data: str, people_data: dict, client: httpx.AsyncClient) -> dict:
    if "results" in people_data:
        items = people_data["results"]
    else:
        items = [people_data]
    
    for person_item in items:
        if data == "planets":
            field_name = "homeworld"
            url = person_item.get(field_name)
            if url:
                try:
                    planet_id = int(url.rstrip('/').split('/')[-1])
                    planet_resp = await client.get(f"{settings.BASE_URL}planets/{planet_id}")
                    if planet_resp.status_code == 200:
                        person_item[field_name] = planet_resp.json()
                except Exception:
                    pass
        else:
            urls = person_item.get(data, [])
            if isinstance(urls, str):
                urls = [urls]
            detailed_data = []
            for url in urls:
                try:
                    data_id = int(url.rstrip('/').split('/')[-1])
                    data_resp = await client.get(f"{settings.BASE_URL}{data}/{data_id}")
                    if data_resp.status_code == 200:
                        detailed_data.append(data_resp.json())
                    else:
                        detailed_data.append(url)
                except Exception:
                    detailed_data.append(url)
            person_item[data] = detailed_data
    
async def validate_details(films: bool, species: bool, starships: bool, vehicles: bool, homeworld: bool, data: dict, client: httpx.AsyncClient) -> dict:
    if films:
        await get_detailed_data("films", data, client)
    if species:
        await get_detailed_data("species", data, client)
    if starships:
        await get_detailed_data("starships", data, client)
    if vehicles:
        await get_detailed_data("vehicles", data, client)
    if homeworld:
        await get_detailed_data("planets", data, client)

@router.get("/people", tags=["people"], description="Get all people or search by name", summary="Get all people")
async def get_people(search: str = None, films: bool = False, species: bool = False, starships: bool = False, vehicles: bool = False, homeworld: bool = False, n: int = 10, page: int = 1) -> search_people:
    if search:
        url = f"{BASE_URL}?search={search}"
    else:
        url = BASE_URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        people_data = response.json()
        await validate_details(films, species, starships, vehicles, homeworld, people_data, client)
        response = search_people(**people_data)
        if response.results:
            start_idx = (page - 1) * n
            end_idx = page * n
            response.results = response.results[start_idx:end_idx]
        return response

@router.get("/people/{person_id}", tags=["people"], description="Get a person by ID", summary="Get a person by ID")
async def get_person(person_id: int, films: bool = False, species: bool = False, starships: bool = False, vehicles: bool = False, homeworld: bool = False) -> person:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{person_id}")
        person_data = response.json()
        await validate_details(films, species, starships, vehicles, homeworld, person_data, client)
        return person(**person_data)