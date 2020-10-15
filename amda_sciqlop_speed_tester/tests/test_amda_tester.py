import unittest
from amda_sciqlop_speed_tester.amda_tester import dl_from_rest_api


class AMDA_Tester(unittest.TestCase):
    def test_can_dl_from_api(self):
        self.assertIsNotNone(dl_from_rest_api())


if __name__ == '__main__':
    unittest.main()
