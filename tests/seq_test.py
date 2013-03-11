import dj_eden_app.seq as seq
import unittest
from itertools import islice, count

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

if __name__ == '__main__':
	unittest.main()

