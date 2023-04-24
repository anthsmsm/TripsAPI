from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from decouple import config


strcon = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(host=config('SQL_HOST'), user=config('SQL_USER'), password=config('SQL_PASSWORD'), database=config('SQL_DATABASE'), port=config('SQL_PORT'))        
engine = create_engine(strcon)
Session = sessionmaker(bind = engine)

"""
Method to return the session connected to the database
"""
def get_session():
    return Session()

"""
Method to return the engine used to get connected to the database
"""
def get_engine():
    return engine

"""
Method to check if the database is created, and if not, create it and create the extension of postgis
"""
def check_db_exists():
    try:
        if not database_exists(engine.url):
            create_database(engine.url)
            with engine.connect() as connection:
                connection.execute(text("CREATE EXTENSION postgis;"))
                connection.commit()
    except Exception as ex:
        raise ex

"""
Method to execute a query in the database.
Params:
    @session: Session used to connect to the database
    @query: Query to execute in the database
    @params: JSON with Parameters used in the query. It needs to be in the proper format, for example {'param1': 'value1', 'param2': 'value2'}. Default value is empty JSON
    @commit: Perform commit after the execution. True by default.
"""
def execute_query(session, query, params = {}, commit = True):
    try:
        session.execute(text(query), params)
        if commit:
            session.commit()
    except Exception as ex:
        raise ex
"""
Method to perform a select in the database and get the result.
Params:
    @session: Session used to connect to the database
    @query: Query to execute in the database
    @params: JSON with Parameters used in the query. It needs to be in the proper format, for example {'param1': 'value1', 'param2': 'value2'}. Default value is empty JSON
Return:
    Resultset
"""
def execute_select(session, query, params = {}):
    try:
        return session.execute(text(query), params)
    except Exception as ex:
        raise ex
    