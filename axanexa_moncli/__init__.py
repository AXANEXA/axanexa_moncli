import importlib

from .enums import *
from .config import *
from .error import *
#ver = "v10_2023"
api = importlib.import_module(f".api_{api_version}", package="axanexa_moncli")

#from . import api_v2 as api
from . import entities as en, column_value as cv

client = en.MondayClient()