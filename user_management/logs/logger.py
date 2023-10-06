import logging.config

import yaml


def get_logger():
    with open(
        "user_management/logs/logging_config.yaml",
        "rt",
    ) as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    return logging.getLogger("development")
