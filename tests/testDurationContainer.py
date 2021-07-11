import sys
sys.path.append('..')

import durationContainer, collection, modifier

import unittest

class DurationTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    pass

  # run after every test
  def tearDown(self):
    pass

if __name__ == '__main__':

  c = collection.Collection()

  dc = durationContainer.DurationContainer(c)

  m = modifier.Modifier()

  dc.add('bleed', m)
  dc.add('bleed', m)
  dc.add('physicalShred', m)

  print(dc.countActiveByName('ignite'))

  print(dc.countActiveByNames('bleed', 'ignite'))

  print(dc.countActive())
  print(dc.countActiveWithType('damagingAilment'))
  print(dc.countActiveWithTypes('damagingAilment','resistanceShred'))


  unittest.main()