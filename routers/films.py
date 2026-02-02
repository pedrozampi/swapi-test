from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional, Union
from config import settings
import httpx
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter()

BASE_URL = settings.BASE_URL + "films"

from cache import get_cache, set_cache, delete_cache

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
    if "results" in films_data:
        items = films_data["results"]
    else:
        items = [films_data]
    for film_item in items:
        urls = film_item.get(data, [])
        detailed_data = []
        for url in urls:
            try:
                data_id = int(url.rstrip('/').split('/')[-1])
                cache_key = f"{data}/{data_id}"
                cached_data = await get_cache(cache_key)
                logger.info(f"Cached data: {cached_data}")
                if cached_data:
                    detailed_data.append(json.loads(cached_data))
                else:
                    data_resp = await client.get(f"{settings.BASE_URL}{data}/{data_id}")
                    logger.info(f"Data response: {data_resp.json()}")
                    if data_resp.status_code == 200:
                        response_data = data_resp.json()
                        detailed_data.append(response_data)
                        await set_cache(cache_key, json.dumps(response_data), 60 * 60 * 24)
                    else:
                        detailed_data.append(url)
            except Exception as e:
                logger.error(f"Error processing {data} for URL {url}: {e}")
                detailed_data.append(url)
        film_item[data] = detailed_data

async def validate_details(species: bool, people: bool, starships: bool, vehicles: bool, planets: bool, data: dict, client: httpx.AsyncClient) -> bool:
    logger.info("Validating details")
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
        page: int = 1,
        order_by: str = "title",
        order_direction: str = "asc"
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

        if order_by:
            # Use getattr to access Pydantic model attributes
            response.results = sorted(response.results, key=lambda x: getattr(x, order_by, ""), reverse=order_direction == "desc")

        return response

@router.get("/films/{film_id}", tags=["films"], description="Get a film by ID", summary="Get a film by ID")
async def get_film(film_id: int, species: bool = False, people: bool = False, starships: bool = False, vehicles: bool = False, planets: bool = False) -> film:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{film_id}")
        film_data = response.json()
        await validate_details(species, people, starships, vehicles, planets, film_data, client)
        return film(**film_data)