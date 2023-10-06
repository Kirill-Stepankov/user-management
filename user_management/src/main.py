from fastapi import Depends, FastAPI
from logs.logger import get_logger
from typing_extensions import Annotated

from . import config

logger = get_logger()
app = FastAPI()


@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(config.get_settings)]):
    logger.warning("TEST")
    return {
        "app_name": settings.logger_config_path,
    }
