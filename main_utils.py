import secrets, re

# this can be used for generating ids of string lenght 12 default
def generate_id(query_table, id_length:int = 20) -> str:
    '''
    this will generate a random id to be used 
    and check the database to veryify it doesn't alredy exsit in the given table
    

    query_table: is the table you wish to check for the id's existance

    id_length: is the length of the returned id, 11 is the default
    '''

    id = secrets.token_hex(round(abs(id_length/2)))

    while True:
        if not check_id(query_table, id): 
            break
        id = secrets.token_hex(round(abs(id_length/2)))

    id = id[:id_length]
    
    return id

# returns true if no id is found in the database
def check_id(query_table, query_id:str) -> bool:
    '''
    returns true if no id is found in the database
    and false is the id is found
    '''
    ans = query_table.query.filter(query_table.id == query_id).first()

    return True if ans else False