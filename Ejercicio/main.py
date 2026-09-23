import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

from database import db
from vistas import router as vistas_router

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise RuntimeError("No se encontró DATABASE_URL en el archivo .env")

    await db.connect(db_url)

    yield

    await db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(vistas_router)