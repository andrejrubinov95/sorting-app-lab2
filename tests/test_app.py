import unittest
from main import parse_numbers, run_sort, load_methods


class ParsingTests(unittest.TestCase):
    def test_spaces(self):
        self.assertEqual(parse_numbers('4 -2 0 4'), [4, -2, 0, 4])

    def test_commas(self):
        self.assertEqual(parse_numbers('5, 2, -9'), [5, 2, -9])

    def test_empty(self):
        with self.assertRaises(ValueError):
            parse_numbers('  ')

    def test_invalid(self):
        with self.assertRaises(ValueError):
            parse_numbers('1 two 3')


class SortingTests(unittest.TestCase):
    def test_submodule_connected(self):
        self.assertIn('bubble', load_methods())
        self.assertIn('insertion', load_methods())

    def test_all_algorithms(self):
        source = [10, -1, 7, 3, 7, 0]
        for method in load_methods():
            with self.subTest(method=method):
                _, result = run_sort(source, method)
                self.assertEqual(result, [-1, 0, 3, 7, 7, 10])
                self.assertEqual(source, [10, -1, 7, 3, 7, 0])

    def test_empty_list(self):
        for method in load_methods():
            with self.subTest(method=method):
                self.assertEqual(run_sort([], method)[1], [])

    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            run_sort([3, 2, 1], 'unknown')


if __name__ == '__main__':
    unittest.main()
