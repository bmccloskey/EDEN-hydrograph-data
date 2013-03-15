import dj_eden_app.stage_data as stage_data

import unittest
from StringIO import StringIO

class _MockResults:
    contents = [[1, 2, 3],
                [2, 3, 4]
                ]
    def keys(self):
        return ["a", "b", "c"]

    def __iter__(self):
        return self.contents.__iter__()

class TestRDBOutput(unittest.TestCase):


    def test_write_no_header(self):
        results = _MockResults()

        outfile = StringIO()
        stage_data.write_rdb(results, outfile)
        expected_h = "a\tb\tc\r\n"
        expected_t = "12s\t12s\t12s\r\n"
        expected_d = "1\t2\t3\r\n2\t3\t4\r\n"
        expected = expected_h + expected_t + expected_d
        self.assertEquals(expected, outfile.getvalue())

    def test_write_with_header(self):
        results = _MockResults()

        outfile = StringIO()
        md = ["hello", "world"]
        stage_data.write_rdb(results, outfile, metadata=md)
        expected_head = "# hello\r\n# world\r\n"
        expected_h = "a\tb\tc\r\n"
        expected_t = "12s\t12s\t12s\r\n"
        expected_d = "1\t2\t3\r\n2\t3\t4\r\n"
        expected_body = expected_h + expected_t + expected_d
        self.assertEquals(expected_head + expected_body, outfile.getvalue())

if __name__ == '__main__':
    unittest.main()


