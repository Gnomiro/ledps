import sys
sys.path.append('..')

import duration

import unittest

class DurationTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    pass

  # run after every test
  def tearDown(self):
    pass

  def test_initImplementedDurations(self):
    for d in duration.getImplementedClasses():
      c = d[0].upper() + d[1:]
      eval('duration.' + c)

  def test_initCooldown(self):
      duration.Cooldown(name_ = 'testcd', duration_ = 4)

  def test_isActive(self):
    b = duration.Bleed()

    b.tick(timestep_ = 0.1)
    self.assertEqual(b.isActive(), True)

    b.tick(timestep_ = 4.01)
    self.assertEqual(b.isActive(), False)

if __name__ == '__main__':
  unittest.main()