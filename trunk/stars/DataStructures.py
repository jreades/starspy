# pylint: disable=W0232,W0201
""" This module models the internal data structure for STARS using a custom
subclass of the numpy ndarray."""

from __future__ import with_statement
import pysal
import numpy as np
import threading

# <-- which pysqlite? -->
import sqlite3.dbapi2  as sqlite   # built-in sqlite api
#from pysqlite2 import dbapi2 as sqlite  # for use with Spatialite

# pysqlite2 supplies the buit-in sqlite3 api for python. The same source must be
# compiled differently for use with spatialite, and called in this manner to
# overwrite the built-in.
# Note as well that sqlite3 has a built-in Rtree implementation, but must be
# specially compiled to access it.
# <-- /which pysqlite? -->

#globals

__all__ = ['StarsArray', 'TagDb' ]

class StarsArray(np.ndarray):
    """
    Subclass of numpy ndarray

    support our tagging scheme
    support regular numpy functions
    support time interval tagging

    Scipy docs on subclassing ndarray:
    http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
    """
    # <-- keeping track of instances --> 
    lock = threading.Lock()
    instance_count = 0
    # <-- /keeping track of instances --> 

    def __new__(cls, input_array, info=None ):
        """
        Required for subclassing ndarray.

        When creating a new StarsArray, we can add tags using the 
        info attribute as follows in the examples. Any slice or subarray
        created on the fly will also be of this class, StarsArray, as long as
        it has the two critical functions __new__ and __array_finalize__ as
        written here. Since each slice or subarray is a StarsArray, the info
        attribute ( an object of any type, but implemented in the examples as
        a list) is always associated with its object, and is mutable. 

        Note
        ----

        Creating the info attr in this function does not cause Python any
        trouble. However, python does not like the tag attr. The info attr is
        not inherited from the super class either, since "numpy.ndarray has no
        attribute 'info'".

        Examples
        --------

        >>> arr = np.arange(50)
        >>> obj = StarsArray(arr, info=None)
        >>> slice = StarsArray(obj[:10], info=['1st Quantile'])
        >>> slice.info
        ['1st Quantile']
        >>> cell = obj[1:10]
        >>> cell
        StarsArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        >>> cell.info = ['Region 1']
        >>> cell.info
        ['Region 1']
        >>> cell.info.append('1990')
        >>> cell.info
        ['Region 1', '1990']
        >>> cell.info.remove('1990')
        >>> cell.info
        ['Region 1']
        >>> '1990' in cell.info
        False
        >>> 'Region 1' in cell.info
        True
        >>> cell.info = []
        >>> cell.info
        []


        """
        with StarsArray.lock:
            StarsArray.instance_count += 1
        obj = np.asarray(input_array).view(cls)
        obj.info = info
        return obj

    def __array_finalize__(self, obj):
        """The __init__ method is replaced by __array_finalize__ when 
        subclassing ndarray.
        """

        if obj is None: 
            return
        self.info = getattr(obj, 'info', None)
        self.tagdb = TagDb('/tmp/example')


    def __array_wrap__(self, out_arr, context=None):
        """ We may or may not need this. See ref url for more info."""
        print 'In __array_wrap__:'
        print '   self is %s' % repr(self)
        print '   arr is %s' % repr(out_arr)
        # then just call the parent
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def _clear_tags_(self, obj):
        """
        This provides a way to remove all tags from the info attr.
        This may not be necessary or useful, after all it's easy to empty the
        list on the fly.

        """
        pass

    def add_column_tag(self, col, tag):
        """
        apply a tag to all cells in a column of the array
        """
        #what dtype is a tag? it should be a string

    def add_row_tag(self):    
        "apply tag to all elements of row. look at row_factory method of sqlite instead" 
        pass
    def add_cell_tag(self, row, col, tag):
        """
        apply a tag to specific cell
        this cell is a scalar, which has all the attributes of an array 
        and can be treated as such. Identifying the cell or scalar is done
        with the ndarray methods (slicing, etc.), and specifying the tag in the
        info attribute. Example,  
        cell = obj[1:20]
        cell.info = ['Region 1']
        """
        pass

    def get_tags(self):
        """
        returns tags associated with cell i,j
        We retrieve tags from the StarsArray object itself by querying its
        info attr. We may need a method of querying the namespace for all
        StarsArray objects, their info attrs, and commonalities. We could
        collect each info attr and place them in a set, which would
        eliminate redundancies, for quicker processing.
        """
        return self.info


class TagDb:
    """Class for storage and retrieval of Tag objects using python built-in
    sqlite or spatialite. 

    Use composition in the StarsArray class to create a TagDb associated
    with the StarsArray, or we might want to make this class part of the 
    larger Data Structure (StarsArray) instead of a separate class.
    """
    import datetime, dateutil 

    def __init__(self, datafile):
        """Instantiate the sqlite3 tag database object.
        
        Parameters
        ----------
        datafile : a source of data that pysal.open() can handle

        Attributes
        ----------
        TBD

        Examples
        --------

        >>> import pysal
        >>> data = pysal.open('NIJ/Final_Data/Tempe_Crime_Clipped.dbf')
        >>> dates = data.by_col['RPTDATE']  
        >>> dates[1]
        datetime.date(2007, 1, 31)
        >>> 

        """
        # Read in a data file
        data = pysal.open(datafile)
        sqlite.enable_callback_tracebacks(flag=True)    #for dev, set to False to turn off

        sqlite.PARSE_COLNAMES = True   #returns 2 for detect_types option to connection creation
        self.con = sqlite.connect(":memory:", detect_types = 2 )    # always remains in memory
        #self.con_alt = sqlite.connect("", detect_types = 2 )  # temp db may be flushed to disk if db becomes too large
        #see http://www.sqlite.org/inmemorydb.html for more info 

        #NO need to create cursor --> execute(), executemany(), and executescript() methods of the Connection object creates the cursor implicitly.
        #self.cursor = self.cxn.cursor()
        
        self.dates = self.data.by_col[datecol]
        
    def week(x):
        """
        Returns the calendar week of a given datetime.date object.

        Parameters
        ----------
        x : datetime.date object

        """
        calweek = x.isocalendar()[1]
        return calweek

    def quarter(x):
        """Map a datetime.date object to its quarter.
        Given an instance x of datetime.date, (x.month-1)//3 will give you the quarter 
        (0 for first quarter, 1 for second quarter, etc -- add 1 if you need to count from 1 instead
        
        Parameters
        ----------
        x : datetime.date object
        
        """
        Q = (x.month - 1)//3 + 1  
        return Q
        

    def add_tag(self, tag):
        """Add a tag to the table."""
        if not tag in self.table:
            self.con.execute("""insert into self.table values 
                    ("""+tag+""")""")
            self.con.commit()

    def get_tags(self):
        """Retrieve tags matching query."""
        taglist = self.con.execute('select * from'+ self.table)
        return taglist
    
    def make_timeslice(self):
        """Create tags matching time query."""
        pass

    def index_datetimes(self):
        """Read the date time fields and create an index for quick lookup."""
        # use sql.datetime


    def get_timetags(self):
        """Retrieve tags matching time query."""
        pass


    def remove_tag(self, tag):
        """Remove a tag from the table."""
        self.con.execute("""delete from table ("""+tag+""")""")
        self.con.commit()

    def close(self):
        """Close the sqlite cursor connection. Call on closing STARS. If using
        in-memory databases, this may not be needed as they're automatically closed."""
        self.con.close()



class Dimension:
    """
    Dimension has tags associated with it

    eg. states - al, cal, ...wy
    eg. time 1941Q1....2001Q4
    """
    def __init__(self):
        self.tags = []

    def open(self):
        """Phony method."""
        pass
    def close(self):
        """Phony method."""
        pass


def _test():
    "Doc test"
    import doctest
    doctest.testmod(verbose=True)    

if __name__ == '__main__':
    #open your example data with pysal
    
    _test()


