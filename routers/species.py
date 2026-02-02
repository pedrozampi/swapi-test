from fastapi import APIRouter
from config import settings
from pydantic import BaseModel, Field
from typing import Optional, Union
import httpx
import json
from cache import get_cache, set_cache, delete_cache

router = APIRouter()

BASE_URL = settings.BASE_URL + "species"

class species(BaseModel):
    name: str = Field(default=None)
    classification: str = Field(default=None)
    designation: str = Field(default=None)
    average_height: Optional[Union[int, str]] = None
    average_lifespan: Optional[Union[int, str]] = None
    eye_colors: str = Field(default=None)
    hair_colors: str = Field(default=None)
    skin_colors: str = Field(default=None)
    language: str = Field(default=None)
    homeworld: Optional[Union[str, dict]] = None
    films: Optional[list[Union[str, dict]]] = None
    people: Optional[list[Union[str, dict]]] = None
    created: str = Field(default=None)
    edited: str = Field(default=None)
    url: str = Field(default=None)

class search_species(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[list[species]] = None


async def get_detailed_data(data: str, species_data: dict, client: httpx.AsyncClient) -> dict:
    if "results" in species_data:
        items = species_data["results"]
    else:
        items = [species_data]
    
    for species_item in items:
        if data == "homeworld":
            field_name = "homeworld"
            url = species_item.get(field_name)
            if url:
                try:
                    planet_id = int(url.rstrip('/').split('/')[-1])
                    cache_key = f"planets/{planet_id}"
                    cached_data = await get_cache(cache_key)
                    if cached_data:
                        species_item[field_name] = json.loads(cached_data)
                    else:
                        planet_resp = await client.get(f"{settings.BASE_URL}planets/{planet_id}")
                        if planet_resp.status_code == 200:
                            species_item[field_name] = planet_resp.json()
                            await set_cache(cache_key, json.dumps(planet_resp.json()), 60 * 60 * 24)
                        else:
                            species_item[field_name] = url
                except Exception:
                    pass
        else:
            field_name = data
            urls = species_item.get(data, [])
            if urls is None:
                urls = []
            elif isinstance(urls, str):
                urls = [urls]
            detailed_data = []
            for url in urls:
                try:
                    data_id = int(url.rstrip('/').split('/')[-1])
                    data_resp = await client.get(f"{settings.BASE_URL}{field_name}/{data_id}")
                    if data_resp.status_code == 200:
                        detailed_data.append(data_resp.json())
                    else:
                        detailed_data.append(url)
                except Exception:
                    detailed_data.append(url)
            species_item[field_name] = detailed_data

async def validate_details(homeworld: bool, films: bool, people: bool, species_data: dict, client: httpx.AsyncClient) -> dict:
    if homeworld:
        await get_detailed_data("homeworld", species_data, client)
    if films:
        await get_detailed_data("films", species_data, client)
    if people:
        await get_detailed_data("people", species_data, client)

@router.get("/species", tags=["species"], description="Get all species or search by name", summary="Get all species")
async def get_species(search: str = None, homeworld: bool = False, films: bool = False, people: bool = False, n: int = 10, page: int = 1, order_by: str = "name", order_direction: str = "asc") -> search_species:
    if search:
        url = f"{BASE_URL}?search={search}"
    else:
        url = BASE_URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        species_data = response.json()
        await validate_details(homeworld, films, people, species_data, client)
        response = search_species(**species_data)
        if response.results:
            start_idx = (page - 1) * n
            end_idx = page * n
            response.results = response.results[start_idx:end_idx]
        if order_by:
            response.results = sorted(response.results, key=lambda x: getattr(x, order_by, ""), reverse=order_direction == "desc")
        return response

@router.get("/species/{species_id}", tags=["species"], description="Get a species by ID", summary="Get a species by ID")
async def get_species(species_id: int, homeworld: bool = False, films: bool = False, people: bool = False) -> species:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{species_id}")
        species_data = response.json()
        await validate_details(homeworld, films, people, species_data, client)
        return species(**species_data)