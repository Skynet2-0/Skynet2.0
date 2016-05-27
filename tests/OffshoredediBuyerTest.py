"""
Created on May 27, 2016

@author: Stefan
"""
import unittest
from VPSBuyerTest import VPSBuyerTest
from agent.OffshoredediBuyer import OffshoredediBuyer


class CNTR(object):
    """Simple counter."""
    counter = 0

    @classmethod
    def getCounter(cls):
        return cls.counter

    @classmethod
    def decrement(cls):
        cls.counter = cls.counter - 1

    @classmethod
    def setCounter(cls, cntr):
        assert type(cls.counter) == int
        cls.counter = cntr


class OffshoredediBuyerTest(VPSBuyerTest):
    """
    Tests the vps buyer.

    Only non buying methods are tested.
    """


    def setUp(self):
        VPSBuyerTest.setUp(self)
        self.sshuser = "root"
        self.sshpassword = ""
        self.buyer = OffshoredediBuyer(self.email, self.password)

    def testSSHPassword(self):
        self.assertEqual(self.sshpassword, self.buyer.getSSHPassword())

    def testSSHName(self):
        self.assertEqual(self.sshuser, self.buyer.getSSHUsername())

    def testWaitForTransactionTrue(self):
        def always_true():
            return True
        self.assertTrue(self.buyer._wait_for_transaction(always_true, 10, 1, False))

    def testWaitForTransactionFalse(self):
        def always_false():
            return False
        self.assertFalse(self.buyer._wait_for_transaction(
        always_false, 5, 0, False))

    def testWaitForTransactionThreeTurnsFinishes(self):
        CNTR.setCounter(3)
        def third_time(self):
            import tests.OffshoredediBuyerTest
            CNTR.decrement()
            return CNTR.getCounter() == 0
        self.assertTrue(self.buyer._wait_for_transaction(third_time, 5, 0, arg=self))

    def testWaitForTransactionThreeTurnsActuallyThree(self):
        CNTR.setCounter(3)
        def third_time():
            import tests.OffshoredediBuyerTest
            CNTR.decrement()
            return CNTR.getCounter() == 0
        self.buyer._wait_for_transaction(third_time, 5, 0, False)
        self.assertEqual(0, CNTR.counter)

    def testWaitWithStaticMethodWithArgumentFinishes(self):
        CNTR.setCounter(10)
        def second_time(arg):
            import tests.OffshoredediBuyerTest
            CNTR.decrement()
            return CNTR.getCounter() == arg
        self.assertTrue(self.buyer._wait_for_transaction(second_time,
                            10, 0, False, arg=8))

    def testWaitWithStaticMethodWithArgumentActually8(self):
        CNTR.setCounter(10)
        def second_time(arg):
            import tests.OffshoredediBuyerTest
            CNTR.decrement()
            return CNTR.getCounter() == arg
        self.buyer._wait_for_transaction(second_time, 10, 0, False, arg=8)
        self.assertEqual(8, CNTR.getCounter())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
