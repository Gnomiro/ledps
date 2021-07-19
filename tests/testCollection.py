import sys
sys.path.append('..')

import collection, duration, container

import unittest

class CollectionTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    self._collection = collection.Collection()
    pass

  # run after every test
  def tearDown(self):
    pass

  def test_getDuration(self):
    b = self._collection.getDuration('bleed')

    self.assertEqual(b.getName(), 'bleed')

  def test_collectionReset(self):

    b = self._collection.getDuration('bleed')

    b._damage.iscaleByFactor(5)

    b2 = self._collection.getDuration('bleed')

    self.assertEqual(b._damage, b2._damage)

    self._collection.resetDurationCollection()

    b3 = self._collection.getDuration('bleed')

    self.assertNotEqual(b._damage, b3._damage)

  def test_copyViability(self):

    # iterates over all implemented durations and calld their constructor in first if statement
    for name in duration.getImplementedClasses():

      if name == 'cooldown':
        continue

      if self._collection.getDuration(name).hasType('damagingAilment'):
        self.copyDamagingAilment(name)
      if self._collection.getDuration(name).hasType('shred'):
        self.copyShred(name)
      if self._collection.getDuration(name).hasType('buff'):
        self.copyBuff(name)

  def copyDamagingAilment(self, name_):
    b = self._collection.getDurationCopy(name_)

    b.setStackSize(1)
    b.tick(8.)

    b._baseDamage = container.ElementContainer(defaultValue_ = 1.)

    b2 = self._collection.getDurationCopy(name_)

    self.assertEqual(b._damage['fire'], b2._damage['fire'])
    self.assertNotEqual(b.isActive(), b2.isActive())
    self.assertNotEqual(b._baseDamage['fire'], b2._baseDamage['fire'])

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
