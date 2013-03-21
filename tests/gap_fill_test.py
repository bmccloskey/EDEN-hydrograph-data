from dj_eden_app.gap_fill import gap_fill, gap_fill_gen, gap_fill_by_3

import unittest

class TestGapFill(unittest.TestCase):

    def test_base_case(self):
        ss = [[100, 101, 102, None, None],
              [None, None, None, 103, 104],
              [None, None, None, None, None]]
        gap_fill(*ss)
        self.assertEquals(ss,
             [[100, 101, 102, 103, None],
              [None, None, None, 103, 104],
              [None, None, None, None, None]]
        )

    def test_base_case_gen_minimal(self):
        ssz = zip([100, None],
                  [None, 101])
        gfg = gap_fill_gen(ssz)
        l = list(gfg)
        self.assertEquals(l,
                          [(100, None),
                           (101, 101)]
                          )

    def test_base_case_gen(self):
        ssz = zip([100, 101, 102, None, None],
                  [None, None, None, 103, 104],
                  [None, None, None, None, None])
        gfg = gap_fill_gen(ssz)
        l = list(gfg)
        self.assertEquals(l,
                          [(100, None, None),
                           (101, None, None),
                           (102, None, None),
                           (103, 103, None),
                           (None, 104, None)]
                          )

    def test_base_case_by_3(self):
        ssz = [('date', 100, None, None, None, None, None),
              ('date', 101, None, None, 0, None, None),
              ('date', None, 102, None, 0, None, None),
              ('date', 103, None, None, None, None, None),
              ('date', None, None, 104, None, None, 1),
              ('date', None, None, 105, None, None, 2),
              ('date', None, None, 106, None, None, None),
              ]
        gfg = gap_fill_by_3(ssz)
        l = list(gfg)
        expected = [
              ('date', 100, None, None, None, None, None),
              ('date', 101, None, None, 0, None, None),
              ('date', 102, 102, None, 0, None, None),
              ('date', 103, 103, None, None, None, None),
              ('date', 104, None, 104, None, None, 1),
              ('date', None, None, 105, None, None, 2),
              ('date', None, None, 106, None, None, None),
              ]
        self.assertEquals(l, expected)

    def test_empty_run(self):
        ss = [[100, 101, None, None, None],
              [None, None, None, 103, 104],
              [None, None, None, None, None]]
        gap_fill(*ss)
        self.assertEquals(ss,
             [[100, 101, None, None, None],
              [None, None, None, 103, 104],
              [None, None, None, None, None]]
        )

    def test_switch(self):
        ss = [[100, 101, None, None, None],
              [None, None, 102, None, None],
              [None, None, None, 103, 104]]
        gap_fill(*ss)
        self.assertEquals(ss,
             [[100, 101, 102, None, None],
              [None, None, 102, 103, None],
              [None, None, None, 103, 104]]
        )

    def test_zeros(self):
        ss = [[0, 0, None, None, None],
              [None, None, 0, None, None],
              [None, None, None, 0, 0]]
        gap_fill(*ss)
        self.assertEquals(ss,
             [[0, 0, 0, None, None],
              [None, None, 0, 0, None],
              [None, None, None, 0, 0]]
        )

    def test_all_empty(self):
        ss = [[None, None, None, None, None],
              [None, None, None, None, None],
              [None, None, None, None, None]]
        gap_fill(*ss)
        self.assertEquals(ss,
             [[None, None, None, None, None],
              [None, None, None, None, None],
              [None, None, None, None, None]]
        )

    def test_all_empty_gen(self):
        ssz = zip([None, None, None, None, None],
              [None, None, None, None, None],
              [None, None, None, None, None])
        gfg = gap_fill_gen(ssz)
        l = list(gfg)
        self.assertEquals(l,
                          5 * [(None, None, None)])

    def test_leading_empty(self):
        ss = [[None, None, 1.2, None, None],
              [None, None, None, None, None],
              [None, None, None, 1.3, 1.4]]
        gap_fill(*ss)
        self.assertEquals(ss,
             [[None, None, 1.2, 1.3, None],
              [None, None, None, None, None],
              [None, None, None, 1.3, 1.4]]
        )
