import sys
sys.path.append('..')

import element, error

import unittest

class ElementTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    pass

  # run after every test
  def tearDown(self):
    pass

  # test constructor
  def test_init(self):
    valid = dict.fromkeys(element.getValidElements(), 0.)
    e = element.ElementContainer(**valid)

  # pass invalid elements to contrructor
  def test_initException(self):
    valid = dict.fromkeys(element.getValidElements(), 0.)

    # add invalid element
    valid[list(valid.keys())[0] + '123'] = 4

    # exception must be risen
    with self.assertRaises(error.InvalidElement):
      element.ElementContainer(**valid)

  # test getSum() routine alongside optional constructor arguments
  def test_getSum(self):
    valid = dict.fromkeys(element.getValidElements(), 0.)
    e = element.ElementContainer(**valid)
    self.assertEqual(e.getSum(), 0.)

    valid = dict.fromkeys(element.getValidElements(), 4.)
    valid[list(valid.keys())[0]] += 1
    e = element.ElementContainer(**valid)
    self.assertEqual(e.getSum(), (4. * len(e._element) + 1))

    valid = dict.fromkeys(element.getValidElements(), 4.)
    e = element.ElementContainer(**valid, default_ = 6)
    self.assertEqual(e.getSum(), (10. * len(e._element)))

  def test_multiplyByFactor(self):
    e = element.ElementContainer(default_ = 1.)
    r = e.multiplyByFactor(2.)
    self.assertEqual(r.getSum(), 2 * len(element.getValidElements()))

    e.imultiplyByFactor(1.5)
    self.assertEqual(e.getSum(), 1.5 * len(element.getValidElements()))


if __name__ == '__main__':
  unittest.main()