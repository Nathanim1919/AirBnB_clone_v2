"""
Module Name: tests/test_console.py
Description: The module tests the command interpreter new functionalities
"""
import json
import os
import unittest
from console import HBNBCommand
from io import StringIO
from models.engine.file_storage import FileStorage
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

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                     "Not supported for database")
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
            self.assertIn(test_key, FileStorage().all())

        with open('file.json', mode='r', encoding='utf-8') as f:
            obj = json.load(f)
            num_obj = len(obj)
        self.assertLess(0, num_obj)

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                     "Not supported for database")
    def test_create_kwargs_none(self):
        """
        Test that none value raises an exception
        """
        with self.assertRaises(NameError):
            HBNBCommand().onecmd('create User name=none')

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                     "Not supported for database")
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
            objs = FileStorage().all()
            self.assertIn(test_key, objs.keys())
            self.assertIn('city_id', objs[test_key].to_dict())
            self.assertIn('user_id', objs[test_key].to_dict())
            self.assertIn('max_guest', objs[test_key].to_dict())
            self.assertIn('number_rooms', objs[test_key].to_dict())
            self.assertIn('latitude', objs[test_key].to_dict())
            self.assertIn('longitude', objs[test_key].to_dict())
