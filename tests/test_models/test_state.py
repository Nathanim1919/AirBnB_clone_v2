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
from models.state import State


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ """
        new = self.value()
        new.save()
        self.assertEqual(type(new.name), str)

    def test_create_kwargs_success(self):
        """
        Test that create method with one keyword argument do not end
        the interpreter
        """
        self.assertFalse(HBNBCommand()
                         .onecmd('create State name="California"'))

    def test_create_kwargs_none(self):
        """
        Test that none value raises an exception
        """
        with self.assertRaises(NameError):
            HBNBCommand().onecmd('create User name=none')

    @unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') != 'db'),
                     "Only database supported")
    def test_create_one_parameter(self):
        """Test that a new instance is created and added to the database
        """
        count_0 = get_current('states')

        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="California"')

        count_1 = get_current('states')

        self.assertEqual(count_1, count_0 + 1)
