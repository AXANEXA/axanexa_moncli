try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Moncli, a pythonic/DDD client for Monday.com. Maintained by Axanexa.',
    'author': 'Axanexa',
    'url': r'https://github.com/AXANEXA/axanexa_moncli',
    'download_url': r'https://github.com/AXANEXA/axanexa_moncli',
    'author_email': 'tphan@axanexa.com',
    'version': '1.0.0',
    'license': 'BSD 3',
    'install_requires': [
        'requests>=2.24.0',
        'pytz>=2020.1',
        'pycountry>=20.7.3',
        'deprecated>=1.2.10',
        'schematics>=2.1.0'
    ],
    'tests_require': [
        'nose>=1.3.7'
    ],
    'packages': [
        'axanexa_moncli',
        'axanexa_moncli.api_v1',
        'axanexa_moncli.api_v2',
        'axanexa_moncli.entities',
        'axanexa_moncli.column_value'
    ],
    'scripts': [],
    'name': 'axanexa_moncli'
}

setup(**config)
