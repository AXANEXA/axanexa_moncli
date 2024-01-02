import json
import types

from schematics.models import Model
from schematics.types import StringType
from datetime import datetime
from axanexa_moncli.config import DATE_FORMAT, TIME_FORMAT

from .. import api, entities as en, models as m, error as e, column_value as cv
from ..error import ItemError
from ..models import MondayModel


class ItemsPage(MondayModel):
    """The entity model for a board
    
    Properties
    
    cursor : `str`
             An opaque cursor that represents the position in the list after the last returned item. Use this cursor for pagination to fetch the next set of items. 
             If the cursor is null, there are no more items to fetch.
     items : `list[moncli.entities.Item]`
                The board's items (rows),The cursor's corresponding item."""
    
    def __init__(self, **kwargs):
       # super().__init__(**kwargs)
        self.__items = kwargs.pop('__items', None)
        self._cursor = kwargs.pop('__cursor', None)

        cursor = kwargs.pop('cursor', None)
        items = kwargs.pop('items', None)

        #super(ItemsPage, self).__init__(kwargs)

        if items and not self.__items:
            self.__items = [en.Item(**item) for item in items]


    @property
    def items(self):
        """Retrieve board items"""

        if not self.__items:
            self.__items = self.get_items()
        return self.__items
    