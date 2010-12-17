# pylint: disable=W0232,W0201
"""Manages all aspects of running STARS and reading, writing to disk."""

#import os.path



class StarsProject(object):
    """Stars project class."""
    def __init__(self):
        """Put docstring here."""
        #attrs
        #self.projectpath
        #self.history
        #self.sqlite_dbase_list
        #self.sqlite_db_path
        #self.starsarray_list
        #self.datetime_created
        #self.datetime_last_modified
        pass

def _test():
    """ This is a test."""
    import doctest
    doctest.testmod()

def embed_ipython():
    """Embed the ipython interpreter."""
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed()
    ipshell()
    

if __name__ == '__main__':

    _test()

