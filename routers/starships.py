from fastapi import APIRouter
from config import settings
from pydantic import BaseModel, Field
from typing import Optional, Union
import httpx

router = APIRouter()

BASE_URL = settings.BASE_URL + "starships"

class starship(BaseModel):
    name: str = Field(default=None)
    model: str = Field(default=None)
    manufacturer: str = Field(default=None)
    cost_in_credits: Optional[Union[int, str]] = None
    length: Optional[Union[int, str]] = None
    max_atmosphering_speed: Optional[Union[int, str]] = None
    crew: Optional[Union[int, str]] = None
    passengers: Optional[Union[int, str]] = None
    cargo_capacity: Optional[Union[int, str]] = None
    consumables: str = Field(default=None)
    films: Optional[list[Union[str, dict]]] = None
    pilots: Optional[list[Union[str, dict]]] = None
    created: str = Field(default=None)
    edited: str = Field(default=None)
    url: str = Field(default=None)

class search_starships(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[list[starship]] = None

async def get_detailed_data(data: str, starships_data: dict, client: httpx.AsyncClient) -> dict:
    if "results" in starships_data:
        items = starships_data["results"]
    else:
        items = [starships_data]
    for starship_item in items:
        urls = starship_item.get(data, [])
        if urls is None:
            urls = []
        elif isinstance(urls, str):
            urls = [urls]
        detailed_data = []
        if data == "pilots":
            field_name = "people"
        else:
            field_name = data
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
        starship_item[data] = detailed_data

async def validate_details(films: bool, pilots: bool, starships_data: dict, client: httpx.AsyncClient) -> dict:
    if films:
        await get_detailed_data("films", starships_data, client)
    if pilots:
        await get_detailed_data("pilots", starships_data, client)

@router.get("/starships", tags=["starships"], description="Get all starships or search by name or model", summary="Get all starships")
async def get_starships(search: str = None, films: bool = False, pilots: bool = False, n: int = 10, page: int = 1) -> search_starships:
    if search:
        url = f"{BASE_URL}?search={search}"
    else:
        url = BASE_URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        starships_data = response.json()
        await validate_details(films, pilots, starships_data, client)
        response = search_starships(**starships_data)
        if response.results:
            start_idx = (page - 1) * n
            end_idx = page * n
            response.results = response.results[start_idx:end_idx]
        return response

@router.get("/starships/{starship_id}", tags=["starships"], description="Get a starship by ID", summary="Get a starship by ID")
async def get_starship(starship_id: int, films: bool = False, pilots: bool = False) -> starship:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{starship_id}")
        starship_data = response.json()
        await validate_details(films, pilots, starship_data, client)
        return starship(**starship_data)