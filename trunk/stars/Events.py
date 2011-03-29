""" Tools for dealing with Event Data"""
import pysal
import sqlite3
import sys

def createTableSQL(tableName,header,field_spec,primaryKey = None):
    create_table_sql = "create table IF NOT EXISTS %s (%s)"
    fields = ["%s %s"%(name,spec2type(spec)) for name,spec in zip(header,field_spec)]
    # primaryKey HARD CODED to NONE for now
    # when working with DBF's let use record order as the primary key.
    primaryKey = None
    if primaryKey:
        fields.append("PRIMARY KEY (%s)"%primaryKey)
    else:
        fields.append("oid INTEGER PRIMARY KEY")
    fields = ', '.join(fields)
    return create_table_sql%(tableName,fields)
def spec2type(spec):
    t,s,p = spec
    if t.lower()=='n':
        if p==0:
            return "INTEGER"
        else:
            return "REAL"
    elif t.lower()=='f':
        return "REAL"
    return "TEXT"

    
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
        self.geocodes = []
        if issubclass(type(events_dbf), basestring):
            events_dbf = pysal.open(events_dbf)
        if not isinstance(events_dbf, pysal.core.IOHandlers.pyDbfIO.DBF):
            raise TypeError, "%r, is not a DBF or path to a DBF"%events_dbf
        self.db = db = events_dbf
        if issubclass(type(events_shp), basestring):
            events_shp = pysal.open(events_shp)
        if not isinstance(events_shp, pysal.core.IOHandlers.pyShpIO.PurePyShpWrapper):
            raise TypeError, "%r, is not a ShapeFile or path to a ShapeFile"%events_shp
        assert events_shp.type == pysal.cg.shapes.Point
        self.shp = events_shp

        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.cur = cur = self.conn.execute(createTableSQL(self.EVENTS_TABLE, db.header, db.field_spec, primaryKey=primaryKey))
        header = db.header+['oid']
        insert_sql = "insert into %s values (%s)"%(self.EVENTS_TABLE, ','.join(['?']*len(header)))
        for i,row in enumerate(db):
            cur.execute(insert_sql, row+[i])
        self.conn.commit()
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

if __name__=='__main__':
    EVENT_DATA_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears/Mesa_ResBurgAllYears.shp"
    EVENT_DATA_DBF = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears/Mesa_ResBurgAllYears.dbf"
    REGIONS_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_Beats/Mesa_Cleaned_withCrimeData.shp"
    REGIONS_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Burglaries_Mesagrids0609/projected.shp"
    REGIONS_DBF = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Burglaries_Mesagrids0609/projected.dbf"
    db = EventCollection(EVENT_DATA_DBF,EVENT_DATA_SHP)
    regions = RegionCollection(REGIONS_SHP,REGIONS_DBF)
