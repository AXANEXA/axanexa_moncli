from dotenv import dotenv_values

# API version
#DEFAULT_API_VERSION = "v2"
DEFAULT_API_VERSION = "v10_2023"
env = dotenv_values()
if 'API_VERSION' in env:
    DEFAULT_API_VERSION = env['API_VERSION']   
     
api_version = DEFAULT_API_VERSION


# Supported date formats.
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
ZULU_FORMAT = '{}T{}.%fZ'

