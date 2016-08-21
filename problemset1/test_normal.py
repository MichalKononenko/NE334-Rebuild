"""
Contains unit tests for :mod:`normal.py`
"""
import unittest
from Scientific.IO import ArrayIO
from normal import NormalDistribution, mean
from numpy.testing import assert_equal

class TestNormalDistribution(unittest.TestCase):
    """
    Base class for unit tests for :mod:`normal.py`
    """
    def setUp(self):
        """
        Set up the unit test for the constructor, picking the
        Z distribution as a test, and a relatively representative
        sample of the normal distribution
        """
        self.mean = 0
        self.standard_deviation = 1
        self.sample_size = 30

class TestNormalDistributionConstructor(TestNormalDistribution):
    def test_constructor(self):
        dist = NormalDistribution(
            self.mean, self.standard_deviation, self.sample_size
        )

        self.assertEqual(self.mean, dist.mean)
        self.assertEqual(self.standard_deviation, dist.standard_deviation)
        self.assertEqual(self.sample_size, dist.sample_size)

class TestNormalDistributionWithFixture(TestNormalDistribution):
    def setUp(self):
        TestNormalDistribution.setUp(self)
        self.dist = NormalDistribution(
            self.mean, self.standard_deviation, self.sample_size
        )

class TestNormalDistributionSampling(TestNormalDistributionWithFixture):
    def test_sample_purity(self):
        sample1 = self.dist.sample
        sample2 = self.dist.sample
        assert_equal(sample1, sample2)

    def test_sample_average_is_none(self):
        self.dist.__dict__['sample'] = None
        self.assertIsNone(self.dist.sample_average)

    def test_sample_average_not_none(self):
        assert_equal(mean(self.dist.sample), self.dist.sample_average)

    def test_sample_square_average_is_none(self):
        self.dist.__dict__['sample'] = None
        self.assertIsNone(self.dist.square_sample_average)

    def test_sample_square_average(self):
        sample = self.dist.sample
        assert_equal(mean(sample * sample), self.dist.square_sample_average)

    def test_len(self):
        self.assertEqual(self.dist.sample_size, len(self.dist))

    def test_getitem(self):
        assert_equal(self.dist[0], self.dist.sample[0])

    def test_setattr(self):
        """
        Tests that when an attribute of the normal distribution is set,
        the new simulation parameters are recalculated immediately after
        being set. The old and new arrays should not be equal, and so the
        equality function should throw an AssertionError. This checks that this
        error was thrown.
        """
        old_sample = self.dist.sample

        self.dist.mean = 1

        new_sample = self.dist.sample

        with self.assertRaises(AssertionError):
            assert_equal(old_sample, new_sample)

class TestShouldUpdate(TestNormalDistributionWithFixture):
    def test_should_update_true(self):
        self.assertTrue(self.dist._should_update)

    def test_should_update_false(self):
        del self.dist.mean
        self.assertFalse(self.dist._should_update)

class TestSampleOutput(TestNormalDistributionWithFixture):
    def test_output(self):
        expected_output = 'output <x^2>= %s \n output <x>= %s' % (
            self.dist.square_sample_average, self.dist.sample_average
        )

        self.assertEqual(expected_output, self.dist.output)

class TestRepr(TestNormalDistributionWithFixture):
    def test_repr(self):
        self.assertIsNotNone(self.dist.__repr__())

# If this script was called directly with pydev, run the test
# suite in this file
if __name__ == '__main__':
    unittest.main()
