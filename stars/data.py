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

        #>>> datecol = ['RPTDATE']
        #>>> dates = data.by_col(datecol)  

        Python / PySAL recognizes common date formats and parses them into
        datetime.date objects

        #>>> dates[1]
        #datetime.date(2007, 1, 31)
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
    the whole db subject to query all the time. ??? """
    
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
        >>> dbf = 'examples/mesa/Export_Output.dbf'
        >>> data = pysal.open(dbf)
        >>> mesa = StarsDb(dbf)
        ADD
        AS
        EXISTS
        IF
        IN
        IS
        NO
        NOT
        OR
        PRIMARY
        <BLANKLINE>
        Database written.
        >>> query = mesa.cur.execute('SELECT * FROM events')
        >>> r = query.fetchone() 
        >>> len(r)
        22
        >>> r[21]
        datetime.date(2008, 6, 19)
        >>> query2 = mesa.cur.execute('SELECT DateFix FROM events WHERE DateFix LIKE "2007%"') 
        >>> query3 = mesa.cur.execute('SELECT * FROM events WHERE DateFix LIKE "2007%"') 
        >>> s = query2.fetchall()
        >>> type(s)
        <type 'list'>
        >>> 

        """
        # write a query that returns all rows where 'FixDate' is in between a set of dates

        #dbf2sql(dbf)
        #self.con = sqlite.connect(":memory:", detect_types = 2) #remains in memory 
        #self.con = sqlite.connect("", detect_types = 2)   #flushed to disk if too large
        #self.con = sqlite.connect("/tmp/stars_sqlite.db", detect_types = 2) #r/w to disk
        
        EVENTS_TABLE = "events"
        self.db = db = pysal.open(dbf)
        self.header = db.header
        self.spec = db.field_spec
        self.info = db.field_info
        self.con = sqlite.connect(":memory:", detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        self.con.row_factory = sqlite.Row
        self.cur = self.con.cursor()
        self.cur.execute(createTableSQL(EVENTS_TABLE, db.header, db.field_spec, primaryKey = None))
        insert_sql = "insert into %s values (%s)" % (EVENTS_TABLE,','.join(['?'] * len(db.header)))
        for row in db:
            self.cur.execute(insert_sql, row)
        self.con.commit()
        print "Database written."

        self.con.create_function("toyear", 1, toyear)
        self.con.create_function("tomonth", 1, tomonth)
        self.con.create_function("toquarter", 1, toquarter)
        self.con.create_function("d2qtr",1, awesome)


    def qrecords(self, year, quarter):
        records = self.cur.execute("SELECT d2qtr(DateFix) from events")
        return records.fetchall()
        
    def get_quarterly_records(self, year, quarter):
        """
        Parameters
        ----------
        datecol : datetime.date column in the table
        year : string 
        quarter : string
        
        """
        sql = 'Select * from events WHERE %s LIKE "%s%s"' % (DATE_COL, year, "%")
        query = self.cur.execute(sql)
        lst = query.fetchall()
        result = []
        for row in lst:
            qtr = toquarter(row[DATE_COL])
            if qtr == quarter:
                print qtr, row
                result.append(row)
        return result 

    def build_simple_query(tableName, field_name, filter=None, groupby=None):
        """Builds queries."""
        #we need an API for gathering user inputs
        start = input() #TBD
        end = input()   #TBD


        #self.cur.execute("select

        #Notes: see 11.13.5.4  and 11.13.5.2.2 
        """Futzing around:
        this returns one column
        x.cur.execute('select RPTDATE from events').fetchall()
        """
    
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
def awesome(date):
    "turn date into a year, quarter tuple"
    return date.year, toquarter(date)
def toyear(date):
    return date.year
def tomonth(date):
    return date.month
def toquarter(date):
    return (date.month - 1)//3 + 1

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
    #TODO add date and timestamp support here
    t,s,p = spec
    if t.lower()=='n':
        if p==0:
            return "INTEGER"
        else:
            return "REAL"
    elif t.lower()=='f':
        return "REAL"
    elif t.lower() == 'd':
        return "DATE"
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

def in_quarter(date):
    """sql wrapper that passes datetime.date object to the db cursor"""
    #pseudo code:
    # want to pass a column of dates into a func to create a table JOIN with
    # year and quarter for quicker lookups?
    #first pass month to quarter
    q = quarter(date)
    
    #SELECT * FROM events WHERE 'FixDate'.year == year AND 'FixDate'.quarter

def mapM2Q(date):
    """Accepts a datetime.date object and returns the quarter in which that
    month exists, irrespective of year."""
    q1 = (1,2,3)
    q2 = (4,5,6)
    q3 = (7,8,9)
    q4 = (10,11,12)
    q = date.month  #returns an integer
    if q in q1:
        return 1
    elif q in q2:
        return 2
    elif q in q3:
        return 3
    elif q in q4:
        return 4

def get_quarter(date):
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
    DATE_COL = 'DateFix'
    dbf = 'examples/mesa/Export_Output.dbf'
    #dbf = '/home/stephens/Desktop/Phil_Data/Mesa_Crime_Clipped.dbf'
    x = StarsDb(dbf)
    _test()
