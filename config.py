from pydantic import BaseSettings
from ruamel.yaml import YAML
from pathlib import Path

BASE_PATH = Path("Data/leetcode_everyday")
CONFIG_PATH = BASE_PATH / "config.yml"
yaml = YAML()


class Config(BaseSettings):
    lce_hour = 8
    lce_subscriber = {}
    lce_admin = {}
    lce_size = {
        "width": 500,
        "height": 300
    }

    class Config:
        extra = "ignore"


def load_config():
    try:
        return yaml.load(CONFIG_PATH)
    except Exception:
        pass
    return None


async def save_config(config: Config):
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    yaml.dump(config.dict(), CONFIG_PATH)
