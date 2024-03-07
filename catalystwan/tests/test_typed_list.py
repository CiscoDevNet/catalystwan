# Copyright 2023 Cisco Systems, Inc. and its affiliates

# type: ignore
import copy
import unittest
from unittest import TestCase

from attr import define  # type: ignore
from parameterized import parameterized

from catalystwan.dataclasses import DataclassBase, Device, User
from catalystwan.exceptions import InvalidOperationError
from catalystwan.typed_list import DataSequence, TypedList


@define
class FakeUser(DataclassBase):
    name: str
    weight: float


class TestTypedList(TestCase):
    def setUp(self):
        self.u = User(username="User1")
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")
        self.users = [u1, u2, u3]
        self.typed_list = TypedList(User, self.users)

    @parameterized.expand([(str, []), (int, [1, 2, 3]), (User, [User("User1")])])
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

    @parameterized.expand(
        [
            (str, ["1"], 1),
            (int, [1, 2, 3], 3),
            (User, None, 0),
            (User, [User(username="User1")], 1),
            (User, [User(username="User1"), User(username="User2")], 2),
        ]
    )
    def test_len(self, _type, iterable, length):
        # Arrange, Act
        output_length = len(TypedList(_type, iterable))

        # Assert
        self.assertEqual(output_length, length)

    @parameterized.expand(
        [
            (str, ["1"], "1"),
            (int, [1, 2, 3], 3),
            (User, [User(username="User1")], User(username="User1")),
            (User, [User(username="User1"), User(username="User2")], User(username="User1")),
        ]
    )
    def test_contains_positive(self, _type, iterable, other):
        # Arrange, Act
        typed_list = TypedList(_type, iterable)

        # Assert
        self.assertTrue(other in typed_list)

    @parameterized.expand(
        [
            (str, ["1"], "2"),
            (int, [1, 2, 3], 4),
            (User, [User(username="User1")], User(username="User2")),
            (User, [User(username="User1"), User(username="User2")], User(username="User3")),
        ]
    )
    def test_negative(self, _type, iterable, other):
        # Arrange, Act
        typed_list = TypedList(_type, iterable)

        # Assert
        self.assertFalse(other in typed_list)

    @parameterized.expand(
        [
            (1, User(username="User2")),
            (slice(1, 3, 1), TypedList(User, [User(username="User2"), User(username="User3")])),
        ]
    )
    def test_get_item(self, index, output):
        self.assertEqual(self.typed_list[index], output)

    @parameterized.expand([(User(username="User1"),), (TypedList(User, [User("User3")]),)])
    def test_eq_negative(self, other):
        self.assertFalse(self.users == other)

    def test_eq_false_sort(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        # Act, Assert
        self.assertFalse(self.users == [u1, u3, u2])

    def test_eq(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        # Act, Assert
        self.assertTrue(self.users == [u1, u2, u3])

    def test_set_item(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        users = TypedList(User, [u1, u2])

        # Act
        users[1] = u3

        # Assert
        self.assertEqual(users[1], u3)
        self.assertEqual(users[0], u1)
        with self.assertRaises(IndexError):
            users[2]
        self.assertNotEqual(users[1], u2)
        with self.assertRaises(TypeError):
            users[1] = 2

    def test_insert(self):
        # Arrange
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")

        users = TypedList(User, [u1, u2])

        # Act
        users.insert(1, u3)

        # Assert
        self.assertEqual(users[0], u1)
        self.assertEqual(users[1], u3)
        self.assertEqual(users[2], u2)
        with self.assertRaises(IndexError):
            users[3]
        self.assertNotEqual(users[1], u2)
        with self.assertRaises(TypeError):
            users.insert(1, "2")

    @parameterized.expand(
        [
            (TypedList(str, ["A", "B"]), TypedList(str, ["C"]), False, TypedList(str, ["A", "B", "C"])),
            (TypedList(int, [1, 2]), TypedList(int, [5]), False, TypedList(int, [1, 2, 5])),
            (TypedList(str, ["Z"]), TypedList(int, [9]), True, None),
        ]
    )
    def test_add(self, term1, term2, raises, expected_result):
        if raises:
            with self.assertRaises(TypeError):
                observed_result = term1 + term2
        else:
            observed_result = term1 + term2
            assert observed_result == expected_result

    @parameterized.expand(
        [
            (TypedList(str, ["A", "B"]), TypedList(str, ["C"]), False, TypedList(str, ["A", "B", "C"])),
            (TypedList(int, [1, 2]), TypedList(int, [5]), False, TypedList(int, [1, 2, 5])),
            (TypedList(str, ["Z"]), TypedList(int, [9]), True, None),
        ]
    )
    def test_iadd(self, term1, term2, raises, expected_result):
        if raises:
            with self.assertRaises(TypeError):
                term1 += term2
        else:
            term1 += term2
            assert term1 == expected_result


class TestDataSequence(TestCase):
    def setUp(self):
        self.u = User(username="User1")
        u1 = User(username="User1")
        u2 = User(username="User2")
        u3 = User(username="User3")
        self.users = [u1, u2, u3]
        self.data_sequence = DataSequence(User, self.users)

    @parameterized.expand(
        [
            (User, [], []),
            (User, None, []),
            (User, [User(username="User1")], [User(username="User1")]),
            (Device, [], []),
        ]
    )
    def test_init(self, _type, items, data):
        # Arrange, Act
        data_seq = DataSequence(_type, items)

        # Assert
        self.assertEqual(data_seq.data, data)

    def test_init_exception(self):
        # Arrage, Act, Assert
        with self.assertRaises(TypeError):
            DataSequence(str, ["1, 2"])

    @parameterized.expand(
        [
            (
                DataSequence(User, [User(username="A")]),
                DataSequence(User, [User(username="B")]),
                False,
                DataSequence(User, [User(username="A"), User(username="B")]),
            ),
            (
                DataSequence(User, [User(username="A")]),
                DataSequence(FakeUser, [FakeUser(name="B", weight=99.9)]),
                True,
                None,
            ),
        ]
    )
    def test_add(self, term1, term2, raises, expected_result):
        if raises:
            with self.assertRaises(TypeError):
                observed_result = term1 + term2
        else:
            observed_result = term1 + term2
            assert observed_result == expected_result

    @parameterized.expand(
        [
            (
                DataSequence(User, [User(username="A")]),
                DataSequence(User, [User(username="B")]),
                False,
                DataSequence(User, [User(username="A"), User(username="B")]),
            ),
            (
                DataSequence(User, [User(username="A")]),
                DataSequence(FakeUser, [FakeUser(name="B", weight=99.9)]),
                True,
                None,
            ),
        ]
    )
    def test_iadd(self, term1, term2, raises, expected_result):
        if raises:
            with self.assertRaises(TypeError):
                term1 += term2
        else:
            term1 += term2
            assert term1 == expected_result

    def test_single_or_default(self):
        # Arrange, Act
        output = DataSequence(User, [self.u]).single_or_default(default="x")

        # Assert
        self.assertEqual(output, self.u)

    @parameterized.expand(
        [
            (User, [], None),
            (User, [], "Test"),
        ]
    )
    def test_single_or_default_empty(self, _type, items, default_value):
        # Arrange
        data_seq = DataSequence(_type, items)

        # Act
        output = data_seq.single_or_default(default=default_value)

        # Assert
        self.assertEqual(output, default_value)

    def test_single_or_default_big_array(self):
        # Arrange
        data_seq = DataSequence(User, self.users)

        # Act, Assert
        with self.assertRaises(InvalidOperationError):
            data_seq.single_or_default()

    @parameterized.expand(
        [
            (None, []),
            ("DoesNotExists", []),
            ("User1", [User("User1")]),
        ]
    )
    def test_filter_single_attribute(self, attribute, users):
        # Arrange
        correct_seq = DataSequence(User, users)

        # Act
        output = self.data_sequence.filter(username=attribute)

        # Assert
        self.assertEqual(output, correct_seq)
        self.assertTrue(isinstance(output, DataSequence))

    def test_filter_two_attributes(self):
        # Arrange
        additional_user = User(username="User1", description="ThisOne")
        users = copy.deepcopy(self.data_sequence)
        users.append(additional_user)
        correct_output = DataSequence(User, [additional_user])

        # Act
        output = users.filter(username="User1", description="ThisOne")

        # Assert
        self.assertEqual(output, correct_output)

    def test_filter_exception(self):
        # Arrange, Act, Assert
        with self.assertRaises(AttributeError):
            self.data_sequence.filter(does_not="exists")


if __name__ == "__main__":
    unittest.main()
