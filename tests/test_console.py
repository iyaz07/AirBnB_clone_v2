#!/usr/bin/python3
"""
Tests the basic functionalities of the console file
"""

from console import HBNBCommand as cons
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import sys
import unittest
from io import StringIO
import MySQLdb


class TestConsole(unittest.TestCase):
    """
    Class used to test the console
    """
    @staticmethod
    def screen_output():
        """
        Function used to save stdout in a variable
        """
        out_screen = StringIO()
        sys.stdout = out_screen
        return out_screen

    def test_create(self):
        """
        Tests the create function of the console
        """
        scr_out = screen_output()
        cons.do_create()
        self.assertEqual(scr_out.getvalue(), "** class name missing **\n")
        scr_out.close()

        scr_out = screen_output()
        cons.do_create("bad class")
        self.assertEqual(scr_out.getvalue(), "class doesn't exist **\n")
        scr_out.close()
