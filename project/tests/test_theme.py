import unittest
from src.ui.theme import lighten_color, set_mode, Theme


class TestThemeUtils(unittest.TestCase):
    def test_lighten_color_increases_brightness(self):
        original = "#102030"
        lighter = lighten_color(original, factor=0.5)
        # Expect hex string and components not darker than original
        self.assertIsInstance(lighter, str)
        self.assertTrue(lighter.startswith("#"))
        # Parse components
        o = original.lstrip('#')
        l = lighter.lstrip('#')
        or_, og, ob = int(o[0:2], 16), int(o[2:4], 16), int(o[4:6], 16)
        lr, lg, lb = int(l[0:2], 16), int(l[2:4], 16), int(l[4:6], 16)
        self.assertGreaterEqual(lr, or_)
        self.assertGreaterEqual(lg, og)
        self.assertGreaterEqual(lb, ob)

    def test_set_mode_light_dark_switch(self):
        set_mode("light")
        self.assertEqual(Theme.MODE, "light")
        light_bg = Theme.BACKGROUND

        set_mode("dark")
        self.assertEqual(Theme.MODE, "dark")
        dark_bg = Theme.BACKGROUND

        self.assertNotEqual(light_bg, dark_bg)


if __name__ == "__main__":
    unittest.main()