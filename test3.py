
import axanexa_moncli
from axanexa_moncli import client
from axanexa_moncli import enums	
from axanexa_moncli.models import MondayModel
from axanexa_moncli.types import *
from axanexa_moncli.column_value import Person,Timeline
from datetime import datetime
import os

from dotenv import dotenv_values


def initaxanexa_moncli():
    #config=DataUtils.readConfig()
    env = dotenv_values()
    #axanexa_moncli.api=axanexa_moncli.api_v2   
    axanexa_moncli.api.api_key="eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMwMjExOTg2OCwiYWFpIjoxMSwidWlkIjo0ODM1NDQyMSwiaWFkIjoiMjAyMy0xMi0xMVQyMDo0NDo1NS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTQ1Mjk0ODYsInJnbiI6InVzZTEifQ.pnFcUdKiKqa8HBd0jpz3N0db3J-n7RZZKuvs35RELf0"
    axanexa_moncli.api.connection_timeout = 300

if __name__ == "__main__":
    initaxanexa_moncli()
    #client= axanexa_moncli.newclient()
    board = client.get_board(id='4947345806')
    #print(board)
   # print('client get_items----')
    #items = client.get_items(ids=['4947345806'])
    #print('board get_items----')

#old  - get_items
    
    


    as_model = {'id','text','value''type'}
    list_item_fields = 'id text value type column{id title} ...on MirrorValue{ display_value } ...on BoardRelationValue{ display_value }'
    print(list_item_fields)
    """
    field = 'items_page.items.column_values.id text value type column{id title} ...on MirrorValue{ display_value } ...on BoardRelationValue{ display_value }'
     #field_split = re.split(r'\.(?!\.\.\.)', field)
    field = field.replace('...','3DOTS')
    print("field",field)
    field_split = field.split('.')
    print("dot3_result",field_split)
   
    parent_field = field_split[0]
    child_fields = field_split[1:] 
    modified_list = [string.replace('3DOTS','...') for string in child_fields]
    child_fields = modified_list
    """
    items=board.get_items(True,items_page={"limit":5} , max_pages=2)   
    print(items)
    if not items:
        #get first item
        item=items[0]
        #get column named 
        column=item.get_column_value(title="Project Master")
        
        if column:
            #change the value of column to "hello" 
            #column.value=[Person(37504458)]
            #column.value=100
            #column.value =  Timeline(datetime(2023, 11, 1), datetime(2023, 12, 31))
            column.value =  [4929471673]
            #update the item
            item.change_multiple_column_values(column_values=[column])
            print(column)
        print(items)
""" 
# new - get_items_page_by_column_values
column_id = 'person'
column_values1=['John Hu','Triet Phan']
#temp = '{}: \"{}\"'.format(column_id, column_values)
items_col_values = board.get_items_page_by_column_values(column_id,column_values1,True,limit=100)
print(items_col_values)
print("get_items_page_by_column_values size",len(items_col_values))

#old  - get_items_by_column_values
column_id = 'person'
column_value = board.get_column_value(column_id)
column_value.text = 'John Hu'
items = board.get_items_by_column_values(column_value,True,limit=100)
print(items)
print("get_items_by_column_values size",len(items))

# old - get_items_by_multiple_column_values
column_name = 'Person'
column = board.columns[column_name]
items = board.get_items_by_multiple_column_values(column, ['John Hu', 'Triet Phan'], True,limit=100)
print(items)
print("get_items_by_multiple_column_values size",len(items))
  #  items_col_values = board.get_items_by_column_values(column_title='Project Master', column_value='hello')



multi_columns = [{'column_id': 'person', 'column_values': column_values1}, {'column_id': 'numbers', 'column_values': ['18']}]
items = board.get_items_page_by_multi_column_values(multi_columns,True,limit=100)
print(items)
print("get_items_page_by_multi_column_values size",len(items))
 """ 


print("Completed!!!")
