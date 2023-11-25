#!/usr/bin/python3
"""
Module Name: tests/test_models/test_engine/test_db_storage.py
Description: This modules tests the new features associated with
             `DBStorage` class defined in equivalent module
             to this module
"""
import MySQLdb
import os
import unittest
from console import HBNBCommand
from io import StringIO
from models import storage
from models.state import State
from unittest.mock import patch


def get_current(table):
    """Get the number of rows in the table `TABLE`
    """
    USER = os.getenv('HBNB_MYSQL_USER')
    PASSWD = os.getenv('HBNB_MYSQL_PWD')
    DATABASE = os.getenv('HBNB_MYSQL_DB')

    conn = MySQLdb.connect(host='localhost', user=USER, passwd=PASSWD,
                           db=DATABASE)
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table};')
    return cur.rowcount


@unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') != 'db'),
                 "Only for DBstorage")
class TestDBStorage(unittest.TestCase):
    """A definition of `TestDBStorage` for testing
    """
    def setUp(self):
        """Set the database cursor for use
        """
        # self.cur = TestDBStorage.cur
        # self.cur.execute('CREATE DATABASE IF NOT EXISTS hbnb_test_db;')

    def tearDown(self):
        """Clean up the database
        """
        # self.cur.execute('DELETE FROM hbnb_test_db.states;')

    def test_console_create_one_parameter(self):
        """Test that a new instance is created and added to the database
        """
        count_0 = get_current('states')

        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="Lagos"')

        count_1 = get_current('states')

        self.assertEqual(count_1, count_0 + 1)

    def test_console_create_more_parameter(self):
        """
        Test that a class (table) with more than a parameter is added
        to the database
        """
        count_states_0 = get_current('states')
        count_city_0 = get_current('cities')

        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Kwara"')
            state_id = output.getvalue().strip()

            HBNBCommand().onecmd(f'create City state_id="{state_id}" \
                                 name="Ilorin"')

        count_states_1 = get_current('states')
        count_city_1 = get_current('cities')

        self.assertEqual(count_states_1, count_states_0 + 1)
        self.assertEqual(count_city_1, count_city_0 + 1)

    def test_console_create_more_parameter(self):
        """Test that a value with "_" is parsed and added
        """
        count_states_0 = get_current('states')
        count_city_0 = get_current('cities')

        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="Oyo"')
            state_id = output.getvalue().strip()

            HBNBCommand().onecmd(f'create City state_id="{state_id}" \
                                  name="Oyo_town"')

        count_states_1 = get_current('states')
        count_city_1 = get_current('cities')

        self.assertEqual(count_states_1, count_states_0 + 1)
        self.assertEqual(count_city_1, count_city_0 + 1)
