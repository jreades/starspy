"""
Tools for managing SQLITE databases in STARS.

deals with Event Data
deals with Region Data
deals with Joins and aggregation

"""
__author__ = "Charles R Schmidt <charles.r.schmidt@asu.edu>"

import pysal
import sqlite3
from data_utils import Table_MetaData, createTableFromSHP

class StarsTable(object):
    """
    Models a Stars Table within a Stars Database
        Valid table types are:
            "data"
            "event"
            "region"
            "event_by_region"

        This class contains zero data, all the data is stored in the StarsDatabase.
        This class is just a helper class to get data out of the StarDatabase in useful ways.
    """
    def __init__(self, database, table_name):
        self._db = database
        self._tableName = table_name
    @classmethod
    def table_factory(cls, database):
        """
        The table_factory is used by StarsDatabase to create table objects without having to explicitly pass itself to the constructor.
        This is useful for something like, map(factory, ['table1','table2','table3'])
        """
        return lambda x: cls(database, x)
    def __get_meta(self):
        return self._db.conn.execute("SELECT meta FROM tables WHERE table_name=? LIMIT 1",[self._tableName]).fetchone()[0]
    def __set_meta(self,value):
        self._db.conn.execute("UPDATE tables SET meta = ? WHERE table_name = ?",[value,self._tableName])
        self._db.conn.commit()
    meta = property(__get_meta,__set_meta)
    @property
    def geom_type(self):
        return self.meta.get('geom_type',None)
    @property
    def type(self):
        return self._db.conn.execute("SELECT table_type FROM tables WHERE table_name=? LIMIT 1",[self._tableName]).fetchone()[0]
    def make_event_table(self, time_field):
        """
        Create an events table from a data table
        Changes the type of the data_table to "event"

        Attributes
        ----------
        data_table -- string -- name of table to alter.
        time_field -- string -- name of the column that contains the time information.
        """
        meta = self.meta
        if time_field in meta['header']:
            meta['time_field'] = time_field
            self.meta = meta
            self._db.conn.execute("UPDATE tables SET table_type='event' WHERE table_name=?",[self._tableName])
            self._db.conn.commit()
            return True
        return False
    def count(self, filters = None, groupby = None):
        """
        rewrite this to use joins
        """
        pkey = self.meta['primaryKey']
        sql = "SELECT count(%s) from %s"%(pkey,self._tableName)
        if filters:
            sql += " WHERE %s"%str(filters)
        if groupby:
            sql += " GROUP BY %s"%groupby
            sql = sql.replace("SELECT ","SELECT %s,"%groupby)
        return self._db.conn.execute(sql).fetchall()
        
class StarsEventTable(StarsTable):
    """Extends the Stars Tables adding special methods to filter and aggregate by date"""

class StarsDatabase(object):
    """
    Models a Stars Database,
        contains:
            event tables
            region tables
            data tables
            ?join tables

    Arguments
    ---------
    connectionString -- string -- Path to SQLITE database, defaults to ":memory:"

    """
    def __init__(self,connectionString=":memory:"):
        self.conn = sqlite3.connect(connectionString, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("create table IF NOT EXISTS tables (table_name PRIMARY KEY, table_type, source_files, meta table_metadata)")
        self.table_factory = StarsTable.table_factory(self)
    @property
    def tables(self):
        tables = [x[0] for x in self.conn.execute("SELECT table_name FROM tables").fetchall()]
        return map(self.table_factory, tables)
    @property
    def data_tables(self):
        tables = [x[0] for x in self.conn.execute("SELECT table_name FROM tables WHERE table_type='data'").fetchall()]
        return map(self.table_factory, tables)
    @property
    def event_tables(self):
        tables = [x[0] for x in self.conn.execute("SELECT table_name FROM tables WHERE table_type='event'").fetchall()]
        return map(self.table_factory, tables)
    @property
    def region_tables(self):
        tables = [x[0] for x in self.conn.execute("SELECT table_name FROM tables WHERE table_type='region'").fetchall()]
        return map(self.table_factory, tables)
    def add_table_from_shp(self, shp, dbf):
        """
        Add a generic Table from a shapefile to the project Database.

        Arguments
        ---------
        dbf -- string,dbf -- Path to dbf or a pysal dbf object
        shp -- string,shp -- Path to shp or a pysal shp object
        
        Returns
        -------
        The table object.
        """
        # Determine type of dbf
        if issubclass(type(dbf), basestring):
            dbf = pysal.open(dbf)
        if not isinstance(dbf, pysal.core.IOHandlers.pyDbfIO.DBF):
            raise TypeError, "%r, is not a DBF or path to a DBF"%dbf

        # Determine type of shp
        if issubclass(type(shp), basestring):
            shp = pysal.open(shp)
        if not isinstance(shp, pysal.core.IOHandlers.pyShpIO.PurePyShpWrapper):
            raise TypeError, "%r, is not a ShapeFile or path to a ShapeFile"%shp

        #acquire next available table.
        table_name = "stars_Table_%d"%len(self.tables)
        pkey = "stars_oid"
        if createTableFromSHP(self.conn, table_name, shp, dbf, pkey):
            meta = Table_MetaData.populate_from_shp(shp, dbf)
            meta['primaryKey'] = pkey
            self.conn.execute("INSERT INTO tables VALUES (?,?,?,?)",[table_name, 'data', dbf.dataPath, meta])
            self.conn.commit()
        

'''


    
class RegionCollection(object):
    def __init__(self, regions_shp, regions_dbf):
        if issubclass(type(regions_shp),basestring):
            regions_shp = pysal.open(regions_shp)
        if not isinstance(regions_shp,pysal.core.IOHandlers.pyShpIO.PurePyShpWrapper):
            raise TypeError, "%r, is not a ShapeFile or path to a ShapeFile"%regions_shp
        assert regions_shp.type == pysal.cg.shapes.Polygon
        if issubclass(type(regions_dbf),basestring):
            regions_dbf = pysal.open(regions_dbf)
        if not isinstance(regions_dbf,pysal.core.IOHandlers.pyDbfIO.DBF):
            raise TypeError, "%r, is not a DBF or path to a DBF"%regions_dbf
        self.shp = regions_shp
        self.dbf = regions_dbf
    def __iter__(self):
        return self.shp
    
class EventCollection(object):
    """Managment Class"""
    EVENTS_TABLE = "events"
    @staticmethod
    def adapt_point(point):
        """ http://docs.python.org/library/sqlite3.html """
        return "%f;%f"%(point[0],point[1])
    @staticmethod
    def convert_point(s):
        """ http://docs.python.org/library/sqlite3.html """
        x,y = map(float, s.split(";"))
        return pysal.cg.Point((x,y))
    def __init__(self, events_dbf, events_shp, primaryKey = None):
    def geoCodeByID(self, evtRegionIds, regions, regionIds):
        """ 
        Geocode events to the supplied regions using the supplied ids
        
        Arguments:
        evtRegionIds -- list -- List of region ids for each event in event record order.
        regions -- RegionCollection -- each event will be assigned to one of these regions or None.
        regionIds -- list -- List of region ids in region record order.
        
        Returns:
            dict[ event j] == region i # offsets.
        """
        tableName = "stars_geocode_%d"%(len(self.geocodes))
        create_table_sql = "create table IF NOT EXISTS %s (oid INTEGER PRIMARY KEY, roid INTEGER)"%tableName
        self.cur.execute(create_table_sql)
        #clear it incase it does exist
        self.cur.execute("DELETE FROM %s"%tableName)
        #try:
        #    assert set(evtIds) == set(regionIds)
        #except AssertionError:
        #    raise ValueError, "evtIds do not match regions Ids!"
        # Note, in practice, evtRegionsIds may contain None or other non-matches.
        insert_sql = "INSERT INTO %s VALUES (?, ?)"%tableName

        regionIds2offset = dict([(id,i) for i,id in enumerate(regionIds)])
        code = {}
        cur = self.cur
        for i,rid in enumerate(evtRegionIds):
            if rid in regionIds2offset:
                code[i] = regionIds2offset[rid]
            else:
                code[i] = None
            cur.execute(insert_sql,[i,code[i]])
        self._regions = regions
        self._geocode = code
        return code
    def geoCode(self,regions):
        """
        Geocode events to the supplied regions
        
        Arguments:
        regions -- RegionCollection -- each event will be assigned to one of these regions or None.
        """
        ppi = pysal.cg.get_polygon_point_intersect
        code = {} # pt to poly
        for i,region in enumerate(regions):
            print "Region:",i
            bbox = region.bounding_box
            for j,pt in enumerate(self.shp):
                if j in code:
                    pass
                elif ppi(region,pt):
                    print "Point, %d, is in Region %d"%(j,i)
                    code[j]=i
        return code

    db = EventCollection(EVENT_DATA_DBF,EVENT_DATA_SHP)
    regions = RegionCollection(REGIONS_SHP,REGIONS_DBF)
        
'''
if __name__=='__main__':
    EVENT_DATA_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears/Mesa_ResBurgAllYears.shp"
    EVENT_DATA_DBF = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears/Mesa_ResBurgAllYears.dbf"
    REGIONS_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_Beats/Mesa_Cleaned_withCrimeData.shp"
    REGIONS_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Burglaries_Mesagrids0609/projected.shp"
    REGIONS_DBF = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Burglaries_Mesagrids0609/projected.dbf"
