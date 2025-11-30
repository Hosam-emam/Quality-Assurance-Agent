from dotenv import load_dotenv
load_dotenv()

from .configs.app_config import get_settings
settings = get_settings()

