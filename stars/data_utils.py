"""
Utilities for managing SQLITE databases in STARS.
"""
__author__ = "Charles R Schmidt <charles.r.schmidt@asu.edu>"

import pysal
import sqlite3
import os
import json
import cPickle

__all__ = ["Table_MetaData", "createTableFromSHP","time_step","xtime_step"]

def time_step(t_0,t_end,window,step):
    """ Return a list of a date pairs, marking the beginning and end of each step. """
    periods = []
    window_end = t_0+window
    window_begin = t_0
    while window_begin <= t_end: #window_end will run off the end of the dates
        periods.append((window_begin,window_end))
        window_begin += step
        window_end += step
    return periods
def xtime_step(t_0,t_end,window,step):
    """ Return a list of a date pairs, marking the beginning and end of each step. """
    window_end = t_0+window
    window_begin = t_0
    while window_begin <= t_end: #window_end will run off the end of the dates
        yield (window_begin,window_end)
        window_begin += step
        window_end += step

def pysalShapeType2name(typ):
    if typ == pysal.cg.Point: return "point"
    elif typ == pysal.cg.Polygon: return "polygon"
    else: return "shape"
class Table_MetaData(dict):
    """
    Stores meta data about tables in the SQL database.
    The metadata refers to the table in the SQL database, not the source from which it was created.

    metadata is just a dictionary, nothing magic happens when you update the metadata.
    To save the meta data to the database you have to set the "meta" property
        of the table to which the metadata belongs.
    
    """
    @classmethod
    def loads(cls, json_data):
        obj = cls()
        obj.update(json.loads(json_data))
        return obj
    def dumps(self):
        return json.dumps(self)
    @classmethod
    def populate_from_dbf(cls, dbf):
        obj = cls()
        obj['title'] = os.path.splitext(os.path.basename(dbf.dataPath))[0]
        obj['sources'] = [dbf.dataPath]
        obj['header'] = dbf.header
        obj['spec'] = dict(zip(dbf.header,dbf.field_spec))
        obj['n'] = len(dbf)
        return obj
    @classmethod
    def populate_from_shp(cls, shp, dbf):
        obj = cls.populate_from_dbf(dbf)
        obj['geom_type'] = pysalShapeType2name(shp.type)
        obj['sources'] = [shp.dataPath,obj['sources']]
        obj['header'] = dbf.header+['geom']
        obj['spec']['geom'] = ('C',1,0)
        return obj

def createTableFromSHP(conn, tableName, shp, dbf, primaryKey = "stars_oid"):
    try:
        #Notes on with conn, http://docs.python.org/library/sqlite3.html#using-the-connection-as-a-context-manager
        with conn:
            create_table_sql = "create table %s (%s)"
            fields = ["%s %s"%(name,spec2type(spec)) for name,spec in zip(dbf.header,dbf.field_spec)]
            header = dbf.header[:]
            header.append("geom")
            fields.append("geom %s"%pysalShapeType2name(shp.type))
            if primaryKey in dbf.header:
                fields.append("PRIMARY KEY (%s)"%primaryKey)
            else:
                # when working with DBF's let use record order as the primary key.
                fields.append("%s INTEGER PRIMARY KEY"%primaryKey)
                header.append(primaryKey)
            fields = ', '.join(fields)
            cur = conn.execute(create_table_sql%(tableName, fields))

            insert_sql = "insert into %s values (%s)"%(tableName, ','.join(['?']*len(header)))
            n = len(header)
            for i,(pt,row) in enumerate(zip(shp,dbf)):
                row = row+[pt]
                if len(row) < n:
                    row = row+[i]
                cur.execute(insert_sql, row)
            #conn.commit() # Called by context manager (with conn:)
            return True
    except sqlite3.IntegrityError:
        print "An error occurred, could not create the events table, you should rebuild your database"
        return False
    except sqlite3.OperationalError:
        print "An error occurred, could not create the events table, you should rebuild your database"
        return False

def spec2type(spec):
    t,s,p = spec
    if t.lower()=='n':
        if p==0:
            return "INTEGER"
        else:
            return "REAL"
    elif t.lower()=='f':
        return "REAL"
    elif t.lower()=='d':
        return "DATE"
    return "TEXT"

# Load SQL Adapters/Converters
# Make sure "detect_types=sqlite3.PARSE_DECLTYPES" is passed to the connect function.
def adapt_point(point):
    return json.dumps(tuple(point))
def convert_point(s):
    return pysal.cg.Point(json.loads(s))
sqlite3.register_adapter(pysal.cg.Point, adapt_point)
sqlite3.register_converter("point", convert_point)
sqlite3.register_adapter(pysal.cg.Polygon, cPickle.dumps)
sqlite3.register_converter("polygon", cPickle.loads)
sqlite3.register_adapter(Table_MetaData, Table_MetaData.dumps)
sqlite3.register_converter("table_metadata", Table_MetaData.loads)
