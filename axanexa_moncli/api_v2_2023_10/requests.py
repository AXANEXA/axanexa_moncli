import requests, json, time

from . import MondayApiError
from .graphql import *
from .constants import *
import re

def execute_query(timeout: int = None, **kwargs):
    """Executes a graphql query via Rest.
    
        Parameters

            timeout : `int`
                The default timeout for Rest requests.
            kwargs : `dict`
                Optional keyword arguments

        Returns
        
            data : `dict`
                Response data in dictionary form.

        Optional Arguments

            api_key : `str`
                The monday.com API v2 user key.
            operation : `moncli.api_v2.graphql.GraphQLOperation`
                Perform request with input graphql operation.
            query_name: `str`:
                The name of the query to execute.
            operation_type: `moncli.api_v2.graphql.OperationType`:
                The type of graphql operation to perform (QUERY or MUTATION).
            fields: `list[str]`:
                List of fields to return.
            arguments: `dict`:
                Additional graphql arguments.
            query : `str`
                Perform request with raw graphql query string.
            variables : `dict`
                Variables added to the query.
    """

    api_key = kwargs.pop('api_key', None)
    if not api_key:
        from . import api_key

    if not timeout:
        from . import connection_timeout
        timeout = connection_timeout

    query_name = kwargs.pop('query_name', None)
    operation_type = kwargs.pop('operation_type', None)
    fields = kwargs.pop('fields', ())
    arguments = kwargs.pop('arguments', {})
    query = kwargs.pop('query', None)
    variables = kwargs.pop('variables', None)
    include_complexity = kwargs.pop('include_complexity', False)

    if not query:
        default_fields, default_arguments = QUERY_MAP.get(query_name, ([],{}))
        fields = get_field_list(default_fields, None, *fields)
        if(query_name == 'next_items_page'):
            fields.append('cursor')
        arguments = get_method_arguments(default_arguments, **arguments)
        query = GraphQLOperation(operation_type, query_name, FIELD_MAP, *fields, **arguments).format_body()

    if include_complexity:
        if 'mutation' in query:
            query = query.replace('query {', 'mutation { complexity { before, after }')
        else:
            query = query.replace('query {', 'query { complexity { before, after }')

    headers = { 'Authorization': api_key , 'API-version':API_VERSION , 'content-type':'application/json'}
    data = { 'query': query, 'variables': variables }
    #convert to json string
    data = json.dumps(data)
    resp = requests.post(
        API_V2_ENDPOINT,
        headers=headers,
        data=data,
        timeout=timeout)

    return _process_repsonse(api_key, timeout, resp, data, **kwargs)[query_name]


def upload_file(file_path: str, timeout = 300, **kwargs):
    """Executes a graphql query to upload a file via Rest.
    
        Parameters

            timeout : `int`
                The default timeout for Rest requests.
            kwargs : `dict`
                Optional keyword arguments

        Returns

            data : `dict`
                Response data in dictionary form.

        Optional Arguments

            api_key : `str`
                The monday.com API v2 user key.
            query_name: `str`:
                The name of the query to execute.
            operation_type: `moncli.api_v2.graphql.OperationType`:
                The type of graphql operation to perform (QUERY or MUTATION).
            fields: `list[str]`:
                List of fields to return.
            arguments: `dict`:
                Additional graphql arguments.
    """

    api_key = kwargs.pop('api_key', None)
    if not api_key:
        from . import api_key

    query_name = kwargs.pop('query_name')
    fields = kwargs.pop('fields', None)
    default_fields, _ = QUERY_MAP.get(query_name, ([],{}))
    fields = get_field_list(default_fields, None, *fields)
    arguments = kwargs.pop('arguments', None)
    operation = GraphQLOperation(OperationType.MUTATION, query_name, FIELD_MAP, *fields, **arguments)
    operation.add_query_variable('file', 'File!')
    query = operation.format_body()
    
    headers = { 'Authorization': api_key }
    data = { 'query': query }
    files = { 'variables[file]': open(file_path, 'rb') }
    resp = requests.post(
        API_V2_FILE_ENDPOINT,
        headers=headers,
        data=data,
        files=files,
        timeout=timeout)
    return _process_repsonse(api_key, timeout, resp, data, **kwargs)[query_name]


def get_field_list(fields: list, prefix: str = None, *args):
    """Get list of query fields.

        Parameters
        
            fields : `list[str]`
                A predefined collection of default fields.
            prefix : `str`
                Any parent fields to be added to the field lookup.
            args : `tuple`
                Field names passed into the request.

        Returns
            
            fields : `list[str]`
                The fields to be retrieved for the query.
    """

    if isinstance(args, tuple):
        args = list(args)
    if not args:
        args = fields
    
    ## Venkat cchanges for Items_Page
    # 
    # aining 

    str_items_page = "items_page"
    str_next_items_page = "next_items_page"
    str_cursor = "cursor"

    if not (prefix==str_items_page or prefix==str_next_items_page) : # check for items_page
               # Check if substring is part of List of Strings
        #temp = '\t'.join(fields)
        found_cursor = found = any(s.find(str_cursor) != -1 for s in fields)
        found_itemspage = found = any(s.find(str_items_page) != -1 for s in fields)

        found_cursor_arg = found = any(s.find(str_cursor) != -1 for s in args)
        found_itemspage_arg = found = any(s.find(str_items_page) != -1 for s in args)


        if not (found_itemspage or found_cursor or found_cursor_arg or found_itemspage_arg):
            if 'id' not in args:
                args.append('id') # add id if not items_page

    if prefix:
        return ['{}.{}'.format(prefix, arg) for arg in args]
    return args


def get_method_arguments(mappings: dict, **kwargs):
    """Get mapped query field arguments.

        Parameters
        
            mappings : `dict`
                A predefined set of default mappings.
            kwargs : `dict`
                Argument parameters passed into the request.

        Returns
            
            arguments : `dict`
                Arguments to be used for the query fields.
    """
    
    optional_args = {}
    for key, value in mappings.items():   
        try:
            if isinstance(value, ArgumentValueKind):
                optional_args[key] = create_value(kwargs[key], value)
            elif isinstance(value, tuple):
                data = [create_value(item, value[1]).format() for item in kwargs[key]]
                optional_args[key] = create_value(data, value[0])
            elif isinstance(value, dict):
                optional_args[key] = get_method_arguments(value, **(kwargs[key]))
        except KeyError:
            # Ignore if no kwargs found
            continue
    for arg in optional_args:
        kwargs[arg] = optional_args[arg]
    return kwargs


def _process_repsonse(api_key: str, timeout: int, resp, data, **kwargs):
    """Process Rest graphql response/retry request."""

    text: dict = resp.json()
    if resp.status_code == 401:
        raise MondayApiError(json.dumps(data), resp.status_code, '', 'Request is not authorized.  Please verify that your API token is valid.')
    if resp.status_code == 403 or resp.status_code == 500:
        raise MondayApiError(json.dumps(data), resp.status_code, '', [text['error_message']])
    if resp.status_code == 429:
        time.sleep(5)
        return execute_query(api_key, timeout, **kwargs)
    if text.__contains__('errors'):
        errors = text['errors']
        if not 'Query has complexity of' in errors[0]['message']: 
            error_query = json.dumps(data)
            status_code = resp.status_code
            errors = text['errors']
            raise MondayApiError(error_query, status_code, '', errors)
        # Wait for 5 seconds and try again in case of rate limiting... ^
        time.sleep(5)
        return execute_query(api_key, timeout, **kwargs)
    # Raise exception for parse errors.
    if text.__contains__('error_code'):
        error_query = json.dumps(data)
        raise MondayApiError(error_query, 400, text['error_code'], [text['error_message']])

    text: dict = resp.json()
    return text['data']

