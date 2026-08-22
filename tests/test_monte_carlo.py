import unittest
from monte_carlo import simulate,analyze,percentile
class Tests(unittest.TestCase):
    def test_repeatable(self): self.assertEqual(simulate(5,1),simulate(5,1))
    def test_count(self): self.assertEqual(analyze(simulate(7,2))["runs"],7)
    def test_percentile(self): self.assertEqual(percentile([1,2,3],.5),2)
    def test_success_rate_range(self): self.assertTrue(0<=analyze(simulate(20,3))["success_rate"]<=1)
if __name__=="__main__": unittest.main()
