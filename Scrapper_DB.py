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


def DBWrite(DB, item:object ):
    """
    Write item into database `DB`.

    :param DB:      The database
    :param item:    Instance of class WikictionaryItem

    ::

        DBWrite( DBWikictionary, item )

    """
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
    table = item.Meta.DB_TABLE_NAME
    sql = """
        INSERT INTO `{0}` 
            ({1}) 
        VALUES 
            ({2})
    """.format(
            table,
            ", ".join(fields),
            ", ".join(itertools.repeat('?', len(values)))
        )

    c = DB.cursor()
    c.execute(sql, values)
    DB.commit()

