import json
import itertools
import sqlite3


def DBExecute( DB, sql, *args ):
    DB.execute( sql, args )


def DBRead(DB, id=None, where=None):
    item = object()
    return item


def DBWrite(DB, item):
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

