from fastapi import APIRouter
from config import settings
from pydantic import BaseModel, Field
from typing import Optional, Union
import httpx
import json

router = APIRouter()

BASE_URL = settings.BASE_URL + "people"

from cache import get_cache, set_cache, delete_cache

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
        if data == "homeworld":
            field_name = "planets"
            url = person_item.get(data)
            if url:
                try:
                    planet_id = int(url.rstrip('/').split('/')[-1])
                    cache_key = f"{field_name}/{planet_id}"
                    cached_data = await get_cache(cache_key)
                    if cached_data:
                        person_item[data] = json.loads(cached_data)
                    else:
                        planet_resp = await client.get(f"{settings.BASE_URL}{field_name}/{planet_id}")
                        if planet_resp.status_code == 200:
                            planet_data = planet_resp.json()
                            person_item[data] = planet_data
                            await set_cache(cache_key, json.dumps(planet_data), 60 * 60 * 24)
                except Exception:
                    pass 
        else:
            field_name = data
            urls = person_item.get(data, [])
            if urls is None:
                urls = []
            elif isinstance(urls, str):
                urls = [urls]
            detailed_data = []
            for url in urls:
                try:
                    data_id = int(url.rstrip('/').split('/')[-1])
                    cache_key = f"{field_name}/{data_id}"
                    cached_data = await get_cache(cache_key)
                    if cached_data:
                        detailed_data.append(json.loads(cached_data))
                    else:
                        data_resp = await client.get(f"{settings.BASE_URL}{field_name}/{data_id}")
                        if data_resp.status_code == 200:
                            response_data = data_resp.json()
                            detailed_data.append(response_data)
                            await set_cache(cache_key, json.dumps(response_data), 60 * 60 * 24)
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
        await get_detailed_data("homeworld", data, client)

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
        await validate_details(films, species, starships, vehicles, homeworld, {"results": [person_data]}, client)
        return person(**person_data)