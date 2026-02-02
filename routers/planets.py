from fastapi import APIRouter
from config import settings
from pydantic import BaseModel, Field
from typing import Optional, Union
import httpx
import json

from cache import get_cache, set_cache, delete_cache

router = APIRouter()

BASE_URL = settings.BASE_URL + "planets"

class planet(BaseModel):
    name: str = Field(default=None)
    rotation_period: Optional[Union[int, str]] = None
    orbital_period: Optional[Union[int, str]] = None
    diameter: Optional[Union[int, str]] = None
    climate: str = Field(default=None)
    gravity: str = Field(default=None)
    terrain: str = Field(default=None)
    surface_water: Optional[Union[int, str]] = None
    population: Optional[Union[int, str]] = None
    residents: Optional[list[Union[str, dict]]] = None
    films: Optional[list[Union[str, dict]]] = None
    created: str = Field(default=None)
    edited: str = Field(default=None)
    url: str = Field(default=None)

class search_planets(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[list[planet]] = None

async def get_detailed_data(data: str, planets_data: dict, client: httpx.AsyncClient) -> dict:
    if "results" in planets_data:
        items = planets_data["results"]
    else:
        items = [planets_data]
    for planet_item in items:
        if data == "residents":
            field_name = "people"
        else:
            field_name = data
        urls = planet_item.get(data)
        if isinstance(urls, str):
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
        planet_item[data] = detailed_data

async def validate_details(residents: bool, films: bool, planets_data: dict, client: httpx.AsyncClient) -> dict:
    if residents:
        await get_detailed_data("residents", planets_data, client)
    if films:
        await get_detailed_data("films", planets_data, client)

@router.get("/planets", tags=["planets"], description="Get all planets or search by name", summary="Get all planets")
async def get_planets(search: str = None, residents: bool = False, films: bool = False, n: int = 10, page: int = 1, order_by: str = "name", order_direction: str = "asc") -> search_planets:
    if search:
        url = f"{BASE_URL}?search={search}"
    else:
        url = BASE_URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        planets_data = response.json()
        await validate_details(residents, films, planets_data, client)
        response = search_planets(**planets_data)
        if response.results:
            start_idx = (page - 1) * n
            end_idx = page * n
            response.results = response.results[start_idx:end_idx]
        if order_by:
            response.results = sorted(response.results, key=lambda x: getattr(x, order_by, ""), reverse=order_direction == "desc")
        return response

@router.get("/planets/{planet_id}", tags=["planets"])
async def get_planet(planet_id: int, residents: bool = False, films: bool = False) -> planet:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{planet_id}")
        planets_data = response.json()
        await validate_details(residents, films, planets_data, client)
        return planet(**planets_data)