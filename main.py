from fastapi import FastAPI
from routers import auth, films, people, planets, species, starships, vehicles, favorites, comments

app = FastAPI(
    title="Star Wars API",
    description="API utilizando o swapi para teste técnico",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(films.router)
app.include_router(people.router)
app.include_router(planets.router)
app.include_router(species.router)
app.include_router(starships.router)
app.include_router(vehicles.router)
app.include_router(favorites.router)
app.include_router(comments.router)