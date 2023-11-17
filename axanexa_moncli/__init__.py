import importlib

from .enums import *
from .config import *
from .error import *
from . import api_v2 as api
from . import entities as en, column_value as cv

api = importlib.import_module(f".api_{api_version}", package="moncli")

client = en.MondayClient()