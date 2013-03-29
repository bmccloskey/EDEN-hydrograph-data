import dj_eden_app.seq as seq
import unittest
from itertools import islice, count
from types import GeneratorType

import datetime

def ident(x):
	return x

def snn(x):
	"second not none"
	return x[1] is not None

class TestCollapse(unittest.TestCase):
	def test_collapse_1(self):
		inlist = [0, 1, 2, 3, 0, 4, 0, 0, 5, 0, 0, 0, 6, 0, 7]
		output = seq.collapse(lambda x: x, inlist)
		self.assertEquals([0, 1, 2, 3, 0, 4, 0, 5, 0, 6, 0, 7], list(output))

	def test_collapse_2(self):
		inlist = [0, 0, 0, 0]
		output = seq.collapse(ident, inlist)
		self.assertEquals([0], list(output))

	def test_collapse_3(self):
		inlist = []
		output = seq.collapse(ident, inlist)
		self.assertEquals([], list(output))

	def test_collapse_4(self):
		inlist = [("a", 1), ("b", 0), ("c", 0), ("d", 1), ("e", None), ("f", None), ("g", True)]
		output = seq.collapse(snn, inlist)
		self.assertEquals(["a", "b", "c", "d", "e", "g"], [x[0] for x in output])

class TestPrepend(unittest.TestCase):
	def test_single(self):
		outlist = list(seq.prepend(self, []))
		self.assertEquals([self], outlist)

	def test_normal(self):
		outlist = seq.prepend(1, [2, 3, 4, 5])
		self.assertEquals(list(outlist), [1, 2, 3, 4, 5])

	def test_infinite(self):
		outgen = seq.prepend(100, count(101))
		outlist = list(islice(outgen, 0, 10))
		self.assertEquals(outlist, range(100, 110))

class TestUnique(unittest.TestCase):
	def test_empty(self):
		outlist = seq.unique([]);
		self.assertEquals([], outlist, "empty")

	def test_unchanged(self):
		a = [1, 6, 3, 8]
		outlist = seq.unique(a)
		self.assertEquals(a, outlist, "unchanged")

	def test_changed(self):
		outlist = seq.unique([1, 2, 1, 3, 2, 5])
		self.assertEquals([1, 2, 3, 5], outlist, "changed")

	def test_changed_obj(self):
		outlist = seq.unique([self, "abc", self, "def", "abc"])
		self.assertEquals([self, "abc", "def"], outlist, "objects")

def is_nan(x):
	return type(x) is float and x != x

class TestNullToNan(unittest.TestCase):
	def test_empty_case(self):
		ipt = [()]
		expected = [()]
		output = list(seq.null_to_nan(ipt, []))
		self.assertEqual(output, expected)

	def test_null_case_1(self):
		ipt = [(1, None),
				(2, 400),
				(3, None)]
		expected = [(1, None),
				(2, 400),
				(3, None)]
		gen = seq.null_to_nan(ipt, [])
		self.assertIsInstance(gen, GeneratorType)
		output = list(gen)
		self.assertEquals(output, expected)

	def test_base_case_1(self):
		ipt = [(1, None, None, 42.1),
				(2, 400, 99.1, None),
				(3, None, 98.6, "nan")]
		for i, t in enumerate(seq.null_to_nan(ipt, [1, 3])):
			for j, x in enumerate(t):
				if j in [1, 3] and ipt[i][j] is None:
					self.assertTrue(is_nan(x))
				else:
					self.assertEquals(x, ipt[i][j])

class TestMergeSorted(unittest.TestCase):
	def test_simple_case(self):
		seq1 = [
			(1, 101, "one"),
			(3, 301, "three"),
			(4, 401, "four"),
			(5, 501, "five")]
		seq2 = [
			(0, 1, "zero"),
			(2, 202, "two"),
			(4, 402, "four"),
			(6, 602, "six")]

		expected = [
				(0, None, None, 1, "zero"),
				(1, 101, "one", None, None),
				(2, None, None, 202, "two"),
				(3, 301, "three", None, None),
				(4, 401, "four", 402, "four"),
				(5, 501, "five", None, None),
				(6, None, None, 602, "six")]

		output = seq.merge_sorted(seq1, seq2)

		self.assertEqual(list(output), expected)

	def test_dates(self):
		seq1 = [
			(datetime.datetime(1999, 4, 1, 0, 0, 1), 101, "one"),
			(datetime.datetime(1999, 4, 1, 0, 0, 3), 301, "three"),
			(datetime.datetime(1999, 4, 1, 0, 0, 4), 401, "four"),
			(datetime.datetime(1999, 4, 1, 0, 5, 0), 501, "five")]
		seq2 = [
			(datetime.datetime(1997, 8, 1, 0, 0, 0), 1, "zero"),
			(datetime.datetime(1999, 4, 1, 0, 0, 2), 202, "two"),
			(datetime.datetime(1999, 4, 1, 0, 0, 4), 402, "four"),
			(datetime.datetime(1999, 6, 1, 0, 5, 0), 602, "six")]

		expected = [
				(datetime.datetime(1997, 8, 1, 0, 0, 0), None, None, 1, "zero"),
				(datetime.datetime(1999, 4, 1, 0, 0, 1), 101, "one", None, None),
				(datetime.datetime(1999, 4, 1, 0, 0, 2), None, None, 202, "two"),
				(datetime.datetime(1999, 4, 1, 0, 0, 3), 301, "three", None, None),
				(datetime.datetime(1999, 4, 1, 0, 0, 4), 401, "four", 402, "four"),
				(datetime.datetime(1999, 4, 1, 0, 5, 0), 501, "five", None, None),
				(datetime.datetime(1999, 6, 1, 0, 5, 0), None, None, 602, "six")]

		output = seq.merge_sorted(seq1, seq2)

		self.assertEqual(list(output), expected)

	def test_empty_left(self):
		seq1 = []
		seq2 = [(1, 33),
				(5, 44),
				(101, 55)]
		expected = [
				(1, 33),
				(5, 44),
				(101, 55)]
		output = seq.merge_sorted(seq1, seq2)

		self.assertEqual(list(output), expected)

	def test_empty_right(self):
		seq1 = [(1, 33),
				(5, 44),
				(101, 55)]
		seq2 = []
		expected = [
				(1, 33),
				(5, 44),
				(101, 55)]
		output = seq.merge_sorted(seq1, seq2)

		self.assertEqual(list(output), expected)

	def test_preserve_nan(self):
		nan = float('NaN')
		seq1 = [(1, nan),
				(5, None),
				(101, 55)]
		seq2 = [(1, 11.1),
				(200.2, 200.4)]
		expected = [
				(1, nan, 11.1),
				(5, None, None),
				(101, 55, None),
				(200.2, None, 200.4)]
		output = seq.merge_sorted(seq1, seq2)

		self.assertEqual(list(output), expected)

if __name__ == '__main__':
	unittest.main()

