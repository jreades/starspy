"""
Tools for managing SQLITE databases in STARS.

deals with Event Data
deals with Region Data
deals with Joins and aggregation

"""
__author__ = "Charles R Schmidt <charles.r.schmidt@asu.edu>"

import numpy
import pysal
import sqlite3
from data_utils import Table_MetaData, createTableFromSHP, time_step
from collections import deque
import datetime

        
class StarsColumn(object):
    """
    Models a Stars Column within a Stars Table
    """
    def __repr__(self):
        return "<%s %s of \"%r\" at 0x%X>"%(self.__class__.__name__,self._fieldName, self.parent_table, id(self))
    def __init__(self, table, field_name):
        self.conn = table._db.conn
        self.parent_table = table
        self._fieldName = field_name
        self.typ = table.meta['spec'][field_name][0].upper()
    @property
    def range(self):
        """The (min,max) of the data column"""
        if self.typ == 'D':
            rs = self.conn.execute("SELECT MIN(%s) AS 'min [date]', MAX(%s) AS 'max [date]' FROM %s"%(self._fieldName,self._fieldName,self.parent_table._tableName)).fetchall()
        else:
            rs = self.conn.execute("SELECT MIN(%s) AS 'min',MAX(%s) AS 'max' FROM %s"%(self._fieldName,self._fieldName,self.parent_table._tableName)).fetchall()
        return rs[0]
    def tolist(self):
        """returns the data column as a list"""
        rs = self.conn.execute("SELECT %s FROM %s"%(self._fieldName,self.parent_table._tableName)).fetchall()
        return [x[0] for x in rs]
    def toset(self):
        """returns the data column as a set"""
        rs = self.conn.execute("SELECT DISTINCT %s FROM %s"%(self._fieldName,self.parent_table._tableName)).fetchall()
        return set([x[0] for x in rs])
    def count_distinct(self):
        """returns len(self.toset())"""
        rs = self.conn.execute("SELECT count(DISTINCT %s) FROM %s"%(self._fieldName,self.parent_table._tableName)).fetchall()[0][0]
        return rs
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

    Examples
    >>> table = StarsTable(db, 'stars_Table_0')
    >>> table['FIELD_NAME']
    <__main__.StarsColumn object at 0x23b05b0>
    """
    def __init__(self, database, table_name):
        self._db = database
        self._tableName = table_name
    def __repr__(self):
        name = self._tableName
        if 'title' in self.meta:
            name = self.meta['title']
        return "<%s %s at 0x%X>"%(self.__class__.__name__,name,id(self))
    @classmethod
    def table_factory(cls, database):
        """
        The table_factory is used by StarsDatabase to create table objects without having to explicitly pass itself to the constructor.
        This is useful for something like, map(factory, ['table1','table2','table3'])
        """
        return lambda x: cls(database, x)
    def __getitem__(self,key):
        if key in self.meta['header']:
            return StarsColumn(self,key)
        elif type(key) == int and key < len(self.meta['header']):
            return StarsColumn(self,self.meta['header'][key])
        raise IndexError, "index out of range"
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
    def make_region_table(self, oid):
        """
        Create a regions table from a data table
        Changes the type of the data_table to "region"

        Attributes
        ----------
        oid -- string -- name of the field contain the "order" of the regions
        """
        meta = self.meta
        if oid in meta['header']:
            meta['oid'] = oid
            self.meta = meta
            self._db.conn.execute("UPDATE tables SET table_type='region' WHERE table_name=?",[self._tableName])
            self._db.conn.commit()
            return True
        return False
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
    def rows(self,filter=None,filterArgs = [], group_by=None, fields=""):
        fields = fields if fields else self._fields
        sql = "SELECT %s FROM %s"%(fields,self._tableName)
        if filter:
            sql += " WHERE "+filter
        if group_by:
            sql += " GROUP BY "+group_by
        return self._db.conn.execute(sql,filterArgs).fetchall()
        
class StarsRegionTable(StarsTable):
    def get_oid(self):
        oid_field = self.meta['oid']
        cur = self._db.conn.execute("SELECT %s FROM %s ORDER BY %s"%(oid_field,self._tableName,oid_field))
        return [x[0] for x in cur.fetchall()]
    def field_to_oid(self,field,flip=False):
        oid_field = self.meta['oid']
        if flip:
            cur = self._db.conn.execute("SELECT %s,%s FROM %s"%(oid_field,field,self._tableName))
        else:
            cur = self._db.conn.execute("SELECT %s,%s FROM %s"%(field,oid_field,self._tableName))
        return dict([(a,b) for a,b in cur.fetchall()])
    def set_events(self,evtTable,evtJoinField,regionJoinField):
        if evtJoinField not in evtTable.meta['header']:
            raise ValueError, "evtTable does not contain join field"
        if regionJoinField not in self.meta['header']:
            raise ValueError, "This table does not contain join field"
        if evtTable.type != 'event':
            raise TypeError, "evtTable is not an a proper StarsEventTable"
        self._evtTable = evtTable
        self._evtJoinField = evtJoinField
        self._regionJoinField = regionJoinField
    def event_count_by_period(self):
        if not hasattr(self,'_evtTable'):
            raise ValueError, "No event table set"
        bridge = self.field_to_oid(self._regionJoinField,True)
        order = self.get_oid()
        n = len(bridge)
        nt = self._evtTable.num_periods
        y_by_t = numpy.zeros((n,nt))
        groupBy = self._evtJoinField
        euid = self._evtTable.meta['primaryKey'] # event_unique_id
        fields = "%s,COUNT(%s)"%(groupBy,euid)
        for t in range(nt):
            counts = dict(self._evtTable.period(t, groupBy, fields))
            y = [counts.get(bridge[x],0) for x in order]
            y_by_t[:,t] = y
        return y_by_t
class StarsEventTable(StarsTable):
    """
    Extends the Stars Tables adding special methods to filter and aggregate by date

    Stars Event Tables are REQUIRED to have at leaste one DATE field.
    The field MUST be specified in meta['time_field']

    These table have special filtering abilities,

    t_0 -- datetime -- Filter out all dates before t_0, Set to None to use the data's own t_0
    t_end -- datetime -- Folter out all dates after t_end, Set to None to use the data's own t_end
    window -- timedelta -- Size of a movable window used to filter the events.
    step -- timedelta -- delta by which to advance the window.
    periods -- getter -- table.periods[n]: returns a table view with the necessary filters set 
                         for time period n, in the range t_0:t_end of size window, 
                         n steps from t_0.
    rows -- list of lists -- returns all rows in the current set (after filters are applied).
    """
    def __init__(self, database, table_name):
        StarsTable.__init__(self, database, table_name)
        self.__filter = None
        self.__t0 = None
        self.__tEnd = None
        self.__window = datetime.timedelta(days=90)
        self.__step = datetime.timedelta(days=30)
        self._periods = None
        self._fields = "*"
    def __set_t0(self,value):
        if value == None:
            self.__t0 = None
            self._periods = None
        elif type(value) != datetime.datetime:
            raise TypeError, "Value must be a datetime object."
        else:
            self.__t0 = value
            self._periods = None
    def __get_t0(self):
        if not self.__t0:
            self.__t0 = self[self.meta['time_field']].range[0]
        return self.__t0
    t_0 = property(__get_t0, __set_t0)
    def __set_tEnd(self, value):
        if value == None:
            self.__tEnd = None
            self._periods = None
        elif type(value) != datetime.datetime:
            raise TypeError, "Value must be a datetime object."
        else:
            self.__tEnd = value
            self._periods = None
    def __get_tEnd(self):
        if not self.__tEnd:
            self.__tEnd = self[self.meta['time_field']].range[1]
        return self.__tEnd
    t_end = property(__get_tEnd, __set_tEnd)
    def __set_window(self, value):
        if type(value) != datetime.timedelta:
            raise TypeError, "Value must be a timedelta object."
        else:
            self.__window = value
            self._periods = None
    def __get_window(self):
        return self.__window
    window = property(__get_window,__set_window)
    def __set_step(self, value):
        if type(value) != datetime.timedelta:
            raise TypeError, "Value must be a timedelta object."
        else:
            self.__step = value
            self._periods = None
    def __get_step(self):
        return self.__step
    step = property(__get_step,__set_step)
    @property
    def num_periods(self):
        if not self._periods:
            x = self.period(0)
        return len(self._periods)
    def period(self, t, group_by = None, fields = None):
        if not self._periods: #would be better to just calculate the period for t.
            self._periods = time_step(self.t_0,self.t_end,self.window,self.step)
        name = self.meta['time_field']
        filt = "%s >= ? AND %s < ?"%(name,name)
        return self.rows(filt, self._periods[t], group_by, fields)
    @property
    def filter(self):
        print "DeprecationWarning"
        if not self.__filter:
            self.__filter = StarsTableFilter(self)
            self.__filter.setRangeField(self.meta['time_field'])
        return self.__filter
    def count(self, filters = None, groupby = None):
        """
        rewrite this to use joins
        """
        print "DeprecationWarning"
        pkey = self.meta['primaryKey']
        sql = "SELECT count(%s) from %s"%(pkey,self._tableName)
        if filters:
            sql += " WHERE %s"%str(filters)
        if groupby:
            sql += " GROUP BY %s"%groupby
            sql = sql.replace("SELECT ","SELECT %s,"%groupby)
        return self._db.conn.execute(sql).fetchall()
    def group_by(self,field,filt=None):
        print "DeprecationWarning"
        sql = "SELECT %s,count(*) from %s"%(field, self._tableName)
        sql2= " GROUP BY %s"%(field)
        if filt:
            sql+= " WHERE "+filt[0]
            return self._db.conn.execute(sql+sql2,filt[1]).fetchall()
        else:
            return self._db.conn.execute(sql+sql2).fetchall()
class StarsTableFilter(object):
    """
    Filter a StarsTable by its attributes.

    modeled after target1_ESDA.js:Filters
    """
    MAX_LEN = 25
    def __init__(self, parent_table):
        self.parent = parent_table
        self.ranges = {}
        self.values = {}
        self.range_field = None
        if 'spec' in parent_table.meta:
            fields = parent_table.meta['spec']
            for field in fields:
                if fields[field][0].upper() == 'D':
                    # use first range field found as the default range field.
                    if not self.range_field:
                        self.range_field = field
                    self.ranges[field] = self.parent[field].range
                # equality filters are not implemented yet
                #else:
                #    values = self.parent[field].toset()
                #    if len(values) <= self.MAX_LEN:
                #        self.values[field] = values
    def setRangeField(self,field):
        if field in self.ranges:
            self.range_field = field
        else:
            raise KeyError,field
    def step(self, window = datetime.timedelta(days=120), step = datetime.timedelta(days=30), direction = "FORWARD", group_by=None):
        """
        Returns a new Series Object

        If direction is "FORWARD" the first event is guaranteed to be included.
        If direction is "BACKWARD" the last event is guaranteed to be included, the last time period will be returned first.

        Arguments
        ---------
        window -- datetime.timedelta -- size of window to collect events
        step -- datetime.timedelta -- how much to move the window each step
        direction -- "FORWARD" or "BACKWARD"
        group_by -- field_name -- If not none, GROUP BY field_name.
        """
        if self.range_field:
            name = self.range_field
            filt = "%s >= ? AND %s < ?"%(name,name)
            t_0,t_end = self.ranges[name]
            if direction == 'BACKWARD':
                window_end = t_end
                window_begin = t_end-window
                while window_begin >= t_0:
                    yield filt,[window_begin,window_end]
                    window_begin -= step
                    window_end -= step
            else:
                window_begin = t_0
                window_end = t_0+window
                while window_end <= t_end:
                    yield filt,[window_begin,window_end]
                    window_begin += step
                    window_end += step
        else:
            raise ValueError, "No range field is not set"
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
        self.conn = sqlite3.connect(connectionString, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("create table IF NOT EXISTS tables (table_name PRIMARY KEY, table_type, source_files, meta table_metadata)")
        self.table_factory = StarsTable.table_factory(self)
        self.evt_table_factory = StarsEventTable.table_factory(self)
        self.table_dispatch = {"event":StarsEventTable, "region":StarsRegionTable}
    @property
    def tables(self):
        tables = self.conn.execute("SELECT table_name,table_type FROM tables").fetchall()
        return [self.table_dispatch.get(x[1],StarsTable)(self,x[0]) for x in tables]
    @property
    def data_tables(self):
        tables = self.conn.execute("SELECT table_name,table_type FROM tables WHERE table_type='data'").fetchall()
        return [self.table_dispatch.get(x[1],StarsTable)(self,x[0]) for x in tables]
    @property
    def event_tables(self):
        tables = self.conn.execute("SELECT table_name,table_type FROM tables WHERE table_type='event'").fetchall()
        return [self.table_dispatch.get(x[1],StarsTable)(self,x[0]) for x in tables]
    @property
    def region_tables(self):
        tables = self.conn.execute("SELECT table_name,table_type FROM tables WHERE table_type='region'").fetchall()
        return [self.table_dispatch.get(x[1],StarsTable)(self,x[0]) for x in tables]
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
            meta['header'].append(pkey)
            meta['spec'][pkey] = ('N',20,0)
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

    import os
    if os.path.exists('test.starsdb'):
        db = StarsDatabase('test.starsdb')
        t = db.tables[0]
        c = t['REPORT_DAT']
    else:
        db = StarsDatabase('test.starsdb')
        db.add_table_from_shp(EVENT_DATA_SHP,EVENT_DATA_DBF)
        db.tables[0].make_event_table('REPORT_DAT')
        db.add_table_from_shp(REGIONS_SHP,REGIONS_DBF)
        t = db.tables[0]
        c = t['REPORT_DAT']
