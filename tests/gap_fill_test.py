from dj_eden_app.gap_fill import gap_fill

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
