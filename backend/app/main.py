from fastapi import FastAPI
from app.dependencies.cors import setup_cors
from app.core.lifespan import lifespan
from app.api.v1.api import api_v1_router
from app.core.auth import init_auth
from app.core.openapi import custom_openapi
from fastapi.staticfiles import StaticFiles

app = FastAPI(lifespan=lifespan)

setup_cors(app)

app.state.auth = init_auth(app)

app.include_router(api_v1_router, prefix="/api/v1")

app.openapi = lambda: custom_openapi(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
