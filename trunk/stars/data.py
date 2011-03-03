"""Data Table Substitutes for Space-Time Visualization."""
import pysal
import datetime
try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite

__author__ = "Phil Stephens <pastephe@asu.edu>"
__all__ = ['StarsDb','StarsTable']

class StarsTable:
    """Query-able table. Create a new instance for each time period you want to query."""
    
    def __init__(self, starsdb_instance):
        """Create an instance of our Table. A table will be a 'view' or 'query'
        of the StarsDb database. 
             
        Parameters
        ----------
        TBD

        Attributes
        ----------
        TBD

        Examples
        --------
        Pass in parameters

        Use PySAL FileIO to parse the data source

        >>> data = pysal.open(dbf)
        >>> dates = data.by_col(datecol)  

        Python / PySAL recognizes common date formats and parses them into
        datetime.date objects

        >>> dates[1]
        datetime.date(2007, 1, 31)
        >>> 

        """
        
        #self.data = pysal.open(dbf)
        #self.dates = self.data.by_col(datecol)  

        # <------ Create Custom Datetime Intervals ---------->

        #THIS HAS A BUG THAT RETURNS 53 WEEKS FOR EARLY 2005 AND LATE 2009.
        # MAYBE THESE SHOULD BE PROPER FUNCS, @PROPERTY's?

        #self.weeks = [date.isocalendar()[1] for date in self.dates]
        #self.quarters = [(date.month -1) //3 + 1 for date in self.dates]

        # USING GENERATORS 
        #self.quarters = ((date.month -1) //3 + 1 for date in self.dates)
        #self.weeks = (date.isocalendar()[1] for date in self.dates)
         
        #</------ Create Custom Datetime Intervals ---------->

class StarsDb:
    """Reads PySAL DataTable and writes to a (py)sqlite database. Once written,
    we use the StarsTbl class to query or view the data, so that we don't have
    the whole db subject to query all the time."""
    
    def __init__(self, dbf):
        """Create an instance of our Database.
             
        Parameters
        ----------
        dbf : a source of data that pysal.open() can handle

        Attributes
        ----------
        TBD

        Examples
        --------

        >>> import pysal
        >>> dbf = 'examples/us48join.dbf'
        >>> data = pysal.open(dbf)
        >>> x = StarsDb(dbf)
        >>> 

        """
        #dbf2sql(dbf)
        self.data = pysal.open(dbf)
        #self.con = sqlite.connect(":memory:", detect_types = 2) #remains in memory 
        #self.con = sqlite.connect("", detect_types = 2)   #flushed to disk if too large
        #self.con = sqlite.connect("/tmp/stars_sqlite.db", detect_types = 2) #r/w to disk
        
        EVENTS_TABLE = "events"
        db = pysal.open(dbf)
        self.con = sqlite.connect(":memory:", detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        self.con.row_factory = sqlite.Row
        #self.cur = self.con.cursor()
        self.cur = cur = self.con.execute(createTableSQL(EVENTS_TABLE, db.header, db.field_spec, primaryKey = None))
        insert_sql = "insert into %s values (%s)" % (EVENTS_TABLE,','.join(['?'] * len(db.header)))
        for row in db:
            cur.execute(insert_sql, row)
        self.con.commit()
        print "Database written."







    
    """Convert a dBase file to an Sqlite3 db, table.

    There are default adapters for the date and datetime types in the
    datetime module. They will be sent as ISO dates/ISO timestamps to SQLite.
    The default converters are registered under the name 'date' for
    datetime.date and under the name 'timestamp' for datetime.datetime.  This
    way, you can use date/timestamps from Python without any additional fiddling
    in most cases. The format of the adapters is also compatible with the
    experimental SQLite date/time functions.
    
    analyse the field descriptions, make a CREATE TABLE statement, execute it, and then 
    start doing inserts.
    
    """


def createTableSQL(tableName,header,field_spec,primaryKey = None):
    create_table_sql = "create table IF NOT EXISTS %s (%s)"
    fields = ["%s %s"%(name,spec2type(spec)) for name,spec in zip(header,field_spec)]
    if primaryKey:
        fields.append("PRIMARY KEY (%s)"%primaryKey)
    fields = ', '.join(fields)
    fields = fields.upper()
    sql = create_table_sql%(tableName,fields)

    keywords = open('sqlite_keywords.txt').read()
    kwlist = keywords.replace('\n', ',').split(',')
    len(kwlist) == 122
    for item in kwlist:
        if item in sql:
            print item
    #repeat this string replacement as needed since several of the items can not
    #be automatically replaced with something else and still form a coherent sql
    #string, such as "EXISTS"
    sql = sql.replace("CASE", "XCASE")
    return sql

def spec2type(spec):
    #TODO add datetime and timestamp support here
    t,s,p = spec
    if t.lower()=='n':
        if p==0:
            return "INTEGER"
        else:
            return "REAL"
    elif t.lower()=='f':
        return "REAL"
    return "TEXT"


    
# some of these funcs are here to document how things work, they may be
# discarded if integration is more efficient


# Example: Convert file existing_db.db to SQL dump file dump.sql
'''
def wrap_dump(db):
    import sqlite, os
    con = sqlite.connect('existing_db.db')
    with open('dump.sql', 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)
'''


def create_static_window(startdate, enddate):
    """Creates a time window between two datetime.date objects."""    
    window = enddate - startdate
    return window
    

def create_advancing_window(startdate, enddate, increment):
    """Creates a list of datetime.date(s) between two datetime.date objects.
    
    Parameters
    ----------

    startdate : datetime.date object, beginning of observation period
    enddate: datetime.date object, end of observation period
    increment: int, 1 for each day, 7 for each week, etc.

    Returns
    -------
    
    List of dates in a range.
    
    Examples
    --------

    >>>
    >>>
    """    
    interval = []
    day = startdate
    while day < enddate:
        interval.append(day)
        day = day + increment
    return interval

def create_moving_window(origindate, daterange):
    """
    Parameters
    ----------
    
    origindate : datetime.date object, center point of date window
    daterange : int, 1 for every day
    
    Returns
    -------
    
    List of dates in a range.

    Examples
    --------

    >>>
    >>>

    """
    moving_window = []
    increment = datetime.timedelta(1)
    date = origindate
    window = datetime.timedelta(daterange)/2
    day = date - window  
    dayX = date + window 
    while day < dayX:
        moving_window.append(day)
        day = day + increment
    return moving_window


def wrap_combine(date, time):
    """A class method that creates a datetime object by combining the contents
    of a date object, date, and a time object, time."""
    dt = datetime.datetime.combine(date, time)
    return dt

def week(date):
    """
    Returns the calendar week of a given datetime.date object.
    THIS HAS A BUG THAT RETURNS 53 WEEKS FOR EARLY 2005 AND LATE 2009.

    Parameters
    ----------
    date : datetime.date object

    Examples
    --------

    >>>
    >>>
    """
    calweek = date.isocalendar()[1]
    return calweek

def quarter(date):
    """Map a datetime.date object to its quarter.
    Given an instance x of datetime.date, (x.month-1)//3 will give you the quarter 
    (0 for first quarter, 1 for second quarter, etc -- add 1 if you need to count from 1 instead
    
    Parameters
    ----------
    date : datetime.date object
    
    Examples
    --------

    >>>
    >>>
    """
    tmp = (date.month - 1)//3 + 1  
    return tmp

def _test():
    import doctest
    doctest.testmod(verbose=True)
       
if __name__ == '__main__':
    #dbf = 'examples/us48join.dbf'
    dbf = '/home/stephens/Dropbox/stars/trunk/stars/examples/us48join.dbf'
    x = StarsDb(dbf)
    _test()
