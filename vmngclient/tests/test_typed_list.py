import unittest
from unittest import TestCase

from parameterized import parameterized  # type: ignore

from vmngclient.dataclasses import User
from vmngclient.typed_list import TypedList


class TestTypedList(TestCase):
    def setUp(self):
        self.u = User(username="User1")
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")
        self.users = [u1, u2, u3]

    @parameterized.expand([(str, []), (int, [1, 2, 3]), (User, [User(username="User1")])])  # type: ignore
    def test_init(self, _type, iterable):
        # Arrange, Act
        TypedList(_type, iterable)

    @parameterized.expand([(str, [1]), (int, [1, 2, "3"]), (User, [User(username="User1"), 1])])  # type: ignore
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

    @parameterized.expand([(str, [], "TypedList(str, [])"), (int, [1, 2, 3], "TypedList(int, [1, 2, 3])")])
    def test_repr_trival(self, _type, iterable, output):
        # Arrange, Act
        representation = repr(TypedList(_type, iterable))

        # Assert
        self.assertEqual(representation, output)

    # Integration
    def test_repr(self):
        # Arrange
        typed_list = TypedList(User, self.users)
        output = (
            "TypedList(User, ["
            "User(username='User1', password=None, group=[], locale=None, description=None, resource_group=None), "
            "User(username='User2', password=None, group=[], locale=None, description=None, resource_group=None), "
            "User(username='User3', password=None, group=[], locale=None, description=None, resource_group=None)])"
        )
        # Act
        representation = repr(typed_list)

        # Assert
        self.assertEqual(representation, output)


if __name__ == "__main__":
    unittest.main()
