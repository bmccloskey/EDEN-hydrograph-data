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

def null_to_nan(seq, columns):
	"generator over a sequence, replace nulls in specified columns to NaN"
	nan = float("nan")
	for t in seq:
		t_l = list(t)
		changed = False
		for c in columns:
			if t_l[c] is None:
				t_l[c] = nan
				changed = True
		if changed:
			yield tuple(t_l)
		else:
			yield t

def merge_sorted(s1, s2):
	"""
	Merge two sequences of tuples (or whatever), which must be sorted on tuple[0].
	Unequal keys will pretend the unmatched sequence produced a tuple of Nones.
	"""
	iter1 = iter(s1)
	iter2 = iter(s2)
	def next_tuple(s):
		try:
			return s.next()
		except StopIteration:
			return None
	def null_fill(t):
		return len(t) * (None,)
	t1 = next_tuple(iter1)
	fill_1 = null_fill(t1 or [])
	t2 = next_tuple(iter2)
	fill_2 = null_fill(t2 or [])
	while t1 and t2:
		if t1[0] < t2[0]:
			yield t1 + fill_2[1:]
			t1 = next_tuple(iter1)
		elif t1[0] > t2[0]:
			yield t2[:1] + fill_1[1:] + t2[1:]
			t2 = next_tuple(iter2)
		else:
			yield t1 + t2[1:]
			t1 = next_tuple(iter1)
			t2 = next_tuple(iter2)
	# run out the tail
	while t1:
		yield t1 + fill_2[1:]
		t1 = next_tuple(iter1)
	while t2:
		yield t2[:1] + fill_1[1:] + t2[1:]
		t2 = next_tuple(iter2)


if __name__ == "__main__":
	vv = list(collapse(lambda x : x, [0, 1, 2, 3, 0, 4, 0, 0, 5, 0, 6, 0, 0, 0, 0, 0, 7]))
	print(vv)

