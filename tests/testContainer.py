import sys
sys.path.append('..')

import container

from toolbox import More

import unittest

class ContainerTestCase(unittest.TestCase):

  # run before every test
  def setUp(self):
    pass

  # run after every test
  def tearDown(self):
    pass

  def test_getSetAdd(self):
    multiplier = container.MultiplierContainer()

    self.assertEqual(0, multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase') )

    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 2.)
    self.assertEqual(2., multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase') )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 2.)
    self.assertEqual(4., multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase') )

    self.assertEqual(More(1.), multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more') )

    multiplier.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 2.)
    self.assertEqual(More(2.), multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more') )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 2.)
    self.assertEqual(More(4.), multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more') )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 7.)
    self.assertEqual(More(28.), multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more') )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 7.)
    self.assertEqual(More(196.), multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more') )
    pass

  def test_addMultiplierContainer(self):
    multiplier1 = container.MultiplierContainer()
    multiplier2 = container.MultiplierContainer()

    multiplier1.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 2.)
    multiplier2.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 3.)
    multiplier1.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 4.)
    multiplier2.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 7.)
    multiplier2.set(attackType_ = 'melee', elementType_ = 'generic', multiplierType_ = 'increase', value_ = 1.)

    multiplier3 = multiplier1 + multiplier2

    self.assertEqual(More(28.), multiplier3.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more'))
    self.assertEqual(5., multiplier3.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    self.assertEqual(1., multiplier3.get(attackType_ = 'melee', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(0., multiplier3.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(More(1.), multiplier3.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'more'))
    self.assertEqual(3., multiplier2.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    pass

  def test_iaddMultiplierContainer(self):
    multiplier1 = container.MultiplierContainer()
    multiplier2 = container.MultiplierContainer()

    multiplier1.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 2.)
    multiplier2.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 3.)
    multiplier1.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 4.)
    multiplier2.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 7.)
    multiplier2.set(attackType_ = 'melee', elementType_ = 'generic', multiplierType_ = 'increase', value_ = 1.)

    multiplier1 += multiplier2

    self.assertEqual(More(28.), multiplier1.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more'))
    self.assertEqual(5., multiplier1.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    self.assertEqual(1., multiplier1.get(attackType_ = 'melee', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(0., multiplier1.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(More(1.), multiplier1.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'more'))
    self.assertEqual(3., multiplier2.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    pass

  def test_addPenetrationContainer(self):
    # ResistanceContainer is the same
    penetration1 = container.PenetrationContainer(defaultValue_ = 10.)
    penetration2 = container.PenetrationContainer(defaultValue_ = 20.)

    penetration2.set(elementType_ = 'fire', value_ = 30.)

    penetration3 = penetration1 + penetration2

    self.assertEqual(30., penetration2.get(elementType_ = 'fire'))
    self.assertEqual(40., penetration3.get(elementType_ = 'fire'))
    self.assertEqual(30., penetration3.get(elementType_ = 'physical'))
    pass

  def test_iaddPenetrationContainer(self):
    # ResistanceContainer is the same
    penetration1 = container.PenetrationContainer(defaultValue_ = 10.)
    penetration2 = container.PenetrationContainer(defaultValue_ = 20.)

    penetration2.set(elementType_ = 'fire', value_ = 30.)

    penetration1 += penetration2

    self.assertEqual(40., penetration1.get(elementType_ = 'fire'))
    self.assertEqual(30., penetration2.get(elementType_ = 'fire'))
    self.assertEqual(30., penetration1.get(elementType_ = 'physical'))
    pass

  def test_addAttributeContainer(self):
    attributes1 = container.AttributeContainer(defaultValue_ = 2.)
    attributes2 = container.AttributeContainer(defaultValue_ = 5.)

    attributes1.set(attributeType_ = 'strength' , value_ = 7.)
    attributes2.set(attributeType_ = 'dexterity' , value_ = -4.)

    attributes3 = attributes1 + attributes2

    self.assertEqual(7., attributes1.get(attributeType_ = 'strength'))
    self.assertEqual(12., attributes3.get(attributeType_ = 'strength'))
    self.assertEqual(-2., attributes3.get(attributeType_ = 'dexterity'))
    self.assertEqual(7., attributes3.get(attributeType_ = 'vitality'))
    pass

  def test_iaddAttributeContainer(self):
    attributes1 = container.AttributeContainer(defaultValue_ = 2.)
    attributes2 = container.AttributeContainer(defaultValue_ = 5.)

    attributes1.set(attributeType_ = 'strength' , value_ = 7.)
    attributes2.set(attributeType_ = 'dexterity' , value_ = -4.)

    attributes1 += attributes2

    self.assertEqual(7., attributes1.get(attributeType_ = 'intelligence'))
    self.assertEqual(12., attributes1.get(attributeType_ = 'strength'))
    self.assertEqual(5., attributes2.get(attributeType_ = 'strength'))
    self.assertEqual(-2., attributes1.get(attributeType_ = 'dexterity'))
    self.assertEqual(5., attributes2.get(attributeType_ = 'vitality'))
    pass

  def test_addDurationModifierContainer(self):

    durationModifier1 = container.DurationModifierContainer()
    durationModifier2 = container.DurationModifierContainer()

    durationModifier1.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 1.)
    durationModifier2.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 2.)
    durationModifier2.set(durationModifierType_ = 'duration', multiplierType_ = 'increase', value_ = 3.)
    durationModifier2.set(durationModifierType_ = 'duration', multiplierType_ = 'more', value_ = 3.)
    durationModifier1.set(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase', value_ = 7.)

    durationModifier3 = durationModifier1 + durationModifier2

    self.assertEqual(1., durationModifier1.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'))
    self.assertEqual(7., durationModifier1.get(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase'))
    self.assertEqual(3., durationModifier3.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'))
    self.assertEqual(3., durationModifier2.get(durationModifierType_ = 'duration', multiplierType_ = 'increase'))
    self.assertEqual(More(3.), durationModifier3.get(durationModifierType_ = 'duration', multiplierType_ = 'more'))
    self.assertEqual(More(1.), durationModifier3.get(durationModifierType_ = 'onHit', multiplierType_ = 'more'))
    pass

  def test_iaddDurationModifierContainer(self):

    durationModifier1 = container.DurationModifierContainer()
    durationModifier2 = container.DurationModifierContainer()

    durationModifier1.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 1.)
    durationModifier2.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 2.)
    durationModifier2.set(durationModifierType_ = 'duration', multiplierType_ = 'increase', value_ = 3.)
    durationModifier2.set(durationModifierType_ = 'duration', multiplierType_ = 'more', value_ = 3.)
    durationModifier1.set(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase', value_ = 7.)

    durationModifier1 += durationModifier2

    self.assertEqual(7., durationModifier1.get(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase'))
    self.assertEqual(3., durationModifier1.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'))
    self.assertEqual(2., durationModifier2.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'))
    self.assertEqual(3., durationModifier2.get(durationModifierType_ = 'duration', multiplierType_ = 'increase'))
    self.assertEqual(More(3.), durationModifier1.get(durationModifierType_ = 'duration', multiplierType_ = 'more'))
    self.assertEqual(More(1.), durationModifier1.get(durationModifierType_ = 'onHit', multiplierType_ = 'more'))

if __name__ == '__main__':
  unittest.main()