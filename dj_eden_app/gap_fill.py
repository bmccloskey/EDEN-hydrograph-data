def bits(v):
    "which elements of v are non-null?"
    return map(lambda x : x is not None, v)

def gap_fill(*ss):
    "fill in data gaps between 3 series, by copying next value to prev column only when data stream changes column"

    prev_bits = len(ss) * [False]
    for i in range(1, len(ss[0])):
        this_bits = bits([s[i] for s in ss])
        if prev_bits != this_bits and any(prev_bits) and any(this_bits):
            prev_idx = next(j for j, x in enumerate(prev_bits) if x)
            this_idx = next(j for j, x in enumerate(this_bits) if x)
            this_val = ss[this_idx][i]
            prev_arr = ss[prev_idx]
            prev_arr[i] = this_val
        prev_bits = this_bits

def gap_fill_gen(gt):
    " fill in the gaps -- gt is a generator of tuples"
    prev_tuple = None
    prev_bits = [False]

    for t in gt:
        if prev_tuple is not None:
            yield prev_tuple
        this_bits = bits(t)
        if prev_bits != this_bits and any(prev_bits) and any(this_bits):
            prev_idx = next(j for j, x in enumerate(prev_bits) if x)
            this_idx = next(j for j, x in enumerate(this_bits) if x)
            this_val = t[this_idx]
            t_as_list = list(t)
            t_as_list[prev_idx] = this_val
            t = tuple(t_as_list)
        prev_bits = this_bits
        prev_tuple = t
    if prev_tuple is not None:
        yield prev_tuple

def revised_group(t, prev_bits, this_bits):
    "copy the first element marked in prev_bits to the first element marked in this_bits"
    if any(prev_bits) and any(this_bits):
        prev_idx = next(j for j, x in enumerate(prev_bits) if x)
        this_idx = next(j for j, x in enumerate(this_bits) if x)
        this_val = t[this_idx]
        t[prev_idx] = this_val
    return t

def gap_fill_by_3(gt):
    " fill in the gaps -- gt is a sequence of tuples, group by 3's leaving out first element."
    prev_tuple = None
    prev_bits = [False]

    for t in gt:
        if prev_tuple is not None:
            yield prev_tuple
        this_bits = bits(t)
        if prev_bits != this_bits and any(prev_bits) and any(this_bits):
            # pick it apart by 3's
            target = list(t)
            for i in range(1, len(t), 3):
                target[i:i + 3] = revised_group(target[i:i + 3], prev_bits[i:i + 3], this_bits[i:i + 3])
            t = tuple(target)
        prev_bits = this_bits
        prev_tuple = t
    if prev_tuple is not None:
        yield prev_tuple

