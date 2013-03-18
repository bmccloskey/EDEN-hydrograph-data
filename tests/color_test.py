from dj_eden_app.colors import ColorRange

import unittest
import re

class TestColorRange(unittest.TestCase):
    pattern = re.compile(r'^#[0-9a-f]{6}$')

    def check_color(self, c):
        self.assertTrue(TestColorRange.pattern.match(c), "Color in expected hex format")

    def check_unique(self, victim):
        u = set(list(victim))
        self.assertEquals(len(u), len(victim))

    def test_default_12(self):
        victim = ColorRange(None, 12)
        self.assertEquals(12, len(victim))
        for c in victim:
            self.check_color(c)
        self.check_unique(victim)

    def test_spectral_12(self):
        victim = ColorRange('spectral', 12)
        self.assertEquals(12, len(victim))
        self.assertEquals('spectral', victim.name())
        for c in victim:
            self.check_color(c)
        self.check_unique(victim)

    def test_spectral_256(self):
        victim = ColorRange('spectral', 256)
        self.assertEquals(256, len(victim))
        self.assertEquals('spectral', victim.name())
        for c in victim:
            self.check_color(c)
        self.check_unique(victim)
