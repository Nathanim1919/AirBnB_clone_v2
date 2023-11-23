#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
from models.base_model import BaseModel
from models.state import State
from models import storage
import os


@unittest.skipIf((os.getenv('HBNB_TYPE_STORAGE') == 'db'),
                 "Only FileStorage test")
class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """ Set up test environment """
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """ Remove storage file at end of tests """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        new.save()
        for obj in storage.all().values():
            temp = obj
        self.assertTrue(temp is obj)

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        new.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to file """
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """ FileStorage save method """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        new.save()
        storage.reload()
        for obj in storage.all().values():
            loaded = obj
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty file """
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._FileStorage__file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        _id = new.to_dict()['id']
        new.save()
        for key in storage.all().keys():
            if key == 'BaseModel' + '.' + _id:
                temp = key
        self.assertEqual(temp, 'BaseModel' + '.' + _id)

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        from models.engine.file_storage import FileStorage
        self.assertEqual(type(storage), FileStorage)

    def test_delete(self):
        """Test that an instance is actually deleted
        """
        new = BaseModel()
        new.save()
        self.assertTrue(new in storage.all().values())
        storage.delete(new)
        self.assertFalse(new in storage.all().values())

        new = State()
        new.save()
        self.assertTrue(new in storage.all().values())
        storage.delete(new)
        self.assertFalse(new in storage.all().values())

    def test_delete_no_arg(self):
        """Test nothing is deleted with no argument"""
        new = State()
        new.save()
        storage.delete()
        self.assertTrue(new in storage.all().values())

    def test_delete_invalid(self):
        """Test excepts raised on invalid argument"""
        with self.assertRaises(AttributeError):
            storage.delete('')

        with self.assertRaises(AttributeError):
            storage.delete({})

    def test_all_return_type(self):
        """Test that dict is returned"""
        result = storage.all()
        self.assertEqual(type(result), dict)

    def test_all_a_class(self):
        """Test listing only a class"""
        new1 = BaseModel()
        new1.save()

        new2 = State()
        new2.save()

        list_ = storage.all(State)
        count = 0
        for obj in list_.values():
            if type(obj) == State:
                count += 1

        self.assertEqual(count, 1)

    def test_all_classes(self):
        """Test that all classes are retrieved"""
        new1 = BaseModel()
        new2 = BaseModel()
        new3 = State()

        new1.save()
        new2.save()
        new3.save()

        list_ = storage.all()
        count = 0
        for obj in list_.values():
            count += 1

        self.assertEqual(count, 3)

    def test_all_invalid(self):
        """Test exception raised on invalid arguments"""
        with self.assertRaises(NameError):
            storage.all(lo)

        new1 = BaseModel()
        new2 = State()

        new1.save()
        new2.save()
        with self.assertRaises(TypeError):
            list_ = storage.all(45)
