"""
Module Name: tests/test_console.py
Description: The module tests the command interpreter new functionalities
"""
import json
import MySQLdb
import os
import unittest
from console import HBNBCommand
from io import StringIO
from models import storage
from tests.test_models.test_engine.test_db_storage import get_current
from unittest.mock import patch


class TestConsole(unittest.TestCase):
    """
    Test console new functionality
    """
    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                     "Not supported for database")
    def setUp(self):
        """
        Cleans file.json and clear up the existing objects
        """
        _FileStorage__objects = {}

        try:
            os.rename('file.json', 'temp')
        except FileNotFoundError:
            pass

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                     "Not supported for database")
    def tearDown(self):
        """
        Restore the previous storage file
        """
        try:
            os.rename('temp', 'file.json')
        except FileNotFoundError:
            pass

    def test_create_kwargs_success(self):
        """
        Test that create method with one keyword argument do not end
        the interpreter
        """
        self.assertFalse(HBNBCommand()
                         .onecmd('create State name="California"'))

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                     "Not supported for database")
    def test_create_kwargs_one(self):
        """
        Test that a state is added with only a name
        """
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create State name="California"')
            result = output.getvalue().strip()
            test_key = f'State.{result}'
            self.assertIn(test_key, storage.all())

        with open('file.json', mode='r', encoding='utf-8') as f:
            obj = json.load(f)
            num_obj = len(obj)
        self.assertLess(0, num_obj)

    def test_create_kwargs_none(self):
        """
        Test that none value raises an exception
        """
        with self.assertRaises(NameError):
            HBNBCommand().onecmd('create User name=none')

    def test_create_kwargs_multiple(self):
        """Test multiple keyword argument on instance creation
        """
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd('create Place city_id="0001" user_id="0001" \
                                 name="My_little_house" number_rooms=4 \
                                 number_bathrooms=2 max_guest=10 \
                                 price_by_night=300 latitude=37.773972 \
                                 longitude=-122.431297')

            result = output.getvalue().strip()
            test_key = f'Place.{result}'
            objs = storage.all()
            self.assertIn(test_key, objs.keys())
            self.assertIn('city_id', objs[test_key].to_dict())
            self.assertIn('user_id', objs[test_key].to_dict())
            self.assertIn('max_guest', objs[test_key].to_dict())
            self.assertIn('number_rooms', objs[test_key].to_dict())
            self.assertIn('latitude', objs[test_key].to_dict())
            self.assertIn('longitude', objs[test_key].to_dict())

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') != 'db'),
                     "Only database supported")
    def test_create_one_parameter(self):
        """Test that a new instance is created and added to the database
        """
        count_0 = get_current('states')

        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="Lagos"')

        count_1 = get_current('states')

        self.assertEqual(count_1, count_0 + 1)

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') != 'db'),
                     "Only database supported")
    def test_create_more_parameter(self):
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

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') != 'db'),
                     "Only database supported")
    def test_create_more_param(self):
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
