import unittest
from amda_sciqlop_speed_tester.network_probes import trace_route


class NetWorkProbes(unittest.TestCase):
    def test_traceroute(self):
        route = trace_route('hephaistos.lpp.polytechnique.fr', ttl=30)
        self.assertGreater(len(route),1)
        self.assertIn("hephaistos.lpp.polytechnique.fr", route[-1])


if __name__ == '__main__':
    unittest.main()
