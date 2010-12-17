# pylint: disable=W0232,W0201
""" This module models the internal data structure for STARS using a custom
subclass of the numpy ndarray."""

from __future__ import with_statement
import numpy as np
#import threading
import sqlite3

#globals

__all__ = ['DataStructures']

class StarsArray(np.ndarray):
    """
    Subclass of numpy ndarray

    support our tagging scheme
    support regular numpy functions

    Scipy docs on subclassing ndarray:
    http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
    """
    #lock = threading.Lock()
    #instance_count = 0

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
        #with StarsArray.lock:
        #    StarsArray.instance_count += 1
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
        """
        apply a tag to all cells in a row of the array
        """
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

class TagDb(object):
    """Class for storage and retrieval of Tag objects using python built-in
    sqlite."""

    def __init__(self, path):
        """Instantiate the sqlite3 tag database object."""
        self.connection = sqlite3.connect(path)
        self.cursor = self.__connect__()
        self.table = self.__create_table__()
        

    def __connect__(self):
        """Create cursor object."""
        cursor = self.connection.cursor()
        return cursor

    def __create_table__(self):
        """Set up the initial table."""
        self.cursor.execute('''create table Tags (row, col, dim, text)''')
        self.connection.commit()

    def close(self):
        """Close the sqlite cursor connection. Call on closing STARS."""
        self.cursor.close()

    def add_tag(self, tag):
        """Add a tag to the table."""
        if not tag in self.table:
            self.cursor.execute("""insert into self.table values 
                    ("""+tag+""")""")
            self.connection.commit()

    def get_tags(self):
        """Retrieve tags."""
        taglist = self.cursor.execute('select * from'+ self.table)
        return taglist

    def remove_tag(self, tag):
        """Remove a tag from the table."""
        self.cursor.execute("""delete from table ("""+tag+""")""")
        self.connection.commit()

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
    """ This is a test."""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()


