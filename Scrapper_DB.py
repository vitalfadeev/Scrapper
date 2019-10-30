#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Scrapper's high-level functions for work with DB.

For scrapping functions see: wiktionary.*, wikidata.*
"""

import json
import itertools


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


def DBRead( DB, table, id=None, where=None, args=tuple ):
    """
    Read item from database `DB`.

    :param DB:      The database
    :param item:    Instance of class WikictionaryItem

    ::

        item = DBRead( DBWikictionary, 'wiktionary', where="PrimaryKey='...'" )

    """
    if where is None:
        sql = "SELECT * FROM `{}`".format( table )
    else:
        sql = "SELECT * FROM `{}` WHERE ".format( table ) + where

    DB.execute( sql, args )

    item = []
    yield from item


def DBWrite(DB, item:object, table=None, if_exists="fail" ):
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
    sql = """
        SELECT * FROM {table} LIMIT 1 
    """.format(
        table=table
    )
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
        sql = """
            ALTER TABLE {table} ADD {column} {t}
            """.format(
                table=table,
                column=column,
                t=t,
            )
        DB.execute( sql )


def DBCheckStructure( DB, table, columns ):
    for column, column_type in columns:
        DBAddColumn( DB, table, column, column_type )


def DBCheckIndex( DB, table, columns ):
    if isinstance( columns, str ):
        columns = [columns]

    sql = """
        SELECT name 
          FROM sqlite_master 
        WHERE type='index' AND tbl_name = '{}'
    """.format( table )

    c = DB.cursor()

    c.execute(sql)

    indb = []

    for rec in c.fetchall():
        indb.append( rec[0] )

    # compare
    if (table + "_" + columns.join('_')) not in indb:
        # create
        #   index_name ON table ( columns )
        index_name = table + "_" + columns.join('_')
        columns_str = columns.join(',')
        pk = ""
        sql = """
            CREATE {} INDEX IF NOT EXISTS {} 
                ON {} ({})
        """\
        .format(
            pk,
            index_name,
            table,
            columns_str
        )
        DBExecute( DB, sql )


def DBCheckIndexes( DB, table, indexes ):
    for columns in indexes:
        DBCheckIndex( DB, table, columns )
