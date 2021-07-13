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

  def test_1(self):

    multiplier = container.MultiplierContainer()
    multiplier2 = container.MultiplierContainer()
    attributes = container.AttributeContainer(defaultValue_ = 1)
    attributes2 = container.AttributeContainer(defaultValue_ = 2)
    penetration = container.PenetrationContainer(defaultValue_ = 0)

    durationModifier = container.DurationModifierContainer()

    durationModifier.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 1)
    durationModifier.set(durationModifierType_ = 'duration', multiplierType_ = 'increase', value_ = 1)

    print('\nDuration Modifer:\n{}'.format(durationModifier))

    multiplier.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more', value_ = 2)
    multiplier.set(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 1)

    print('\n')

    print(multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more'))
    print(multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))

    print(multiplier.get(attackType_ = 'generic', elementType_ = 'fire', multiplierType_ = 'increase'))

    multiplier.set(attackType_ = 'spell', elementType_ = 'fire', multiplierType_ = 'increase', value_ = 1)
    print(multiplier)
    print('\nMultiplier1:\n{}'.format(multiplier))

    multiplier2.set(attackType_ = 'melee', multiplierType_ = 'increase', value_ = 4)
    print('\nMultiplier2:\n{}'.format(multiplier2))

    print('\nMultiplier1:\n{}'.format(multiplier))

    print('\nMultiplier1+2:\n{}'.format(multiplier + multiplier2))

    print('\n')

    print(multiplier.get(attackType_ = 'melee', multiplierType_ = 'more'))
    print(multiplier.get(attackType_ = 'melee', multiplierType_ = 'increase'))
    print(multiplier)

    attributes.set(attributeType_ = 'strength', value_ = 4)
    attributes2.set(attributeType_ = 'dexterity', value_ = 1)
    print(attributes)
    print(attributes2)
    print(attributes + attributes2)

    pass


if __name__ == '__main__':
  unittest.main()