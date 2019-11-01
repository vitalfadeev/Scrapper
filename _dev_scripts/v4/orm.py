# ORM
#
# Goal - fast development, high-level coding
# Very fast. Coding speed = Idea speed.
# Comfortable coding
#
# instead, for execution speed, need low-level programming. hardcode

# SQL                   # OOP
# PrimaryKey            id
#   1 PK -> always 1 object
#     SELECT * FROM words WHERE PK = 'Cat' -> Word() -> a
#     SELECT * FROM words WHERE PK = 'Cat' -> Word() -> b
#     a == b
#     id(a) = id(b)
#
# Link
# Word.Related          word.related
# kitty                 ptr -> kitty
#   - expand id on get()
#   - preload ids for expand many id on get()
#   w1.related[1]                       # id
#   w1.related[1].Label                 # expand on get
#   w1.related._preload()               # preload 1,2,...
#   preload( w1.related, w1.seeAlso )   # preload
#   preload( w1, .related, .seeAlso )   # preload
#   w1.related[2].Label                 # after preload - get
#
# Word can be use without DB
#

# w = Word()
# w.Label = "cat"
# w.write()
# write( w )
#
# w = read( Word )
# w = Word.read()
#
# w = read( Word, Label="cat" )
# w = read( Word, where="Label = 'cat'" )
# w = read( Word, where="Label = ?", "cat" )
# w = read( Word, sql="SELECT * FROM Word WHERE Label = ?", "cat" )
#
# class Word:
#   PK = required( str )
#   Label = optional( str )
#   Related = optional( list )
#
# class Word:
#   __slots__ = []
#   PK = required( str )
#   Label = optional( str )
#   Related = optional( list )

# Registers
# Cache
# RAM           <- shared
# Hard disk     <- shared

# Word
#
# write()
#   str  ->         TEXT
#   int  ->         INTEGER
#   list -> json -> TEXT
#   dict -> json -> TEXT
#   bool ->         INTEGER
#   None
#
# read()
#   TEXT    ->          str
#   TEXT    -> json ->  list
#   TEXT    -> json ->  dict
#   INTEGER ->          int
#   INTEGER ->          bool
#   None
#
# table = type(o).__name__
# table = o._table
#
# pk = o.PK
# pk = getattr( o, o._pk )
#
# indexes
import functools
import itertools
import json
import sqlite3


class Word:
    _database = "word.db"
    _table = "Word"
    _pk = "PK"

    def __init__(self):
        self.LabelName = ""

    def __repr__(self):
        name = type(self).__name__

        pk_defined = False

        if hasattr( self, "_pk" ):
            pk = getattr( self, self._pk )
            pk_defined = True

        if pk_defined == False:
            if hasattr( self, "PK" ):
                pk = self.PK
                pk_defined = True

        if pk_defined == False:
            pk = ""

        return f"{name}(pk)"


# word = Word()
# DBWrite( word )

# DB
# databases = {
#    'Word': Word._database
#    'Word': 'Word.db',
# }
# connections = {
#    'Word': sqlite3.connect( db )
# }
#
# Write  -> | DB.connections
# Read   -> |
#
DB = {}


def Write( obj, if_exists="fail", _database=None, _table=None, *args, **kwargs ):
    # if exists
    if if_exists == "replace":
        mode = "OR REPLACE"

    elif if_exists == "fail":
        mode = "OR FAIL"

    elif if_exists == "ignore":
        mode = "OR IGNORE"

    else:
        mode = ""


    # sql
    fields = []
    values = []

    for field, value in vars( obj ).items():
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

    # table
    if _table is None:
        if hasattr( obj, "_table" ):
            table = obj._table

    if _table is None:
        _table = type( obj ).__name__

    sql = """
        INSERT {mode} INTO `{table}` 
            ({fields}) 
        VALUES 
            ({values})
    """.format(
            mode=mode,
            table=_table,
            fields=", ".join(fields),
            values=", ".join(itertools.repeat('?', len(values)))
        )

    # database
    if _database is None:
        if hasattr( obj, "_database" ):
            _database = obj._database

    if _database is None:
        _database = type( obj ).__name__

    # connection
    if _database in DB:
        connection = DB[ _database ]
    else:
        connection = sqlite3.connect( _database )
        DB[ _database ] = connection

    # cursor
    c = connection.cursor()

    # execute
    c.execute(sql, values)

    # commit
    connection.commit()


def DBRead( cls, _database=None, _table=None, where=None, sql=None, params=None, *args, **kwargs ):
    """

    Args:
        cls:
        _database:
        _table:
        where:
        sql:
        params:
        *args:
        **kwargs:

    Returns:

        ::

            DBRead( Word )
            DBRead( Word, where="LabelName = ?", "Cat" )
            DBRead( Word, sql="SELECT * FROM Word LabelName = ?", "Cat" )
            DBRead( Word, sql="SELECT ExplanationTxt FROM Word LabelName = ?", "Cat" )
            DBRead( Word, sql="SELECT LabelName, count(*) as cnt FROM Word GROUP BY LabelName" )
            # DBRead( sql="SELECT LabelName, count(*) as cnt FROM Word GROUP BY LabelName" ) # FROM Word extraction, map to Word class
            # DBRead( "SELECT LabelName, count(*) as cnt FROM Word GROUP BY LabelName" ) # FROM Word extraction, map to Word class

    """
    # database
    if _database is None:
        if hasattr( cls, "_database" ):
            _database = cls._database

    if _database is None:
        _database = cls.__name__

    # connection
    if _database in DB:
        connection = DB[ _database ]
    else:
        connection = sqlite3.connect( _database )
        DB[ _database ] = connection

    # sql
    if sql is None:
        sql = f"SELECT * FROM {_table}"

    if where is not None:
        sql = f"{sql} WHERE {where}"

    #
    if params is None:
        params = args

    # cursor
    cursor = connection.cursor()

    # execute
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
                if value is None:
                    pass
                else:
                    if isinstance( value, str ):
                        # detect by property type
                        # list  <- json  <- TEXT
                        # dict  <- json  <- TEXT
                        # str   <-          TEXT
                        # int   <- int   <- TEXT
                        # float <- float <- TEXT
                        a = getattr( o, field )

                        if isinstance( a, list ):
                            setattr( o, field, json.loads( value ) )

                        elif isinstance( a, dict ):
                            setattr( o, field, json.loads( value ) )

                        elif isinstance( a, int ):
                            setattr( o, field, int( value ) )

                        elif isinstance( a, float ):
                            setattr( o, field, float( value ) )

                        else: # property: not dict | list
                            setattr( o, field, value )

                    else: # sql column: not str
                        setattr( o, field, value )

            return o

        fields = [ x[0] for x in query_result.description ]
        fn = functools.partial( convert_to_cls, cls, fields )

        result = map( fn, query_result )

    return result

