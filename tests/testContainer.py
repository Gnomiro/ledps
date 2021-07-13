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
    attributes = container.AttributeContainer()
    penetration = container.PenetrationContainer(defaultValue_ = 0)

    durationModifier = container.DurationModifierContainer()

    durationModifier.set(durationModifierType_ = 'onHit', multiplierType_ = 'increase', value_ = 1)
    durationModifier.set(durationModifierType_ = 'duration', multiplierType_ = 'increase', value_ = 1)

    print(durationModifier)

    print(multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'more'))
    print(multiplier.get(attackType_ = 'melee', elementType_ = 'fire', multiplierType_ = 'increase'))
    print(multiplier.get(attackType_ = 'melee'))

    print(multiplier)

    multiplier.set(value_ = 4, attackType_ = 'melee', multiplierType_ = 'increase')
    print(multiplier.get(attackType_ = 'melee', multiplierType_ = 'more'))
    print(multiplier.get(attackType_ = 'melee', multiplierType_ = 'increase'))
    print(multiplier.get(attackType_ = 'melee'))
    print(multiplier)

    pass


if __name__ == '__main__':
  unittest.main()