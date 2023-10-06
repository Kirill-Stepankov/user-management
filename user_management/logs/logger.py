import logging.config

import yaml
from src.config import get_settings


def get_logger():
    settings = get_settings()
    with open(
        settings.logger_config_path,
        "rt",
    ) as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    return logging.getLogger("development")
