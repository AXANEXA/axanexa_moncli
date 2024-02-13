import axanexa_moncli
from axanexa_moncli import client
from axanexa_moncli import enums	
from axanexa_moncli.models import MondayModel
from axanexa_moncli.types import *
import os

from dotenv import dotenv_values


def initaxanexa_moncli():
    #config=DataUtils.readConfig()
    env = dotenv_values()
    axanexa_moncli.api.api_key="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwMjExOTg2OCwiYWFpIjoxMSwidWlkIjo0ODM1NDQyMSwiaWFkIjoiMjAyMy0xMi0xMVQyMDo0NDo1NS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQ1Mjk0ODYsInJnbiI6InVzZTEifQ.pnFcUdKiKqa8HBd0jpz3N0db3J-n7RZZKuvs35RELf0"
    axanexa_moncli.api.connection_timeout = 300

if __name__ == "__main__":
    initaxanexa_moncli()
    board = client.get_board(id='5512650713')
    print(board)