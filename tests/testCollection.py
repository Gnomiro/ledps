import sys
sys.path.append('..')

import collection, duration, element

import unittest

class CollectionTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    self.collection_ = collection.Collection()
    pass

  # run after every test
  def tearDown(self):
    pass

  def test_getDuration(self):
    b = self.collection_.getDuration('bleed')

    self.assertEqual(b.getName(), 'bleed')

  def test_copyViability(self):

    # iterates over all implemented durations and calld their constructor in first if statement
    for name in duration.getImplementedClasses():

      if name == 'cooldown':
        continue

      if collection_.getDuration(name).hasType('damagingAilment'):
        self.copyDamagingAilment(name)
      if collection_.getDuration(name).hasType('shred'):
        self.copyShred(name)
      if collection_.getDuration(name).hasType('buff'):
        self.copyBuff(name)

  def copyDamagingAilment(self, name_):
    b = collection_.getDurationCopy(name_)

    b.tick(8.)

    b._baseDamage = element.ElementContainer(default_ = 1.)

    b2 = collection_.getDurationCopy(name_)

    self.assertEqual(b._damage.getSum(), b2._damage.getSum())
    self.assertNotEqual(b.isActive(), b2.isActive())
    self.assertNotEqual(b._baseDamage.getSum(), b2._baseDamage.getSum())

    pass

  def copyShred(self, name_):
    print('CollectionTest: Add copyShred test not implemented yet.')
    pass

  def copyBuff(self, name_):
    print('CollectionTest: Add copyBuff test not implemented yet.')
    pass

if __name__ == '__main__':
  collection_ = collection.Collection()


  unittest.main()
