from unittest.mock import patch
from nose.tools import ok_, eq_, raises

from moncli import MondayClient, entities as en

USERNAME = 'test.user@foobar.org' 
GET_ME_RETURN_VALUE = en.User(**{'creds': None, 'id': '1', 'email': USERNAME})

@patch.object(MondayClient, 'get_me')
@patch.object(MondayClient, 'get_updates')
def test_update_should_return_list_of_replies(get_updates, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [en.Update(creds=None, **{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]})]
    client = MondayClient(USERNAME, '', '')
    
    # Act
    updates = client.get_updates()
    
    # Assert
    ok_(updates != None)
    eq_(len(updates), 1)
    eq_(len(updates[0].replies), 1)

@patch.object(MondayClient, 'get_me')
@patch.object(MondayClient, 'get_updates')
@patch('moncli.api_v2.get_users')
def test_update_should_return_creator(get_users, get_updates, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [en.Update(creds=en.MondayClientCredentials('', ''), **{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]})]
    get_users.return_value = [GET_ME_RETURN_VALUE.to_primitive()]
    client = MondayClient(USERNAME, '', '')
    update = client.get_updates()[0]

    # Assert
    ok_(update != None)
    eq_(update.creator.to_primitive(), GET_ME_RETURN_VALUE.to_primitive())


@patch.object(MondayClient, 'get_me')
@patch.object(MondayClient, 'get_updates')
@patch('moncli.api_v2.get_users')
def test_update_should_return_creator_of_update_reply(get_users, get_updates, get_me):

    # Arrange
    get_me.return_value = GET_ME_RETURN_VALUE
    get_updates.return_value = [en.Update(creds=en.MondayClientCredentials('', ''), **{'id': '1', 'creator_id': '1', 'item_id': '1', 'replies': [{'id': '2', 'creator_id': '1'}]})]
    get_users.return_value = [GET_ME_RETURN_VALUE.to_primitive()]
    client = MondayClient(USERNAME, '', '')
    reply = client.get_updates()[0].replies[0]

    # Assert
    ok_(reply != None)
    eq_(reply.creator.to_primitive(), GET_ME_RETURN_VALUE.to_primitive())