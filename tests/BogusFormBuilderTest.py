'''
Created on Apr 20, 2016

@author: Niels
'''
import unittest
from agent.BogusFormBuilder import BogusFormBuilder


class BogusFormBuilderTest(unittest.TestCase):

    def setUp(self):
        self.that = BogusFormBuilder()

    def testPassword(self):
        pwd = self.that.getPassword()
        self.assertTrue(len(pwd)>=15, "an insecure password was created")
        self.assertEqual(pwd, self.that.getPassword(), "memoization of password failed")

    def testPhoneNumLength(self):
        self.assertEqual(len(self.that.getPhoneNum()), 10)

    def testPhoneNumDuplicate(self):
        number = self.that.getPhoneNum()
        self.assertEqual(number, self.that.getPhoneNum())

    def testEmailDuplicate(self):
        email = self.that.getEmail()
        self.assertEqual(email, self.that.getEmail())

    def testEmailDot(self):
        self.assertTrue("." in self.that.getEmail())

    def testEmailAt(self):
        self.assertTrue("@" in self.that.getEmail())

    def testFirstNameDuplicate(self):
        name = self.that.getFirstName()
        self.assertEqual(name, self.that.getFirstName())

    def testSurNameDuplicate(self):
        name = self.that.getSurname()
        self.assertEqual(name, self.that.getSurname())

    def testCityDuplicate(self):
        city = self.that.getCity()
        self.assertEqual(city, self.that.getCity())

    def testZipcodeDuplicate(self):
        zipcode = self.that.getZipcode()
        self.assertEqual(zipcode, self.that.getZipcode())

    def testZipCodeLength(self):
        self.assertEqual(len(self.that.getZipcode()), 5)

    def testZipCodeNumberical(self):
        self.assertTrue(self.that.getZipcode().isdigit())

    def testPhoneNumberNumberical(self):
        self.assertTrue(self.that.getPhoneNum().isdigit())

    def testSurnameAlphabetical(self):
        self.assertTrue(self.that.getSurname().isalpha())

    def testFirstNameAlphabetical(self):
        self.assertTrue(self.that.getSurname().isalpha())

    def testCityLength(self):
        city = self.that.getCity()
        self.assertTrue(len(city) >= 3)
        self.assertTrue(len(city) <= 10)

    def testFirstNameLength(self):
        name = self.that.getFirstName()
        self.assertTrue(len(name) >= 3)
        self.assertTrue(len(name) <= 10)

    def testSurnameLength(self):
        name = self.that.getSurname()
        self.assertTrue(len(name) >= 3)
        self.assertTrue(len(name) <= 10)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
