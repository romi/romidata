import tempfile
import unittest
from dirsync import sync

from romidata import FSDB

DATABASE_LOCATION = "testdata"

class TemporaryCloneDB(object):
    """
    Class for doing tests on a copy of a local DB.

    Parameters
    __________
        db_location : str
            location of the source database

    Attributes
    __________
        tmpdir : tempfile.TemporaryDirectory
    """
    def __init__(self, db_location):
        self.tmpdir = tempfile.TemporaryDirectory()
        sync(db_location, self.tmpdir.name, action="sync")

    def __del__(self):
        self.tmpdir.cleanup()

class DBTestCase(unittest.TestCase):
    def __del__(self):
        try:
            self.db.disconnect()
        except:
            return

    def get_test_db(self):
        self.tmpclone = TemporaryCloneDB(DATABASE_LOCATION)
        self.db = FSDB(self.tmpclone.tmpdir.name)
        self.db.connect()
        return self.db
