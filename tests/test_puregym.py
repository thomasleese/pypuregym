import os
from unittest import TestCase

from puregym import PureGym


class TestPureGym(TestCase):

    def setUp(self):
        self.puregym = PureGym()

    def test_gyms(self):
        gyms = self.puregym.gyms
        assert len(gyms) != 0
