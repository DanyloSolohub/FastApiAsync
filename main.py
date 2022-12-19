import os
import time

from src.settings.routes import api_v1_router
from src.settings.config import configuration

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

os.environ['TZ'] = configuration.TIMEZONE
time.tzset()


def get_application() -> FastAPI:
    application = FastAPI(
        title=configuration.TITLE,
        description=configuration.DESCRIPTION,
        debug=configuration.DEBUG,
        # docs_url=os.getenv('SWAGGER_URL', None),
        # redoc_url=None,
    )
    application.include_router(api_v1_router, prefix=configuration.API_V1_STR)
    return application


app = get_application()


@app.get('/')
def main():
    return {'status': 'alive'}
