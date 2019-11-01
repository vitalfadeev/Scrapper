#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Scrapper's high-level functions for work with DB.

For scrapping functions see: wiktionary.*, wikidata.*
"""
import functools
import json
import itertools
import sqlite3
import logging

log = logging.getLogger(__name__)


def DBExecute( DB, sql, *args ):
    """
    Execute SQL command in database `DB`

    Args:
        DB :      The database
        sql (str):  SQL command
        *args:      sql-command arguments

    ::

        DBWikictionary = sqlite3.connect( DB_NAME )
        DBExecute( DBWikictionary, "SELECT * FROM wiktionary WHERE id = ?", (1, ) )
    """
    DB.execute( sql, args )


def DBExecuteScript( DB, sql, *args ):
    """
    Execute many SQL script in database `DB`

    :param DB:      The database
    :param sql:     SQL script (commands separated by ';')

    ::

        DBWikictionary = sqlite3.connect( DB_NAME )
        DBExecute( DBWikictionary,
            "CREATE TABLE wiktionary (LanguageCode CHAR(2));  CREATE INDEX LanguageCode ON wiktionary (LanguageCode);"
        )
    """
    DB.executescript( sql )


def DBRead( DB, table=None, where=None, sql=None, params=None, cls=None, *args, **kwargs ):
    """
    Read item from database `DB`.

    :param DB:      The database
    :param item:    Instance of class WikictionaryItem

    ::

        rows = DBRead( DBWikictionary, 'wiktionary', where="PrimaryKey='...'" )
        rows = DBRead( DBWikictionary, 'SELECT * FROM wiktionary" )
        rows = DBRead( DBWikictionary, 'SELECT * FROM wiktionary LabelName=?", 'Cat' )
        rows = DBRead( DBWikictionary, 'SELECT * FROM wiktionary LabelName=?", 'Cat', cls=WiktionaryItem )

    """
    assert isinstance( DB, sqlite3.Connection ), "expect sqlite3.Connection"

    connection = DB

    #
    if sql is None:
        sql = f"SELECT * FROM {table}"

    if where is not None:
        sql = f"{sql} WHERE {where}"

    #
    if params is None:
        params = args

    # execute
    cursor = connection.cursor()
    query_result = cursor.execute( sql, params )
    # convert result to object | list | dict | ...
    if cls is None:
        result = query_result

    elif cls is tuple:
        result = query_result

    elif cls is list:
        result = query_result

    elif cls is dict:
        def convert_to_dict( fields, row ):
            return dict( zip( fields, row ) )

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_dict, fields )

        result = map( fn, query_result )

    else: # cls is class
        def convert_to_cls( cls, fields, row ):
            # str -> str
            #     -> []
            #     -> {}
            # int -> int
            # nul -> str
            #     -> []
            #     -> {}
            #     -> int
            # depends of cls.attr type

            o = cls()

            for field, value in zip( fields, row ):
                a = getattr( o, field )

                if value is None:
                    pass
                else:
                    if isinstance( a, list ):
                        setattr( o, field, json.loads( value ) )

                    elif isinstance( a, dict ):
                        setattr( o, field, json.loads( value ) )

                    else:
                        setattr( o, field, value )

            return o

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_cls, cls, fields )

        result = map( fn, query_result )

    return result


def DBWrite(DB, item:object, table=None, if_exists="fail", *args, **kwargs ):
    """
    Write item into database `DB`.

    :param DB:      The database
    :param item:    Instance of class WikictionaryItem

    ::

        DBWrite( DBWikictionary, item )

    """
    if if_exists == "replace":
        mode = "OR REPLACE"

    elif if_exists == "fail":
        mode = "OR FAIL"

    elif if_exists == "ignore":
        mode = "OR IGNORE"

    else:
        mode = ""


    #
    fields = []
    values = []

    for field, value in vars(item).items():
        if isinstance(value, (dict, list)):
            if value:
                jsoned = json.dumps(value, sort_keys=False, ensure_ascii=False)
                fields.append( field )
                values.append( jsoned )
            else:
                fields.append( field )
                values.append( None )
        elif isinstance( value, str ) and not value:
            fields.append( field )
            values.append( None )
        elif value is bool:
            fields.append( field )
            values.append( None )
        elif value is str:
            fields.append( field )
            values.append( None )
        elif value is int:
            fields.append( field )
            values.append( None )
        else:
            fields.append( field )
            values.append( value )

    # dump
    #for field, value in zip(fields, values):
    #    print( field.ljust(40), str(value).ljust(20), type(value) )

    #table = item.__class__.__name__
    if table is None:
        if hasattr( item, "Meta" ) and hasattr( item.Meta, "DB_TABLE_NAME" ):
            table = item.Meta.DB_TABLE_NAME

    sql = """
        INSERT {mode} INTO `{table}` 
            ({fields}) 
        VALUES 
            ({values})
    """.format(
            mode=mode,
            table=table,
            fields=", ".join(fields),
            values=", ".join(itertools.repeat('?', len(values)))
        )

    c = DB.cursor()
    c.execute(sql, values)
    DB.commit()


def _is_column_exists( DB, table, column ):
    # 1.select info from DB info_scheme
    # 2. find column
    # 3. return True - ok, False - not
    sql = f""" SELECT * FROM {table} LIMIT 1 """

    c = DB.cursor()
    c.execute( sql )
    # get first row, and fetch row titles
    db_fields = [ description[ 0 ] for description in c.description ]

    # find required column
    if column in db_fields:
        return True
    else:
        return False


def DBAddColumn( DB, table, column, t ):
    # 1. check table structure for column name
    # 2. add column
    if _is_column_exists( DB, table, column ):
        pass

    else:
        sql = f""" 
            ALTER TABLE {table} 
                    ADD {column} {t} 
            """
        DB.execute( sql )


def DBCheckStructure( DB, table:str, columns:dict ):
    for column, column_type in columns.items():
        DBAddColumn( DB, table, column, column_type )


def DBCheckIndex( DB, table, columns ):
    if isinstance( columns, str ):
        columns = [columns]

    sql = f"""
        SELECT name 
          FROM sqlite_master 
         WHERE type='index' 
           AND tbl_name = '{table}'
        """

    c = DB.cursor()

    c.execute(sql)

    indb = []

    for rec in c.fetchall():
        indb.append( rec[0] )

    #
    index_name = table + "_" + '_'.join( columns )

    # compare
    if index_name not in indb:
        # create
        #   index_name ON table ( columns )
        columns_str = ','.join(columns)
        pk = ""
        sql = f"""
            CREATE {pk} INDEX IF NOT EXISTS {index_name} 
                ON {table} ({columns_str})
        """

        log.info( f"Creating index: ON {table} ({columns_str})" )

        DBExecute( DB, sql )


def DBCheckIndexes( DB, table, indexes ):
    for columns in indexes:
        DBCheckIndex( DB, table, columns )
