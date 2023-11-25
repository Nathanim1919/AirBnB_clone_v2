#!/usr/bin/python3
""" """
import MySQLdb
import os
import unittest
from console import HBNBCommand
from io import StringIO
from tests.test_models.test_base_model import test_basemodel
from tests.test_models.test_engine.test_db_storage import get_current
from unittest.mock import patch
from models.city import City


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """ """
        new = self.value()
        new.save()
        self.assertEqual(type(new.state_id), str)

    def test_name(self):
        """ """
        new = self.value()
        new.save()
        self.assertEqual(type(new.name), str)

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
            HBNBCommand().onecmd('create State name="California"')
            state_id = output.getvalue().strip()

            HBNBCommand().onecmd(f'create City state_id="{state_id}" \
                                 name="San_Francisco"')

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
            HBNBCommand().onecmd('create State name="California"')
            state_id = output.getvalue().strip()

            HBNBCommand().onecmd(f'create City state_id="{state_id}" \
                                  name="Fremont"')

        count_states_1 = get_current('states')
        count_city_1 = get_current('cities')

        self.assertEqual(count_states_1, count_states_0 + 1)
        self.assertEqual(count_city_1, count_city_0 + 1)
