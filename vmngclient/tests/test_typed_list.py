import unittest
from unittest import TestCase, mock
from vmngclient.data_sequence import TypedList
from parameterized import parameterized
from vmngclient.data_sequence import TypedList

class TestTypedList(TestCase):
    def setUp(self):
        pass
    
    
    @parameterized.expand([
        (str, []), (int, [1, 2, 3])
    ])
    def test_init(self, _type, iterable):
        # Arrange, Act
        TypedList(_type, iterable)
        
    @parameterized.expand([
        (str, [1]), (int, [1, 2, "3"])
    ])
    def test_init_type_error(self, _type, iterable):
        # Arrange, Act, Assert
        with self.assertRaises(TypeError):
            TypedList(_type, iterable)
    
    def test_init_no_args(self):
        # Arrange, Act, Assert
        with self.assertRaises(TypeError):
            TypedList() 

    def test_init_only_type(self):
        # Arrange, Act, Assert
        TypedList(str)
        
    @parameterized.expand([
        (str, []), (int, [1, 2, 3])
    ])
    def test_init(self, _type, iterable):
        # Arrange, Act
        represenatation = TypedList(_type, iterable)
        
    def test_filter(self):
        
        
if __name__ == "__main__":
    unittest.main()
