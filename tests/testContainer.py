import sys
sys.path.append('..')

import container

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

    self.assertEqual(1., multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value)

    multiplier.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 2.)
    self.assertEqual(3., multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 2.)
    self.assertEqual(9., multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 7.)
    self.assertEqual(72, multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value )
    multiplier.add(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 7.)
    self.assertEqual(576, multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value )
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

    self.assertEqual(40, multiplier3.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value)
    self.assertEqual(5., multiplier3.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    self.assertEqual(1., multiplier3.get(attackType_ = 'melee', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(0., multiplier3.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(1, multiplier3.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'more')._value)
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

    self.assertEqual(40, multiplier1.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more')._value)
    self.assertEqual(5., multiplier1.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    self.assertEqual(1., multiplier1.get(attackType_ = 'melee', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(0., multiplier1.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'increase'))
    self.assertEqual(1, multiplier1.get(attackType_ = 'spell', elementType_ = 'generic', multiplierType_ = 'more')._value)
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
    self.assertEqual(4., durationModifier3.get(durationModifierType_ = 'duration', multiplierType_ = 'more')._value)
    self.assertEqual(1., durationModifier3.get(durationModifierType_ = 'onHit', multiplierType_ = 'more')._value)
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
    self.assertEqual(4., durationModifier1.get(durationModifierType_ = 'duration', multiplierType_ = 'more')._value)
    self.assertEqual(1., durationModifier1.get(durationModifierType_ = 'onHit', multiplierType_ = 'more')._value)
    pass

  def test_copyFromContainer(self):
    durationModifier1 = container.DurationModifierContainer()
    durationModifier2 = container.DurationModifierContainer()

    durationModifier1.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 1.)
    durationModifier1.set(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase', value_ = 7.)
    durationModifier2.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 2.)
    durationModifier2.set(durationModifierType_ = 'duration', multiplierType_ = 'increase', value_ = 3.)
    durationModifier2.set(durationModifierType_ = 'duration', multiplierType_ = 'more', value_ = 3.)

    durationModifier1.copyFrom(durationModifier2)
    durationModifier2.reset()
    self.assertEqual(durationModifier1.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'), 2)
    self.assertEqual(durationModifier1.get(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase'), 0)
    self.assertEqual(durationModifier1.get(durationModifierType_ = 'duration', multiplierType_ = 'more')._value, 4.)

    self.assertEqual(durationModifier2.get(durationModifierType_ = 'duration', multiplierType_ = 'more')._value, 1.)
    self.assertEqual(durationModifier2.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'), 0)
    self.assertEqual(durationModifier2.get(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase'), 0)

    self.assertEqual(durationModifier1.get(durationModifierType_ = 'onHit', multiplierType_ = 'increase'), 2)
    self.assertEqual(durationModifier1.get(durationModifierType_ = 'onHit', attackType_ = 'melee', multiplierType_ = 'increase'), 0)
    self.assertEqual(durationModifier1.get(durationModifierType_ = 'duration', multiplierType_ = 'more')._value, 4.)
    pass

  def test_initContainerKwargs(self):

    element = container.DamageContainer(fire = 4., defaultValue_ = 3)

    element2 = container.DamageContainer(fire = 4., physical = 3)

    result1 = container.DamageContainer()
    result2 = container.DamageContainer()

    result1.iaddIgnoreDefault(element)
    result2.iaddIgnoreDefault(element2)

    self.assertEqual(0, result1.get(elementType_ = 'physical'))
    self.assertEqual(3, result2.get(elementType_ = 'physical'))

    element2.iaddIgnoreDefault(element)
    self.assertEqual(3, element2.get(elementType_ = 'physical'))

    element2 += element
    self.assertEqual(6, element2.get(elementType_ = 'physical'))

    element3 = container.DamageContainer(**element2)
    self.assertEqual(element3['fire'], element2['fire'])
    self.assertEqual(element3['lightning'], element2['lightning'])
    self.assertEqual(element3['cold'], element2['cold'])
    self.assertEqual(element3['void'], element2['void'])
    self.assertEqual(element3['poison'], element2['poison'])
    self.assertEqual(element3['physical'], element2['physical'])
    self.assertEqual(element3['necrotic'], element2['necrotic'])

    # element4 = container.DamageContainer(*element2)
    pass


if __name__ == '__main__':
  unittest.main()