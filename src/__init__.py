"""
poop
"""
from clank.config import app_config
from clank.models.base_model import BaseModel

# Initialize shared resources
base_model = BaseModel(app_config["base_model_path"])
