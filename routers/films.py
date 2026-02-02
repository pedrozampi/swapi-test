from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Union
from config import settings
import httpx
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)
router = APIRouter()

BASE_URL = settings.BASE_URL + "films"

class film(BaseModel):
    title: str = Field(default=None)
    episode_id: int = Field(default=None)
    opening_crawl: str = Field(default=None)
    director: str = Field(default=None)
    producer: str = Field(default=None)
    release_date: str = Field(default=None)
    characters: Optional[list[Union[str, dict]]] = None
    people: Optional[list[Union[str, dict]]] = None
    starships: Optional[list[Union[str, dict]]] = None
    vehicles: Optional[list[Union[str, dict]]] = None
    planets: Optional[list[Union[str, dict]]] = None
    species: Optional[list[Union[str, dict]]] = None
    created: str = Field(default=None)
    edited: str = Field(default=None)
    url: str = Field(default=None)

class search_films(BaseModel):
    count: Optional[int] = None
    next: Optional[str] = None
    previous: Optional[str] = None
    results: Optional[list[film]] = None

async def get_detailed_data(data: str, films_data: dict, client: httpx.AsyncClient) -> dict:
        results = films_data.get("results", [])
        for film_item in results:
            urls = film_item.get(data, [])
            detailed_species = []
            for url in urls:
                try:
                    species_id = int(url.rstrip('/').split('/')[-1])
                    species_resp = await client.get(f"{settings.BASE_URL}{data}/{species_id}")
                    if species_resp.status_code == 200:
                        detailed_species.append(species_resp.json())
                    else:
                        detailed_species.append(url)
                except Exception:
                    detailed_species.append(url)
            film_item[data] = detailed_species

async def validate_details(species: bool, people: bool, starships: bool, vehicles: bool, planets: bool, data: dict, client: httpx.AsyncClient) -> bool:
    if species:
        await get_detailed_data("species", data, client)
    if people:
        await get_detailed_data("characters", data, client)
    if starships:
        await get_detailed_data("starships", data, client)
    if vehicles:
        await get_detailed_data("vehicles", data, client)
    if planets:
        await get_detailed_data("planets", data, client)



@router.get("/films", tags=["films"], description="Get all films or search by title", summary="Get all films")
async def get_films(
        search: str = None, 
        species: bool = False, 
        people: bool = False, 
        starships: bool = False, 
        vehicles: bool = False, 
        planets: bool = False,
        n: int = 10,
        page: int = 1
    ) -> search_films:
    if search:
        url = f"{BASE_URL}?search={search}"
    else:
        url = BASE_URL
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        films_data = response.json()

        await validate_details(species, people, starships, vehicles, planets, films_data, client)

        response = search_films(**films_data)
        if response.results:
            start_idx = (page - 1) * n
            end_idx = page * n
            response.results = response.results[start_idx:end_idx]

        return response

@router.get("/films/{film_id}", tags=["films"], description="Get a film by ID", summary="Get a film by ID")
async def get_film(film_id: int, species: bool = False, people: bool = False, starships: bool = False, vehicles: bool = False, planets: bool = False) -> film:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{film_id}")
        film_data = response.json()
        await validate_details(species, people, starships, vehicles, planets, film_data, client)
        return film(**film_data)