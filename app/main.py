from starlette.responses import HTMLResponse

from app.config import config

# NB: do not add imports here!

from pathlib import Path
import os



# ...and here!!

if Path(__file__).parent == Path(os.getcwd()):
    config.root_dir = "."

# You can add imports from here...

from fastapi import FastAPI, Request #importa la classe FastAPI necessaria per creare l'applicazione web
from app.routers import frontend, events, users, registrations #prima c'era app.routers
#importa il modulo events che contiene un oggetto router definito con APIRouter
from app.routers.frontend import templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.data.db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on start
    init_database()
    yield
    # on close


app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=config.root_dir / "static"),
    name="static"
)
app.include_router(frontend.router)
app.include_router(events.router, tags=["events"]) #include il router definito in routers/events.py. Il campo tags è facoltativo ma è utile per la documentazione.
app.include_router(users.router, tags=["users"])
app.include_router(registrations.router, tags=["registrations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)


