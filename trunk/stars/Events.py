""" Tools for dealing with Event Data"""
import pysal
import sqlite3
import sys

def createTableSQL(tableName,header,field_spec,primaryKey = None):
    create_table_sql = "create table IF NOT EXISTS %s (%s)"
    fields = ["%s %s"%(name,spec2type(spec)) for name,spec in zip(header,field_spec)]
    if primaryKey:
        fields.append("PRIMARY KEY (%s)"%primaryKey)
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
    def __init__(self, regions_shp):
        if issubclass(type(regions_shp),basestring):
            regions_shp = pysal.open(regions_shp)
        if not isinstance(regions_shp,pysal.core.IOHandlers.pyShpIO.PurePyShpWrapper):
            raise TypeError, "%r, is not a ShapeFile or path to a ShapeFile"%regions_shp
        assert regions_shp.type == pysal.cg.shapes.Polygon
        self.shp = regions_shp
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
    def __init__(self,events_dbf,events_shp):
        if issubclass(type(events_dbf),basestring):
            events_dbf = pysal.open(events_dbf)
        if not isinstance(events_dbf,pysal.core.IOHandlers.pyDbfIO.DBF):
            raise TypeError, "%r, is not a DBF or path to a DBF"%events_dbf
        self.db = db = events_dbf
        if issubclass(type(events_shp),basestring):
            events_shp = pysal.open(events_shp)
        if not isinstance(events_shp,pysal.core.IOHandlers.pyShpIO.PurePyShpWrapper):
            raise TypeError, "%r, is not a ShapeFile or path to a ShapeFile"%events_shp
        assert events_shp.type == pysal.cg.shapes.Point
        self.shp = events_shp

        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.cur = cur = self.conn.execute(createTableSQL(self.EVENTS_TABLE, db.header, db.field_spec, primaryKey="CASE_ID"))
        insert_sql = "insert into %s values (%s)"%(self.EVENTS_TABLE,','.join(['?']*len(db.header)))
        for row in db:
            cur.execute(insert_sql,row)
        self.conn.commit()
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
                    print "Point, %d, is in Regoin %d"%(j,i)
                    code[j]=i
        return code

if __name__=='__main__':
    EVENT_DATA_DBF = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears_withGrids/Mesa_ResBurgAllYears_withGrids.dbf"
    EVENT_DATA_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_ResBurgAllYears_withGrids/Mesa_ResBurgAllYears_withGrids.shp"
    REGIONS_SHP = "/Users/charlie/Documents/Work/NIJ/Target1/Mesa Data/Mesa_Beats/Mesa_Cleaned_withCrimeData.shp"
    db = EventCollection(EVENT_DATA_DBF,EVENT_DATA_SHP)
    regions = RegionCollection(REGIONS_SHP)
