import collections

def collapse(pred, seq):
	"""
	Produce a sub-sequence of seq, where no two consecutive elements 
	fail to satisfy predicate pred
	"""
	prevP = True
	for v in seq:
		thisP = pred(v)
		if thisP or prevP:
			yield v
		prevP = thisP

def prepend(item, seq):
	yield item
	for i in seq:
		yield i

def unique(seq):
	"The unique elements of SEQ, in the input order. Not suitable for infinite sequences."
	od = collections.OrderedDict([(x, 1) for x in seq])
	return od.keys()

if __name__ == "__main__":
	vv = list(collapse(lambda x : x, [0, 1, 2, 3, 0, 4, 0, 0, 5, 0, 6, 0, 0, 0, 0, 0, 7]))
	print(vv)



